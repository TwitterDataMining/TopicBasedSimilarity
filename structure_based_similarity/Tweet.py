import datetime


class Tweet:
    MENTION = "user_mentions"
    QUOTE_FIELD = "quoted_status"
    REPLY_FIELD = "in_reply_to_user_id"
    RETWEET_FIELD = "retweeted_status"
    HASHTAG_FIELD = "hashtags"

    def __init__(self, tweet):
        self.tweet = tweet
        #self.author_id = int(self.tweet['user']['id'])
        self.author_id = int(self.tweet['user_id'])
        # self.create_time = int(
        #     datetime.datetime.strptime(self.tweet['created_at'], "%a %b %d %H:%M:%S %z %Y").timestamp())

        # Retweet field
        if Tweet.RETWEET_FIELD in tweet:
            self.retweet_author_id = int(tweet[Tweet.RETWEET_FIELD]["user"]["id"])
        else:
            self.retweet_author_id = None

        # Quote field
        if Tweet.QUOTE_FIELD in tweet:
            self.quote_author_id = int(tweet[Tweet.QUOTE_FIELD]["user"]["id"])
        else:
            self.quote_author_id = None

        # Mention field
        if Tweet.MENTION in tweet["entities"]:
            self.mentions = [int(user['id']) for user in tweet["entities"][Tweet.MENTION]]
        else:
            self.mentions = None

        # Reply field
        if Tweet.REPLY_FIELD in tweet and tweet[Tweet.REPLY_FIELD]:
            self.reply_id = int(tweet[Tweet.REPLY_FIELD])
        else:
            self.reply_id = None

        if Tweet.HASHTAG_FIELD in tweet["entities"]:
            self.hashtags = [hashtag for  hashtag in tweet["entities"][Tweet.HASHTAG_FIELD]]
        else:
            self.hashtags = None

