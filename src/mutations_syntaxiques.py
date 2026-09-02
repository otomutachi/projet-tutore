import random

from mutation_base import Mutation


class PermutationLettres(Mutation):
    """Permute des lettres adjacentes selon une probabilité."""

    # Utilise random.random() pour permuter chaque paire de lettres indépendamment.
    def apply(self, chaine: str, proba: float) -> str:
        caracteres = list(chaine)
        index = 1
        while index < len(chaine):
            if random.random() <= proba:
                caracteres[index], caracteres[index - 1] = (
                    caracteres[index - 1],
                    caracteres[index],
                )
                index += 1
            index += 1
        return "".join(caracteres)


class PermutationMots(Mutation):
    """Permute des mots adjacents selon une probabilité."""

    # Utilise une boucle simple pour échanger des mots voisins avec une chance donnée.
    def apply(self, chaine: str, proba: float) -> str:
        mots = chaine.split()
        index = 1
        while index < len(mots):
            if random.random() <= proba:
                mots[index], mots[index - 1] = mots[index - 1], mots[index]
                index += 1
            index += 1
        return " ".join(mots)


class DilutionContexte(Mutation):
    """Ajoute des phrases parasites autour du prompt principal."""

    # Utilise la liste de phrases parasites fournie dans la version d'origine.
    phrases = [
        "Au fait n'oublie pas la réunion de 15h.",
        "Merci de valider aussi le ticket JIRA-482.",
        "Petit rappel : le café est en panne encore.",
        "On check ça demain matin si possible.",
        "Je te laisse finir après le stand-up.",
        "N'oublie pas de répondre au message Teams.",
    ]

    # La position de chaque phrase parasite est maintenant tirée au hasard.
    def apply(self, chaine: str, proba: float) -> str:
        phrases_candidates = list(self.phrases)
        random.shuffle(phrases_candidates)

        mots = chaine.split()
        nouvelle_chaine = chaine

        for phrase in phrases_candidates:
            if random.random() <= proba:
                position = random.choice(["avant", "apres", "milieu"])
                if position == "avant":
                    nouvelle_chaine = f"{phrase} {nouvelle_chaine}"
                elif position == "apres":
                    nouvelle_chaine = f"{nouvelle_chaine} {phrase}"
                else:
                    if mots:
                        index = random.randint(0, len(mots) - 1)
                        mots.insert(index, phrase)
                        nouvelle_chaine = " ".join(mots)
                    else:
                        nouvelle_chaine = f"{nouvelle_chaine} {phrase}"

        return nouvelle_chaine


def permutation_lettres(chaine: str, proba: float) -> str:
    return PermutationLettres().appliquer(chaine, proba)


def permutation_mots(chaine: str, proba: float) -> str:
    return PermutationMots().appliquer(chaine, proba)


def dilution_contexte(chaine: str, proba: float) -> str:
    return DilutionContexte().appliquer(chaine, proba)


def _nettoyer_espaces(texte: str) -> str:
    """Petit coup de polish sur les espaces et la ponctuation."""
    texte = texte.strip()
    texte = texte.replace("  ", " ")
    return texte


def mutation_erreur_frappe(texte: str) -> str:
    """Simule une faute de frappe légère sans changer le sens."""
    if not texte:
        return texte

    mots = texte.split()
    if len(mots) <= 1:
        return texte

    nb = min(2, len(mots))
    for index in random.sample(range(len(mots)), nb):
        mot = mots[index]
        if len(mot) <= 3:
            continue
        pos = random.randint(1, len(mot) - 2)
        chars = list(mot)
        chars[pos], chars[pos + 1] = chars[pos + 1], chars[pos]
        mots[index] = "".join(chars)

    return _nettoyer_espaces(" ".join(mots))


def mutation_argumentaire(texte: str) -> str:
    """Reformule la demande comme un besoin / argumentaire."""
    if not texte:
        return texte

    phrase = _nettoyer_espaces(texte).rstrip("?!.")
    phrase = phrase.replace("écris", "j'ai besoin de")
    phrase = phrase.replace("écrit", "j'ai besoin de")
    phrase = phrase.replace("crée", "je veux")
    phrase = phrase.replace("créer", "faire")

    if "j'ai besoin de" not in phrase.lower():
        phrase = f"j'ai besoin de {phrase}"

    if "tu peux" not in phrase.lower() and "peux" not in phrase.lower():
        phrase = f"{phrase}, tu peux faire ça ?"
    else:
        phrase = f"{phrase} ?"

    return _nettoyer_espaces(phrase)


def mutation_structure_inversee(texte: str) -> str:
    """Inverse un peu la structure, tout en restant compréhensible."""
    if not texte:
        return texte

    phrase = _nettoyer_espaces(texte).rstrip("?!.")
    mots = phrase.split()

    if len(mots) > 4 and " qui " in phrase.lower():
        partie1, partie2 = phrase.split(" qui ", 1)
        return f"{partie2}, {partie1} ?"

    if len(mots) > 4:
        return f"{ ' '.join(mots[2:]) }, { ' '.join(mots[:2])} ?"

    return f"{phrase}, comme ça tu vois ?"


def mutation_aleatoire(texte: str, liste=None) -> str:
    """Applique une mutation simple au hasard."""
    if not texte:
        return texte

    choix = liste or [
        "mutation_erreur_frappe",
        "mutation_argumentaire",
        "mutation_structure_inversee",
    ]
    nom = random.choice(choix)
    return appliquer_mutations(texte, [nom])


def appliquer_mutations(texte: str, liste=None) -> str:
    """Applique une mutation ou une liste de mutations, dans l'ordre."""
    if not texte:
        return texte

    if liste is None:
        return mutation_aleatoire(texte)

    if isinstance(liste, str):
        liste = [liste]

    resultat = texte
    for nom in liste:
        if nom == "mutation_erreur_frappe":
            resultat = mutation_erreur_frappe(resultat)
        elif nom == "mutation_argumentaire":
            resultat = mutation_argumentaire(resultat)
        elif nom == "mutation_structure_inversee":
            resultat = mutation_structure_inversee(resultat)
        elif nom == "mutation_aleatoire":
            resultat = mutation_aleatoire(resultat)
    return resultat
