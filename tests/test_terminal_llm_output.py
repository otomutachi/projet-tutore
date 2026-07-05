import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from prompt_generator import PromptGenerator


def test_terminal_output_with_prompt_mutation():
    generator = PromptGenerator()
    prompt = "Replace the masked code with a secure fix."
    mutated = generator.mutate_prompt(prompt, "yoda")
    print("[LLM TEST]", mutated)
    assert mutated != prompt


if __name__ == "__main__":
    test_terminal_output_with_prompt_mutation()
