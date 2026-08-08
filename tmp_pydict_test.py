from PyDictionary import PyDictionary

d=PyDictionary()
words=['hello','house','car','code','prompt','good','happy','safe']
for w in words:
    print('syn', w, '->', d.synonym(w))
print('translate house es ->', d.translate('house','es'))
print('translate hello fr ->', d.translate('hello','fr'))
print('translate code es ->', d.translate('code','es'))
