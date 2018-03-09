import torch
from nltk.tokenize import word_tokenize
import random

def split_data(x,y):
    data = zip(x,y)
    random.shuffle(data)
    #zip(*data)
    total = len(data)
    train = data[:int(0.7*total)]
    valid = data[int(0.7*total): int(0.85*total)]
    test = data[int(0.85*total)]
    return train, valid, test

def word2int(review_text):
    assert isinstance(review_text, list)

    all_text = ' '.join(review_text)
    words = word_tokenize(all_text)
    word2int = dict((a, b) for b, a in enumerate(list(set(words))))
    return word2int, size(word2int)

def text2numbers(text, word2int):
    assert isinstance(text,list)
    assert isinstance(word2int,dict)

    encoded_text = []
    for t in text: 
        words = word_tokenize(t)
        words_int = list(map(lambda x: word2int[x], words))
        encoded_text.append(new_t)
    return encoded_text

