import numpy
from keras.utils import np_utils


def getFileLines(filepath):
    with open(filepath) as f:
        content = f.readlines()
    content = [x.strip('\n') for x in content]
    return content


print('hello!')

fragsUnique = getFileLines('../output/fragsUnique.txt')
fragIndices = getFileLines('../output/fragIndices.txt')
wholeWordsUnique = getFileLines('../output/wholeWordsUnique.txt')
wholeWordIndices = getFileLines('../output/wholeWordIndices.txt')

print('fragsUnique len: ' + str(len(fragsUnique)))
print('fragIndices len: ' + str(len(fragIndices)))
print('wholeWordsUnique len: ' + str(len(wholeWordsUnique)))
print('wholeWordIndices len: ' + str(len(wholeWordIndices)))

m_frag_i = dict((s, i) for i, s in enumerate(fragsUnique))
m_i_frag = dict((i, s) for s, i in m_frag_i.items())

m_word_i = dict((s, i) for i, s in enumerate(wholeWordsUnique))
m_i_word = dict((i, s) for s, i in m_word_i.items())

# use frags

# prepare the dataset of input to output pairs encoded as integers
seq_length = 100
dataX = []
dataY = []
for i in range(0, len(fragIndices) - seq_length, 1):
    seq_in = fragIndices[i:i + seq_length]
    seq_out = fragIndices[i + seq_length]
    dataX.append(seq_in)
    dataY.append(seq_out)
n_patterns = len(dataX)
print("Total Patterns: ", n_patterns)

# reshape X to be [samples, time steps, features]
X = numpy.reshape(dataX, (n_patterns, seq_length, 1))

# no - he recommends one-hot encoding these days
# # normalize
# X = X / float(n_vocab)

X = np_utils.to_categorical(X)  # ????

# one hot encode the output variable
y = np_utils.to_categorical(dataY)
