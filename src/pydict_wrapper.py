#!/usr/bin/env python3
"""Petit wrapper autour de PyDictionary pour traduire du texte.

Fonctions principales:
- `traduire_texte(texte, langue_cible='en')` : tente de traduire chaque mot du texte.
- `rechercher_synonymes(mot)` : récupère une liste de synonymes pour un mot.

Ce module capture et ignore les sorties de PyDictionary, car PyDictionary peut
imprimer des messages d'erreur inutiles comme "has no Synonyms in the API".
En cas d'erreur ou si PyDictionary est absent, on renvoie simplement le texte
original sans interrompre le programme.
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
    """Retourne un contexte qui redirige stdout vers un buffer vide.

    Cela empêche PyDictionary d'afficher des messages de log ou des erreurs
    légitimes sur la sortie standard.
    """
    return contextlib.redirect_stdout(io.StringIO())


def _appliquer_casse(mot: str, traduction: str) -> str:
    """Preserve la casse du mot original dans la traduction."""
    if mot.istitle():
        return traduction.capitalize()
    if mot.isupper():
        return traduction.upper()
    return traduction


def _traduire_mot(mot: str, client_dictionnaire: Optional[object], langue_cible: str) -> str:
    """Traduit un seul mot avec PyDictionary.

    Si PyDictionary n'est pas disponible ou si la traduction échoue, le
    mot original est retourné.
    """
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
    """Récupère la liste des synonymes via PyDictionary.

    Renvoie None si PyDictionary n'est pas disponible, si la méthode lève une
    exception ou si le résultat n'est pas une liste de synonymes.
    """
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
    """Traduit chaque mot dans une chaîne en utilisant PyDictionary.

    Si un mot ne peut pas être traduit, il reste inchangé. Les caractères
    non alphabétiques (ponctuation, espaces) sont conservés tels quels.
    """
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
    """Fonction publique pour rechercher les synonymes d'un mot.

    Crée une instance de PyDictionary si disponible, puis délègue au helper.
    """
    client_dictionnaire = PyDictionary() if PyDictionary is not None else None
    return _rechercher_synonymes(mot, client_dictionnaire)
