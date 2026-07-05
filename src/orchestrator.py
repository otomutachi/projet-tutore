"""Compatibilité minimale pour l'ancien point d'entrée du projet."""

from prompt_generator import PromptGenerator


class SecurityEvaluationPipeline:
    """Orchestre une démo simple de génération de variantes de prompts."""

    def __init__(self):
        self.generator = PromptGenerator()

    def run_all(self, max_cves: int = 1, max_prompts_per_cve: int = 1):
        """Génère des variantes de prompts et les affiche de façon simple."""
        base_prompt = "Replace the masked code with a secure fix."
        variants = self.generator.generate_mutation_variants(
            base_prompt,
            mutation_types=["synonymes", "yoda", "anglais", "francais", "cyber"],
        )

        print(f"[INFO] Génération de {min(max_prompts_per_cve, len(variants))} variantes")
        for variant in variants[:max_prompts_per_cve]:
            print(variant)

        return {"base_prompt": base_prompt, "variants": variants[:max_prompts_per_cve]}
