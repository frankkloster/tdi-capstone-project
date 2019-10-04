# Used for text processing
import re
import string

# To load saved data.
import dill

# Pandas for data processing.
import pandas as pd

# Use pyLDAvis for visualization of LDA topic analysis.
import pyLDAvis.sklearn

# Tweepy, to access the Twitter API.
import tweepy

# Scikit-Learn for machine learning techniques, such as vectorizing and
# LDA for topic analysis.
from sklearn.decomposition import NMF, LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

# spaCy for language processing.
from spacy.lang.en import Englishy
from spacy.lang.en.stop_words import STOP_WORDS

from tqdm import tqdm

# Helpful scripts defined in text_analysis.py.
from text_analysis import get_topics, get_words, spacy_tokenizer

# Commonly used functions and variables.
parser = English()
stopwords = list(STOP_WORDS)
punctuations = string.punctuation

# Personal authorization files.
keys = dill.load(open('.secrets/api-keys.pkd', 'rb'))
auth = tweepy.OAuthHandler(keys['API'], keys['API secret'])

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
        self.df["processed_text"] = self.df[column].progress_apply(
            spacy_tokenizer)
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
        tf, tf_vectorizer, tfidf, tfidf_vectorizer = get_words(
            self.df.processed_text.dropna().values)
        lda, nmf = get_topics(tf, tfidf, n_components)
        pyLDAvis.enable_notebook()
        dash = pyLDAvis.sklearn.prepare(lda, tf, tf_vectorizer, mds='tsne')
        if save_as:
            pyLDAvis.save_html(dash, save_as)
        return dash