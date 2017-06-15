
"""
STEP-1

Small utility that reads the usernames frrom the the usernamees-tweet file
reads topics from theta file (output of jLDADMM java program and dumps the dictionary pickle

input :
    username-tweet-file :
            this is a csv/text with format
            username, tweet_Words  (in a single line)
            // note that there are multiple lined per user.
    topic assignment filename:
            output file from jLDADMM java program - DMM Model
            contains topic assignment for tweet per line.
            eg 2 2 (we pick just the first words assignment as one tweet is assigned to one topic only)

    name_of_dict:
        for output file

"""

from pymongo import  MongoClient
import argparse
from itertools import izip
from gensim import corpora, matutils, models
import csv
import pickle
import logging


# Input arguments
PROGRAM_DESCRIPTION = "Read the topic asignment file from jLDADMM algorithm and creates the topic vectors"
parser = argparse.ArgumentParser(description=PROGRAM_DESCRIPTION)
parser.add_argument('filename', type=str, help='topic file')
parser.add_argument('usernames', type=str, help='usernames , tweet')
parser.add_argument('dict_name', type=str, help='List name to pickle')
parser.add_argument('logfile', type=str, help='logfile')
args = vars(parser.parse_args())


def main():
    filename = args['filename']
    usernames = args['usernames']
    dict_name = args['dict_name']
    log_file = args['logfile']

    logging.basicConfig(filename=log_file, level=logging.DEBUG, format='%(asctime)s %(message)s')
    logging.info("starting user topic list creation for {}".format(filename))
    user_topic_dict = []
    count = 0
    with open(filename, 'r') as topics, open(usernames, 'r') as users:
        for userid, topic_list in izip(users, topics):
            count += 1
            userid = userid.split(',')[0]
            topic = topic_list.split()[0]
            dict = {}
            dict['userid'] = userid
            dict['topic'] = topic
            user_topic_dict.append(dict)
            if count % 1000000 == 0:
                logging.info("users done : {}".format(count))
                print(count)

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