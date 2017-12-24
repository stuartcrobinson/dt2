import numpy

np = numpy
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import LSTM
from keras.callbacks import ModelCheckpoint
from keras.preprocessing.sequence import pad_sequences


def getFileLines(filepath):
    with open(filepath) as f:
        content = f.readlines()
    content = [x.strip('\n') for x in content]
    return content


def getFileIntLines(filepath):
    with open(filepath) as f:
        content = f.readlines()
    content = [int(x.strip('\n')) for x in content]
    return content


print('hello!')

fragsUnique = getFileLines('../output/fragsUnique.txt')
fragIndices0 = getFileIntLines('../output/fragIndices.txt')
wholeWordsUnique = getFileLines('../output/wholeWordsUnique.txt')
wholeWordIndices = getFileIntLines('../output/wholeWordIndices.txt')

# asdf = numpy.loadtxt('../output/fragIndices.txt')


print('fragsUnique len: ' + str(len(fragsUnique)))
print('fragIndices len: ' + str(len(fragIndices0)))
print('wholeWordsUnique len: ' + str(len(wholeWordsUnique)))
print('wholeWordIndices len: ' + str(len(wholeWordIndices)))

# fragIndices0_ = np_utils.to_categorical(fragIndices0)

m_frag_i = dict((s, i) for i, s in enumerate(fragsUnique))
m_i_frag = dict((i, s) for s, i in m_frag_i.items())

m_word_i = dict((s, i) for i, s in enumerate(wholeWordsUnique))
m_i_word = dict((i, s) for s, i in m_word_i.items())

# use frags

fragIndices = fragIndices0[0:int(len(fragIndices0) / 1)]

# save space by using boolean lists/arrays somehow

# prepare the dataset of input to output pairs encoded as integers
seq_length = 100
sentences = []
next_chars = []
for i in range(0, len(fragIndices) - seq_length, 1):
    sentence = fragIndices[i:i + seq_length]
    next_frag = fragIndices[i + seq_length]
    sentences.append(sentence)
    next_chars.append(next_frag)

print('Vectorization...')
x = np.zeros((len(sentences), seq_length, len(fragsUnique)), dtype=np.bool)
y = np.zeros((len(sentences), len(fragsUnique)), dtype=np.bool)
for i, sentence in enumerate(sentences):
    for t, fragIndex in enumerate(sentence):
        x[i, t, fragIndex] = 1
    y[i, next_chars[i]] = 1

########################################################################################################
########################################################################################################
m_capFrag_fragIndexToCap = {'ሏ': -1, 'ሐ': 0, 'ሑ': 1, 'ሒ': 2, 'ሓ': 3, 'ሔ': 4, 'ሕ': 5, 'ሖ': 6, 'ሗ': 7, 'መ': 8, 'ሙ': 9}
capFrags = set(m_capFrag_fragIndexToCap.keys())


def createTextFromFragsList(seedFrags0):
    seedFrags = seedFrags0[:]
    fragsList = [m_i_frag[x] for x in seedFrags]
    # find a cap frag and replace appropriate char w/ capitalized version
    while len(capFrags.intersection(set(fragsList))) > 0:
        for capFrag in capFrags:
            if capFrag in fragsList:
                i = fragsList.index(capFrag)
                if i < len(fragsList) - 1:
                    if capFrag == 'ሏ':
                        fragsList[i + 1] = fragsList[i + 1].upper()
                    else:
                        indexToCap = m_capFrag_fragIndexToCap[capFrag]
                        j = indexToCap
                        frag = fragsList[i + 1]
                        x = frag
                        x = x[0:j] + x[j].upper() + x[j + 1:len(x)]
                        frag = x
                        fragsList[i + 1] = frag
                    del fragsList[i]
    return ''.join(fragsList)


def generateText(model, seedFrags_):
    seedFrags = seedFrags_[:]
    for loop in range(0, 500):
        padded = pad_sequences([seedFrags], seq_length)[0]
        x_pred = np.zeros((1, seq_length, len(fragsUnique)), dtype=np.bool)
        for i, fragIndex in enumerate(padded):
            x_pred[0, i, fragIndex] = 1
        preds = model.predict(x_pred, verbose=0)[0]
        predFragIndex = np.argmax(preds)
        seedFrags.append(predFragIndex)
    return createTextFromFragsList(seedFrags)


