
import pandas as pd
import numpy as np
import argparse
import json
import utilities as utils
from nltk.corpus import stopwords
import contractions_dict

"""This file is to pre-process the data"""
parser = argparse.ArgumentParser()
parser.add_argument("-b", "--business_data", default='./dataset/business.json')
parser.add_argument("-r", "--review_data", default='./dataset/review.json')
parser.add_argument("-u", "--user_data", default='./dataset/user.json')


# read in arguments from the commandline
args = parser.parse_args()


def load_businesses():
    businesses = set()
    with open(args.business_data, 'r') as f:
        for line in f:
            line = line.lower()
            business_info = json.loads(line)
            if 'food' in business_info['categories']:
                businesses.add(business_info['business_id'])
    print('Total Number of Businesses: %d' %len(businesses))
    return businesses

def load_reviews():
    stop_words = set(stopwords.words('english'))
    contractions = contractions_dict.contractions
    businesses = load_businesses()
    review_text = []
    review_star = []
    with open(args.review_data, 'r') as f:
        i = 0
        for line in f:
            
            line = line.lower()
            review_info = json.loads(line)
            try:

                if review_info['business_id'] not in businesses:
                    continue
                i+=1
                # Check first if review has star rating and text
                # TODO: filter out diff languages???
                star = review_info['stars']
                text = review_info['text']
                assert star is not None
                assert text is not None

                text = utils.clean_text(text)
                print(text)
                review_text.append(text)
                review_star.append(star)

            # Key errors, assertion errors, etc. 
            except:
                continue
    print(i)
    print("Total Number of Reviews: %d" %len(review_star))
    return review_text, review_star


def main():
    review_text, review_star = load_reviews()
    #json_to_csv(args.review_data)
    #json_to_csv(args.user_data)


if __name__=="__main__":
    #json.loads(args.business_data)
    main()