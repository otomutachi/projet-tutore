import random

from mutation_base import Mutation


class PermutationLettres(Mutation):
    """Permute des lettres adjacentes selon une probabilité."""

    # Utilise random.random() pour permuter chaque paire de lettres indépendamment.
    def apply(self, chaine: str, proba: float) -> str:
        caracteres = list(chaine)
        index = 1
        while index < len(chaine):
            if random.random() <= proba:
                caracteres[index], caracteres[index - 1] = (
                    caracteres[index - 1],
                    caracteres[index],
                )
                index += 1
            index += 1
        return "".join(caracteres)


class PermutationMots(Mutation):
    """Permute des mots adjacents selon une probabilité."""

    # Utilise une boucle simple pour échanger des mots voisins avec une chance donnée.
    def apply(self, chaine: str, proba: float) -> str:
        mots = chaine.split()
        index = 1
        while index < len(mots):
            if random.random() <= proba:
                mots[index], mots[index - 1] = mots[index - 1], mots[index]
                index += 1
            index += 1
        return " ".join(mots)


class DilutionContexte(Mutation):
    """Ajoute des phrases parasites autour du prompt principal."""

    # Utilise la liste de phrases parasites fournie dans la version d'origine.
    phrases = [
        "Au fait n'oublie pas la réunion de 15h.",
        "Merci de valider aussi le ticket JIRA-482.",
        "Petit rappel : le café est en panne encore.",
        "On check ça demain matin si possible.",
        "Je te laisse finir après le stand-up.",
        "N'oublie pas de répondre au message Teams.",
    ]

    # La position de chaque phrase parasite est maintenant tirée au hasard.
    def apply(self, chaine: str, proba: float) -> str:
        phrases_candidates = list(self.phrases)
        random.shuffle(phrases_candidates)

        mots = chaine.split()
        nouvelle_chaine = chaine

        for phrase in phrases_candidates:
            if random.random() <= proba:
                position = random.choice(["avant", "apres", "milieu"])
                if position == "avant":
                    nouvelle_chaine = f"{phrase} {nouvelle_chaine}"
                elif position == "apres":
                    nouvelle_chaine = f"{nouvelle_chaine} {phrase}"
                else:
                    if mots:
                        index = random.randint(0, len(mots) - 1)
                        mots.insert(index, phrase)
                        nouvelle_chaine = " ".join(mots)
                    else:
                        nouvelle_chaine = f"{nouvelle_chaine} {phrase}"

        return nouvelle_chaine


def permutation_lettres(chaine: str, proba: float) -> str:
    return PermutationLettres().appliquer(chaine, proba)


def permutation_mots(chaine: str, proba: float) -> str:
    return PermutationMots().appliquer(chaine, proba)


def dilution_contexte(chaine: str, proba: float) -> str:
    return DilutionContexte().appliquer(chaine, proba)
