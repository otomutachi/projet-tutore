#!/usr/bin/env python3
"""Petit wrapper autour de PyDictionary pour traduire du texte.

Fonctions:
- `translate_text(text, target_lang='en')` : retourne le texte traduit si possible,
  sinon retourne le texte original.

Le module gère l'absence de `PyDictionary` en renvoyant simplement la chaîne
originale (comportement de fallback silencieux).
"""
from typing import Optional
import re

try:
    from PyDictionary import PyDictionary
except Exception:  # ImportError ou erreurs d'initialisation réseau
    PyDictionary = None


_WORD_RE = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ]+")


def _translate_token(token: str, dict_client: Optional[object], target_lang: str) -> str:
    if not dict_client:
        return token
    try:
        translated = dict_client.translate(token, target_lang)
    except Exception:
        return token
    if not translated:
        return token
    # Preserve capitalization (Title case)
    if token.istitle():
        return translated.capitalize()
    if token.isupper():
        return translated.upper()
    return translated


def translate_text(text: str, target_lang: str = "en") -> str:
    """Translate `text` into `target_lang` using PyDictionary.

    - If PyDictionary is not available or a translation fails, returns the
      original text unchanged for that token.
    - The function splits the input preserving punctuation and whitespace.
    """
    if PyDictionary is None:
        return text

    dict_client = PyDictionary()

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
