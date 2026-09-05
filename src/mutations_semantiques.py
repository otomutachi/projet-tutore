import re
import random

from mutation_base import Mutation
from pydict_wrapper import obtenir_synonyme, obtenir_traduction


_TOKEN_MOT = re.compile(r"^(?P<prefix>[^\wÀ-ÿ]*)(?P<mot>[\wÀ-ÿ]+)(?P<suffix>[^\wÀ-ÿ]*)$", re.UNICODE)
_MOTS_OUTILS = {
    "a", "au", "aux", "avec", "ce", "ces", "dans", "de", "des", "du",
    "en", "et", "il", "la", "le", "les", "mais", "ne", "nos", "ou",
    "par", "pas", "pour", "que", "qui", "sur", "un", "une", "vos", "vous",
}


def _decomposer_mot(mot: str):
    correspondance = _TOKEN_MOT.match(mot)
    if correspondance is None:
        return None
    return (
        correspondance.group("prefix"),
        correspondance.group("mot"),
        correspondance.group("suffix"),
    )


def reformuler_phrase(chaine: str, proba: float = 0.5, seed=None) -> str:
    """Reformule les mots en conservant espaces et ponctuation."""
    if not chaine:
        return chaine

    generateur = random.Random(seed)
    morceaux = re.findall(r"\s+|\S+", chaine, re.UNICODE)
    resultat = []
    for morceau in morceaux:
        parties = _decomposer_mot(morceau)
        if parties is None:
            resultat.append(morceau)
            continue
        prefixe, mot, suffixe = parties
        if generateur.random() >= proba:
            resultat.append(morceau)
            continue
        sous_seed = generateur.randrange(2**32)
        remplacement = obtenir_synonyme(mot, sous_seed)
        if remplacement is None:
            remplacement = obtenir_traduction(mot, sous_seed)
        if remplacement and remplacement.lower() not in _MOTS_OUTILS:
            if mot.istitle():
                remplacement = remplacement.capitalize()
            resultat.append(prefixe + remplacement + suffixe)
        else:
            resultat.append(morceau)
    return "".join(resultat)


class RemplacementSynonymes(Mutation):
    """Mutation qui remplace certains mots par un synonyme via wn."""

    def __init__(self):
        super().__init__()

    def appliquer(self, chaine: str, proba: float, seed=None) -> str:
        if not 0 <= proba <= 1:
            raise ValueError("proba doit être compris entre 0 et 1")
        return self.apply(chaine, proba, seed)

    def apply(self, chaine: str, proba: float, seed=None) -> str:
        """Applique une substitution de synonymes sur chaque mot de la chaîne.

        Pour chaque mot, la probabilité `proba` détermine si on tente de chercher
        un synonyme. Si la liste est valide, on choisit un synonyme au hasard pour
        faire varier les résultats d'un run à l'autre.
        """
        if not chaine:
            return chaine

        mots = chaine.split()
        nouvelle_liste = []
        generateur = random.Random(seed)
        for mot in mots:
            parties = _decomposer_mot(mot)
            if parties is not None:
                prefixe, mot_propre, suffixe = parties
                if generateur.random() < proba:
                    sous_seed = generateur.randrange(2**32)
                    remplacement = obtenir_synonyme(mot_propre, sous_seed)
                    if remplacement and remplacement.lower() not in _MOTS_OUTILS:
                        if mot_propre.istitle():
                            remplacement = remplacement.capitalize()
                        nouvelle_liste.append(prefixe + remplacement + suffixe)
                        continue
            nouvelle_liste.append(mot)
        return " ".join(nouvelle_liste)


class TraductionGenerique(Mutation):
    """Mutation qui traduit certains mots via argostranslate."""

    def __init__(self, langue_cible: str = "en"):
        super().__init__()
        self.langue_cible = langue_cible

    def appliquer(self, chaine: str, proba: float, seed=None) -> str:
        if not 0 <= proba <= 1:
            raise ValueError("proba doit être compris entre 0 et 1")
        return self.apply(chaine, proba, seed)

    def apply(self, chaine: str, proba: float, seed=None) -> str:
        """Applique une traduction mot-à-mot à un texte.

        Chaque mot est isolé, on tente sa traduction si la probabilité est respectée.
        Les mots non traduits restent inchangés, et la ponctuation est conservée.
        """
        if not chaine:
            return chaine

        mots = chaine.split()
        nouvelle_liste = []
        generateur = random.Random(seed)
        for mot in mots:
            parties = _decomposer_mot(mot)
            if parties is not None:
                prefixe, mot_propre, suffixe = parties
                if generateur.random() < proba:
                    remplacement = obtenir_synonyme(mot_propre, generateur.randrange(2**32))
                    if remplacement is None:
                        remplacement = obtenir_traduction(mot_propre, generateur.randrange(2**32))
                    if remplacement and remplacement != mot_propre:
                        nouvelle_liste.append(prefixe + remplacement + suffixe)
                        continue
            nouvelle_liste.append(mot)
        return " ".join(nouvelle_liste)


def remplacement_synonymes(chaine: str, proba: float, seed=None) -> str:
    """Facilité exportable pour appliquer la mutation de synonymes."""
    return RemplacementSynonymes().appliquer(chaine, proba, seed)


def traduction_vers(chaine: str, target_lang: str, proba: float, seed=None) -> str:
    """Facilité exportable pour appliquer une traduction vers une langue cible."""
    return TraductionGenerique(target_lang).appliquer(chaine, proba, seed)


TraductionAnglais = TraductionGenerique


def traduction_anglais(chaine: str, proba: float, seed=None) -> str:
    """Facilité exportable pour traduire vers l'anglais."""
    return TraductionGenerique("en").appliquer(chaine, proba, seed)
