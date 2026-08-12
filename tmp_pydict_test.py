from pathlib import Path
import sys

root = Path(r"e:/2025 info/semestre 6/projet tutoré/projet-tutore")
sys.path.insert(0, str(root / 'src'))

from PyDictionary import PyDictionary
from pydict_wrapper import translate_text
from mutations_semantiques import RemplacementSynonymes, TraductionAnglais

print('PYTHON', sys.executable)

d = PyDictionary()
for w in ['voiture', 'rapide', 'sécurisée', 'ordinateur', 'réseau', 'projet', 'tutoré', 'sur', 'les', 'prompts']:
    print(f'word={w} -> {repr(d.translate(w, "en"))}')

print('wrapper phrase:', repr(translate_text('voiture rapide et sécurisée', 'en')))
print('wrapper sentence:', repr(translate_text('Projet tutoré sur les prompts', 'en')))
print('TraductionAnglais:', repr(TraductionAnglais().appliquer('voiture rapide et sécurisée', 1.0)))
print('RemplacementSynonymes:', repr(RemplacementSynonymes().appliquer('Projet tutoré sur les prompts', 1.0)))
