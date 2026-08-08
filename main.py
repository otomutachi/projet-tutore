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
from utils import afficher_resultats, charger_prompts, charger_prompts_cve, sauvegarder_prompts
from pydict_wrapper import translate_text

PROMPTS_DE_FALLBACK = [
    "Projet tutoré sur les prompts",
    "Chaîne de caractères en entrée",
    "Génère un code sécurisé pour cette fonction.",
    "String as input",
    "Projets tutorés sur les LLMs",
]


def appliquer_mutations(chaine: str, liste_mutations, proba: float) -> str:
    resultat = chaine
    for mutation in liste_mutations:
        if hasattr(mutation, "appliquer"):
            resultat = mutation.appliquer(resultat, proba)
        else:
            resultat = mutation(resultat, proba)
    return resultat


def main() -> int:
    prompts = charger_prompts(PROJECT_ROOT / "dataset1_of_prompts.json")
    if not prompts:
        prompts = charger_prompts(PROJECT_ROOT / "prompts.json")
    if not prompts:
        prompts = PROMPTS_DE_FALLBACK

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
    prompts_affiches = prompts[: min(2, len(prompts))]
    if not prompts_affiches:
        prompts_affiches = ["Projet tutoré sur les prompts"]

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

    cve_prompts = charger_prompts_cve(PROJECT_ROOT / "prompts_cve.json")
    if cve_prompts:
        print("\n" + "=" * 60)
        print("TEST A GRANDE ECHELLE AVEC PROMPTS CVE")
        print("=" * 60)
        exemples = list(cve_prompts.items())[:2]
        mutations_grandes = [RemplacementSynonymes(), PermutationLettres(), DilutionContexte()]
        for constraint, prompt in exemples:
            print(f"\nContrainte : {constraint}")
            # use afficher_resultats sanitizer by passing single-item lists
            afficher_resultats([prompt], [prompt], nom_mutation="original_cve_preview")
            for mutation in mutations_grandes:
                resultat = mutation.appliquer(prompt, 0.7)
                afficher_resultats([prompt], [resultat], nom_mutation=mutation.__class__.__name__)

    print("\n" + "=" * 60)
    print("Résultats sauvegardés dans 'resultats.json'")
    print("=" * 60)

    # Démonstration simple de la fonction de traduction PyDictionary
    try:
        exemple = "voiture rapide et sécurisée"
        trad = translate_text(exemple, "en")
        print("\n=== DEMO TRADUCTION PYDICTIONARY ===")
        print("Original :", exemple)
        print("Traduction (en) :", trad)
    except Exception:
        # Ne pas faire échouer le script si PyDictionary n'est pas disponible
        pass

    return 0


if __name__ == "__main__":
    main()
