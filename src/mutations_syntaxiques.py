import random
import re

from mutation_base import Mutation
from mutations_semantiques import reformuler_phrase


_TOKEN_NON_ESPACE = re.compile(r"^(?P<prefix>[^\wÀ-ÿ]*)(?P<mot>[\wÀ-ÿ]+)(?P<suffix>[^\wÀ-ÿ]*)$", re.UNICODE)


def _separer_tokens(chaine: str):
    """Retourne les morceaux non espaces avec leurs mots séparés de la ponctuation."""
    morceaux = re.findall(r"\s+|\S+", chaine, re.UNICODE)
    tokens = []
    for morceau in morceaux:
        correspondance = _TOKEN_NON_ESPACE.match(morceau)
        if correspondance is None:
            tokens.append((morceau, None, None, None))
        else:
            tokens.append(
                (
                    morceau,
                    correspondance.group("prefix"),
                    correspondance.group("mot"),
                    correspondance.group("suffix"),
                )
            )
    return tokens


class PermutationLettres(Mutation):
    """Permute des lettres adjacentes selon une probabilité."""

    # Utilise random.random() pour permuter chaque paire de lettres indépendamment.
    def apply(self, chaine: str, proba: float) -> str:
        resultat = []
        for original, prefix, mot, suffix in _separer_tokens(chaine):
            if mot is None:
                resultat.append(original)
                continue
            caracteres = list(mot)
            index = 1
            while index < len(caracteres):
                if random.random() < proba:
                    caracteres[index], caracteres[index - 1] = (
                        caracteres[index - 1],
                        caracteres[index],
                    )
                    index += 1
                index += 1
            resultat.append(prefix + "".join(caracteres) + suffix)
        return "".join(resultat)


class PermutationMots(Mutation):
    """Permute des mots adjacents selon une probabilité."""

    # Utilise une boucle simple pour échanger des mots voisins avec une chance donnée.
    def apply(self, chaine: str, proba: float) -> str:
        tokens = _separer_tokens(chaine)
        indices_mots = [
            index for index, (_, prefix, mot, suffix) in enumerate(tokens)
            if mot is not None
        ]
        index = 1
        while index < len(indices_mots):
            index_gauche = indices_mots[index - 1]
            index_droit = indices_mots[index]
            if random.random() < proba:
                gauche = tokens[index_gauche][2]
                droit = tokens[index_droit][2]
                tokens[index_gauche] = (
                    tokens[index_gauche][0],
                    tokens[index_gauche][1],
                    droit,
                    tokens[index_gauche][3],
                )
                tokens[index_droit] = (
                    tokens[index_droit][0],
                    tokens[index_droit][1],
                    gauche,
                    tokens[index_droit][3],
                )
                index += 1
            index += 1
        resultat = []
        for original, prefix, mot, suffix in tokens:
            if mot is None:
                resultat.append(original)
            else:
                resultat.append(prefix + mot + suffix)
        return "".join(resultat)


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

    def appliquer(self, chaine: str, proba: float, seed=None) -> str:
        if not 0 <= proba <= 1:
            raise ValueError("proba doit être compris entre 0 et 1")
        return self.apply(chaine, proba, seed)

    def apply(self, chaine: str, proba: float, seed=None) -> str:
        if not chaine:
            return chaine

        generateur = random.Random(seed)
        phrases = list(self.phrases)
        generateur.shuffle(phrases)
        blocs = [chaine]

        for phrase in phrases:
            if generateur.random() >= proba:
                continue
            position = generateur.choice(["avant", "apres", "milieu"])
            if position == "avant":
                blocs.insert(0, phrase)
            elif position == "apres":
                blocs.append(phrase)
            else:
                blocs.insert(generateur.randint(0, len(blocs)), phrase)

        return " ".join(blocs)


def permutation_lettres(chaine: str, proba: float) -> str:
    return PermutationLettres().appliquer(chaine, proba)


def permutation_mots(chaine: str, proba: float) -> str:
    return PermutationMots().appliquer(chaine, proba)


def dilution_contexte(chaine: str, proba: float = 0.5, seed=None) -> str:
    return DilutionContexte().appliquer(chaine, proba, seed)


