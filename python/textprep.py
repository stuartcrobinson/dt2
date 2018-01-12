import re

from PIL.WmfImagePlugin import word
from nltk import pos_tag
import nltk
from nltk.corpus import wordnet as wn
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize

# import capsParser
from pattern.en import parse, comparative, superlative, pluralize

wnl = WordNetLemmatizer()

##################################################################################################################################################################
###############################################################  capsParser.py - eclipse too stupid for sep file? ################################################
##################################################################################################################################################################
##################################################################################################################################################################
'''
use these for caps chars:
█ - all caps
▟ -1
▙ -2
▛ -3
▜ -4
▞ -5
▚ -6
▘ -7
▝ -8
▗ -9
▖ -10 
'''

'''

input a word.  

create empty array of caps chars

make int count = 0

start at the end.  i = 0.  last letter.  if it's cap, prepend capschar(len(word)).  and count++

move to prev letter.  i = 1.  if cap, prepend capschar(len(word) - i + count).  and count++
move to prev letter.  i = 2.  if not cap, move on
move to prev letter.  i = 3.  if cap, prepend capschar(len(word) - i + count).  and count++

salaD

len = 5
5th letter
caps char - 5 letters away
capschar(5)


sAlaDS

len = 6
 fuck it let's try it.  i think i works.

'''

capsCharsList = ['█' , '▟' , '▙' , '▛' , '▜' , '▞' , '▚' , '▘' , '▝' , '▗' , '▖']

m_i_capChar = dict((i, c) for i, c in enumerate(capsCharsList))
m_capChar_i = dict((c, i) for i, c in enumerate(capsCharsList))
# 
# 
# def getCapsChar(n):
#     # this is stupid.  should be a map.
#     if n == 0: return '█'  # all caps
#     if n == 1: return '▟'  # all caps
#     if n == 2: return '▙'  # all caps
#     if n == 3: return '▛'  # all caps
#     if n == 4: return '▜'  # all caps
#     if n == 5: return '▞'  # all caps
#     if n == 6: return '▚'  # all caps
#     if n == 7: return '▘'  # all caps
#     if n == 8: return '▝'  # all caps
#     if n == 9: return '▗'  # all caps
#     if n == 10: return '▖'  # all caps
#     raise Exception("n must be between 0 and 10 inclusive")


def getCapsChars(word):
    if word.isupper():
        return [m_i_capChar[0]]
    wordlen = len(word)
    
    capsChars = []
    
    capsCount = 0
    for i in range(0, wordlen):
        letterIndex = wordlen - 1 - i
        letter = word[letterIndex]
        if letter.isupper():
            capsChars = [m_i_capChar[wordlen - i + capsCount]] + capsChars
            capsCount += 1
    return capsChars


def capitalizeSpecificLetterAtIndex(my_string, n):
    try:
        return ''.join([my_string[:n], my_string[n].upper(), my_string[n + 1:]])
    except:
        return my_string


def capitalizeWord(word, capsChars):
    '''
    salaD
    
    
    for char in capsChar, GOING BACKWARDS - start at end!
    
    count = 0;
    
    determine capNumber cn.  capitalize word at index CN - 1.  then count++
    
    next caps char
    
    determine capNmber CN.  capitalize word at index CN - 1 + count
    '''
    if capsChars[0] == '█':
        return word.upper()
    
    count = 0
    for i in range(len(capsChars) - 1, 0 - 1, -1):
        capsChar = capsChars[i]
        word = capitalizeSpecificLetterAtIndex(word, m_capChar_i[capsChar] - 1 - count)
        count += 1
    return word
##################################################################################################################################################################
##################################################################################################################################################################
##################################################################################################################################################################
##################################################################################################################################################################

 
#
# 1.  split corpus at spaces and punct:
# https://stackoverflow.com/questions/1059559/split-strings-with-multiple-delimiters
# https://stackoverflow.com/a/16840963/8870055
def getAdverbRoot(adverb):
    winner = ""
    try:
        wordtoinv = adverb
        s = []
        for ss in wn.synsets(wordtoinv):
            for lemmas in ss.lemmas():  # all possible lemmas.
                s.append(lemmas)
        for pers in s:
            posword = pers.pertainyms()[0].name()
            if posword[0:3] == wordtoinv[0:3]:
                winner = posword
                break
    except IndexError:
        pass
    # print(winner) # undue
    # print("in getAdverbRoot: input: " + adverb + ", result: <" + winner + ">")
    if winner == '':
        return adverb
    else:
        return winner


# TODO what if not found?
def getAdjectiveRoot(superlativeOrComparative):
    return wnl.lemmatize(superlativeOrComparative, 'a')


