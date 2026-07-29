import json
from pathlib import Path
p = Path('data/synonymes.json')
with open(p, 'r', encoding='utf-8') as fh:
    data = json.load(fh)
print('JSON_OK', len(data))
import sys
sys.path.insert(0, 'src')
from mutations_semantiques import RemplacementSynonymes
r = RemplacementSynonymes()
print('DICT_OK', len(r.dictionnaire))
