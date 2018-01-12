    from nltk.corpus import wordnet as wn
     
    # Just to make it a bit more readable
    WN_NOUN = 'n'
    WN_VERB = 'v'
    WN_ADJECTIVE = 'a'
    WN_ADJECTIVE_SATELLITE = 's'
    WN_ADVERB = 'r'
    
     
    def convert(word, from_pos, to_pos):    
        """ Transform words given from/to POS tags """
        
        synsets = wn.synsets(word, pos=from_pos)
        
        # Word not found
        if not synsets:
            return []
        
        # Get all lemmas of the word (consider 'a'and 's' equivalent)
        lemmas = []
        for s in synsets:
            for l in s.lemmas():
                if s.name().split('.')[1] == from_pos or from_pos in (WN_ADJECTIVE, WN_ADJECTIVE_SATELLITE) and s.name().split('.')[1] in (WN_ADJECTIVE, WN_ADJECTIVE_SATELLITE):
                    lemmas += [l]
     
        # Get related forms
        derivationally_related_forms = [(l, l.derivationally_related_forms()) for l in lemmas]
        
        # filter only the desired pos (consider 'a' and 's' equivalent)
        related_noun_lemmas = []
        
        for drf in derivationally_related_forms:
            for l in drf[1]:
                if l.synset().name().split('.')[1] == to_pos or to_pos in (WN_ADJECTIVE, WN_ADJECTIVE_SATELLITE) and l.synset().name().split('.')[1] in (WN_ADJECTIVE, WN_ADJECTIVE_SATELLITE):
                    related_noun_lemmas += [l]
     
        # Extract the words from the lemmas
        words = [l.name() for l in related_noun_lemmas]
        len_words = len(words)
        
        # Build the result in the form of a list containing tuples (word, probability)
        result = [(w, float(words.count(w)) / len_words) for w in set(words)]
        result.sort(key=lambda w:-w[1])
        
        # return all the possibilities sorted by probability
        return result

convert('run', 'v', 'a')

convert('direct', 'a', 'r')
convert('tired', 'a', 'r')
convert('tired', 'a', 'v')
convert('tired', 'a', 'n')
convert('tired', 'a', 's')
convert('wonder', 'v', 'n')
convert('wonder', 'n', 'a')
convert('direct', 'a', 'n')


'''
    >>> convert('tired', 'a', 'r')
    []
    >>> convert('tired', 'a', 'v')
    []
    >>> convert('tired', 'a', 'n')
    [('triteness', 0.25), ('banality', 0.25), ('tiredness', 0.25), ('commonplace', 0.25)]
    >>> convert('tired', 'a', 's')
    []
    >>> convert('wonder', 'v', 'n')
    [('wonder', 0.3333333333333333), ('wonderer', 0.2222222222222222), ('marveller', 0.1111111111111111), ('marvel', 0.1111111111111111), ('wonderment', 0.1111111111111111), ('question', 0.1111111111111111)]
    >>> convert('wonder', 'n', 'a')
    [('curious', 0.4), ('wondrous', 0.2), ('marvelous', 0.2), ('marvellous', 0.2)]
'''



import re

from nltk import pos_tag
import nltk
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

from pattern.en import parse, comparative, superlative, pluralize
from PIL.WmfImagePlugin import word

wnl = WordNetLemmatizer()

wnl.lemmatize('quickly', 'a')
wnl.lemmatize('quicker', 'a')
wnl.lemmatize('lighter', 'a')
wnl.lemmatize('better', 'a')

# 2.  use pattern.en to parse individual words.

wnl.lemmatize('quicken', 'v')

print(parse("i'm not ready because she didn't finish but it's too late", relations=True, lemmata=True))
parsed = parse("it's stuart's cat's we're she's its", relations=True, lemmata=True)
print(parse('easily', relations=True, lemmata=True))
print(parse('quickly', relations=True, lemmata=True))
print(parse('exceedingly', relations=True, lemmata=True))
print(parse('lightly', relations=True, lemmata=True))

print(parse('easiest', relations=True, lemmata=True))
print(parse('quickest', relations=True, lemmata=True))
print(parse('lightest', relations=True, lemmata=True))

print(parse('easier', relations=True, lemmata=True))
print(parse('quicker', relations=True, lemmata=True))
print(parse('lighter', relations=True, lemmata=True))

print(parse('ridden', relations=True, lemmata=True))
print(parse('swum', relations=True, lemmata=True))
print(parse('swam', relations=True, lemmata=True))
print(parse('swimming', relations=True, lemmata=True))
print(parse('quickening', relations=True, lemmata=True))
print(parse('talking', relations=True, lemmata=True))
print(parse('eating', relations=True, lemmata=True))
print(parse('running', relations=True, lemmata=True))
print(parse('ring', relations=True, lemmata=True))
print(parse('taken', relations=True, lemmata=True))
print(parse('eaten', relations=True, lemmata=True))
print(parse('which', relations=True, lemmata=True))
print(parse('whatever', relations=True, lemmata=True))
print(parse('whichever', relations=True, lemmata=True))
print(parse('uh', relations=True, lemmata=True))
print(parse('gosh', relations=True, lemmata=True))

print(parse('darnedest', relations=True, lemmata=True))
print(parse('whatever', relations=True, lemmata=True))
print(parse('whichever', relations=True, lemmata=True))
print(parse('uh', relations=True, lemmata=True))
print(parse('gosh', relations=True, lemmata=True))
print(parse('has', relations=True, lemmata=True))
print(parse('"', relations=True, lemmata=True))
print(parse(';', relations=True, lemmata=True))
print(parse('%', relations=True, lemmata=True))

print(parse('deprived', relations=True, lemmata=True))
print(parse('quicken', relations=True, lemmata=True))
print(parse('enlighten', relations=True, lemmata=True))
print(parse('eaten', relations=True, lemmata=True))
print(parse('sunken', relations=True, lemmata=True))
print(parse('listlessness', relations=True, lemmata=True))
print(parse("isn't", relations=True, lemmata=True))

# darnedest fails.   doens't know it's an adjective

# TODO - how to parse a word if i know it's a gerund?

# look at this https://stackoverflow.com/questions/25534214/nltk-wordnet-lemmatizer-shouldnt-it-lemmatize-all-inflections-of-a-word

# if this is VBG
nltk.pos_tag(word_tokenize("swimming"))
nltk.pos_tag(word_tokenize("darnedest"))
# [('darnedest', 'NN')]

# then get verb root like so
nltk.stem.WordNetLemmatizer().lemmatize('loving', 'v')

# TODO this is all stupid.  easier to just make stupid word chart.  use this code?

'''

word, root, tag, count

sink, sank, sunk, sunken? 

accuracy, accurate, NOUN_FORM_OF_ADJ
swimmer, swim, ONE_WHO_DOES
knitter, knit, ONE_WHO_DOES
swam, swim, PAST
swum, swim, PAST_PARTICIPLE
sunken, sink, PAST_EN
sank, sink, PAST
sunk, sink, PAST_PARTICIPLE


'''
