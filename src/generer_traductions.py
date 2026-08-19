from __future__ import annotations

import json
from pathlib import Path

from argostranslate import translate as argos_translate

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
    resultats: dict[str, str] = {}
    for terme in TERMES:
        try:
            traduction = argos_translate.translate(terme, "fr", "en")
        except Exception:
            traduction = None
        if isinstance(traduction, str) and traduction:
            resultats[terme] = traduction
    return resultats


if __name__ == "__main__":
    traductions = generer_traductions()
    SORTIE.parent.mkdir(parents=True, exist_ok=True)
    with SORTIE.open("w", encoding="utf-8") as fichier:
        json.dump(traductions, fichier, ensure_ascii=False, indent=2)
    print(f"Écrit {len(traductions)} traductions dans {SORTIE}")
