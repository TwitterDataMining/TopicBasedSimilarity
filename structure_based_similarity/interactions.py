'''
Class Interactions
Class User
'''

from collections import Counter

import pickle
from pymongo import MongoClient
from Tweet import Tweet


class Interactions:

    FILE = "../data/TheGoodPlace/TheGoodPlace.csv"
    COLLECTION = "old_tweets"
    OUTPUT_FILE = "TheGoodPlace_interactions.p"
    HOST = "10.1.10.96" # default localhost

    def __init__(self, read_collection, query="user.id"):
        self.users = self.get_unique_users_fromfile(Interactions.FILE)
        self.db = self.get_mongo_connection(host=Interactions.HOST)
        self.read_collection = read_collection
        self.query = query

    def get_interactions_for_user(self, user_id):
        user_obj = User(user_id)
        query_string = {self.query: int(user_id)}
        tweets = self.read_collection.find(query_string)
        print(tweets.count())
        for t in tweets:
            tweet = Tweet(t)
            user_obj.add_connections(tweet)
        return user_obj


    def get_interactions_and_hashtags(self):
        self.file_out = open(Interactions.OUTPUT_FILE, 'wb')
        count = 0
        remains = len(self.users)
        for user in self.users:
            user_obj = User(user)
            query_string = {"user.id": int(user)}
            tweets = self.db.old_tweets.find(query_string)
            print(tweets.count())
            for t in tweets:
                tweet = Tweet(t)
                user_obj.add_connections(tweet)
            count += 1
            pickle.dump(user_obj, self.file_out)
            if count % 10 == 0:
                print count, " /", (remains-count)


        self.file_out.close()



    def get_length(self):
        return len(self.users)

    def get_hashtags(users, db):
        pass


    def get_unique_users_fromfile(self, filename):
        users = []
        with open(filename, 'rb') as f:
            users = map(int, f.readlines())
        return users

    def get_mongo_connection(self, host="localhost", port=27017, db_name="stream_store"):
        return MongoClient(host=host, port=port)[db_name]


class User:

    def __init__(self, user):
        self.id = user
        self.mentions = Counter()
        self.replies = Counter()
        self.quotes = Counter()
        self.retweets = Counter()
        self.interactions = Counter()
        self.hashtags = set()


    @classmethod
    def create_from_dict(cls, dict):
        user = cls(dict['id'])
        user.hashtags = set(dict['hashtags'])
        user.mentions = dict['mentions'];
        user.replies = dict['replies']
        user.retweets = dict['retweets']
        user.interactions = dict['interactions']
        user.quotes = dict['quotes']
        return user


    def add_connections(self, tweet):
        if tweet.retweet_author_id:
            self.add_retweet(tweet.retweet_author_id)
        if tweet.quote_author_id:
            self.add_quotes(tweet.quote_author_id)
        if tweet.mentions:
            self.add_mention(tweet.mentions)
        if tweet.reply_id:
            self.add_replies(tweet.reply_id)
        if tweet.hashtags:
            self.add_hashtags(tweet.hashtags)



    def add_mention(self, users):
        for user in users:
            self.mentions[user] += 1
            self.interactions[user] += 1

    def add_replies(self, user):
        self.replies[user] += 1
        self.interactions[user] += 1

    def add_retweet(self, user):
        self.retweets[user] += 1
        self.interactions[user] += 1

    def add_quotes(self, user):
        self.quotes[user] += 1
        self.interactions[user] += 1

    def add_hashtags(self, hashtags):
        for h in hashtags:
            self.hashtags.add(h['text'])

    def toJson(self):
        d = {}
        d['id'] = self.id
        d['mentions'] = self.change_to_str(self.mentions)
        d['retweets'] = self.change_to_str(self.retweets)
        d['quotes'] = self.change_to_str(self.quotes)
        d['interactions'] = self.change_to_str(self.interactions)
        d['hashtags'] = list(self.hashtags)
        d['replies'] = self.change_to_str(self.replies)
        return d

    def change_to_str(self, d):
        return {str(k): v for k, v in d.items()}