def _nettoyer_espaces(texte: str) -> str:
    """Nettoie les espaces inutiles."""
    texte = texte.strip()
    texte = texte.replace("  ", " ")
    return texte


class MutationArgumentaire(Mutation):
    """Reformule la demande comme un besoin ou un argumentaire."""

    def appliquer(self, texte: str, proba: float = 0.5, seed=None) -> str:
        return self.apply(texte, proba, seed)

    def apply(self, texte: str, proba: float = 0.5, seed=None) -> str:
        if not texte:
            return texte

        phrase = _nettoyer_espaces(texte).rstrip("?!. ").strip()
        phrase = reformuler_phrase(phrase, proba, seed)

        if "j'ai besoin de" not in phrase.lower():
            phrase = f"j'ai besoin de {phrase}"

        if "tu peux" not in phrase.lower() and "peux" not in phrase.lower():
            phrase = f"{phrase}, tu peux faire ça ?"
        else:
            phrase = f"{phrase} ?"

        return _nettoyer_espaces(phrase)


class MutationStructureInversee(Mutation):
    """Inverse une partie de la structure d'une phrase."""

    def appliquer(self, texte: str, proba: float = 0.5, seed=None) -> str:
        return self.apply(texte, proba, seed)

    def apply(self, texte: str, proba: float = 0.5, seed=None) -> str:
        if not texte:
            return texte

        _ = (proba, seed)
        phrase = _nettoyer_espaces(texte).rstrip("?!. ").strip()
        mots = phrase.split()

        if len(mots) > 4 and " qui " in phrase.lower():
            partie1, partie2 = phrase.split(" qui ", 1)
            return f"{partie2}, {partie1} ?"

        if len(mots) > 4:
            return f"{' '.join(mots[2:])}, {' '.join(mots[:2])} ?"

        return f"{phrase}, comme ça tu vois ?"


class ApplicationMutations(Mutation):
    """Applique une liste de mutations syntaxiques dans l'ordre."""

    def appliquer(self, texte: str, liste=None, proba: float = 0.5, seed=None) -> str:
        return self.apply(texte, liste, proba, seed)

    def apply(self, texte: str, liste=None, proba: float = 0.5, seed=None) -> str:
        if not texte:
            return texte

        if liste is None:
            return MutationAleatoire().apply(texte, proba, seed=seed)

        if isinstance(liste, str):
            liste = [liste]

        resultat = texte
        for nom in liste:
            if nom == "mutation_argumentaire":
                resultat = MutationArgumentaire().apply(resultat, proba, seed)
            elif nom == "mutation_structure_inversee":
                resultat = MutationStructureInversee().apply(resultat, proba, seed)
            elif nom == "mutation_aleatoire":
                resultat = MutationAleatoire().apply(resultat, proba=proba, seed=seed)
        return resultat


class MutationAleatoire(Mutation):
    """Choisit et applique aléatoirement une mutation syntaxique."""

    def appliquer(self, texte: str, liste=None, proba: float = 0.5, seed=None) -> str:
        return self.apply(texte, liste, proba, seed)

    def apply(self, texte: str, liste=None, proba: float = 0.5, seed=None) -> str:
        if not texte:
            return texte

        choix = liste or [
            "mutation_argumentaire",
            "mutation_structure_inversee",
        ]
        nom = random.Random(seed).choice(choix)
        return ApplicationMutations().apply(texte, [nom], proba, seed)


def mutation_argumentaire(texte: str, proba: float = 0.5, seed=None) -> str:
    """Compatibilité : applique la mutation argumentaire."""
    return MutationArgumentaire().appliquer(texte, proba, seed)


def mutation_structure_inversee(texte: str, proba: float = 0.5) -> str:
    """Compatibilité : applique la mutation de structure inversée."""
    return MutationStructureInversee().appliquer(texte, proba)


def mutation_aleatoire(texte: str, liste=None, proba: float = 0.5, seed=None) -> str:
    """Compatibilité : applique une mutation syntaxique aléatoire."""
    return MutationAleatoire().appliquer(texte, liste, proba, seed)


def appliquer_mutations(texte: str, liste=None, proba: float = 0.5, seed=None) -> str:
    """Compatibilité : applique une liste de mutations syntaxiques."""
    return ApplicationMutations().appliquer(texte, liste, proba, seed)
