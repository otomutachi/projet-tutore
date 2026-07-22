# Module d'enregistrement des mutations de prompts


def enregistrer_resultat(nom_mutation, prompt_original, prompt_mute, chemin_fichier):
    # ajoute une ligne au fichier CSV avec la mutation et les prompts
    with open(chemin_fichier, "a", encoding="utf-8") as fichier:
        ligne = f"{nom_mutation};{prompt_original};{prompt_mute}\n"
        fichier.write(ligne)
