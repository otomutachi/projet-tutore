#!/usr/bin/env python3
# Script principal simple qui montre des mutations de prompts

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from mutations_orthographiques import (
    AlphabetGrec,
    FauteDeFrappe,
    RemplacementAccents,
    RemplacementEPar3,
)
from mutations_semantiques import RemplacementSynonymes, TraductionAnglais
from mutations_syntaxiques import DilutionContexte, PermutationLettres, PermutationMots
from utils import afficher_resultats, charger_prompts, sauvegarder_prompts


def appliquer_mutations(chaine: str, liste_mutations, proba: float) -> str:
    resultat = chaine
    for mutation in liste_mutations:
        if hasattr(mutation, "appliquer"):
            resultat = mutation.appliquer(resultat, proba)
        else:
            resultat = mutation(resultat, proba)
    return resultat


def main() -> int:
    prompts = charger_prompts(PROJECT_ROOT / "prompts.json")
    if not prompts:
        prompts = [
            "Projet tutoré sur les prompts",
            "Chaîne de caractères en entrée",
            "Génère un code sécurisé pour cette fonction.",
            "String as input",
            "Projets tutorés sur les LLMs",
        ]

    mutations = [
        ("remplacement_e_par_3", RemplacementEPar3()),
        ("remplacement_accents", RemplacementAccents()),
        ("faute_de_frappe", FauteDeFrappe()),
        ("alphabet_grec", AlphabetGrec()),
        ("permutation_lettres", PermutationLettres()),
        ("permutation_mots", PermutationMots()),
        ("dilution_contexte", DilutionContexte()),
        ("remplacement_synonymes", RemplacementSynonymes()),
        ("traduction_anglais", TraductionAnglais()),
    ]

    resultats = []
    probas = [0.2, 0.8]
    prompts_affiches = [prompts[0], prompts[2]]

    print("=" * 60)
    print("DEMONSTRATION DES MUTATIONS PROBABILISTES")
    print("=" * 60)

    for nom_mutation, mutation in mutations:
        print(f"\n=== {nom_mutation.upper()} ===")
        for proba in probas:
            prompts_mutes = [mutation.appliquer(prompt, proba) for prompt in prompts]
            prompts_affiches_mutes = [
                mutation.appliquer(prompt, proba) for prompt in prompts_affiches
            ]
            print(f"\nProbabilite : {proba}")
            afficher_resultats(prompts_affiches, prompts_affiches_mutes, nom_mutation)
            resultats.append(
                {
                    "mutation": nom_mutation,
                    "proba": proba,
                    "prompts": [
                        {"original": original, "mute": mute}
                        for original, mute in zip(prompts, prompts_mutes)
                    ],
                }
            )

    sauvegarder_prompts(resultats, PROJECT_ROOT / "resultats.json")

    print("\n" + "=" * 60)
    print("Résultats sauvegardés dans 'resultats.json'")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    main()
