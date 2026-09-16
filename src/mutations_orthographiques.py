import random
import string

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


class MutationPonctuation(Mutation):
    """Base des mutations de ponctuation utilisant une graine locale."""

    def appliquer(self, texte: str, proba: float = 1.0, seed=None) -> str:
        if not 0 <= proba <= 1:
            raise ValueError("proba doit être compris entre 0 et 1")
        return self.apply(texte, proba, seed)


class DoublerPonctuation(MutationPonctuation):
    """Duplique un signe de ponctuation choisi au hasard."""

    def apply(self, texte: str, proba: float = 1.0, seed=None) -> str:
        generateur = random.Random(seed)
        if not texte or proba == 0:
            return texte
        if proba < 1 and generateur.random() >= proba:
            return texte

        positions = [
            index for index, caractere in enumerate(texte)
            if caractere in string.punctuation
        ]
        if not positions:
            return texte

        position = generateur.choice(positions)
        return texte[:position] + texte[position] + texte[position:]


class InsererVirguleAleatoire(MutationPonctuation):
    """Insère une virgule entre deux mots à une position aléatoire."""

    def apply(self, texte: str, proba: float = 1.0, seed=None) -> str:
        generateur = random.Random(seed)
        if not texte or proba == 0:
            return texte
        if proba < 1 and generateur.random() >= proba:
            return texte

        positions = []
        for index in range(len(texte) - 1):
            if not texte[index].isspace() and texte[index + 1].isspace():
                suite = texte[index + 1:].lstrip()
                if suite:
                    positions.append(index + 1)
        if not positions:
            return texte

        position = generateur.choice(positions)
        return texte[:position] + "," + texte[position:]


class CasseApresPonctuation(MutationPonctuation):
    """Met en minuscule une lettre choisie après un point."""

    def apply(self, texte: str, proba: float = 1.0, seed=None) -> str:
        generateur = random.Random(seed)
        if not texte or proba == 0:
            return texte
        if proba < 1 and generateur.random() >= proba:
            return texte

        positions = []
        for index in range(len(texte) - 2):
            if texte[index:index + 2] == ". " and texte[index + 2].isupper():
                positions.append(index + 2)
        if not positions:
            return texte

        position = generateur.choice(positions)
        return texte[:position] + texte[position].lower() + texte[position + 1:]


class RemplacerPonctuationAleatoire(MutationPonctuation):
    """Remplace un signe de ponctuation par un autre signe."""

    def apply(self, texte: str, proba: float = 1.0, seed=None) -> str:
        generateur = random.Random(seed)
        if not texte or proba == 0:
            return texte
        if proba < 1 and generateur.random() >= proba:
            return texte

        signes = string.punctuation
        positions = [index for index, caractere in enumerate(texte) if caractere in signes]
        if not positions:
            return texte

        position = generateur.choice(positions)
        original = texte[position]
        remplacement = generateur.choice(signes.replace(original, ""))
        return texte[:position] + remplacement + texte[position + 1:]


def doubler_ponctuation(texte: str, seed: int) -> str:
    """Compatibilité : duplique un signe de ponctuation choisi au hasard."""
    return DoublerPonctuation().apply(texte, 1.0, seed)


def inserer_virgule_aleatoire(texte: str, seed: int) -> str:
    """Compatibilité : insère une virgule à une position aléatoire."""
    return InsererVirguleAleatoire().apply(texte, 1.0, seed)


def casse_apres_ponctuation(texte: str, seed: int) -> str:
    """Compatibilité : met en minuscule une lettre après un point."""
    return CasseApresPonctuation().apply(texte, 1.0, seed)


def remplacer_ponctuation_aleatoire(texte: str, seed: int) -> str:
    """Compatibilité : remplace un signe de ponctuation au hasard."""
    return RemplacerPonctuationAleatoire().apply(texte, 1.0, seed)
