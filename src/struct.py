# Compatibilité avec l'ancien module struct.py

from mutations_orthographiques import (
    AlphabetGrec,
    FauteDeFrappe,
    RemplacementAccents,
    RemplacementEPar3,
    alphabet_grec,
    faute_de_frappe,
    remplacement_accents,
    remplacement_e_par_3,
)
from mutations_semantiques import RemplacementSynonymes, TraductionAnglais, remplacement_synonymes, traduction_anglais
from mutations_syntaxiques import DilutionContexte, PermutationLettres, PermutationMots, dilution_contexte, permutation_lettres, permutation_mots


class MutationBase:
    def appliquer(self, chaine, proba):
        return self.apply(chaine, proba)


class RemplacementEPar3Compat(RemplacementEPar3, MutationBase):
    pass


class RemplacementAccentsCompat(RemplacementAccents, MutationBase):
    pass


class FauteDeFrappeCompat(FauteDeFrappe, MutationBase):
    pass


class AlphabetGrecCompat(AlphabetGrec, MutationBase):
    pass


class PermutationLettresCompat(PermutationLettres, MutationBase):
    pass


class PermutationMotsCompat(PermutationMots, MutationBase):
    pass


class DilutionContexteCompat(DilutionContexte, MutationBase):
    pass


class RemplacementSynonymesCompat(RemplacementSynonymes, MutationBase):
    pass


class TraductionAnglaisCompat(TraductionAnglais, MutationBase):
    pass


def appliquer_mutations(chaine, liste_mutations, proba):
    resultat = chaine
    for mutation in liste_mutations:
        if hasattr(mutation, "appliquer"):
            resultat = mutation.appliquer(resultat, proba)
        else:
            resultat = mutation(resultat, proba)
    return resultat
