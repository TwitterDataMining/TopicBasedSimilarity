"""
read date for a tv show and prepare for topic modelling, uses the collections for specific show ie.

input  : collection name, path to unique users list
process : reads from collection
output :
        - csv file of preprocessed tweets - one line per user
        - csv file of preprocessed tweets - one line = username- single tweet

"""
from pymongo import MongoClient
import argparse
import os
import logging
import datetime

import numpy as np
import nltk
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag
from functools32 import lru_cache
import re


TWEET_PER_USER = 1000


# Input arguments
PROGRAM_DESCRIPTION = "Read tweets from collection"
parser = argparse.ArgumentParser(description=PROGRAM_DESCRIPTION)
parser.add_argument('collection_name', type=str, help='collection_to_read_tweets')
parser.add_argument('directory', type=str, help='directory to store')
parser.add_argument('unique_user_file', type=str, help='path to unique user list in csv')
parser.add_argument('prefix', type=str, help='used in output file name eg hashtag')

args = vars(parser.parse_args())

# initializing lemmatizer
stemmer = SnowballStemmer("english")
wordnet_lemmatizer = WordNetLemmatizer()
lemmatize = lru_cache(maxsize=50000)(wordnet_lemmatizer.lemmatize)


def main():
    collection_name = args['collection_name']
    dir = args['directory']
    unique_user_file = args['unique_user_file']
    DIRECTORY = args['prefix']

    try:
        os.stat(dir)
    except:
        os.mkdir(dir)

    log_file = dir + '/' + DIRECTORY + "_log.log"
    logging.basicConfig(filename=log_file, level=logging.DEBUG, format='%(asctime)s %(message)s')
    logging.debug("reading users fof topic modelling: {0} for hashtags : {1}".format(datetime.date.today(), collection_name))


    coll = get_mongo_connection()[collection_name]
    user_list = get_unique_users_fromfile(unique_user_file)
    total_users = 0
    discarded= 0
    with open(dir + '/' + DIRECTORY + '_raw_username.csv', 'w') as raw_u,\
            open(dir + '/' + DIRECTORY + '_username.csv', 'w') as f,\
            open(dir + '/' + DIRECTORY + '_text.csv', 'w') as ftext, \
            open(dir + '/' + DIRECTORY + '_s_username.csv', 'w') as fs, \
            open(dir + '/' + DIRECTORY + '_s_text.csv', 'w') as fstext:
        for user in user_list:
            total_users +=1
            if total_users % 50 ==0:
                logging.debug("User processed : {0}".format(total_users))
            tweets, u_tweets = get_tweet_preprocessed(coll, user)
            if len(tweets) < 6:
                discarded += 1
                continue
            for tweet, u_tweet in zip(tweets, u_tweets):
                raw_u.write(str(user).encode('utf-8') + ",")
                raw_u.write(u_tweet.encode('utf-8') + '\n')
                fs.write(str(user) + ",")
                fs.write(tweet + '\n')
                fstext.write(tweet + '\n')

            f.write(str(user) + ",")
            text = " ".join(tweets)
            f.write(text + "\n")
            ftext.write(text + "\n")

    logging.debug("Total unique users : {0}".format(total_users))
    logging.debug("discarded tweets < 10 : {0}".format(discarded))


def get_tweet_preprocessed(coll, user):
    query ={}
    query['user_id'] = user
    query['lang'] = 'en'
    projection = {'user_id' : 1,  'text': 1}
    tweets = coll.find(query, projection)
    print("user {0} tweets {1}".format(user, tweets.count()))
    tweet_list = []
    unprocessed_tweets = []
    count = 0
    for tweet in tweets:
        count += 1
        unprocessed_tweets.append(remove_puct(tweet['text']))
        if count >= TWEET_PER_USER:
            break
    tweet_list = preprocess(unprocessed_tweets)
    return tweet_list, unprocessed_tweets

def remove_puct(text):

    text = remove_urls(text)
    text = remove_non_ascii(text)
    text = text.replace(',', '')
    text = re.sub(r"""[\'\"]""", '', text)
    text = ' '.join(text.split())
    return text

def preprocess(tweet_list):
    return_list = []
    stop_words = stop_words_list()
    for tweet in tweet_list:
        return_list.append(tokenize_and_lemmatize(tweet, stop_words))
    return return_list

def get_unique_users(coll):
    return coll.distinct('user_id')

def get_unique_users_fromfile(filename):
    users = []
    with open(filename, 'rb') as f:
        users = map(int, f.readlines())
    print users
    return users


def get_mongo_connection(host="localhost", port=27017, db_name="stream_store"):
    return MongoClient(host=host, port=port)[db_name]



def remove_non_ascii(s):
    return "".join(i for i in s if ord(i) < 128)


def stop_words_list():
    """
        A stop list specific to the observed timelines composed of noisy words
        This list would change for different set of timelines
    """
    stop_words = ['bc', 'http', 'https', 'co', 'com','rt', 'one', 'us', 'new',
              'lol', 'may', 'get', 'want', 'like', 'love', 'no', 'thank', 'would', 'thanks',
              'good', 'much', 'low', 'roger']

    stoplist  = set( nltk.corpus.stopwords.words("english") + stop_words)
    return stoplist


def remove_urls(text):
    text = re.sub(r"(?:\@|http?\://)\S+", "", text)
    text = re.sub(r"(?:\@|https?\://)\S+", "", text)
    return text

def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return 'a'
    elif treebank_tag.startswith('V'):
        return 'v'
    elif treebank_tag.startswith('N'):
        return 'n'
    elif treebank_tag.startswith('R'):
        return 'r'
    else:
        return None

def tokenize(text):
    """
    helper function to readTweets() removes url and tokenizes text
    :param text
    """
    text = remove_urls(text)
    text = remove_non_ascii(text)
    text = re.sub(r"""[\'\"]""",'', text)
    regexps = (
        r"""(?:[\w_]+)""",                          # regular word
        r"""(?:[a-z][a-z'\-_]+[a-z])"""             # word with an apostrophe or a dash
    )
    tokens_regexp = re.compile(r"""(%s)""" % "|".join(regexps),
                               re.VERBOSE | re.I | re.UNICODE)
    return tokens_regexp.findall(text)


def tokenize_and_lemmatize(text, stop_words):
    # get the tokens, lowercase - replace acronym
    tokens = [item.strip().lower() for item in tokenize(text)]

    tokens_pos = pos_tag(tokens)
    words = []
    for token in tokens_pos:
        pos = get_wordnet_pos(token[1])
        # if verb, noun, adj or adverb include them after lemmatization
        if pos is not None and token[0] not in stop_words and len(token[0]) > 3:
            try:
                tok = lemmatize(token[0], pos)
                words.append(tok)
            except UnicodeDecodeError:
                pass
    # print words
    return " ".join(words)
if __name__ == "__main__":
    main()
