import re

ALL_LETTERS = "\n !\"&'(),-.0123456789:;>?ABCDEFGHIJKLMNOPQRSTUVWXYZ[]abcdefghijklmnopqrstuvwxyz}"
NUM_LETTERS = len(ALL_LETTERS)

def _one_hot(index, size):
    vec = [0 for _ in range(size)]
    vec[int(index)] = 1
    return vec

def letter_to_vec(letter):
    index = ALL_LETTERS.find(letter)
    return _one_hot(index, NUM_LETTERS)


def word_to_indices(word):
    indices = []
    for c in word:
        indices.append(ALL_LETTERS.find(c))
    return indices


def split_line(line):
    return re.findall(r"[\w']+|[.,!?;]", line)

def _word_to_index(word, indd):
    if word in indd:
        return indd[word]
    else:
        return len(indd)


def line_to_indices(line, indd, max_words=25):
    line_list = split_line(line)  # split phrase in words
    indl = []
    for word in line_list:
        cind = _word_to_index(word, indd)
        indl.append(cind)
        if len(indl) == max_words:
            break
    for i in range(max_words - len(indl)):
        indl.append(len(indd))
    return indl

def bag_of_words(line, vocab):
    bag = [0]*len(vocab)
    words = split_line(line)
    for w in words:
        if w in vocab:
            bag[vocab[w]] += 1
    return bag