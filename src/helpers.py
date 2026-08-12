import json
import os
import re


def _charger_json(chemin_fichier):
    chemin = chemin_fichier
    if not os.path.isabs(chemin):
        chemin = os.path.join(os.path.dirname(os.path.dirname(__file__)), chemin)

    if not os.path.exists(chemin):
        return None

    try:
        with open(chemin, "r", encoding="utf-8") as fichier:
            return json.load(fichier)
    except (json.JSONDecodeError, OSError):
        return None


def charger_dictionnaire_json(chemin_fichier):
    """Charge un fichier JSON contenant un dictionnaire de synonymes."""
    dictionnaire = _charger_json(chemin_fichier)
    if dictionnaire is None:
        print(f"Fichier de dictionnaire introuvable ou invalide : {chemin_fichier}")
        return {}

    if not isinstance(dictionnaire, dict):
        print(f"Le fichier {chemin_fichier} ne contient pas un dictionnaire JSON valide.")
        return {}

    print(f"{len(dictionnaire)} synonymes chargés depuis {chemin_fichier}")
    return dictionnaire


def charger_prompts(chemin_fichier):
    """Charge une liste de prompts depuis un fichier JSON."""
    donnees = _charger_json(chemin_fichier)
    if not isinstance(donnees, list):
        return []

    prompts = []
    for item in donnees:
        if isinstance(item, dict) and "prompt" in item:
            prompts.append(str(item["prompt"]))
        else:
            prompts.append(str(item))
    return prompts


def charger_prompts_cve(chemin_fichier):
    """Charge un fichier JSON de prompts CVE et retourne un dictionnaire."""
    donnees = _charger_json(chemin_fichier)
    if donnees is None:
        return {}

    dictionnaire_prompts = {}
    if isinstance(donnees, list):
        for index, entree in enumerate(donnees):
            if isinstance(entree, dict):
                constraint = entree.get("related_constraint")
                prompt = entree.get("prompt")
                if constraint is not None and prompt is not None:
                    dictionnaire_prompts[str(constraint)] = str(prompt)
                    continue
            dictionnaire_prompts[f"prompt_{index}"] = str(entree)
    elif isinstance(donnees, dict):
        for cle, valeur in donnees.items():
            dictionnaire_prompts[str(cle)] = str(valeur)
    return dictionnaire_prompts


def sauvegarder_prompts(prompts, chemin_fichier):
    """Sauvegarde une liste de résultats de mutation dans un fichier JSON."""
    with open(chemin_fichier, "w", encoding="utf-8") as fichier:
        json.dump(prompts, fichier, ensure_ascii=False, indent=2)


def afficher_resultats(prompts_original, prompts_mutes, nom_mutation=""):
    """Affiche proprement la comparaison original/mutation."""
    if nom_mutation:
        print(f"Fonction utilisée : {nom_mutation}")
    def sanitize_for_display(text, max_len=320):
        if text is None:
            return ""
        # remove fenced code blocks
        cleaned = re.sub(r"```.*?```", "", str(text), flags=re.S)
        # detect probable code presence
        code_markers = ['#include', 'malloc(', 'printf(', 'strcpy(', 'char ', 'int ', '<MASK>', '{', '}']
        first_idx = None
        for marker in code_markers:
            idx = cleaned.find(marker)
            if idx != -1:
                if first_idx is None or idx < first_idx:
                    first_idx = idx
        if first_idx is not None:
            # keep text before code marker, prefer splitting at paragraph boundary
            before = cleaned[:first_idx]
            if '\n\n' in before:
                before = before.split('\n\n')[0]
            # remove code and do not append any marker
            cleaned = before.strip()
        # collapse whitespace and truncate
        single = ' '.join(cleaned.split())
        if len(single) > max_len:
            single = single[:max_len] + '...'
        return single

    for original, mute in zip(prompts_original, prompts_mutes):
        print(f"Original : {sanitize_for_display(original)}")
        print(f"Muté     : {sanitize_for_display(mute)}")
        print("-" * 40)
