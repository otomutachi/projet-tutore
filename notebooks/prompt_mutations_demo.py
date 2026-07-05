import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from prompt_generator import PromptGenerator


def build_mutation_table(base_prompt: str):
    """Crée un DataFrame avec plusieurs mutations de prompt."""
    generator = PromptGenerator()
    mutation_types = ["synonymes", "yoda", "anglais", "allemand", "cyber", "francais", "fusion"]
    rows = []
    for mutation_type in mutation_types:
        mutated = generator.mutate_prompt(base_prompt, mutation_type)
        if mutated and mutated != base_prompt:
            rows.append({"mutation": mutation_type, "prompt": mutated})
    return pd.DataFrame(rows)


if __name__ == "__main__":
    base_prompt = "Act as an expert C developer and replace the masked code safely."
    df = build_mutation_table(base_prompt)
    print(df.to_string(index=False))
    print(json.dumps(df.to_dict(orient="records"), ensure_ascii=False, indent=2))
