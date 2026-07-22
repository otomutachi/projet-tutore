import random


class Mutation:
    """Classe de base simple pour les mutations probabilistes."""

    # Utilise une vérification simple pour garder la probabilité dans l'intervalle attendu.
    def appliquer(self, chaine: str, proba: float) -> str:
        if not 0 <= proba <= 1:
            raise ValueError("proba doit être compris entre 0 et 1")
        return self.apply(chaine, proba)

    def apply(self, chaine: str, proba: float) -> str:
        return chaine
