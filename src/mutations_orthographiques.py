import random

from mutation_base import Mutation


class RemplacementEPar3(Mutation):
    """Remplace les lettres e/E par 3 selon une probabilité."""

    # Utilise random.random() pour remplacer chaque lettre e/E indépendamment.
    def apply(self, chaine: str, proba: float) -> str:
        nouvelle_chaine = ""
        remplacements = 0
        for caractere in chaine:
            if caractere == "e" and random.random() <= proba:
                nouvelle_chaine += "3"
                remplacements += 1
            elif caractere == "E" and random.random() <= proba:
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
            if caractere in self.remplacement and random.random() <= proba:
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
            if remplacement is not None and random.random() <= proba:
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
            if remplacement is not None and random.random() <= proba:
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
