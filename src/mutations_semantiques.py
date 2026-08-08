import random

try:
    from PyDictionary import PyDictionary
except ImportError:
    PyDictionary = None

from mutation_base import Mutation


# prend une phrase et remplace des mots par leurs synonymes trouvés via PyDictionary
class RemplacementSynonymes(Mutation):
    def __init__(self):
        super().__init__()
        self._dict = PyDictionary() if PyDictionary is not None else None

    def apply(self, chaine: str, proba: float) -> str:
        if not chaine:
            return chaine
        if self._dict is None:
            return chaine

        mots = chaine.split()
        nouvelle_liste = []
        for mot in mots:
            mot_propre = mot.strip(".,!?;:")
            # decide per-word whether to try replacing
            if random.random() <= proba:
                try:
                    syns = self._dict.synonym(mot_propre)
                except Exception:
                    syns = None
                if syns:
                    # syns may be a list; choose first and preserve capitalization
                    syn = syns[0]
                    if mot_propre.istitle():
                        syn = syn.capitalize()
                    # keep trailing punctuation
                    suffix = mot[len(mot_propre) :]
                    nouvelle_liste.append(syn + suffix)
                    continue
            nouvelle_liste.append(mot)
        return " ".join(nouvelle_liste)


# traduit une phrase vers la langue cible en utilisant PyDictionary.translate
# param: target_lang est un code de langue ISO (ex: 'en', 'es')
class TraductionGenerique(Mutation):
    def __init__(self, target_lang: str = "en"):
        super().__init__()
        self.target_lang = target_lang
        self._dict = PyDictionary() if PyDictionary is not None else None

    def apply(self, chaine: str, proba: float) -> str:
        if not chaine:
            return chaine
        if self._dict is None:
            return chaine

        mots = chaine.split()
        nouvelle_liste = []
        for mot in mots:
            mot_propre = mot.strip(".,!?;:")
            if random.random() <= proba:
                try:
                    tr = self._dict.translate(mot_propre, self.target_lang)
                except Exception:
                    tr = None
                if tr:
                    if mot_propre.istitle():
                        tr = tr.capitalize()
                    suffix = mot[len(mot_propre) :]
                    nouvelle_liste.append(tr + suffix)
                    continue
            nouvelle_liste.append(mot)
        return " ".join(nouvelle_liste)


def remplacement_synonymes(chaine: str, proba: float) -> str:
    return RemplacementSynonymes().appliquer(chaine, proba)


def traduction_vers(chaine: str, target_lang: str, proba: float) -> str:
    return TraductionGenerique(target_lang).appliquer(chaine, proba)


# backward compatibility: keep the old name `TraductionAnglais` and helper
TraductionAnglais = TraductionGenerique


def traduction_anglais(chaine: str, proba: float) -> str:
    """Compatibility wrapper: translate to English using PyDictionary."""
    return TraductionGenerique("en").appliquer(chaine, proba)
