# Fonctions de mutation simple pour les prompts


def remplacement_e_par_3(chaine, intensite):
    # remplace les premiers 'e' ou 'E' par '3' selon l'intensité
    nouvelle_chaine = ""
    remplacements = 0

    for caractere in chaine:
        if remplacements < intensite and caractere == "e":
            nouvelle_chaine += "3"
            remplacements += 1
        elif remplacements < intensite and caractere == "E":
            nouvelle_chaine += "3"
            remplacements += 1
        else:
            nouvelle_chaine += caractere

    return nouvelle_chaine


def permutation_lettres(chaine, intensite):
    # permute des paires de lettres pour rendre le texte un peu déformé
    caracteres = list(chaine)
    index = 0
    permutations = 0

    while index + 1 < len(caracteres) and permutations < intensite:
        caracteres[index], caracteres[index + 1] = caracteres[index + 1], caracteres[index]
        permutations += 1
        index += 2

    return "".join(caracteres)


def remplacement_synonymes(chaine, intensite):
    # remplace quelques mots par des synonymes simples
    dictionnaire = {
        "projet": "travail",
        "tutoré": "guidé",
        "prompts": "instructions",
        "chaine": "suite",
        "caractères": "lettres",
        "entrée": "input",
        "sur": "concernant",
        "en": "dans",
        "LLMs": "modèles",
    }

    mots = chaine.split()
    nouvelle_liste = []
    remplacements = 0

    for mot in mots:
        mot_propre = mot.strip(".,!?;:")
        cle = mot_propre.lower()

        if remplacements < intensite and cle in dictionnaire:
            synonyme = dictionnaire[cle]
            if mot_propre.istitle():
                synonyme = synonyme.capitalize()
            nouvelle_liste.append(synonyme)
            remplacements += 1
        else:
            nouvelle_liste.append(mot)

    return " ".join(nouvelle_liste)


def remplacement_accents(chaine, intensite):
    # retire quelques accents pour modifier le texte tout en restant lisible
    remplacement = {
        "é": "e",
        "è": "e",
        "ê": "e",
        "à": "a",
        "ù": "u",
        "û": "u",
        "ô": "o",
        "î": "i",
        "ç": "c",
    }

    nouvelle_chaine = ""
    remplacements = 0

    for caractere in chaine:
        if remplacements < intensite and caractere in remplacement:
            nouvelle_chaine += remplacement[caractere]
            remplacements += 1
        else:
            nouvelle_chaine += caractere

    return nouvelle_chaine
