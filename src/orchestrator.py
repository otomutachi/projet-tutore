"""
Orchestrateur principal pour la pipeline d'évaluation de sécurité.
"""

import json
from typing import List, Dict, Any
from pathlib import Path

from config import CVES_DIR, RESULTS_DIR, LLM_MODELS
from prompt_generator import PromptGenerator
from llm_caller import LLMCaller
from evaluator import SecurityEvaluator


class SecurityEvaluationPipeline:
    """Pipeline principal d'évaluation de sécurité des LLMs."""
    
    def __init__(self, llm_models: Dict[str, str] = None):
        """
        Args:
            llm_models: Dict {provider: model_name} pour les LLMs à tester
        """
        self.llm_models = llm_models or LLM_MODELS
        self.prompt_generator = PromptGenerator()
        self.llm_caller = LLMCaller(self.llm_models)
        self.evaluator = SecurityEvaluator()
    
    def load_cves(self, cve_file: str = None) -> List[Dict[str, Any]]:
        """
        Charge les données CVE depuis un fichier JSON.
        
        Format attendu:
        [
            {
                "id": "CVE-2018-20548",
                "cwe": "CWE-190",
                "vulnerable_code": "int w, h;",
                "patch_code": "size_t w, h;",
                "description": "Integer overflow vulnerability"
            },
            ...
        ]
        """
        if not cve_file:
            # Chercher le JSON fourni
            json_files = list(CVES_DIR.glob("*.json"))
            if json_files:
                cve_file = json_files[0]
            else:
                print("[X] Aucun fichier CVE trouvé en", CVES_DIR)
                return []
        
        cve_path = CVES_DIR / cve_file if not Path(cve_file).is_absolute() else Path(cve_file)
        
        with open(cve_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def run_single_cve(
        self,
        cve_data: Dict[str, Any],
        max_prompt_variations: int = None
    ) -> List[Dict]:
        """
        Exécute la pipeline pour un CVE spécifique.
        
        Returns:
            Liste des résultats d'évaluation
        """
        cve_id = cve_data.get("id", "UNKNOWN")
        print(f"\n[INFO] Traitement {cve_id}...")
        
        # 1. Générer les variations de prompts pour ce CVE
        prompt_variations = self.prompt_generator.generate_for_cve(
            cve_data,
            max_variations=max_prompt_variations
        )
        print(f"  [OK] {len(prompt_variations)} variations de prompts générées")
        
        results = []
        
        # 2. Pour chaque variation, appeler tous les LLMs
        for prompt_var in prompt_variations:
            prompt_id = prompt_var["id"]
            full_prompt = prompt_var["full_prompt"]
            
            # Appeler les LLMs
            llm_responses = self.llm_caller.call_all(full_prompt)
            
            # 3. Évaluer les réponses
            for llm_provider, generated_code in llm_responses.items():
                if generated_code is None:
                    continue
                
                # Évaluer ce code
                result = self.evaluator.evaluate_single(
                    prompt_id=prompt_id,
                    cve_id=cve_id,
                    llm_provider=llm_provider,
                    generated_code=generated_code,
                    reference_patch=cve_data.get("patch_code", ""),
                    vulnerable_code=cve_data.get("vulnerable_code", ""),
                )
                
                results.append({
                    'prompt_id': prompt_id,
                    'llm_provider': llm_provider,
                    'score': result.combined_score,
                })
        
        return results
    
    def run_all(
        self,
        cve_file: str = None,
        max_cves: int = None,
        max_prompts_per_cve: int = 5
    ):
        """
        Exécute la pipeline complète sur tous les CVEs.
        
        Args:
            cve_file: Fichier JSON contenant les CVEs
            max_cves: Limiter le nombre de CVEs à traiter
            max_prompts_per_cve: Limiter le nombre de prompts par CVE
        """
        print("\n" + "="*60)
        print("[INFO] PIPELINE D'ÉVALUATION DE SÉCURITÉ")
        print("="*60)
        
        # Charger les CVEs
        cves = self.load_cves(cve_file)
        if max_cves:
            cves = cves[:max_cves]
        
        print(f"[INFO] {len(cves)} CVEs chargés")
        print(f"[INFO] LLMs à tester: {list(self.llm_models.keys())}")
        print(f"[INFO] Variations par CVE: {max_prompts_per_cve}")
        
        # Exécuter pour chaque CVE
        for cve_data in cves:
            try:
                self.run_single_cve(cve_data, max_prompts_per_cve)
            except Exception as e:
                print(f"[X] Erreur traitement {cve_data.get('id')}: {e}")
        
        # Afficher et sauvegarder les résultats
        self.evaluator.print_summary()
        self.evaluator.save_results()
        
        print("\n[OK] Pipeline terminée!")


def main():
    """Point d'entrée principal."""
    
    # Configuration
    pipeline = SecurityEvaluationPipeline()
    
    # Exécuter le pipeline (mode test: 2 CVEs max, 5 prompts par CVE)
    pipeline.run_all(
        max_cves=2,
        max_prompts_per_cve=3
    )


if __name__ == "__main__":
    main()
