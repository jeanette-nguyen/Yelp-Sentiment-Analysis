import utilities as utils
import logger

import pandas as pd
import numpy as np
import argparse
import json
from nltk.corpus import stopwords
import datetime
import tqdm

"""This file is to pre-process the data"""

# Read in arguments from 'command_args.txt'
args = logger.read_args('command_args.txt')

# Load reviews and perform some preprocessing
def load_reviews():
    businesses = utils.load_businesses(args.business_data)
    review_text = []
    review_star = []
    with open(args.review_data, 'r') as f:
        counter = 0
        for line in f:
            line = line.lower()
            review_info = json.loads(line)
            try:
                if review_info['business_id'] not in businesses:
                    continue
                
                # TODO: filter out diff languages???

                # Check first if review has star rating and text
                star = review_info['stars']
                text = review_info['text']
                assert star is not None
                assert text is not None

                review_text.append(text)
                review_star.append(star)
                counter += 1

                if (counter >= args.num_reviews):
                    return  review_text,review_star

            except KeyError:
                continue
            except AssertionError:
                continue

# Clean syntax of the reviews
def clean_reviews(review_text):
    stop_words = set(stopwords.words('english'))
    review_text_cleaned = []

    counter = 0
    for review in review_text:
        text = utils.clean_text(review,stop_words)
        review_text_cleaned.append(text)
        counter += 1
        if counter%10000 == 0:
            print("Reviews Cleaned: %d"%counter)
            print(text)
    return review_text_cleaned

# Remove sparse words
def reduce_reviews(review_text):
    vocab = utils.reduce_vocab(review_text,args.min_freq)

    review_text_cleaned = []
    for review in review_text:
        r = [w for w in review.split() if w in vocab]
        review_text_cleaned.append(' '.join(r))

    return review_text_cleaned

#Truncate or pad reviews
def reshape_reviews(review_text):
    avg,std = utils.text_length_stats(review_text)

    #review_length = int(avg + std)
    review_length = int(avg)

    review_text_reshaped = []
    for review in review_text:
        r = utils.reshape_text(review,review_length)
        review_text_reshaped.append(r)
    return review_text_reshaped


def main():
    review_text,review_star = load_reviews()
    review_text_cleaned = clean_reviews(review_text)
    review_text_reduced = reduce_reviews(review_text_cleaned)
    review_text_reshaped = reshape_reviews(review_text_reduced)


    print("Pickling files...")
    logger.pickle_files(args.processed_review_text,review_text_reshaped)
    logger.pickle_files(args.processed_review_star,review_star)
    print("Pickling done :)")

if __name__=="__main__":
    main()