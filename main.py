#!/usr/bin/env python3
# Script principal simple qui montre des mutations de prompts

import random
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PROJECT_ROOT = Path(__file__).resolve().parent
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from mutations_orthographiques import (
    AlphabetGrec,
    FauteDeFrappe,
    RemplacementAccents,
    RemplacementEPar3,
    casse_apres_ponctuation,
    doubler_ponctuation,
    inserer_virgule_aleatoire,
    remplacer_ponctuation_aleatoire,
)
from mutations_semantiques import RemplacementSynonymes, TraductionAnglais
from mutations_syntaxiques import DilutionContexte, PermutationLettres, PermutationMots
from helpers import afficher_resultats, charger_prompts, charger_prompts_cve, sauvegarder_prompts
from pydict_wrapper import traduire_texte

SOURCE_PROMPTS_FILE = PROJECT_ROOT / "dataset1_of_prompts.json"
PROMPTS_DE_FALLBACK = [
    "Projet tutoré sur les prompts",
    "Chaîne de caractères en entrée",
    "Génère un code sécurisé pour cette fonction.",
    "String as input",
    "Projets tutorés sur les LLMs",
]
DEMO_PROMPT_LIMIT = 2
DEMO_SEED = 20260904
PROMPTS_PONCTUATION = [
    "Bonjour. Comment vas-tu?",
    "Peux-tu corriger ce code, s'il te plaît!",
    "Attention; cette fonction doit être fiable.",
]


def tester_mutations_ponctuation() -> None:
    """Teste et affiche les mutations de ponctuation."""
    mutations = {
        "doubler": doubler_ponctuation,
        "virgule": inserer_virgule_aleatoire,
        "casse": casse_apres_ponctuation,
        "remplacer": remplacer_ponctuation_aleatoire,
    }

    print("\n=== TESTS DES MUTATIONS DE PONCTUATION ===")
    for nom, mutation in mutations.items():
        print(f"\n--- {nom} ---")
        changements = 0
        for index, texte in enumerate(PROMPTS_PONCTUATION):
            resultat = mutation(texte, DEMO_SEED + index)
            print("Original :", texte)
            print("Muté     :", resultat)
            changements += resultat != texte

            if nom == "doubler":
                assert len(resultat) == len(texte) + 1
            elif nom == "virgule":
                assert "," in resultat
        assert changements > 0
    print("Tests de ponctuation reussis")


def _appliquer_mutation(mutation, prompt: str, proba: float, seed: int) -> str:
    """Applique une mutation avec seed quand son API le permet."""
    random.seed(seed)
    try:
        return mutation.appliquer(prompt, proba, seed=seed)
    except TypeError:
        return mutation.appliquer(prompt, proba)


def appliquer_mutations(chaine: str, liste_mutations, proba: float) -> str:
    """Applique une liste de mutations sur une chaîne.

    Cette fonction accepte des objets mutation qui exposent `appliquer` ou des
    fonctions directes. Elle enchaîne les mutations les unes après les autres.
    """
    resultat = chaine
    for mutation in liste_mutations:
        if hasattr(mutation, "appliquer"):
            resultat = mutation.appliquer(resultat, proba)
        else:
            resultat = mutation(resultat, proba)
    return resultat


def main() -> int:
    """Point d'entrée principal du script.

    Charge les prompts depuis `dataset1_of_prompts.json`, puis applique les
    mutations. Si le fichier est absent ou invalide, une liste de secours est
    utilisée.
    """
    prompts = charger_prompts(SOURCE_PROMPTS_FILE)
    if not prompts:
        prompts = charger_prompts(PROJECT_ROOT / "prompts.json")
    if not prompts:
        prompts = PROMPTS_DE_FALLBACK

    tester_mutations_ponctuation()

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
    prompts_demo = prompts[:DEMO_PROMPT_LIMIT]
    prompts_affiches = prompts_demo
    if not prompts_affiches:
        prompts_affiches = ["Projet tutoré sur les prompts"]

    print("=" * 60)
    print("DÉMONSTRATION DES MUTATIONS PROBABILISTES")
    print("=" * 60)

    for nom_mutation, mutation in mutations:
        print(f"\n=== {nom_mutation.upper()} ===")
        for proba in probas:
            prompts_mutes = [
                _appliquer_mutation(mutation, prompt, proba, DEMO_SEED + index)
                for index, prompt in enumerate(prompts_demo)
            ]
            prompts_affiches_mutes = prompts_mutes
            print(f"\nProbabilité : {proba}")
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

    print("\n=== DÉMONSTRATION DU SYNONYME FORCÉ ===")
    exemple = "Projet tutoré sur les prompts"
    mut_syn = RemplacementSynonymes().appliquer(exemple, 1.0)
    print("Original :", exemple)
    print("Muté     :", mut_syn)

    sauvegarder_prompts(resultats, PROJECT_ROOT / "resultats.json")

    cve_prompts = charger_prompts_cve(PROJECT_ROOT / "prompts_cve.json")
    if cve_prompts:
        print("\n" + "=" * 60)
        print("TEST À GRANDE ÉCHELLE AVEC LES PROMPTS CVE")
        print("=" * 60)
        exemples = list(cve_prompts.items())[:2]
        mutations_grandes = [RemplacementSynonymes(), PermutationLettres(), DilutionContexte()]
        for constraint, prompt in exemples:
            print(f"\nContrainte : {constraint}")
            # Utilise l'affichage avec une seule entrée.
            afficher_resultats([prompt], [prompt], nom_mutation="original_cve_preview")
            for mutation in mutations_grandes:
                resultat = mutation.appliquer(prompt, 0.7)
                afficher_resultats([prompt], [resultat], nom_mutation=mutation.__class__.__name__)

    print("\n" + "=" * 60)
    print("Résultats sauvegardés dans 'resultats.json'")
    print("=" * 60)

    # Démonstration simple de la fonction de traduction via argostranslate
    try:
        exemple = "voiture rapide et sécurisée"
        trad = traduire_texte(exemple, "en")
        print("\n=== DÉMONSTRATION DE TRADUCTION ARGOS ===")
        print("Original :", exemple)
        print("Traduction (en) :", trad)
    except Exception:
        pass

    return 0


if __name__ == "__main__":
    main()
