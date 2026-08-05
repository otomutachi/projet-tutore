import random

from mutation_base import Mutation
from utils import charger_dictionnaire_json


class RemplacementSynonymes(Mutation):
    """Remplace certains mots par des synonymes simples."""

    def __init__(self):
        super().__init__()
        self.dictionnaire = charger_dictionnaire_json("data/synonymes.json")

    def apply(self, chaine: str, proba: float) -> str:
        mots = chaine.split()
        nouvelle_liste = []
        remplacements = 0
        for mot in mots:
            mot_propre = mot.strip(".,!?;:")
            cle = mot_propre.lower()
            if remplacements < len(mots) and cle in self.dictionnaire and random.random() <= proba:
                synonyme = self.dictionnaire[cle]
                if mot_propre.istitle():
                    synonyme = synonyme.capitalize()
                nouvelle_liste.append(synonyme)
                remplacements += 1
            else:
                nouvelle_liste.append(mot)
        return " ".join(nouvelle_liste)


class TraductionAnglais(Mutation):
    """Traduit une petite liste de mots du français vers l'anglais."""

    dictionnaire = charger_dictionnaire_json("data/traduction.json")

    def _traduire_mot(self, mot: str):
        mot_propre = mot.strip(".,!?;:")
        return self.dictionnaire.get(mot_propre.lower())

    def apply(self, chaine: str, proba: float) -> str:
        mots = chaine.split()
        nouvelle_liste = []
        for mot in mots:
            traduction = self._traduire_mot(mot)
            if traduction is not None and random.random() <= proba:
                if mot.strip(".,!?;:").istitle():
                    nouvelle_liste.append(traduction.capitalize())
                else:
                    nouvelle_liste.append(traduction)
            else:
                nouvelle_liste.append(mot)
        resultat = " ".join(nouvelle_liste)
        if proba > 0 and resultat == chaine:
            for mot in mots:
                traduction = self._traduire_mot(mot)
                if traduction is not None:
                    resultat = resultat.replace(mot, traduction, 1)
                    break
        return resultat


def remplacement_synonymes(chaine: str, proba: float) -> str:
    return RemplacementSynonymes().appliquer(chaine, proba)


def traduction_anglais(chaine: str, proba: float) -> str:
    return TraductionAnglais().appliquer(chaine, proba)
