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
import random

try:
    import wn
except Exception:
    wn = None

try:
    from argostranslate import translate as argos_translate
except Exception:
    argos_translate = None

try:
    from argostranslate import package as argos_package
except Exception:
    argos_package = None


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


def _lang_candidates(langue: str) -> list[str]:
    """Retourne les codes de langue acceptés par wn pour une langue donnée."""
    langue = (langue or "").lower()
    candidats = [langue]
    mapping = {
        "en": ["en", "eng"],
        "eng": ["eng", "en"],
        "fr": ["fr", "fra"],
        "fra": ["fra", "fr"],
    }
    for item in mapping.get(langue, [langue]):
        if item not in candidats:
            candidats.append(item)
    return candidats


def _charger_lexiques_wn() -> None:
    """Télécharge les lexiques WordNet nécessaires si aucun n'est présent."""
    if wn is None:
        return
    try:
        lexiques = [lex.id.lower() for lex in wn.lexicons()]
    except Exception:
        pass
        lexiques = []

    for ressource in ("oewn:2021", "omw-en:1.4", "omw-fr:1.4"):
        identifiant = ressource.split(":", 1)[0].lower()
        if identifiant in lexiques:
            continue
        try:
            with _masquer_sortie_pydictionary():
                wn.download(ressource)
        except Exception:
            continue


def _installer_modele_argos(source: str, cible: str) -> None:
    """Installe le modèle Argos fr-en ou en-fr s'il est absent."""
    if argos_translate is None or argos_package is None:
        return

    source = source.lower()
    cible = cible.lower()
    if (source, cible) not in (("fr", "en"), ("en", "fr")):
        return

    try:
        langues = argos_translate.get_installed_languages()
        langue_source = next(langue for langue in langues if langue.code == source)
        langue_cible = next(langue for langue in langues if langue.code == cible)
        if langue_source.get_translation(langue_cible) is not None:
            return
    except Exception:
        pass

    try:
        with _masquer_sortie_pydictionary():
            argos_package.update_package_index()
            paquets = argos_package.get_available_packages()
            paquet = next(
                paquet
                for paquet in paquets
                if paquet.from_code == source and paquet.to_code == cible
            )
            chemin = paquet.download()
            argos_package.install_from_path(chemin)
    except Exception:
        pass


def _traduire_phrase_complete(texte: str, langue_cible: str) -> Optional[str]:
    """Tente une traduction de la phrase entière via argostranslate."""
    if not texte or argos_translate is None:
        return None

    try:
        source = "fr" if langue_cible.lower() == "en" else "en"
        callback = getattr(argos_translate, "translate", None)
        if callback is None or not callable(callback):
            return None

        with _masquer_sortie_pydictionary():
            traduit = callback(texte, source, langue_cible.lower())

        if isinstance(traduit, (list, tuple)):
            traduit = traduit[0] if traduit else None
        if isinstance(traduit, str) and traduit.strip() and traduit.strip().lower() != texte.strip().lower():
            return traduit.strip()
    except Exception:
        pass
    return None


def _traduire_mot(mot: str, client_dictionnaire: Optional[object], langue_cible: str) -> str:
    """Traduit un seul mot avec argostranslate."""
    if client_dictionnaire is None:
        return mot
    try:
        if hasattr(client_dictionnaire, "translate"):
            callback = client_dictionnaire.translate
        elif hasattr(client_dictionnaire, "__call__"):
            callback = client_dictionnaire
        else:
            return mot

        with _masquer_sortie_pydictionary():
            if langue_cible.lower() == "en":
                traduit = callback(mot, "fr", "en")
            elif langue_cible.lower() == "fr":
                traduit = callback(mot, "en", "fr")
            else:
                traduit = callback(mot, "fr", langue_cible)
    except Exception:
        return mot

    if isinstance(traduit, (list, tuple)):
        traduit = traduit[0] if traduit else mot
    if not traduit or not isinstance(traduit, str):
        return mot
    return _appliquer_casse(mot, traduit.strip())


def _rechercher_synonymes(mot: str, client_dictionnaire: Optional[object]) -> Optional[list[str]]:
    """Récupère la liste des synonymes via wn."""
    if client_dictionnaire is None:
        return None
    try:
        _charger_lexiques_wn()
        synonymes: list[str] = []
        seen = set()

        essais = [
            lambda: client_dictionnaire.synsets(form=mot, lang="en", lexicon="oewn:2021"),
            lambda: client_dictionnaire.synsets(form=mot, lang="en", lexicon="omw-en:1.4"),
            lambda: client_dictionnaire.synsets(form=mot, lang="eng", lexicon="oewn:2021"),
            lambda: client_dictionnaire.synsets(form=mot, lang="eng", lexicon="omw-en:1.4"),
            lambda: client_dictionnaire.synsets(form=mot),
            lambda: client_dictionnaire.synsets(form=mot, lang="en"),
            lambda: client_dictionnaire.synsets(form=mot, lang="fr"),
            lambda: client_dictionnaire.synsets(form=mot, lang="fra"),
        ]
        for appel in essais:
            try:
                for synset in appel():
                    for lemme in synset.lemmas():
                        nom = lemme if isinstance(lemme, str) else lemme.name()
                        nom = nom.replace("_", " ")
                        if not nom or nom.lower() == mot.lower():
                            continue
                        if nom.lower() not in seen:
                            seen.add(nom.lower())
                            synonymes.append(nom)
                if synonymes:
                    return synonymes
            except Exception:
                continue
        return synonymes or None
    except Exception:
        return None


def traduire_texte(texte: str, langue_cible: str = "en") -> str:
    """Traduit une chaîne; essaye d'abord la phrase complète, puis retombe sur mot par mot."""
    if not texte:
        return texte

    source = "fr" if langue_cible.lower() == "en" else "en"
    _installer_modele_argos(source, langue_cible)

    phrase_traduite = _traduire_phrase_complete(texte, langue_cible)
    if phrase_traduite is not None:
        return phrase_traduite

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
