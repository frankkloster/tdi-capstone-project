import tweepy
import pandas as pd
import re

class UserPosts():
    def __init__(self, auth, username):
        self.api = tweepy.API(auth)
        self.username = username

    def get_posts():
        tweets = []
        for page in range(1, 16 + 1):
            tweets = tweets + api.user_timeline(self.username, count=200, tweet_mode='extended', page=page)
            time.sleep(65)

        self.tweets
        return self

class Tweets():
    def __init__(self, tweets):
        self.tweets = tweets

    def process_tweets_into_df(self, columns=['full_text', 'created_at']):
        tweet_info = {column: [] for column in columns}
        for tweet in self.tweets:
            for column in columns:
                tweet_info[column].append(tweet._json[column])

        df = pd.DataFrame(tweet_info)

        return df

    def search_for_text(self, word):
        tweet_matches = []
        word_pattern = re.compile('(\s|#){}\s'.format(word))
        for tweet in self.tweets:
            tweet_text = tweet.full_text
            if re.match(word_pattern, tweet_text.lower()):
                tweet_matches.append(tweet_text)
        return tweet_matches
