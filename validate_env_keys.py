import os
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()
keys = {
    'OPENAI_API_KEY': os.getenv('OPENAI_API_KEY'),
    'ANTHROPIC_API_KEY': os.getenv('ANTHROPIC_API_KEY'),
}
print('cwd=', Path('.').resolve())
for name, value in keys.items():
    if value is None:
        print(name, 'MISSING')
        continue
    print(name, 'present=', True)
    print(name, 'prefix=', value[:5])
    print(name, 'length=', len(value))
    print(name, 'contains space=', ' ' in value)
    print(name, 'contains newline=', '\n' in value)
