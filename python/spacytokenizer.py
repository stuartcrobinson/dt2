import spacy

nlp = spacy.load('en')

doc = nlp(u'Apple is  always quickly looking at buying an easier* good-hearted U.K. startup for $1 billion ! !!')
#
# for token in doc:
#     print(token.text, token.lemma_, '<'+token.text_with_ws+'>', '<'+token.whitespace_+'>', token.pos_, token.tag_, token.dep_,
#           token.shape_, token.is_alpha, token.is_stop)

def showparsed2(doc):
    for token in doc:
        print(token.text, token.lemma_, '<'+token.text_with_ws+'>', '<'+token.whitespace_+'>', token.pos_, token.tag_, token.dep_, token.shape_, token.is_alpha, token.is_stop)

# .pos_ --  http://universaldependencies.org/en/pos/index.html ?
# .tag_ --  http://web.mit.edu/6.863/www/PennTreebankTags.html ?  not included: NFP
# .dep_ --  http://universaldependencies.org/en/dep/ ???????? sometimes. :(  not "prep" - dep_ for "at". or pcomp (buying).

def showparsed(doc):
    for token in doc:
        print()
        print(token.text)
        print('  lemma:  ' + token.lemma_)
        print('  tkwws:  ' + '<'+token.text_with_ws+'>')
        print('  ws:     ' + '<'+token.whitespace_+'>')
        print('  pos_:   ' + token.pos_)
        print('  tag_:   ' + token.tag_)
        print('  dep_:   ' + token.dep_)
        print('  shape_: ' + token.shape_)
        print('  is_alp: ' + str(token.is_alpha))
        print('  is_stp: ' + str(token.is_stop))

showparsed(nlp("colors"))
print()
showparsed(nlp("Apple is  always quickly looking at buying an easier* good-hearted U.K. startup for $1 billion ! !!"))
print()
showparsed(nlp("really better than the best"))
print()
showparsed(nlp("The fastest ladies were able to grab milk, sugar, eggs, an apple, and 10 donuts from the corner store."))

string = "Our church had a simple, potluck Christmas party with Santa Claus and face painting to start off the festivities.  The girls were so funny!  They were sooooo excited to see him the whole day leading up to the party and then when it was go time, Ash because totally star struck and tongue-tied.  Britt was friendly but not her usual exuberant self.  Elle cuddle up on his shoulder because she really didn't know what else to do, and Tate stuck out her lip and threatened to cry until a helpful elf handed her a cany cane! " + "Dinner was nice and I ate the BEST sweet potato casserole in the whole wide world.  My breadsticks were snatched up immediately which made me feel good.  :)  The girls all got up on the stage and sang their little Christmas songs.  Actually, Elle refused.  I have no idea why, but she got really grumpy after that so we left.  I was sorry to miss the rest of the prepared entertainment, but it was an hour past bedtime for the younger set anyways."
print()
print()
print()
print()
showparsed(nlp(string))

'''
Text: The original word text.
Lemma: The base form of the word.
POS: The simple part-of-speech tag.
Tag: The detailed part-of-speech tag.
Dep: Syntactic dependency, i.e. the relation between tokens.
Shape: The word shape – capitalisation, punctuation, digits.
is alpha: Is the token an alpha character?
is stop: Is the token part of a stop list, i.e. the most common words of the language?
'''

#TODO - i think .tag_ is sufficient for both model and word untokenizing.

'''

uhhhhhhh. ..... spacy's parsing sucks.


face
  lemma:  face
  tkwws:  <face >
  ws:     < >
  pos_:   VERB
  tag_:   VB
  dep_:   conj
  shape_: xxxx
  is_alp: True
  is_stp: False

painting
  lemma:  painting
  tkwws:  <painting >
  ws:     < >
  pos_:   NOUN
  tag_:   NN
  dep_:   dobj
  shape_: xxxx
  is_alp: True
  is_stp: False


don't use it.  i think it would just confuse the model.  what we want is just to make these conversions:

something like

easiest --> easy + EST
dropped --> drop + ED
bought --> buy + PASTTENSE

so.... i think i should only add POS tags for words whose lemma differs from the original word. 

the point is to reduce the number of dimensions (words) in the RNN.  do spacy tokenization for words individually, not in sentence context.

use the "TAG" token parameter

if is_alpha

split corpus by space.

tokenize each element.

if tokenizer splits element into two tokens, make into two atoms

NO -- split corpus by spaces and all punctuation.  like we did in java.  keep spaces and punctuation. 

if element is alphabetical world length 3 or more, parse it.  if lemma diff from original word, add "TAG_" as follow-up atom in atom list.

python2 only:

from pattern.en import conjugate, lemma, lexeme, parse

print parse('ridden', relations=True, lemmata=True)
print parse('swum', relations=True, lemmata=True)
print parse('swum', relations=True, lemmata=True)
print parse('swum', relations=True, lemmata=True)

uhm. hm.  pattern.en is actually better tha spacy at word deconstruction.  succeeds at ridden and swum. spacy fails on these.

pattern returns easiest from easiest, but knows it's a superlative adj - so i can prob just reduce that manually??

how to go from "easiest" to root?
like this!!!!

https://stackoverflow.com/questions/17487406/adjectives-superlative-and-comparative-to-positive-form

from nltk.stem.wordnet import WordNetLemmatizer
wnl = WordNetLemmatizer()
wnl.lemmatize('biggest', 'a')
>  u'big'

could i use nltk for everything?  parser?  

http://www.nltk.org/book/ch05.html ?

no it sucks
>>> nltk.pos_tag(word_tokenize("swum"))
[('swum', 'NN')]
>>> nltk.pos_tag(word_tokenize("swam"))
[('swam', 'NN')]
>>> nltk.pos_tag(word_tokenize("swim"))
[('swim', 'NN')]
>>> nltk.pos_tag(word_tokenize("i swam yesterday"))
[('i', 'NN'), ('swam', 'NN'), ('yesterday', 'NN')]
>>>

NLTK SUCKS AT PARSING WORDS.  PATTERN.EN is the best bet!!




so.... split sentences up around spaces and punctuation.  (how?)
so ... use pattern.en to parse individual words
then.. use nltk's WordNetLemmatizer to further parse adverbs (and others?) into lemma, knowing the word type.
 
1.  split corpus at spaces and punct:

https://stackoverflow.com/questions/1059559/split-strings-with-multiple-delimiters


this works but gives extra empty values:
re.split('(\W|_| )', "Words, words, wo_rds wasn't this fun! oh yeah good-hearted.")

just filter to remove empties:
https://stackoverflow.com/a/16840963/8870055
time_info = filter(None, str_list)

like above ^^ ignore next stuff:

>>> re.split('(\W+)', 'Words, words, words.')
['Words', ', ', 'words', ', ', 'words', '.', '']

https://stackoverflow.com/questions/1059559/split-strings-with-multiple-delimiters

NEXT:

2.  use pattern.en to parse individual words

'''


showparsed(nlp("painting"))

showparsed(nlp("let's watch 7even"))
showparsed(nlp("let's"))

showparsed(nlp("easiest"))


