import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from prompt_generator import PromptGenerator


class PromptMutationTests(unittest.TestCase):
    def setUp(self):
        self.generator = PromptGenerator()

    def test_mutate_prompt_with_yoda_style_changes_text(self):
        base = "Act as an expert C developer and replace the masked code safely."
        mutated = self.generator.mutate_prompt(base, "yoda")
        self.assertNotEqual(mutated, base)
        self.assertIn("masked", mutated.lower())
        self.assertIn("code", mutated.lower())

    def test_mutate_prompt_with_letter_obfuscation_is_readable(self):
        base = "Replace the vulnerable code with a secure fix."
        mutated = self.generator.mutate_prompt(base, "cyber")
        self.assertNotEqual(mutated, base)
        self.assertTrue(any(token in mutated.lower() for token in ["vuln", "c0d3", "s3cur3"]))

    def test_generate_mutation_variants_returns_multiple_prompts(self):
        base = "Protect the code and fix the vulnerability safely."
        variants = self.generator.generate_mutation_variants(base, mutation_types=["synonymes", "yoda", "anglais"])
        self.assertGreaterEqual(len(variants), 3)
        self.assertTrue(all(v != base for v in variants))

    def test_fusion_mutation_combines_multiple_styles(self):
        base = "Replace the masked code with a secure fix."
        fused = self.generator.mutate_prompt(base, "fusion")
        self.assertNotEqual(fused, base)
        self.assertTrue(any(token in fused.lower() for token in ["secure", "s3cur3"]))


if __name__ == "__main__":
    unittest.main()
