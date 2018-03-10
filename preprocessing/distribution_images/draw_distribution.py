import pp_utilities as utils
import pp_logger as logger
import matplotlib.pyplot as plt

#import pandas as pd
#import numpy as np
#import argparse
import json
#from nltk.corpus import stopwords
import datetime
#import tqdm

"""This file is to pre-process the data"""

# Read in arguments from 'command_args.txt'
args = logger.read_args('pp_args.txt')

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

def main():
    review_text, review_star = load_reviews()
    star_distribution = [0]*5
    for star in review_star:
        star_distribution[star-1] += 1
    left = [1,2,3,4,5]
    plt.bar(left, star_distribution, width=1, align = 'center',  alpha = 0.5)
    plt.xlabel("star rating")
    plt.ylabel("rating numbers")
    plt.title("yelp rating distribution")
    plt.show()

    text_length = []
    for text in review_text:
        text_length.append(len(text))
    plt.hist(text_length, alpha=0.5)
    plt.xlabel("review text length")
    plt.ylabel("review text length counts")
    plt.title("yelp review text length distribution")
    plt.show()



if __name__ == "__main__":
    main()