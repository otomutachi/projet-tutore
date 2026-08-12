import random

from mutation_base import Mutation
from pydict_wrapper import lookup_synonyms, translate_text


class RemplacementSynonymes(Mutation):
    def __init__(self):
        super().__init__()

    def apply(self, chaine: str, proba: float) -> str:
        if not chaine:
            return chaine

        mots = chaine.split()
        nouvelle_liste = []
        for mot in mots:
            mot_propre = mot.strip(".,!?;:")
            if random.random() <= proba:
                syns = lookup_synonyms(mot_propre)
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
    def __init__(self, target_lang: str = "en"):
        super().__init__()
        self.target_lang = target_lang

    def apply(self, chaine: str, proba: float) -> str:
        if not chaine:
            return chaine

        mots = chaine.split()
        nouvelle_liste = []
        for mot in mots:
            mot_propre = mot.strip(".,!?;:")
            if random.random() <= proba:
                tr = translate_text(mot_propre, self.target_lang)
                if tr and tr != mot_propre:
                    suffix = mot[len(mot_propre) :]
                    nouvelle_liste.append(tr + suffix)
                    continue
            nouvelle_liste.append(mot)
        return " ".join(nouvelle_liste)


def remplacement_synonymes(chaine: str, proba: float) -> str:
    return RemplacementSynonymes().appliquer(chaine, proba)


def traduction_vers(chaine: str, target_lang: str, proba: float) -> str:
    return TraductionGenerique(target_lang).appliquer(chaine, proba)


TraductionAnglais = TraductionGenerique


def traduction_anglais(chaine: str, proba: float) -> str:
    return TraductionGenerique("en").appliquer(chaine, proba)
