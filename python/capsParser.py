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

# utf8 shapes http://www.fileformat.info/info/charset/UTF-8/list.htm?start=8000

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
... eh let's just try it
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
#     print('  in getCapsChars')
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
#             print('    capsChars:', capsChars, 'word: ', word)
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



# 
# '''
# use these for caps chars:
# █ - all caps
# ▟ -1
# ▙ -2
# ▛ -3
# ▜ -4
# ▞ -5
# ▚ -6
# ▘ -7
# ▝ -8
# ▗ -9
# ▖ -10 
# '''
# 
# '''
# 
# input a word.  
# 
# create empty array of caps chars
# 
# make int count = 0
# 
# start at the end.  i = 0.  last letter.  if it's cap, prepend capschar(len(word)).  and count++
# 
# move to prev letter.  i = 1.  if cap, prepend capschar(len(word) - i + count).  and count++
# move to prev letter.  i = 2.  if not cap, move on
# move to prev letter.  i = 3.  if cap, prepend capschar(len(word) - i + count).  and count++
# 
# salaD
# 
# len = 5
# 5th letter
# caps char - 5 letters away
# capschar(5)
# 
# 
# sAlaDS
# 
# len = 6
#  fuck it let's try it.  i think i works.
# 
# '''
# 
# capsChars = ['█' , '▟' , '▙' , '▛' , '▜' , '▞' , '▚' , '▘' , '▝' , '▗' , '▖']
# 
# m_i_capChar = dict((i, c) for i, c in enumerate(capsChars))
# m_capChar_i = dict((c, i) for i, c in enumerate(capsChars))
# # 
# # 
# # def getCapsChar(n):
# #     # this is stupid.  should be a map.
# #     if n == 0: return '█'  # all caps
# #     if n == 1: return '▟'  # all caps
# #     if n == 2: return '▙'  # all caps
# #     if n == 3: return '▛'  # all caps
# #     if n == 4: return '▜'  # all caps
# #     if n == 5: return '▞'  # all caps
# #     if n == 6: return '▚'  # all caps
# #     if n == 7: return '▘'  # all caps
# #     if n == 8: return '▝'  # all caps
# #     if n == 9: return '▗'  # all caps
# #     if n == 10: return '▖'  # all caps
# #     raise Exception("n must be between 0 and 10 inclusive")
# 
# 
# def getCapsChars(word):
#     if word.isupper():
#         return m_i_capChar[0]
#     wordlen = len(word)
#     
#     capsChars = []
#     
#     capsCount = 0
#     for i in range(0, wordlen):
#         letterIndex = wordlen - 1 - i
#         letter = word[letterIndex]
#         if letter.isupper():
#             capsChars = [m_i_capChar[wordlen - i + capsCount]] + capsChars
#             capsCount += 1
#     return capsChars
# 
# def capitalizeSpecificLetterAtIndex(my_string, n):
#     try:
#         return ''.join([my_string[:n], my_string[n].upper(), my_string[n + 1:]])
#     except:
#         return my_string
# 
# def capitalizeWord(word, capsChars):
#     '''
#     salaD
#     
#     
#     for char in capsChar, GOING BACKWARDS - start at end!
#     
#     count = 0;
#     
#     determine capNumber cn.  capitalize word at index CN - 1.  then count++
#     
#     next caps char
#     
#     determine capNmber CN.  capitalize word at index CN - 1 + count
#     '''
#     if capsChars[0] == '█':
#         return word.upper()
#     
#     
#     count = 0
#     for i in range(len(capsChars) - 1, 0 - 1, -1):
#         capsChar = capsChars[i]
#         word = capitalizeSpecificLetterAtIndex(word, m_capChar_i[capsChar] - 1 - count)
#         count += 1
#     return word

# capitalizeWord('house', ['▝' ,'▙'])

# print(getCapsChars('gloveS'))
        
#       
#       
#       
#       
#       
#       
#       
#       
#       
#       
#       
#       
#       
#       
#       
#       
#       
#       
#       
#       
#       
#       
#       
# qwfasdf        
    
