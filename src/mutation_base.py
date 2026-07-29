import random


class Mutation:
    """Classe de base simple pour les mutations probabilistes.

    Optimisations appliquées :
    - Factorisation des boucles communes de remplacement dans la classe de base,
      pour éviter de dupliquer la même logique dans plusieurs mutations.
    - Les helpers restent simples, lisibles et adaptés à un niveau L3.
    """

    # Utilise une vérification simple pour garder la probabilité dans l'intervalle attendu.
    def appliquer(self, chaine: str, proba: float) -> str:
        if not 0 <= proba <= 1:
            raise ValueError("proba doit être compris entre 0 et 1")
        return self.apply(chaine, proba)

    def _apply_char_map(self, chaine: str, mapping: dict, proba: float) -> str:
        if not chaine:
            return chaine
        nouvelle_chaine = []
        for caractere in chaine:
            if caractere in mapping and random.random() <= proba:
                nouvelle_chaine.append(mapping[caractere])
            else:
                nouvelle_chaine.append(caractere)
        return "".join(nouvelle_chaine)

    def _apply_char_map_preserve_case(self, chaine: str, mapping: dict, proba: float) -> str:
        if not chaine:
            return chaine
        nouvelle_chaine = []
        for caractere in chaine:
            remplacement = mapping.get(caractere.lower())
            if remplacement is not None and random.random() <= proba:
                nouvelle_chaine.append(remplacement.upper() if caractere.isupper() else remplacement)
            else:
                nouvelle_chaine.append(caractere)
        return "".join(nouvelle_chaine)

    def apply(self, chaine: str, proba: float) -> str:
        return chaine
