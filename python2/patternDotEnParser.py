#python2


from pattern.en import conjugate, lemma, lexeme, parse

print(parse('ridden', relations=True, lemmata=True))


print(parse('swum', relations=True, lemmata=True))
print(parse('swum', relations=True, lemmata=True))
print(parse('swum', relations=True, lemmata=True))

'''

>>> print parse('ridden', relations=True, lemmata=True)
ridden/VBN/B-VP/O/O/ride
>>> print parse('swum', relations=True, lemmata=True)
swum/VBN/B-VP/O/O/swim
>>> print parse('swum', relations=True, lemmata=True)
swum/VBN/B-VP/O/O/swim
>>> print parse('swum', relations=True, lemmata=True)
swum/VBN/B-VP/O/O/swim
'''

#now how to deal with parsed object properly

parsed = parse('ridden', relations=True, lemmata=True)

print(parsed)

# cat = u'hello'



import nltk
import ssl

try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

nltk.download('wordnet_ic')

