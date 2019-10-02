# Used for text processing
import string
import re

# To load saved data.
import dill

# Tweepy, to access the Twitter API.
import tweepy

# Pandas for data processing.
import pandas as pd
from tqdm import tqdm

# Scikit-Learn for machine learning techniques, such as vectorizing and
# LDA for topic analysis.
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation 

# Use pyLDAvis for visualization of LDA topic analysis.
import pyLDAvis.sklearn

# spaCy for language processing.
from spacy.lang.en import English
from spacy.lang.en.stop_words import STOP_WORDS

# Helpful scripts defined in text_analysis.py.
from text_analysis import spacy_tokenizer, get_topics, get_words

# Commonly used functions and variables.
parser = English()
stopwords = list(STOP_WORDS)
punctuations = string.punctuation

# Personal authorization files.
keys = dill.load(open('.secrets/api-keys.pkd', 'rb'))
auth = tweepy.OAuthHandler(keys['API'], keys['API secret'])

class ScrapeTweets():
    '''
    Used as a simplified interface to grab several aspects about a Twitter user. For example,
    one could obtain the users info, recent tweets, followers, etc.

    Keyword Arguments
    auth: 
    '''
    def __init__(self, auth, username):
        self.api = tweepy.API(auth, 
            wait_on_rate_limit=True, 
            wait_on_rate_limit_notify=True)
        self.username = username

    def get_posts(self, pages=300):
        tweets = []
        for page in tweepy.Cursor(self.api.user_timeline, q=self.username, tweet_mode='extended').pages(pages):
            tweets = tweets + page

        return tweets

    def get_followers(self):
        followers = []
        for page in tweepy.Cursor(self.api.followers, screen_name=self.username).pages(pages):
            followers.extend(page)
        
        return followers

class Tweets():
    def __init__(self, tweets):
        self.tweets = tweets

    def process_tweets_into_df(self, columns=['full_text', 'created_at']):
        tweet_info = {column: [] for column in columns}
        for tweet in self.tweets:
            for column in columns:
                tweet_info[column].append(tweet._json[column])

        self.df = pd.DataFrame(tweet_info)

        return self

    def clean_column(self, column='full_text'):
        tqdm.pandas()
        self.df["processed_text"] = self.df[column].progress_apply(spacy_tokenizer)
        return self

    def search_for_text(self, word):
        tweet_matches = []
        word_pattern = re.compile('(\s|#){}\s'.format(word))
        for tweet in self.tweets:
            tweet_text = tweet.full_text
            if re.match(word_pattern, tweet_text.lower()):
                tweet_matches.append(tweet_text)
        return tweet_matches

    def generate_lda_graph(self, n_components=10, save_as=None):
        tf, tf_vectorizer, tfidf, tfidf_vectorizer = get_words(self.df.processed_text.dropna().values)
        lda, nmf = get_topics(tf, tfidf, n_components)
        pyLDAvis.enable_notebook()
        dash = pyLDAvis.sklearn.prepare(lda, tf, tf_vectorizer, mds='tsne')
        if save_as:
            pyLDAvis.save_html(dash, save_as)
        return dash
