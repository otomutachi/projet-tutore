from PyDictionary import PyDictionary

d = PyDictionary()
words = [
    'Range', 'happy', 'good', 'sad', 'house', 'car', 'code', 'prompt', 'function',
    'project', 'hello', 'world', 'day', 'night', 'open', 'close', 'start', 'stop',
    'write', 'read', 'test', 'safe', 'secure', 'clean', 'dirty', 'fast', 'slow',
    'strong', 'weak', 'easy', 'hard', 'language', 'python', 'problem', 'solution'
]
print('SYNONYMS')
for w in words:
    try:
        syn = d.synonym(w)
    except Exception as e:
        syn = f'ERROR: {e}'
    if syn is not None:
        print(repr(w), '->', syn)

print('\nTRANSLATIONS')
for w in words:
    try:
        tr = d.translate(w, 'es')
    except Exception as e:
        tr = f'ERROR: {e}'
    if tr is not None:
        print(repr(w), '->', tr)