def isGerund(word):
    return pos_tag(word_tokenize(word))[0][1] == 'VBG'


def getGerundRoot(gerund):
    return WordNetLemmatizer().lemmatize(gerund, 'v')

# think about 'quickening' - nested lemmas


posChar = '▓'


def postParse(patternParsed):
    '''
    if it can be broken, return array of root and POS atoms.  else, return array containing root
    also - return original word w/ no POS for unsupported POSs (like MD for can --> could. cant untokenize)
    '''
    word = patternParsed[0]
    root = patternParsed[5]
    pos = patternParsed[1]
    # print('root: <' + root + '>, pos: <' + pos + '>, patternParsed: <' + str(patternParsed) + '>')
    #
    unsupportedPosSet = set(['MD'])
    # adverb - get root adjective
    if pos in unsupportedPosSet:
        root = word
    elif pos == 'RB':
        root = getAdverbRoot(root)
    #
    # superlatives and comparative - get root adjective
    elif pos == 'JJS' or pos == 'JJR' or pos == 'RBR':
        root = getAdjectiveRoot(root)
    #
    # ends in ing - pattern.en fails to parse swimming and eating.  but works for talking (talk, VBG)
    elif root[-3:] == 'ing':
        if isGerund(root):
            root = getGerundRoot(root)
            pos = 'VBG'
    return word, root, posChar + pos


'''
use these for caps chars:
█ - all caps
▟ -1
▙ -2
▛ -3
▜ -4
▞ -5
▚ -6
▘ -7
▝ -8
▗ -9
▖ -10 
'''

# utf8 shapes http://www.fileformat.info/info/charset/UTF-8/list.htm?start=8000


# accepts an array like [quickening] or [quicken, VBG] or [quick,
def getBroken(atoms):
    # print(str(atoms))
    word = atoms[0]
    if len(word) == 1:
        return [word]
    returner = []
    patternParsedList = parse(word, relations=True, lemmata=True).split()[0]
    # print("patternParsedList: " + str(patternParsedList))
    for patternParsed in patternParsedList:
        word, root, pos = postParse(patternParsed)
        #
        if root == word:
            returner += [word]
        else:
            # newAtoms = [root, pos] + atoms[1:]
            # returner += getBroken([root, pos])
            returner += [root, pos]
    return returner + atoms[1:]


def displayParsed(text):
    text = text.lower()
    text = text.replace('′', "'")
    text = text.replace('‘', "'")
    text = text.replace('’', "'")
    text = text.replace('“', '"')
    text = text.replace('”', '"')
    text = text.replace('“', '"')
    text = text.replace('”', '"')
    ar = re.split('([^\w\'′]|_| )', text) 
    ar = list(filter(None, ar))
    # print(*ar, sep='\n')
    for s in ar:
        wordAtoms = getBroken([s])
        print('orig: <' + str(s) + '> broken: ' + str(wordAtoms))


def getParsed(text):
    # TODO caps chars
#     text = text.lower()
    text = text.replace('′', "'")
    text = text.replace('‘', "'")
    text = text.replace('’', "'")
    text = text.replace('“', '"')
    text = text.replace('”', '"')
    text = text.replace('“', '"')
    text = text.replace('”', '"')
    ar = re.split('([^\w\'′]|_| )', text) 
    ar = list(filter(None, ar))
    parsed = []
    for s in ar:
        capsChars = getCapsChars(s)
        s = s.lower()
        wordAtoms = getBroken([s])
        print('wordAtoms', wordAtoms)
        print('capsChars', capsChars)
        print('type(capsChars)', type(capsChars))
        parsed += capsChars + wordAtoms
        print('parsed', parsed)
    return parsed


def myUntokenize(atom, pos):
#     print('untokeninzing', atom, pos)
    '''
    https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html
    https://web.archive.org/web/20140519174100/https://www.clips.uantwerpen.be/pages/pattern-en
   '''
#     if pos == 'CC':
#     if pos == 'CD':
#     if pos == 'DT':
#     if pos == 'EX':
#     if pos == 'FW':
#     if pos == 'IN':
#     if pos == 'JJ':
    if pos == 'JJR':
        return comparative(atom)
    if pos == 'JJS':
        return superlative(atom)
#     if pos == 'LS':
#     if pos == 'MD':
#     if pos == 'NN':
    if pos == 'NNS':
        return pluralize(atom)
#     if pos == 'NNP':
#     if pos == 'NNP':
#     if pos == 'PDT':
#     if pos == 'POS':
#     if pos == 'PRP':
#     if pos == 'PRP':
    if pos == 'RB':
        return atom + 'ly'
    if pos == 'RBR':
        return comparative(atom)
    if pos == 'RBS':
        return superlative(atom)
