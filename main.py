#!/usr/bin/env python3
"""Point d'entrée principal du projet.

Ce script affiche quelques variantes de prompts générées par le module
prompts_generator pour illustrer le comportement du projet.
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from prompt_generator import PromptGenerator


def main() -> int:
    """Génère et affiche des variantes de prompts simples."""
    print("""
    ============================================================
      Prompt Mutation Demo
      Génération de variantes de prompts avec le même sens
    ============================================================
    """)

    generator = PromptGenerator()
    base_prompt = "Replace the masked code with a secure fix."
    variants = generator.generate_mutation_variants(
        base_prompt,
        mutation_types=["synonymes", "yoda", "anglais", "francais", "cyber"],
    )

    if not variants:
        print("[INFO] Aucune variante n'a pu être générée.")
        return 1

    print(f"[INFO] {len(variants)} variantes générées")
    for index, variant in enumerate(variants, start=1):
        print(f"{index}. {variant}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
