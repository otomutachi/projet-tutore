#!/usr/bin/env python3
"""Petit wrapper autour de wn et argostranslate pour traduire du texte.

Fonctions principales:
- `traduire_texte(texte, langue_cible='en')` : tente de traduire chaque mot du texte.
- `rechercher_synonymes(mot)` : récupère une liste de synonymes pour un mot.
"""
from typing import Optional
import contextlib
import io
import re

try:
    import wn
except Exception:
    wn = None

try:
    from argostranslate import translate as argos_translate
except Exception:
    argos_translate = None


_REGEX_MOT = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ]+")


def _masquer_sortie_pydictionary():
    """Retourne un contexte qui redirige stdout vers un buffer vide."""
    return contextlib.redirect_stdout(io.StringIO())


def _appliquer_casse(mot: str, traduction: str) -> str:
    """Preserve la casse du mot original dans la traduction."""
    if mot.istitle():
        return traduction.capitalize()
    if mot.isupper():
        return traduction.upper()
    return traduction


def _traduire_mot(mot: str, client_dictionnaire: Optional[object], langue_cible: str) -> str:
    """Traduit un seul mot avec argostranslate."""
    if client_dictionnaire is None:
        return mot
    try:
        with _masquer_sortie_pydictionary():
            if langue_cible.lower() == "en":
                traduit = client_dictionnaire.translate(mot, "fr", "en")
            elif langue_cible.lower() == "fr":
                traduit = client_dictionnaire.translate(mot, "en", "fr")
            else:
                traduit = client_dictionnaire.translate(mot, "fr", langue_cible)
    except Exception:
        return mot
    if not traduit:
        return mot
    return _appliquer_casse(mot, traduit)


def _rechercher_synonymes(mot: str, client_dictionnaire: Optional[object]) -> Optional[list[str]]:
    """Récupère la liste des synonymes via wn."""
    if client_dictionnaire is None:
        return None
    try:
        lemmas = client_dictionnaire.lemmas(mot, lang="en")
        for lemme in lemmas:
            synset = getattr(lemme, "synset", lambda: None)()
            if synset is None:
                continue
            synonymes = []
            for autre in synset.lemmas():
                nom = autre.name()
                if nom != mot and nom not in synonymes:
                    synonymes.append(nom)
            if synonymes:
                return synonymes
        return None
    except Exception:
        return None


def traduire_texte(texte: str, langue_cible: str = "en") -> str:
    """Traduit chaque mot dans une chaîne en utilisant argostranslate."""
    client_dictionnaire = argos_translate if argos_translate is not None else None

    morceaux = re.split(r"(" + _REGEX_MOT.pattern + r")", texte)
    morceaux_traduits = []
    for morceau in morceaux:
        if not morceau:
            continue
        if _REGEX_MOT.fullmatch(morceau):
            morceaux_traduits.append(_traduire_mot(morceau, client_dictionnaire, langue_cible))
        else:
            morceaux_traduits.append(morceau)
    return "".join(morceaux_traduits)


def rechercher_synonymes(mot: str) -> Optional[list[str]]:
    """Fonction publique pour rechercher les synonymes d'un mot."""
    client_dictionnaire = wn if wn is not None else None
    return _rechercher_synonymes(mot, client_dictionnaire)