#     if pos == 'RP':
#     if pos == 'SYM':
#     if pos == 'TO':
#     if pos == 'UH':
    if pos == 'VB': 
        return conjugate(atom, 'inf')
    if pos == 'VBD':
        return conjugate(atom, 'p')
    if pos == 'VBG':
        return conjugate(atom, 'part')
    if pos == 'VBN':
        return conjugate(atom, 'ppart')
    if pos == 'VBP':
        return conjugate(atom, '1sg')
    if pos == 'VBZ':
        return conjugate(atom, '3sg')
#     if pos == 'WDT':
#     if pos == 'WP':
#     if pos == 'WP$':
#     if pos == 'WRB':
    raise Exception("failed to untokenize: " + atom + ", " + pos)
    return prevAtoms + pos


def myUnparse(atoms):
    capsChars = []
    i = 0
    while i < len(atoms):
        atom = atoms[i]
        print('main i', i)
        print('main atom', atom)
        print('main atoms', atoms)
        if atom in capsCharsList:
            print('found caps char')
            capsChars += [atom]
            print('capsChars', capsChars)
            print('atoms', atoms)
            print('i', i)
            del atoms[i]
            print('after remove')
            print('atoms', atoms)
            i -= 1
            print('i', i)
            print('capsChars', capsChars)
            continue
        if atom[0] == posChar:
#             if i == 0:    #will never happen prob
#                 raise Exception("the first character was a POS character wtf")
            pos = atom[1:]  # remove the leading posChar
            prevAtom = atoms[i - 1]
            del atoms[i]
            i -= 1
            atoms[i] = myUntokenize(prevAtom, pos)
        if len(capsChars) > 0:
            print('capschars non empty!')
            print('atom', atom)
            print('capsChars', capsChars)
            print('capitalizeWord', capitalizeWord(atom, capsChars))
            atoms[i] = capitalizeWord(atom, capsChars)
            print('after edit')
            print('atoms', atoms)
            capsChars = []
    i += 1


'''
TODO - caps chars.  then tokenizing and untokeninzing will be complete!!!!!!!!!!!!!!!!!!!

then, get texts, read texts, build word2vec (or glove????) embedding, then use to train NN!



'''

# displayParsed("isn't rather we're very quickly exceedingly sleep-deprived deprived of sleep hungrier than their's quicken the sunken ship")

# str = "Mrs. Stephens took in her long flowing auburn hair, her slightly pale face with large blue eyes. She wore a fair bit of make up, with blue eyeshadow filling her eyelids and deep red lipstick emphasisng her lips. She wore clothes Severus could only identify as a Muggles mini dress mixed with a traditional witch's corset."
# str = "do you want an apple or a carrot"
# print(getParsed(str))

# str = """‘How queer it seems,’ Alice said to herself, ‘to be going messages for a rabbit! I suppose Dinah’ll be sending me on messages next!’ And she began fancying the sort of thing that would happen: ‘“Miss Alice! Come here directly, and get ready for your walk!” “Coming in a minute, nurse! But I’ve got to see that the mouse doesn’t get out.” Only I don’t think,’ Alice went on, ‘that they’d let Dinah stop in the house if it began ordering people about like that!’
# By this time she had found her way into a tidy little room with a table in the window, and on it (as she had hoped) a fan and two or three pairs of tiny white kid gloves: she took up the fan and a pair of the gloves, and was just going to leave the room, when her eye fell upon a little bottle that stood near the looking-glass. There was no label this time with the words ‘DRINK ME,’ but nevertheless she uncorked it and put it to her lips. ‘I know something interesting is sure to happen,’ she said to herself, ‘whenever I eat or drink anything; so I’ll just see what this bottle does. I do hope it’ll make me grow large again, for really I’m quite tired of being such a tiny little thing!’
# It did so indeed, and much sooner than she had expected: before she had drunk half the bottle, she found her head pressing against the ceiling, and had to stoop to save her neck from being broken. She hastily put down the bottle, saying to herself ‘That’s quite enough—I hope I shan’t grow any more—As it is, I can’t get out at the door—I do wish I hadn’t drunk quite so much!’""" 


# str = ' afterward already almost back better best even far fast hard here how late long low more near never next now often quick rather slow so soon still then today tomorrow too very well where yesterday quickly eat the pizzas' 
str = 'QUICK eat the pizzas'
atoms = getParsed(str)
print(atoms)

print()
myUnparse(atoms)
print(atoms)

print()
print(str)
print()
print(''.join(atoms))

