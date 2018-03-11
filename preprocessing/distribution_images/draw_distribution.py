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
    import re
    text_words = []
    for idx in range(len(review_text)):
        words = re.split('\W+', review_text[idx])
        text_words.append(0)
        #print len(words)
        for word in words:
            if len(word) != 0:
                text_words[idx] += 1
    #print len(text_words)
    for i in range(10):
        print text_words[i]
        print review_text[i]
        print "*"*100
    plt.hist(text_words, alpha=0.5)
    plt.xlabel("review text word numbers")
    plt.ylabel("word number counts distribution")
    plt.title("yelp review number of words distribution")
    plt.show()



if __name__ == "__main__":
    main()