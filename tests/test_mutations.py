
import sys
import unittest
from contextlib import ExitStack
from unittest.mock import patch
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from mutations_orthographiques import (
    AlphabetGrec,
    FauteDeFrappe,
    RemplacementAccents,
    RemplacementEPar3,
    casse_apres_ponctuation,
    doubler_ponctuation,
    inserer_virgule_aleatoire,
    remplacer_ponctuation_aleatoire,
)
from mutations_semantiques import (
    RemplacementSynonymes,
    TraductionAnglais,
    remplacement_synonymes,
    traduction_vers,
    traduction_anglais,
)
import mutations_semantiques
from mutations_syntaxiques import (
    DilutionContexte,
    PermutationLettres,
    PermutationMots,
    appliquer_mutations,
    mutation_aleatoire,
    mutation_argumentaire,
    mutation_structure_inversee,
)
from runner import appliquer_liste, appliquer_mutation, mutation_aleatoire as mutation_aleatoire_runner
from helpers import charger_prompts_cve


class TestMutations(unittest.TestCase):
    def _appliquer_synonyme_fixe(self, entree, synonyme):
        with patch.object(mutations_semantiques, "obtenir_synonyme", return_value=synonyme):
            with patch.object(mutations_semantiques, "obtenir_traduction", return_value=None):
                return remplacement_synonymes(entree, 1.0, seed=7)

    def _appliquer_traduction_fixe(self, entree, traduction):
        with patch.object(mutations_semantiques, "obtenir_synonyme", return_value=None):
            with patch.object(mutations_semantiques, "obtenir_traduction", return_value=traduction):
                return traduction_vers(entree, "en", 1.0, seed=7)

    def test_synonyme_live_exemple(self):
        entree = "hello"
        attendu = "salut"
        self.assertEqual(self._appliquer_synonyme_fixe(entree, attendu), attendu)

    def test_remplacement_synonymes_mot_connu_exact_prompts(self):
        entree = "prompts"
        attendu = "requêtes"
        self.assertEqual(self._appliquer_synonyme_fixe(entree, attendu), attendu)

    def test_remplacement_synonymes_mot_connu_exact_code(self):
        entree = "code"
        attendu = "programme"
        self.assertEqual(self._appliquer_synonyme_fixe(entree, attendu), attendu)

    def test_remplacement_synonymes_mot_connu_exact_securise(self):
        entree = "sécurisé"
        attendu = "protégé"
        self.assertEqual(self._appliquer_synonyme_fixe(entree, attendu), attendu)

    def test_remplacement_synonymes_mot_connu_exact_fonction(self):
        entree = "fonction"
        attendu = "méthode"
        self.assertEqual(self._appliquer_synonyme_fixe(entree, attendu), attendu)

    def test_remplacement_synonymes_phrase(self):
        entree = "Projet tutoré sur les prompts"
        attendu = "Application encadrée sur les requêtes"
        with patch.object(mutations_semantiques, "obtenir_synonyme", side_effect=["Application", "encadrée", "parmi", "les", "requêtes"]):
            with patch.object(mutations_semantiques, "obtenir_traduction", return_value=None):
                resultat = remplacement_synonymes(entree, 1.0, seed=7)
        self.assertEqual(resultat, attendu)

    def test_traduction_generique_exemple(self):
        entree = "house"
        attendu = "casa"
        self.assertEqual(self._appliquer_traduction_fixe(entree, attendu), attendu)

    def test_traduction_generique_phrase(self):
        entree = "bonjour monde"
        attendu = "hello world"
        with patch.object(mutations_semantiques, "obtenir_synonyme", side_effect=[None, None]):
            with patch.object(mutations_semantiques, "obtenir_traduction", side_effect=["hello", "world"]):
                resultat = traduction_vers(entree, "en", 1.0, seed=7)
        self.assertEqual(resultat, attendu)

    def test_traduction_n_utilise_pas_les_synonymes(self):
        with patch.object(
            mutations_semantiques,
            "obtenir_synonyme",
            side_effect=AssertionError("La traduction ne doit pas chercher de synonyme"),
        ):
            with patch.object(
                mutations_semantiques,
                "obtenir_traduction",
                return_value="project",
            ):
                resultat = traduction_vers("projet", "en", 1.0, seed=7)

        self.assertEqual(resultat, "project")

    def test_traduction_anglais_mot_connu_exact_projet(self):
        entree = "projet"
        attendu = "project"
        self.assertEqual(self._appliquer_traduction_fixe(entree, attendu), attendu)

    def test_traduction_anglais_mot_connu_exact_prompts(self):
        entree = "prompts"
        attendu = "requests"
        self.assertEqual(self._appliquer_traduction_fixe(entree, attendu), attendu)

    def test_traduction_anglais_mot_connu_exact_genere(self):
        entree = "genere"
        attendu = "generates"
        self.assertEqual(self._appliquer_traduction_fixe(entree, attendu), attendu)

    def test_traduction_anglais_mot_connu_exact_fonction(self):
        entree = "fonction"
        attendu = "function"
        self.assertEqual(self._appliquer_traduction_fixe(entree, attendu), attendu)

    def test_remplacement_synonymes_prompt_cve_exact(self):
        prompts = charger_prompts_cve(PROJECT_ROOT / "prompts_cve.json")
        prompt = prompts.get("CVE-2024-23456", "").splitlines()[0]
        attendu = prompt
        self.assertEqual(remplacement_synonymes(prompt, 0, seed=7), attendu)

    def test_remplacement_e_par_3_proba_zero(self):
        chaine = "eEe"
        self.assertEqual(RemplacementEPar3().appliquer(chaine, 0), chaine)

    def test_remplacement_e_par_3_proba_un(self):
        chaine = "eEe"
        attendu = "333"
        self.assertEqual(RemplacementEPar3().appliquer(chaine, 1), attendu)

    def test_remplacement_e_par_3_chaine_vide(self):
        self.assertEqual(RemplacementEPar3().appliquer("", 0.5), "")

    def test_remplacement_accents_proba_zero(self):
        chaine = "éèê"
        self.assertEqual(RemplacementAccents().appliquer(chaine, 0), chaine)

    def test_remplacement_accents_proba_un(self):
        chaine = "éèê"
        attendu = "eee"
        self.assertEqual(RemplacementAccents().appliquer(chaine, 1), attendu)

    def test_remplacement_accents_chaine_vide(self):
        self.assertEqual(RemplacementAccents().appliquer("", 0.5), "")

    def test_faute_de_frappe_proba_zero(self):
        chaine = "azerty"
        self.assertEqual(FauteDeFrappe().appliquer(chaine, 0), chaine)

    def test_faute_de_frappe_proba_un(self):
        chaine = "azerty"
        attendu = "qsreyt"
        self.assertEqual(FauteDeFrappe().appliquer(chaine, 1), attendu)

    def test_faute_de_frappe_chaine_vide(self):
        self.assertEqual(FauteDeFrappe().appliquer("", 0.5), "")

    def test_doubler_ponctuation_sortie_attendue_avec_seed(self):
        texte = "Bonjour tout le monde."
        self.assertEqual(doubler_ponctuation(texte, seed=7), "Bonjour tout le monde..")

    def test_inserer_virgule_sortie_attendue_avec_seed(self):
        texte = "Bonjour tout le monde."
        self.assertEqual(inserer_virgule_aleatoire(texte, seed=7), "Bonjour tout, le monde.")

    def test_casse_apres_ponctuation_sortie_attendue_avec_seed(self):
        texte = "Bonjour. Comment vas-tu?"
        self.assertEqual(casse_apres_ponctuation(texte, seed=7), "Bonjour. comment vas-tu?")

    def test_remplacer_ponctuation_sortie_attendue_avec_seed(self):
        texte = "Bonjour tout le monde."
        self.assertEqual(remplacer_ponctuation_aleatoire(texte, seed=7), "Bonjour tout le monde~")

    def test_ponctuation_est_deterministe_avec_le_meme_seed(self):
        texte = "Bonjour. Comment vas-tu?"
        fonctions = (
            doubler_ponctuation,
            inserer_virgule_aleatoire,
            casse_apres_ponctuation,
            remplacer_ponctuation_aleatoire,
        )
        for fonction in fonctions:
            with self.subTest(fonction=fonction.__name__):
                resultat1 = fonction(texte, seed=7)
                resultat2 = fonction(texte, seed=7)
                self.assertEqual(resultat1, resultat2)

    def test_alphabet_grec_proba_zero(self):
        chaine = "aeiou"
        self.assertEqual(AlphabetGrec().appliquer(chaine, 0), chaine)

    def test_alphabet_grec_proba_un(self):
        chaine = "aeiou"
        attendu = "αειου"
        self.assertEqual(AlphabetGrec().appliquer(chaine, 1), attendu)

    def test_alphabet_grec_chaine_vide(self):
        self.assertEqual(AlphabetGrec().appliquer("", 0.5), "")

    def test_permutation_lettres_proba_zero(self):
        chaine = "bonjour"
        self.assertEqual(PermutationLettres().appliquer(chaine, 0), chaine)

    def test_permutation_lettres_proba_un(self):
        chaine = "abc"
        attendu = "bac"
        self.assertEqual(PermutationLettres().appliquer(chaine, 1), attendu)

    def test_permutation_lettres_chaine_vide(self):
        self.assertEqual(PermutationLettres().appliquer("", 0.5), "")

    def test_permutation_mots_proba_zero(self):
        chaine = "un deux trois"
        self.assertEqual(PermutationMots().appliquer(chaine, 0), chaine)

    def test_permutation_mots_preserve_ponctuation_et_espaces(self):
        chaine = "Bonjour,   monde !"
        with patch("mutations_syntaxiques.random.random", return_value=0.0):
            resultat = PermutationMots().appliquer(chaine, 1.0)
        self.assertEqual(resultat, "monde,   Bonjour !")

    def test_permutation_lettres_ne_deplace_pas_la_ponctuation(self):
        chaine = "ab, cd!"
        with patch("mutations_syntaxiques.random.random", return_value=0.0):
            resultat = PermutationLettres().appliquer(chaine, 1.0)
        self.assertEqual(resultat, "ba, dc!")

    def test_permutation_mots_proba_un(self):
        chaine = "un deux trois"
        attendu = "deux un trois"
        self.assertEqual(PermutationMots().appliquer(chaine, 1), attendu)

    def test_permutation_mots_chaine_vide(self):
        self.assertEqual(PermutationMots().appliquer("", 0.5), "")

    def test_dilution_contexte_proba_zero(self):
        chaine = "Projet tutoré sur les prompts"
        self.assertEqual(DilutionContexte().appliquer(chaine, 0), chaine)

    def test_dilution_contexte_sorties_attendues(self):
        cas = (
            (
                "texte",
                "Projet tutoré sur les prompts",
                "Merci de valider aussi le ticket JIRA-482. "
                "N'oublie pas de répondre au message Teams. "
                "Au fait n'oublie pas la réunion de 15h. "
                "Je te laisse finir après le stand-up. "
                "Projet tutoré sur les prompts On check ça demain matin si possible. "
                "Petit rappel : le café est en panne encore.",
            ),
            ("chaine vide", "", ""),
        )
        for nom, chaine, attendu in cas:
            with self.subTest(nom=nom):
                resultat = DilutionContexte().appliquer(chaine, 1, seed=7)
                self.assertEqual(resultat, attendu)

    def test_mutation_argumentaire_retourne_une_chaine(self):
        entree = "écris une fonction qui trie une liste"
        attendu = "j'ai besoin de une fonction qui trie une liste, tu peux faire ça ?"
        with patch("mutations_syntaxiques.reformuler_phrase", return_value="une fonction qui trie une liste"):
            self.assertEqual(mutation_argumentaire(entree), attendu)

    def test_mutation_structure_inversee_retourne_une_chaine(self):
        entree = "écris une fonction qui trie une liste"
        attendu = "trie une liste, écris une fonction ?"
        self.assertEqual(mutation_structure_inversee(entree), attendu)

    def test_mutation_aleatoire_et_appliquer_mutations(self):
        entree = "écris une fonction qui trie une liste"
        attendu = "j'ai besoin de une fonction qui trie une liste, tu peux faire ça ?"
        with patch("mutations_syntaxiques.reformuler_phrase", return_value="une fonction qui trie une liste"):
            self.assertEqual(
                mutation_aleatoire(entree, ["mutation_argumentaire"]),
                attendu,
            )
            self.assertEqual(appliquer_mutations(entree, ["mutation_argumentaire"]), attendu)

    def test_runner_mutation_centrale(self):
        entree = "écris une fonction qui trie une liste"
        self.assertEqual(appliquer_mutation(entree, "erreur_frappe", 0), entree)
        with patch("mutations_syntaxiques.reformuler_phrase", return_value="une fonction qui trie une liste"):
            self.assertEqual(
                appliquer_liste(entree, ["argumentaire", "structure_inversee"], 0.5),
                "trie une liste, tu peux faire ça, j'ai besoin de une fonction ?",
            )
            with patch("runner.random.choice", return_value="argumentaire"):
                self.assertEqual(
                    mutation_aleatoire_runner(entree, 0.5),
                    "j'ai besoin de une fonction qui trie une liste, tu peux faire ça ?",
                )

    def test_remplacement_synonymes_proba_zero(self):
        chaine = "Projet tutoré sur les prompts"
        self.assertEqual(RemplacementSynonymes().appliquer(chaine, 0), chaine)

    def test_remplacement_synonymes_chaine_vide(self):
        self.assertEqual(RemplacementSynonymes().appliquer("", 0.5), "")

    def test_remplacement_synonymes_reste_francais_sans_fallback_traduction(self):
        with patch.object(
            mutations_semantiques, "obtenir_synonyme", side_effect=["salut", None]
        ):
            with patch.object(
                mutations_semantiques, "obtenir_traduction", return_value="earth"
            ) as traduction:
                resultat = remplacement_synonymes("bonjour monde", 1.0, seed=42)

        self.assertEqual(resultat, "salut monde")
        traduction.assert_not_called()

    def test_traduction_anglais_proba_zero(self):
        chaine = "Génère un code sécurisé"
        self.assertEqual(TraductionAnglais().appliquer(chaine, 0), chaine)

    def test_traduction_anglais_chaine_vide(self):
        self.assertEqual(TraductionAnglais().appliquer("", 0.5), "")

    def test_synonyme_preserve_la_ponctuation(self):
        with patch("mutations_semantiques.obtenir_synonyme", return_value="salut"):
            with patch("mutations_semantiques.random.Random.random", return_value=0.0):
                resultat = remplacement_synonymes("(hello),", 1.0)
        self.assertEqual(resultat, "(salut),")

    def test_aleatoire_est_deterministe_avec_un_choix_controle(self):
        entree = "j'ai besoin de créer une fonction"
        with patch("mutations_syntaxiques.reformuler_phrase", return_value="j'ai besoin de faire une fonction"):
            resultat = mutation_aleatoire(
                entree, ["mutation_argumentaire"], proba=0.5, seed=42
            )
        self.assertEqual(resultat, "j'ai besoin de faire une fonction, tu peux faire ça ?")

    def test_charger_prompts_cve_retourne_dictionnaire(self):
        dictionnaire = charger_prompts_cve(PROJECT_ROOT / "prompts_cve.json")
        self.assertIn("CVE-2024-12345", dictionnaire)

    def test_charger_prompts_cve_fichier_inexistant(self):
        dictionnaire = charger_prompts_cve(PROJECT_ROOT / "fichier_inexistant.json")
        self.assertEqual(dictionnaire, {})

    def test_main_produit_les_resultats_attendus(self):
        import main

        class MutationControlee:
            def __init__(self, nom):
                self.nom = nom

            def appliquer(self, texte, proba):
                return f"{texte}|{self.nom}|{proba}"

        noms_mutations = (
            "RemplacementEPar3",
            "RemplacementAccents",
            "FauteDeFrappe",
            "AlphabetGrec",
            "PermutationLettres",
            "PermutationMots",
            "DilutionContexte",
            "RemplacementSynonymes",
            "TraductionAnglais",
        )
        with ExitStack() as pile:
            pile.enter_context(patch.object(main, "charger_prompts", return_value=["prompt test"]))
            pile.enter_context(patch.object(main, "charger_prompts_cve", return_value={}))
            sauvegarde = pile.enter_context(patch.object(main, "sauvegarder_prompts"))
            pile.enter_context(patch.object(main, "afficher_resultats"))
            pile.enter_context(patch.object(main, "traduire_texte", return_value="translated"))
            for nom in noms_mutations:
                pile.enter_context(
                    patch.object(main, nom, return_value=MutationControlee(nom))
                )
            resultat = main.main()

        self.assertEqual(resultat, 0)
        resultats = sauvegarde.call_args.args[0]
        self.assertEqual(len(resultats), 18)
        self.assertEqual(resultats[0]["prompts"][0]["mute"], "prompt test|RemplacementEPar3|0.2")


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
