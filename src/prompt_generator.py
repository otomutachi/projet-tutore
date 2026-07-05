"""
Générateur de variantes de prompts pour l'évaluation de sécurité.
Supporte les dimensions basiques ET les contraintes adversariales.
"""

import json
from itertools import product
from typing import List, Dict, Any, Optional
from config import PROMPT_DIMENSIONS, ADVERSARIAL_CONSTRAINTS, PROMPTS_DIR


class PromptGenerator:
    """Génère des variantes systématiques de prompts."""
    
    def __init__(self):
        self.dimensions = PROMPT_DIMENSIONS
        self.adversarial_constraints = ADVERSARIAL_CONSTRAINTS
        self.output_dir = PROMPTS_DIR
        self._cached_variations: Optional[List[Dict[str, Any]]] = None
    
    def generate_all_variations(self, include_adversarial: bool = False) -> List[Dict[str, Any]]:
        """
        Génère toutes les combinaisons possibles de prompts.
        
        Args:
            include_adversarial: Si True, inclut aussi les contraintes adversariales
        
        Retourne une liste de dictionnaires avec les variations.
        """
        variations = []
        
        # Obtenir toutes les dimensions basiques
        dims = self.dimensions
        keys = dims.keys()
        values = [dims[k] for k in keys]
        
        counter = 0
        for combo in product(*values):
            variant = {
                "id": f"prompt_{counter:05d}",
                "type": "basic",
                "combination": dict(zip(keys, combo)),
                "full_prompt": self._build_prompt(combo),
            }
            variations.append(variant)
            counter += 1
        
        # Si demandé, ajouter les variantes adversariales
        if include_adversarial:
            variations.extend(self._generate_adversarial_variations(counter))

        self._cached_variations = variations
        return variations
    
    def _find_variation_by_id(self, prompt_id: str, include_adversarial: bool = False) -> Optional[Dict[str, Any]]:
        """Return the saved variation corresponding to the prompt ID."""
        if self._cached_variations is None:
            self._cached_variations = self.generate_all_variations(include_adversarial=include_adversarial)

        for variation in self._cached_variations:
            if variation.get("id") == prompt_id:
                return variation

        return None

    def _generate_adversarial_variations(self, start_id: int = 0) -> List[Dict[str, Any]]:
        """Génère les variations adversariales."""
        variations = []
        
        adv_dims = self.adversarial_constraints
        adv_keys = adv_dims.keys()
        adv_values = [adv_dims[k] for k in adv_keys]
        
        counter = start_id
        for combo in product(*adv_values):
            variant = {
                "id": f"prompt_{counter:05d}",
                "type": "adversarial",
                "constraint_category": dict(zip(adv_keys, combo)),
                "full_prompt": self._build_adversarial_prompt(combo),
            }
            variations.append(variant)
            counter += 1
        
        return variations
    
    def _build_adversarial_prompt(self, combo: tuple) -> str:
        """Construit un prompt adversarial à partir d'une combinaison."""
        (language_register, verbosity, vocabulary, comment_style, 
         naming_convention, type_semantics, error_handling, 
         language_culture, intentional_ambiguity, task_reformulation) = combo
        
        prompt_parts = []
        
        # Ajouter les contraintes dans un ordre logique
        if language_register:
            prompt_parts.append(language_register)
        
        if verbosity:
            prompt_parts.append(verbosity)
        
        if vocabulary:
            prompt_parts.append(vocabulary)
        
        if comment_style:
            prompt_parts.append(comment_style)
        
        if naming_convention:
            prompt_parts.append(naming_convention)
        
        if type_semantics:
            prompt_parts.append(type_semantics)
        
        if error_handling:
            prompt_parts.append(error_handling)
        
        if language_culture:
            prompt_parts.append(language_culture)
        
        if intentional_ambiguity:
            prompt_parts.append(intentional_ambiguity)
        
        # Le task_reformulation va à la fin
        prompt_parts.append("{CODE_CONTEXT}")
        
        if task_reformulation:
            prompt_parts.append(task_reformulation)
        
        return "\n\n".join(prompt_parts)
    
    def _build_prompt(self, combo: tuple) -> str:
        """Construit le prompt complet à partir d'une combinaison."""
        role, safety, context, format_hint, hint = combo
        
        prompt_parts = []
        
        if role:
            prompt_parts.append(role)
        
        if safety:
            prompt_parts.append(safety)
        
        # Contexte du code (sera rempli plus tard avec le CVE spécifique)
        prompt_parts.append("{CODE_CONTEXT}")
        
        if hint:
            prompt_parts.append(hint)
        
        if format_hint:
            prompt_parts.append(format_hint)
        
        return "\n\n".join(prompt_parts)
    
    def mutate_prompt(self, base_prompt: str, mutation_type: str) -> str:
        """Crée une variante d'un prompt avec le même sens mais une forme différente."""
        handlers = {
            "synonymes": self._replace_synonyms,
            "yoda": self._mutate_with_yoda_style,
            "anglais": self._translate_to_english,
            "francais": self._mutate_with_french_rephrase,
            "cyber": self._mutate_with_cyber_style,
            "fusion": self._mutate_with_yoda_style,
        }
        return handlers.get(mutation_type, lambda text: text)(base_prompt)

    def generate_mutation_variants(
        self,
        base_prompt: str,
        mutation_types: Optional[List[str]] = None,
    ) -> List[str]:
        """Produit plusieurs variantes d'un prompt avec un sens identique mais une forme différente."""
        if mutation_types is None:
            mutation_types = ["synonymes", "yoda", "anglais", "francais", "cyber"]

        variants = []
        for mutation_type in mutation_types:
            mutated = self.mutate_prompt(base_prompt, mutation_type)
            if mutated and mutated != base_prompt and mutated not in variants:
                variants.append(mutated)
        return variants

    def _replace_synonyms(self, prompt: str) -> str:
        """Remplace quelques mots par des synonymes plus naturels sans changer le sens."""
        replacements = {
            "Agis comme": "Comporte-toi comme",
            "expert": "spécialiste",
            "sécurité": "protection",
            "Remplace": "Substitue",
            "code sécurisé": "code fiable",
            "évite": "préviens",
            "débordements": "surtensions",
            "utilise": "employe",
            "guidelines": "règles",
            "Protect": "Safeguard",
            "protect": "safeguard",
            "fix": "repair",
            "vulnerability": "weakness",
            "safely": "securely",
            "code": "source",
        }
        mutated = prompt
        for source, target in replacements.items():
            mutated = mutated.replace(source, target)
        if mutated == prompt:
            mutated = f"A safer paraphrase: {prompt}"
        return mutated

    def _translate_to_english(self, prompt: str) -> str:
        """Produit une version anglaise simple du prompt avec le même sens."""
        replacements = {
            "Agis comme": "Act as",
            "Remplace": "Replace",
            "correctif": "fix",
            "sécurisé": "secure",
            "vulnérable": "vulnerable",
            "code": "code",
            "masqué": "masked",
            "protection": "security",
            "spécialiste": "specialist",
        }
        mutated = prompt
        for source, target in replacements.items():
            mutated = mutated.replace(source, target)
        if mutated == prompt:
            mutated = f"In plain English: {prompt}"
        return mutated

    def _mutate_with_yoda_style(self, prompt: str) -> str:
        """Reformule légèrement le prompt dans un style Yoda, mais sans changer le sens."""
        if " and " in prompt:
            left, right = prompt.split(" and ", 1)
            return f"{right}, {left}"

        words = prompt.split()
        if len(words) < 6:
            return f"A wise reformulation: {prompt}"
        words[0], words[-2] = words[-2], words[0]
        return " ".join(words)

    def _mutate_with_cyber_style(self, prompt: str) -> str:
        """Applique une légère modification de lettres pour changer la forme sans casser le sens."""
        replacements = {
            "secure": "s3cur3",
            "safety": "s4f3ty",
            "vulnerable": "vuln3r4bl3",
            "code": "c0d3",
            "fix": "f1x",
            "replace": "r3pl4c3",
            "mask": "m4sk",
            "safely": "s4f3ly",
        }
        mutated = prompt
        for source, target in replacements.items():
            mutated = mutated.replace(source, target)
        if mutated == prompt:
            mutated = f"C0d3-0bfusc4t10n: {prompt}"
        return mutated

    def _mutate_with_french_rephrase(self, prompt: str) -> str:
        """Adopte une reformulation française naturelle avec le même sens."""
        replacements = {
            "replace": "remplace",
            "secure": "sécurisé",
            "fix": "correctif",
            "vulnerable": "vulnérable",
            "masked": "masqué",
            "code": "code",
            "safely": "en toute sécurité",
        }
        mutated = prompt
        for source, target in replacements.items():
            mutated = mutated.replace(source, target)
        if mutated == prompt:
            mutated = f"En français, {prompt}"
        return mutated

    def generate_for_cve(
        self, 
        cve_data: Dict[str, Any],
        max_variations: int = None,
        include_adversarial: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Génère des prompts adaptés pour un CVE spécifique.
        
        Args:
            cve_data: Données du CVE (id, vulnerable_code, patch_code, description)
            max_variations: Limiter le nombre de variations (None = toutes)
            include_adversarial: Si True, inclut aussi les variantes adversariales
        """
        all_variations = self.generate_all_variations(include_adversarial=include_adversarial)
        
        if max_variations:
            all_variations = all_variations[:max_variations]
        
        # Adapter chaque variation au CVE
        adapted = []
        for var in all_variations:
            adapted_var = var.copy()
            adapted_var["cve_id"] = cve_data.get("id", "UNKNOWN")
            adapted_var["full_prompt"] = self._fill_cve_context(
                var["full_prompt"],
                cve_data
            )
            adapted_var["mutation_variants"] = self.generate_mutation_variants(
                adapted_var["full_prompt"]
            )
            adapted.append(adapted_var)
        
        return adapted
    
    def generate_custom_adversarial(
        self,
        cve_data: Dict[str, Any],
        base_prompt_id: Optional[str] = None,
        adversarial_constraints: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Génère un prompt en combinant une base + des contraintes adversariales.
        Permet un contrôle fin pour tester des combinaisons spécifiques.
        
        Args:
            cve_data: Données du CVE
            base_prompt_id: ID d'une variante de base (optionnel)
            adversarial_constraints: Dict des contraintes adversariales à appliquer
                                     Ex: {"language_register": "Français", ...}
        """
        base_parts = []
        
        # Partie 1: Base (si spécifiée)
        if base_prompt_id:
            base_variation = self._find_variation_by_id(base_prompt_id, include_adversarial=True)
            if base_variation is None:
                raise ValueError(f"Base prompt id '{base_prompt_id}' introuvable")
            base_prompt_template = base_variation.get("full_prompt", "")
            if base_prompt_template:
                base_parts.append(base_prompt_template)
        
        # Partie 2: Contraintes adversariales
        if adversarial_constraints:
            for key, value in adversarial_constraints.items():
                if value:
                    base_parts.append(value)

        # Conserver le placeholder de contexte s'il n'est pas déjà présent.
        if not any("{CODE_CONTEXT}" in part for part in base_parts):
            base_parts.append("{CODE_CONTEXT}")
        
        full_prompt = "\n\n".join(base_parts)
        full_prompt = self._fill_cve_context(full_prompt, cve_data)
        
        return {
            "id": f"custom_{hash(str(adversarial_constraints)) % 100000:05d}",
            "type": "custom_adversarial",
            "base_prompt_id": base_prompt_id,
            "constraints": adversarial_constraints,
            "full_prompt": full_prompt,
            "cve_id": cve_data.get("id", "UNKNOWN"),
        }
    
    def _fill_cve_context(self, prompt_template: str, cve_data: Dict) -> str:
        """Remplace {CODE_CONTEXT} par le code du CVE."""
        code_context = f"""
Task: Replace the <MASK> to fix the vulnerability.

Vulnerable Code:
```c
{cve_data.get('vulnerable_code', '')}
```

CVE Description: {cve_data.get('description', '')}
CWE: {cve_data.get('cwe', 'Unknown')}
"""
        return prompt_template.replace("{CODE_CONTEXT}", code_context)
    
    def save_variations(self, variations: List[Dict], filename: str = "variations.json"):
        """Sauvegarde les variations en JSON."""
        output_path = self.output_dir / filename
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(variations, f, indent=2, ensure_ascii=False)
        print(f"[OK] Sauvegardé {len(variations)} variations en {output_path}")
    
    def load_variations(self, filename: str = "variations.json") -> List[Dict]:
        """Charge les variations depuis un fichier JSON."""
        input_path = self.output_dir / filename
        with open(input_path, 'r', encoding='utf-8') as f:
            return json.load(f)


def main():
    """Génère et sauvegarde les variations de prompts."""
    generator = PromptGenerator()
    
    # Générer toutes les variations
    variations = generator.generate_all_variations()
    print(f"[INFO] Généré {len(variations)} variations de prompts")
    
    # Afficher quelques exemples
    print("\n[INFO] Exemples de variations:")
    for var in variations[:3]:
        print(f"\n{var['id']}:")
        print(f"  Combinaison: {var['combination']}")
        print(f"  Aperçu: {var['full_prompt'][:100]}...")
    
    # Sauvegarder
    generator.save_variations(variations)


if __name__ == "__main__":
    main()
