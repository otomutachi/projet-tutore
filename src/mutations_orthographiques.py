import random

from mutation_base import Mutation


class RemplacementEPar3(Mutation):
    """Remplace les lettres e/E par 3 selon une probabilité."""

    # Utilise random.random() pour remplacer chaque lettre e/E indépendamment.
    def apply(self, chaine: str, proba: float) -> str:
        nouvelle_chaine = ""
        remplacements = 0
        for caractere in chaine:
            if caractere == "e" and random.random() < proba:
                nouvelle_chaine += "3"
                remplacements += 1
            elif caractere == "E" and random.random() < proba:
                nouvelle_chaine += "3"
                remplacements += 1
            else:
                nouvelle_chaine += caractere
        return nouvelle_chaine


class RemplacementAccents(Mutation):
    """Retire quelques accents pour modifier le texte."""

    # Utilise le dictionnaire d'accents exact fourni dans la version d'origine.
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

    def apply(self, chaine: str, proba: float) -> str:
        nouvelle_chaine = ""
        remplacements = 0
        for caractere in chaine:
            if caractere in self.remplacement and random.random() < proba:
                nouvelle_chaine += self.remplacement[caractere]
                remplacements += 1
            else:
                nouvelle_chaine += caractere
        return nouvelle_chaine


class FauteDeFrappe(Mutation):
    """Simule une faute de frappe avec un voisinage de clavier AZERTY."""

    # Utilise un petit dictionnaire de voisinage pour imiter les erreurs de frappe.
    voisinage = {
        "a": "q",
        "q": "a",
        "z": "s",
        "s": "z",
        "e": "r",
        "r": "e",
        "t": "y",
        "y": "t",
        "u": "i",
        "i": "u",
        "o": "p",
        "p": "o",
        "l": "m",
        "m": "l",
        "d": "f",
        "f": "d",
    }

    def apply(self, chaine: str, proba: float) -> str:
        nouvelle_chaine = ""
        for caractere in chaine:
            remplacement = self.voisinage.get(caractere)
            if remplacement is not None and random.random() < proba:
                nouvelle_chaine += remplacement
            else:
                nouvelle_chaine += caractere
        return nouvelle_chaine


class AlphabetGrec(Mutation):
    """Remplace certaines lettres par des équivalents grecs visuellement proches."""

    # Utilise un dictionnaire simple pour changer quelques lettres sans changer le sens.
    remplacement = {
        "a": "α",
        "e": "ε",
        "o": "ο",
        "p": "ρ",
        "i": "ι",
        "u": "υ",
        "c": "ϲ",
        "s": "ς",
        "v": "ν",
        "x": "χ",
    }

    def apply(self, chaine: str, proba: float) -> str:
        nouvelle_chaine = ""
        for caractere in chaine:
            remplacement = self.remplacement.get(caractere.lower())
            if remplacement is not None and random.random() < proba:
                if caractere.isupper():
                    nouvelle_chaine += remplacement.upper()
                else:
                    nouvelle_chaine += remplacement
            else:
                nouvelle_chaine += caractere
        return nouvelle_chaine


def remplacement_e_par_3(chaine: str, proba: float) -> str:
    return RemplacementEPar3().appliquer(chaine, proba)


def remplacement_accents(chaine: str, proba: float) -> str:
    return RemplacementAccents().appliquer(chaine, proba)


def faute_de_frappe(chaine: str, proba: float) -> str:
    return FauteDeFrappe().appliquer(chaine, proba)


def alphabet_grec(chaine: str, proba: float) -> str:
    return AlphabetGrec().appliquer(chaine, proba)


def doubler_ponctuation(texte: str, seed: int) -> str:
    """Duplique un signe de ponctuation choisi au hasard."""
    positions = [index for index, caractere in enumerate(texte) if caractere in ".,!?"]
    if not positions:
        return texte

    generateur = random.Random(seed)
    position = generateur.choice(positions)
    return texte[:position] + texte[position] + texte[position:]


def inserer_virgule_aleatoire(texte: str, seed: int) -> str:
    """Insere une virgule entre deux mots a une position aleatoire."""
    import re

    if not any(caractere in texte for caractere in ".,!?"):
        return texte

    positions = [
        correspondance.end()
        for correspondance in re.finditer(r"\S+(?=\s+\S)", texte)
    ]
    if not positions:
        return texte

    generateur = random.Random(seed)
    position = generateur.choice(positions)
    return texte[:position] + "," + texte[position:]


def casse_apres_ponctuation(texte: str, seed: int) -> str:
    """Met en minuscule une lettre choisie apres un point."""
    import re

    correspondances = list(re.finditer(r"\.\s([A-ZÀ-ÖØ-Þ])", texte))
    if not correspondances:
        return texte

    generateur = random.Random(seed)
    correspondance = generateur.choice(correspondances)
    position = correspondance.start(1)
    return texte[:position] + texte[position].lower() + texte[position + 1:]


def remplacer_ponctuation_aleatoire(texte: str, seed: int) -> str:
    """Remplace un signe de ponctuation par un autre signe."""
    signes = ".,!?;"
    positions = [index for index, caractere in enumerate(texte) if caractere in signes]
    if not positions:
        return texte

    generateur = random.Random(seed)
    position = generateur.choice(positions)
    original = texte[position]
    remplacements = [signe for signe in signes if signe != original]
    remplacement = generateur.choice(remplacements)
    return texte[:position] + remplacement + texte[position + 1:]
