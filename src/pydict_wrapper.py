#!/usr/bin/env python3
"""Petit wrapper autour de PyDictionary pour traduire du texte.

Fonctions:
- `translate_text(text, target_lang='en')` : retourne le texte traduit si possible,
  sinon retourne le texte original.

Le module gère l'absence de `PyDictionary` en renvoyant simplement la chaîne
originale (comportement de fallback silencieux).
"""
from typing import Optional
import contextlib
import io
import re

try:
    from PyDictionary import PyDictionary
except Exception:
    PyDictionary = None


_REGEX_MOT = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ]+")


def _masquer_sortie_pydictionary():
    return contextlib.redirect_stdout(io.StringIO())


def _appliquer_casse(mot: str, traduction: str) -> str:
    if mot.istitle():
        return traduction.capitalize()
    if mot.isupper():
        return traduction.upper()
    return traduction


def _traduire_mot(mot: str, client_dictionnaire: Optional[object], langue_cible: str) -> str:
    if client_dictionnaire is None:
        return mot
    try:
        with _masquer_sortie_pydictionary():
            traduit = client_dictionnaire.translate(mot, langue_cible)
    except Exception:
        return mot
    if not traduit:
        return mot
    return _appliquer_casse(mot, traduit)


def _rechercher_synonymes(mot: str, client_dictionnaire: Optional[object]) -> Optional[list[str]]:
    if client_dictionnaire is None:
        return None
    try:
        with _masquer_sortie_pydictionary():
            synonymes = client_dictionnaire.synonym(mot)
    except Exception:
        return None
    if not synonymes or not isinstance(synonymes, list):
        return None
    return synonymes


def traduire_texte(texte: str, langue_cible: str = "en") -> str:
    client_dictionnaire = PyDictionary() if PyDictionary is not None else None

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
    client_dictionnaire = PyDictionary() if PyDictionary is not None else None
    return _rechercher_synonymes(mot, client_dictionnaire)
