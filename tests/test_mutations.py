import random
import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from mutations_orthographiques import AlphabetGrec, FauteDeFrappe, RemplacementAccents, RemplacementEPar3
from mutations_semantiques import RemplacementSynonymes, TraductionAnglais
from mutations_syntaxiques import DilutionContexte, PermutationLettres, PermutationMots


class TestMutations(unittest.TestCase):
    def test_proba_zero_ne_change_pas(self):
        chaine = "bonjour"
        self.assertEqual(RemplacementEPar3().appliquer(chaine, 0), chaine)
        self.assertEqual(RemplacementAccents().appliquer(chaine, 0), chaine)
        self.assertEqual(PermutationLettres().appliquer(chaine, 0), chaine)
        self.assertEqual(PermutationMots().appliquer(chaine, 0), chaine)
        self.assertEqual(RemplacementSynonymes().appliquer(chaine, 0), chaine)

    def test_proba_un_change_toujours_si_concerne(self):
        chaine = "eéa"
        self.assertNotEqual(RemplacementEPar3().appliquer(chaine, 1), chaine)
        self.assertNotEqual(RemplacementAccents().appliquer(chaine, 1), chaine)
        self.assertNotEqual(FauteDeFrappe().appliquer(chaine, 1), chaine)
        self.assertNotEqual(AlphabetGrec().appliquer(chaine, 1), chaine)

    def test_longueur_rest_coherente(self):
        chaine = "abcde"
        self.assertEqual(len(RemplacementEPar3().appliquer(chaine, 1)), len(chaine))
        self.assertEqual(len(RemplacementAccents().appliquer(chaine, 1)), len(chaine))
        self.assertEqual(len(PermutationLettres().appliquer(chaine, 1)), len(chaine))
        self.assertEqual(len(PermutationMots().appliquer(chaine, 1)), len(chaine))
        self.assertGreaterEqual(len(DilutionContexte().appliquer(chaine, 1)), len(chaine))
        self.assertEqual(len(RemplacementSynonymes().appliquer(chaine, 1)), len(chaine))
        self.assertEqual(len(TraductionAnglais().appliquer(chaine, 1)), len(chaine))

    def test_dilution_contexte_change_ordre_et_position(self):
        chaine = "Projet tutoré sur les prompts"
        random.seed(1)
        resultat1 = DilutionContexte().appliquer(chaine, 1)
        random.seed(2)
        resultat2 = DilutionContexte().appliquer(chaine, 1)
        self.assertNotEqual(resultat1, resultat2)

    def test_traduction_anglaise_change_un_prompt_français(self):
        chaine = "Génère un code sécurisé pour cette fonction."
        resultat = TraductionAnglais().appliquer(chaine, 1)
        self.assertNotEqual(resultat, chaine)


if __name__ == "__main__":
    unittest.main()
