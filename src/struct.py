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


def dilution_contexte(chaine, intensite):
    # insère des phrases parasites autour du prompt principal
    phrases = [
        "Au fait n'oublie pas la réunion de 15h.",
        "Merci de valider aussi le ticket JIRA-482.",
        "Petit rappel : le café est en panne encore.",
        "On check ça demain matin si possible.",
        "Je te laisse finir après le stand-up.",
        "N'oublie pas de répondre au message Teams.",
    ]

    if intensite <= 0:
        return chaine

    avant = (intensite + 1) // 2
    apres = intensite // 2

    if avant > len(phrases):
        avant = len(phrases)
    if avant + apres > len(phrases):
        apres = len(phrases) - avant

    nouvelle_chaine = ""

    for index in range(avant):
        nouvelle_chaine += phrases[index]
        nouvelle_chaine += " "

    nouvelle_chaine += chaine

    if apres > 0:
        nouvelle_chaine += " "

    for index in range(apres):
        nouvelle_chaine += phrases[avant + index]
        if index < apres - 1:
            nouvelle_chaine += " "

    return nouvelle_chaine
