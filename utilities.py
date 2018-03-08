# File to contain overhead functions
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer, WordNetLemmatizer
import string
import contractions_dict
import pickle

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

    return text

    '''
    # LEMMANIZE: Convert words to base word i.e are-->be
    lt = WordNetLemmatizer()
    text = [lt.lemmatize(w) for w in text]
    
    '''

    # TODO: remove "sparse" terms

def pickle_files(filename, stuff):
    '''
    Save files to be loaded in the future
    :param filename: name of file to save
    :type filename: str
    :param stuff: Datastructure to be saved
    :return: None
    '''
    with open(filename, 'wb') as f:
        pickle.dump(stuff, f)


def load_files(filename):
    '''
    Load files from pickle
    :param filename: name of pickle to load
    :type filename: str
    :return: None
    '''
    saved_stuff = open(filename,"rb")
    stuff = pickle.load(saved_stuff)
    saved_stuff.close()
    return stuff
