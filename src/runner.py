import random

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
