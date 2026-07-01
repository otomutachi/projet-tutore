import os
from pathlib import Path
print('cwd=', Path('.').resolve())
print('OPENAI_KEY present=', os.getenv('OPENAI_API_KEY') is not None)
print('ANTHROPIC_KEY present=', os.getenv('ANTHROPIC_API_KEY') is not None)
print('OPENAI_KEY=', os.getenv('OPENAI_API_KEY'))
print('ANTHROPIC_KEY=', os.getenv('ANTHROPIC_API_KEY'))
