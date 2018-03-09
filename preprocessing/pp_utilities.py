import contractions_dict

from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
import string
import pickle
import collections
import json
import numpy as np


# Get businesses which only have 'food' in categories
def load_businesses(filename):
    businesses = set()
    with open(filename, 'r') as f:
        for line in f:
            line = line.lower()
            business_info = json.loads(line)
            if 'food' in business_info['categories']:
                businesses.add(business_info['business_id'])
    print('Total Number of Businesses: %d' %len(businesses))
    return businesses


def clean_text(text, stop_words):
    assert isinstance(text, str)
    assert isinstance(stop_words,set)

    # Remove numbers from text
    text = ''.join([c for c in text if not c.isdigit()])

    # Replace punctuation from text with space
    translator = str.maketrans(string.punctuation,' '*len(string.punctuation))
    text = text.translate(translator)

    # Replace contractions
    text = word_tokenize(text)
    contractions = contractions_dict.contractions
    for i in range(len(text)):
        if text[i] in contractions:
            text[i] = contractions[text[i]]
    text = ' '.join(text)

    # Remove stop words from text
    text = word_tokenize(text)
    text = [t for t in text if t not in stop_words]

    # STEM: Convert words to 'root' word i.e. tenses
    ps = PorterStemmer()
    text = [ps.stem(w) for w in text]

    text = ' '.join(text)

    '''
    # LEMMANIZE: Convert words to base word i.e are-->be
    lt = WordNetLemmatizer()
    text = [lt.lemmatize(w) for w in text]
    
    '''
    return text

def reduce_vocab(review_text, min_freq):
    assert isinstance(review_text,list)

    all_words = ' '.join(review_text)
    words = word_tokenize(all_words)

    word_count = collections.Counter()
    for w in words:
        word_count[w] += 1

    reduced_vocab = [w for w in word_count if word_count[w] > min_freq]

    return reduced_vocab

def text_length_stats(review_text):
    assert isinstance(review_text,list)


    length_reviews = np.zeros((len(review_text),1)) #to calc AVG/STD
    for i in range(len(review_text)):
        text = word_tokenize(review_text[i])
        length_reviews[i] = len(text)
    return np.mean(length_reviews), np.std(length_reviews)

def reshape_text(text, length):
    assert isinstance(text,str)
    assert isinstance(length,int)

    new_text = ['0']*length

    words = word_tokenize(text)
    if len(words) < length:
        new_text[:len(words)] = words[:]
    elif len(words) > length:
        new_text[:length] = words[:length]

    new_text = ' '.join(new_text)
    return new_text

    

    


