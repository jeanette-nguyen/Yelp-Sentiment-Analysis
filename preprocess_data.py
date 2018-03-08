
import pandas as pd
import numpy as np
import argparse
import json
import utilities as utils
from nltk.corpus import stopwords
import datetime
import tqdm

"""This file is to pre-process the data"""
parser = argparse.ArgumentParser()
parser.add_argument("-b", "--business_data", default='./dataset/business.json')
parser.add_argument("-r", "--review_data", default='./dataset/review.json')
parser.add_argument("-u", "--user_data", default='./dataset/user.json')
parser.add_argument("-s", "--save_name", default='./dataset/processed_data/' + \
    ('{:%b_%d_%H:%M}'.format(datetime.datetime.now())))


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
    businesses = load_businesses()
    data = []
    counter = 0
    with open(args.review_data, 'r') as f:
        for line in f:#tqdm(f):
            line = line.lower()
            review_info = json.loads(line)
            try:

                if review_info['business_id'] not in businesses:
                    continue
                # Check first if review has star rating and text
                # TODO: filter out diff languages???
                counter += 1
                star = review_info['stars']
                text = review_info['text']
                assert star is not None
                assert text is not None

                text = utils.clean_text(text,stop_words)
                data.append((text,star))

                if counter%10000 == 0:
                    print("Counter: %d"%counter)
                    print(text)
                if (counter%300000 == 0):
                    print("Pickling files...")
                    pickle_name = './dataset/processed_data/'+args.save_name+'.p'
                    utils.pickle_files(pickle_name, data)
                    print("Done pickling")
                    break

            # Key errors, assertion errors, etc. 
            except KeyError:
                continue
            except AssertionError:
                continue

        #utils.pickle_file(args.save_name+'.p', data)

    print("Total Number of Reviews: %d" %len(data))
    #return review_text, review_star


def main():
    load_reviews()
    #json_to_csv(args.review_data)
    #json_to_csv(args.user_data)


if __name__=="__main__":
    #json.loads(args.business_data)
    main()