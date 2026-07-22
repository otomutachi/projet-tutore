import json
import os


def charger_prompts(chemin_fichier):
    """Charge une liste de prompts depuis un fichier JSON."""
    if not os.path.exists(chemin_fichier):
        return []
    with open(chemin_fichier, "r", encoding="utf-8") as fichier:
        donnees = json.load(fichier)
    if isinstance(donnees, list):
        return [str(item) for item in donnees]
    return []


def sauvegarder_prompts(prompts, chemin_fichier):
    """Sauvegarde une liste de résultats de mutation dans un fichier JSON."""
    with open(chemin_fichier, "w", encoding="utf-8") as fichier:
        json.dump(prompts, fichier, ensure_ascii=False, indent=2)


def afficher_resultats(prompts_original, prompts_mutes, nom_mutation=""):
    """Affiche proprement la comparaison original/mutation."""
    if nom_mutation:
        print(f"Fonction utilisée : {nom_mutation}")
    for original, mute in zip(prompts_original, prompts_mutes):
        print(f"Original : {original}")
        print(f"Muté     : {mute}")
        print("-" * 40)
