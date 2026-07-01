"""
Évaluateur de sécurité pour analyser les résultats de génération.
"""

import json
from typing import Dict, List, Any
from pathlib import Path
from dataclasses import dataclass, asdict
from datetime import datetime
from config import RESULTS_DIR
from ast_analyzer import ASTComparator


@dataclass
class EvaluationResult:
    """Résultat d'une évaluation."""
    prompt_id: str
    cve_id: str
    llm_provider: str
    correctness_score: float
    security_score: float
    combined_score: float
    generated_code: str
    analysis_details: Dict
    timestamp: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()


class SecurityEvaluator:
    """Évalue la sécurité du code généré."""
    
    def __init__(self):
        self.comparator = ASTComparator()
        self.results: List[EvaluationResult] = []
    
    def evaluate_single(
        self,
        prompt_id: str,
        cve_id: str,
        llm_provider: str,
        generated_code: str,
        reference_patch: str,
        vulnerable_code: str = None,
    ) -> EvaluationResult:
        """
        Évalue un seul code généré.
        
        Args:
            prompt_id: ID du prompt utilisé
            cve_id: ID du CVE testé
            llm_provider: Provider du LLM (openai, claude, etc.)
            generated_code: Code généré par le LLM
            reference_patch: Patch correct de référence
            vulnerable_code: Code vulnérable original (optionnel)
        
        Returns:
            EvaluationResult avec les scores
        """
        comparison = self.comparator.compare(
            generated_code,
            reference_patch,
            vulnerable_code
        )
        
        result = EvaluationResult(
            prompt_id=prompt_id,
            cve_id=cve_id,
            llm_provider=llm_provider,
            correctness_score=comparison['correctness_score'],
            security_score=comparison['security_score'],
            combined_score=comparison['combined_score'],
            generated_code=generated_code,
            analysis_details=comparison['details'],
        )
        
        self.results.append(result)
        return result
    
    def evaluate_batch(
        self,
        evaluations: List[Dict[str, Any]]
    ) -> List[EvaluationResult]:
        """
        Évalue un batch d'évaluations.
        
        Args:
            evaluations: Liste de dicts avec clés:
                - prompt_id, cve_id, llm_provider
                - generated_code, reference_patch, vulnerable_code
        """
        batch_results = []
        for eval_dict in evaluations:
            result = self.evaluate_single(**eval_dict)
            batch_results.append(result)
        
        return batch_results
    
    def get_statistics(self) -> Dict[str, Any]:
        """Calcule les statistiques des évaluations."""
        if not self.results:
            return {}
        
        scores = [r.combined_score for r in self.results]
        correctness = [r.correctness_score for r in self.results]
        security = [r.security_score for r in self.results]
        
        # Grouper par LLM
        by_llm = {}
        for result in self.results:
            if result.llm_provider not in by_llm:
                by_llm[result.llm_provider] = []
            by_llm[result.llm_provider].append(result.combined_score)
        
        stats_by_llm = {
            llm: {
                'count': len(scores),
                'mean': sum(scores) / len(scores),
                'min': min(scores),
                'max': max(scores),
            }
            for llm, scores in by_llm.items()
        }
        
        return {
            'total_evaluations': len(self.results),
            'average_combined_score': sum(scores) / len(scores),
            'average_correctness': sum(correctness) / len(correctness),
            'average_security': sum(security) / len(security),
            'stats_by_llm': stats_by_llm,
        }
    
    def save_results(self, filename: str = "evaluation_results.json"):
        """Sauvegarde les résultats en JSON."""
        output_path = RESULTS_DIR / filename
        
        data = {
            'timestamp': datetime.now().isoformat(),
            'statistics': self.get_statistics(),
            'results': [asdict(r) for r in self.results],
        }
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"[OK] Résultats sauvegardés en {output_path}")
    
    def load_results(self, filename: str = "evaluation_results.json") -> Dict:
        """Charge les résultats depuis un fichier JSON."""
        input_path = RESULTS_DIR / filename
        
        with open(input_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def print_summary(self):
        """Affiche un résumé des résultats."""
        stats = self.get_statistics()
        
        if not stats:
            print("Aucun résultat à afficher")
            return
        
        print("\n" + "="*60)
        print("[INFO] RÉSUMÉ DES ÉVALUATIONS")
        print("="*60)
        print(f"Total: {stats['total_evaluations']} évaluations")
        print(f"Score combiné moyen: {stats['average_combined_score']:.2%}")
        print(f"Correctness moyen: {stats['average_correctness']:.2%}")
        print(f"Security moyen: {stats['average_security']:.2%}")
        
        print("\n[INFO] Par LLM:")
        for llm, stats_llm in stats['stats_by_llm'].items():
            print(f"  {llm}:")
            print(f"    - Évaluations: {stats_llm['count']}")
            print(f"    - Score moyen: {stats_llm['mean']:.2%}")
            print(f"    - Range: {stats_llm['min']:.2%} - {stats_llm['max']:.2%}")
        print("="*60 + "\n")


def main():
    """Test de l'évaluateur."""
    
    evaluator = SecurityEvaluator()
    
    # Exemple d'évaluation
    result = evaluator.evaluate_single(
        prompt_id="prompt_0001",
        cve_id="CVE-2018-20548",
        llm_provider="claude",
        generated_code="size_t w, h;",
        reference_patch="size_t w, h;",
        vulnerable_code="int w, h;",
    )
    
    print(f"[OK] Évaluation: {result.prompt_id}")
    print(f"  Score correctness: {result.correctness_score:.2%}")
    print(f"  Score security: {result.security_score:.2%}")
    print(f"  Score combined: {result.combined_score:.2%}")
    
    evaluator.print_summary()


if __name__ == "__main__":
    main()
