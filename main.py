#!/usr/bin/env python3
# Script principal simple qui montre des mutations de prompts

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from struct import (
    remplacement_e_par_3,
    permutation_lettres,
    remplacement_synonymes,
    remplacement_accents,
    dilution_contexte,
)


def main():
    # liste de prompts d'exemple
    prompts = [
        "Projet tutoré sur les prompts",
        "chaine de caractères en entrée",
        "Génère un code sécurisé pour cette fonction.",
        "String as input",
        "Projets tutorés sur les LLMs",
    ]

    for prompt in prompts:
        print("\nPrompt original:")
        print(prompt)

        print("\nMutation 1: e -> 3")
        print(remplacement_e_par_3(prompt, 2))

        print("\nMutation 2: permutation de lettres")
        print(permutation_lettres(prompt, 2))

        print("\nMutation 3: synonymes")
        print(remplacement_synonymes(prompt, 2))

        print("\nMutation 4: accents retirés")
        print(remplacement_accents(prompt, 2))

        print("\nMutation 5: dilution de contexte")
        print(dilution_contexte(prompt, 2))
        print("\n" + "-" * 40)

    return 0


if __name__ == "__main__":
    main()
