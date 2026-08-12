import random

from mutation_base import Mutation
from pydict_wrapper import rechercher_synonymes, traduire_texte


class RemplacementSynonymes(Mutation):
    """Mutation qui remplace certains mots par un synonyme live PyDictionary."""

    def __init__(self):
        super().__init__()

    def apply(self, chaine: str, proba: float) -> str:
        """Applique une substitution de synonymes sur chaque mot de la chaîne.

        Pour chaque mot, la probabilité `proba` détermine si on tente de chercher
        un synonyme. Si PyDictionary retourne une liste valide, on prend le premier
        synonyme et on conserve la ponctuation finale.
        """
        if not chaine:
            return chaine

        mots = chaine.split()
        nouvelle_liste = []
        for mot in mots:
            mot_propre = mot.strip(".,!?;:")
            if random.random() <= proba:
                syns = rechercher_synonymes(mot_propre)
                if syns:
                    syn = syns[0]
                    if mot_propre.istitle():
                        syn = syn.capitalize()
                    suffix = mot[len(mot_propre) :]
                    nouvelle_liste.append(syn + suffix)
                    continue
            nouvelle_liste.append(mot)
        return " ".join(nouvelle_liste)


class TraductionGenerique(Mutation):
    """Mutation qui traduit certains mots en utilisant PyDictionary."""

    def __init__(self, langue_cible: str = "en"):
        super().__init__()
        self.langue_cible = langue_cible

    def apply(self, chaine: str, proba: float) -> str:
        """Applique une traduction mot-à-mot à un texte.

        Chaque mot est isolé, on tente sa traduction si la probabilité est respectée.
        Les mots non traduits restent inchangés, et la ponctuation est conservée.
        """
        if not chaine:
            return chaine

        mots = chaine.split()
        nouvelle_liste = []
        for mot in mots:
            mot_propre = mot.strip(".,!?;:")
            if random.random() <= proba:
                traduction = traduire_texte(mot_propre, self.langue_cible)
                if traduction and traduction != mot_propre:
                    suffix = mot[len(mot_propre) :]
                    nouvelle_liste.append(traduction + suffix)
                    continue
            nouvelle_liste.append(mot)
        return " ".join(nouvelle_liste)


def remplacement_synonymes(chaine: str, proba: float) -> str:
    """Facilité exportable pour appliquer la mutation de synonymes."""
    return RemplacementSynonymes().appliquer(chaine, proba)


def traduction_vers(chaine: str, target_lang: str, proba: float) -> str:
    """Facilité exportable pour appliquer une traduction vers une langue cible."""
    return TraductionGenerique(target_lang).appliquer(chaine, proba)


TraductionAnglais = TraductionGenerique


def traduction_anglais(chaine: str, proba: float) -> str:
    """Facilité exportable pour traduire vers l'anglais."""
    return TraductionGenerique("en").appliquer(chaine, proba)
