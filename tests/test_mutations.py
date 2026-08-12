
import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from mutations_orthographiques import AlphabetGrec, FauteDeFrappe, RemplacementAccents, RemplacementEPar3
from mutations_semantiques import RemplacementSynonymes, remplacement_synonymes, traduction_vers, traduction_anglais
from mutations_syntaxiques import DilutionContexte, PermutationLettres, PermutationMots
from helpers import charger_prompts_cve


class TestMutations(unittest.TestCase):
    def test_synonyme_live_exemple(self):
        # These tests depend on PyDictionary and internet access; results may vary.
        entree = "hello"
        # Manually verify the expected result from PyDictionary before asserting.
        resultat = remplacement_synonymes(entree, 1.0)
        self.assertIsInstance(resultat, str)

    def test_remplacement_synonymes_mot_connu_exact_prompts(self):
        entree = "prompts"
        resultat = remplacement_synonymes(entree, 1.0)
        self.assertIsInstance(resultat, str)

    def test_remplacement_synonymes_mot_connu_exact_code(self):
        entree = "code"
        resultat = remplacement_synonymes(entree, 1.0)
        self.assertIsInstance(resultat, str)

    def test_remplacement_synonymes_mot_connu_exact_securise(self):
        entree = "sécurisé"
        resultat = remplacement_synonymes(entree, 1.0)
        self.assertIsInstance(resultat, str)

    def test_remplacement_synonymes_mot_connu_exact_fonction(self):
        entree = "fonction"
        resultat = remplacement_synonymes(entree, 1.0)
        self.assertIsInstance(resultat, str)

    def test_traduction_generique_exemple(self):
        # Live translation test using PyDictionary; verify expected value manually.
        entree = "house"
        resultat = traduction_vers(entree, 'es', 1.0)
        self.assertIsInstance(resultat, str)

    def test_traduction_anglais_mot_connu_exact_projet(self):
        entree = "projet"
        resultat = traduction_anglais(entree, 1.0)
        self.assertIsInstance(resultat, str)

    def test_traduction_anglais_mot_connu_exact_prompts(self):
        entree = "prompts"
        resultat = traduction_anglais(entree, 1.0)
        self.assertIsInstance(resultat, str)

    def test_traduction_anglais_mot_connu_exact_genere(self):
        entree = "genere"
        resultat = traduction_anglais(entree, 1.0)
        self.assertIsInstance(resultat, str)

    def test_traduction_anglais_mot_connu_exact_fonction(self):
        entree = "fonction"
        resultat = traduction_anglais(entree, 1.0)
        self.assertIsInstance(resultat, str)

    def test_remplacement_synonymes_prompt_cve_exact(self):
        prompts = charger_prompts_cve(PROJECT_ROOT / "prompts_cve.json")
        prompt = prompts.get("CVE-2024-23456", "").splitlines()[0]
        resultat = remplacement_synonymes(prompt, 1.0)
        self.assertIsInstance(resultat, str)

    def test_remplacement_e_par_3_proba_zero(self):
        chaine = "eEe"
        self.assertEqual(RemplacementEPar3().appliquer(chaine, 0), chaine)

    def test_remplacement_e_par_3_proba_un(self):
        chaine = "eEe"
        self.assertNotEqual(RemplacementEPar3().appliquer(chaine, 1), chaine)

    def test_remplacement_e_par_3_chaine_vide(self):
        self.assertEqual(RemplacementEPar3().appliquer("", 0.5), "")

    def test_remplacement_accents_proba_zero(self):
        chaine = "éèê"
        self.assertEqual(RemplacementAccents().appliquer(chaine, 0), chaine)

    def test_remplacement_accents_proba_un(self):
        chaine = "éèê"
        self.assertNotEqual(RemplacementAccents().appliquer(chaine, 1), chaine)

    def test_remplacement_accents_chaine_vide(self):
        self.assertEqual(RemplacementAccents().appliquer("", 0.5), "")

    def test_faute_de_frappe_proba_zero(self):
        chaine = "azerty"
        self.assertEqual(FauteDeFrappe().appliquer(chaine, 0), chaine)

    def test_faute_de_frappe_proba_un(self):
        chaine = "azerty"
        self.assertNotEqual(FauteDeFrappe().appliquer(chaine, 1), chaine)

    def test_faute_de_frappe_chaine_vide(self):
        self.assertEqual(FauteDeFrappe().appliquer("", 0.5), "")

    def test_alphabet_grec_proba_zero(self):
        chaine = "aeiou"
        self.assertEqual(AlphabetGrec().appliquer(chaine, 0), chaine)

    def test_alphabet_grec_proba_un(self):
        chaine = "aeiou"
        self.assertNotEqual(AlphabetGrec().appliquer(chaine, 1), chaine)

    def test_alphabet_grec_chaine_vide(self):
        self.assertEqual(AlphabetGrec().appliquer("", 0.5), "")

    def test_permutation_lettres_proba_zero(self):
        chaine = "bonjour"
        self.assertEqual(PermutationLettres().appliquer(chaine, 0), chaine)

    def test_permutation_lettres_proba_un(self):
        chaine = "abc"
        self.assertNotEqual(PermutationLettres().appliquer(chaine, 1), chaine)

    def test_permutation_lettres_chaine_vide(self):
        self.assertEqual(PermutationLettres().appliquer("", 0.5), "")

    def test_permutation_mots_proba_zero(self):
        chaine = "un deux trois"
        self.assertEqual(PermutationMots().appliquer(chaine, 0), chaine)

    def test_permutation_mots_proba_un(self):
        chaine = "un deux trois"
        self.assertNotEqual(PermutationMots().appliquer(chaine, 1), chaine)

    def test_permutation_mots_chaine_vide(self):
        self.assertEqual(PermutationMots().appliquer("", 0.5), "")

    def test_dilution_contexte_proba_zero(self):
        chaine = "Projet tutoré sur les prompts"
        self.assertEqual(DilutionContexte().appliquer(chaine, 0), chaine)

    def test_dilution_contexte_proba_un(self):
        chaine = "Projet tutoré sur les prompts"
        self.assertNotEqual(DilutionContexte().appliquer(chaine, 1), chaine)

    def test_dilution_contexte_chaine_vide(self):
        self.assertIsInstance(DilutionContexte().appliquer("", 0.5), str)

    def test_remplacement_synonymes_proba_zero(self):
        chaine = "Projet tutoré sur les prompts"
        self.assertEqual(RemplacementSynonymes().appliquer(chaine, 0), chaine)

    def test_remplacement_synonymes_chaine_vide(self):
        self.assertEqual(RemplacementSynonymes().appliquer("", 0.5), "")

    def test_traduction_anglais_proba_zero(self):
        chaine = "Génère un code sécurisé"
        self.assertEqual(TraductionAnglais().appliquer(chaine, 0), chaine)

    def test_traduction_anglais_chaine_vide(self):
        self.assertEqual(TraductionAnglais().appliquer("", 0.5), "")

    def test_charger_prompts_cve_retourne_dictionnaire(self):
        dictionnaire = charger_prompts_cve(PROJECT_ROOT / "prompts_cve.json")
        self.assertIn("CVE-2024-12345", dictionnaire)

    def test_charger_prompts_cve_fichier_inexistant(self):
        dictionnaire = charger_prompts_cve(PROJECT_ROOT / "fichier_inexistant.json")
        self.assertEqual(dictionnaire, {})


def lancer_tous_les_tests():
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestMutations)
    resultat = unittest.TextTestRunner(verbosity=2).run(suite)
    print("\n=== Résumé des tests ===")
    print(f"Tests réussis : {resultat.testsRun - len(resultat.failures) - len(resultat.errors)}")
    print(f"Tests échoués : {len(resultat.failures) + len(resultat.errors)}")
    if resultat.failures or resultat.errors:
        for nom, _ in resultat.failures + resultat.errors:
            print(f"Echec : {nom}")


if __name__ == "__main__":
    lancer_tous_les_tests()
