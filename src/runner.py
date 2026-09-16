import random
import re

from mutations_orthographiques import faute_de_frappe
from mutations_semantiques import remplacement_synonymes, traduction_anglais
from mutations_syntaxiques import (
    mutation_argumentaire,
    mutation_structure_inversee,
)

MUTATIONS = {
    "erreur_frappe": faute_de_frappe,
    "argumentaire": mutation_argumentaire,
    "structure_inversee": mutation_structure_inversee,
    "synonyme": remplacement_synonymes,
    "traduction_anglais": traduction_anglais,
}

_MOT = re.compile(r"^[^\wÀ-ÿ]*(?P<mot>[\wÀ-ÿ]+)[^\wÀ-ÿ]*$", re.UNICODE)


def nettoyer_mutation(texte: str) -> str:
    """Nettoie les espaces ajoutés accidentellement par une mutation."""
    if not texte:
        return texte
    lignes = [ligne.rstrip() for ligne in texte.replace("\r\n", "\n").split("\n")]
    return "\n".join(lignes).strip()


def analyser_entree(texte: str, exclusions=()):
    """Sépare les éléments mutables, protégés et les séparateurs, dans l'ordre."""
    protections = {str(element).casefold() for element in exclusions}
    morceaux = re.findall(r"\s+|\S+", texte or "", re.UNICODE)
    elements = []
    for index, morceau in enumerate(morceaux):
        correspondance = _MOT.match(morceau)
        mot = correspondance.group("mot") if correspondance else None
        protege = mot is None or mot.casefold() in protections
        elements.append(
            {
                "index": index,
                "texte": morceau,
                "mot": mot,
                "protege": protege,
                "mutable": mot is not None and not protege,
            }
        )
    return elements


def appliquer_mutations_controlees(
    texte: str,
    noms,
    proba: float = 0.5,
    nombre=None,
    exclusions=(),
    seed=None,
) -> str:
    """Mute un nombre contrôlé de mots sans toucher aux exclusions."""
    if not 0 <= proba <= 1:
        raise ValueError("proba doit être compris entre 0 et 1")
    if isinstance(noms, str):
        noms = [noms]
    noms = list(noms)
    elements = analyser_entree(texte, exclusions)
    candidats = [element for element in elements if element["mutable"]]
    generateur = random.Random(seed)

    if nombre is None:
        nombre = generateur.randint(0, len(candidats)) if candidats else 0
    if not isinstance(nombre, int) or isinstance(nombre, bool):
        raise TypeError("nombre doit être un entier ou None")
    if nombre < 0 or nombre > len(candidats):
        raise ValueError("nombre doit être compris entre 0 et le nombre de mots mutables")

    selection = {id(element) for element in generateur.sample(candidats, nombre)}
    resultat = []
    for element in elements:
        morceau = element["texte"]
        if id(element) in selection:
            for nom in noms:
                morceau = appliquer_mutation(morceau, nom, proba)
        resultat.append(morceau)
    return nettoyer_mutation("".join(resultat))


def presenter_mutation(texte: str, resultat: str, nom="mutation") -> str:
    """Construit une présentation lisible de l'entrée et de la sortie."""
    return f"Mutation : {nom}\nEntrée : {texte}\nSortie : {resultat}"


def appliquer_mutation(texte: str, nom: str, proba: float = 0.5):
    """Applique une mutation donnée sur un texte."""
    if not texte:
        return texte

    if nom not in MUTATIONS:
        raise ValueError(f"Mutation inconnue : {nom}")

    return MUTATIONS[nom](texte, proba)


def appliquer_liste(texte: str, noms, proba: float = 0.5):
    """Applique plusieurs mutations dans l'ordre donné."""
    resultat = texte
    for nom in noms:
        resultat = appliquer_mutation(resultat, nom, proba)
    return resultat


def mutation_aleatoire(texte: str, proba: float = 0.5):
    """Applique une mutation choisie au hasard."""
    if not texte:
        return texte
    nom = random.choice(list(MUTATIONS.keys()))
    return appliquer_mutation(texte, nom, proba)
