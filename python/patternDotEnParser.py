#python2


from pattern.en import conjugate, lemma, lexeme, parse

print(parse('ridden', relations=True, lemmata=True))
print(parse('swum', relations=True, lemmata=True))
print(parse('swum', relations=True, lemmata=True))
print(parse('swum', relations=True, lemmata=True))

parsed = parse('ridden', relations=True, lemmata=True)

print(parsed.split())

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
