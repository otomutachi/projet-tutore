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


_WORD_RE = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ]+")


def _suppress_pydictionary_output():
    return contextlib.redirect_stdout(io.StringIO())


def _apply_case(token: str, traduction: str) -> str:
    if token.istitle():
        return traduction.capitalize()
    if token.isupper():
        return traduction.upper()
    return traduction


def _translate_token(token: str, dict_client: Optional[object], target_lang: str) -> str:
    if dict_client is None:
        return token
    try:
        with _suppress_pydictionary_output():
            translated = dict_client.translate(token, target_lang)
    except Exception:
        return token
    if not translated:
        return token
    return _apply_case(token, translated)


def _lookup_synonyms(token: str, dict_client: Optional[object]) -> Optional[list[str]]:
    if dict_client is None:
        return None
    try:
        with _suppress_pydictionary_output():
            synonyms = dict_client.synonym(token)
    except Exception:
        return None
    if not synonyms or not isinstance(synonyms, list):
        return None
    return synonyms


def translate_text(text: str, target_lang: str = "en") -> str:
    dict_client = PyDictionary() if PyDictionary is not None else None

    parts = re.split(r"(" + _WORD_RE.pattern + r")", text)
    translated_parts = []
    for part in parts:
        if not part:
            continue
        if _WORD_RE.fullmatch(part):
            translated_parts.append(_translate_token(part, dict_client, target_lang))
        else:
            translated_parts.append(part)
    return "".join(translated_parts)


def lookup_synonyms(term: str) -> Optional[list[str]]:
    dict_client = PyDictionary() if PyDictionary is not None else None
    return _lookup_synonyms(term, dict_client)
