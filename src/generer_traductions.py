from __future__ import annotations

import json
from pathlib import Path

try:
    from PyDictionary import PyDictionary
except ImportError:
    PyDictionary = None

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SORTIE = PROJECT_ROOT / "data" / "traduction.json"
TERMES = [
    "projet",
    "tutoré",
    "tutorés",
    "prompts",
    "chaine",
    "chaîne",
    "caractères",
    "caracteres",
    "entrée",
    "entree",
    "sur",
    "en",
    "code",
    "sécurisé",
    "secure",
    "fonction",
    "génère",
    "genere",
    "pour",
    "cette",
    "des",
    "les",
    "un",
]


def generer_traductions() -> dict[str, str]:
    if PyDictionary is None:
        raise RuntimeError("PyDictionary n'est pas installé.")

    traducteur = PyDictionary()
    resultats: dict[str, str] = {}
    for terme in TERMES:
        traductions = traducteur.translate(terme, "fr", "en")
        if traductions:
            resultats[terme] = traductions[0]
    return resultats


if __name__ == "__main__":
    traductions = generer_traductions()
    SORTIE.parent.mkdir(parents=True, exist_ok=True)
    with SORTIE.open("w", encoding="utf-8") as fichier:
        json.dump(traductions, fichier, ensure_ascii=False, indent=2)