########################################################################################################
########################################################################################################

model = Sequential()
model.add(LSTM(256, input_shape=(seq_length, len(fragsUnique))))
model.add(Dropout(0.2))
model.add(Dense(y.shape[1], activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam')
# define the checkpoint
# filepath = "weights-improvement-{epoch:02d}-{loss:.4f}.hdf5"
filepath = "weights.hdf5"
checkpoint = ModelCheckpoint(filepath, monitor='loss', verbose=1, save_best_only=True, mode='min')
# fit the model
callbacks_list = [checkpoint]

model.load_weights(filepath)

seedFrags = [277, 231, 107, 49, 205, 107, 134, 195, 0, 160, 0]  # victims of

for loop in range(0, 100000):
    print(generateText(model, seedFrags))
    model.fit(x, y, epochs=2, batch_size=1000, callbacks=callbacks_list)

# fragsList = ['v', 'i', 'c', 't', 'i', 'm', 's', ' ', 'of', ' ', 'the', ' ', 'ሐ', 'uni', 't', 'ed', ' ', 'ሐ', 'n', 'at', 'ions', ' ', 'ሐ', 'peac', 'e', ' ', 'ሐ', 'priz', 'e', ' ', 'ሐ', 'l', 'a', 'u', 'r', 'e', 'at', 'e', ' ', 'ሐ', 'l', 'a', 'u', 'r', 'e', 'at', 'e', ' ', 'ሐ', 'a', 'l', 'a', 'r', 'm', 'a', 'n', 'c', 'e', ' ', 'ሐ', 'a', 'l', 'a', 'r', ' ', 'ሐ', 'a', 'l', 'a', 'r', 'a', 'm', 'i', 'c', ' ', 'ሐ', 'a', 'l', 'a', 'r', ' ', 'ሐ', 'a', 'l', 'a', 'r', 'a', 'm', 'i', 'c', ' ', 'ሐ', 'a', 'l', 'a', 'r', ' ', 'ሐ', 'a', 'l', 'a', 'r', 'a', 'm', 'i', 'c', ' ', 'ሐ', 'a', 'l', 'a', 'r', ' ', 'ሐ', 'a', 'l', 'a', 'r', 'a', 'm', 'i', 'c', ' ', 'ሐ', 'a', 'l', 'a', 'r', ' ', 'ሐ', 'a', 'l', 'a', 'r', 'a', 'r', 'i', 'an', ' ', 'ሐ', 'n', 'obel', ' ', 'ሐ', 'peac', 'e', ' ', 'ሐ', 'priz', 'e', ' ', 'for', ' ', 'ሐ', 's', 'u', 'l', 'd', 'a', 'm', 'a', ' ', 'and', ' ', 'ሐ', 'g', 'r', 'o', 'u', 's', ' ', 'ሐ', 'a', 'r', 'm', 'a', 'n', 'c', 'i', 'l', 'a', ' ', 'ሐ', 'r', 'o', 't', 'e', ' ', 'ሐ', 'a', 'l', 'i', 'e', ' ', 'ሐ', 'a', 'l', 'a', 'r', 'a', 's', ' ', 'ሐ', 's', 'o', 'u', 'th', ' ', 'ሐ', 'a', 'f']


# nohup python3 test.py >out20171223.log 2>&1 &

# https://www.kaggle.com/lystdo/lstm-with-word2vec-embeddings

# https://stats.stackexchange.com/questions/202544/handling-unknown-words-in-language-modeling-tasks-using-lstm

# https://stats.stackexchange.com/questions/163005/how-to-set-the-dictionary-for-text-analysis-using-neural-networks/163032#163032

# http://www.orbifold.net/default/2017/01/10/embedding-and-tokenizer-in-keras/

# https://www.google.com/search?q=best+way+generate+text+lstm+word2vec+embedding&oq=best+way+generate+text+lstm+word2vec+embedding&aqs=chrome..69i57.11191j0j1&sourceid=chrome&ie=UTF-8
'''
 the Embedding class does indeed map discrete labels (i.e. words) into a continuous vector space. It should be just as clear that this embedding does not in any way take the semantic similarity of the words into account. Check the source code if want to see it even more clearly.

So if word2vec does bring along some extra info into the game how can you use it together with Keras?
'''
