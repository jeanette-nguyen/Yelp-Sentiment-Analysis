# File to contain overhead functions
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import string

def clean_text(text, stop_words):
    assert isinstance(str, text)
    assert isinstance(set,stop_words)

    # Remove numbers from text
    text = ''.join([c for c in text if not c.isdigit()])

    # Remove punctuation from text
    translator = str.maketrans('', '', string.punctuation)
    text = text.translate(translator)


    # Remove stop words from text
    text = word_tokenize(text)
    #text = ''.join([t for t in text if t not in stop_words])

    # Convert words to 'root' word i.e. tenses
    ps = PorterStemmer()
    text = [ps.stem(w) for w in text]

    # TODO: remove "sparse" terms