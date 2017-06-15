
"""
STEP-1

utility that reads the usernames from the the usernames-tweet file
reads topics from theta file (output of jLDADMM java program and dumps the dictionary pickle

input :
    username-tweet-file :
            this is a csv/text with format
            username, tweet_Words  (in a single line)
    theta filename:
            output file from jLDADMM java program
            contains topic probability for users per line.
            eg 0.233 0.212 0.002  (per line)
    name_of_dict:
        for output file

"""

from pymongo import  MongoClient
import argparse
from itertools import izip
from gensim import corpora, matutils, models
import csv
import pickle


# Input arguments
PROGRAM_DESCRIPTION = "Read the topic asignment file from jLDADMM algorithm and creates the topic vectors"
parser = argparse.ArgumentParser(description=PROGRAM_DESCRIPTION)
parser.add_argument('filename', type=str, help='user, words file')
parser.add_argument('usernames', type=str, help='usernames file')
parser.add_argument('dict_name', type=str, help='dictionary name to pickle')
args = vars(parser.parse_args())


def main():
    filename = args['filename']
    usernames = args['usernames']
    dict_name = args['dict_name']

    user_topic_dict = {}
    with open(filename, 'r') as topics, open(usernames, 'r') as users:
        for userid, topic_list in izip(users, topics):
            userid = userid.split(',')[0]
            topic_list_dict = create_dict(map(float, topic_list.split()))
            user_topic_dict[userid] = topic_list_dict

    pickle.dump(user_topic_dict, open(dict_name, 'w'))

def create_dict(l):
    i = 0
    mydict = {}
    for elem in l :
        mydict[i] = elem
        i += 1
    return mydict

if __name__ == "__main__":
    main()