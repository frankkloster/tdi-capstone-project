import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import NMF, LatentDirichletAllocation 

def get_words(text, n_features=5000):
    '''
    Returns both the tf and tfidf features of a column in a dataframe.

    Keyword Arguments:
    df - Dataframe containing text.
    column - What column to look at.

    Return value:
    tf - A term frequency vectorizer fitted with the text.
    tfidf - A tfidf vectorizer fitted with the text.
    '''

#    text = df[column].dropna().values

    tfidf_vectorizer = TfidfVectorizer(max_df=0.99, min_df=2,
                                   max_features=n_features,
                                   stop_words='english')

    tfidf = tfidf_vectorizer.fit_transform(text)

    tf_vectorizer = CountVectorizer(max_df=0.95, min_df=2,
                                max_features=n_features,
                                stop_words='english')

    tf = tf_vectorizer.fit_transform(text)

    return tf, tf_vectorizer, tfidf, tfidf_vectorizer

def get_topics(tf, tfidf, n_components):
    """
    Given a tf and tfidf, returns an LDA and NMF fit of the text.
    """
    lda = LatentDirichletAllocation(n_components=n_components, max_iter=5,
                                learning_method='online',
                                learning_offset=50.,
                                random_state=0)

    lda.fit(tf)

    nmf = NMF(n_components=n_components, random_state=1,
          alpha=.1, l1_ratio=.5)

    nmf.fit(tfidf)

    return lda, nmf

def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        message = "Topic #%d: " % topic_idx
        message += " ".join([feature_names[i]
                             for i in topic.argsort()[:-n_top_words - 1:-1]])
        print(message)
    print()

def topic_analysis_pipeline(text, n_components=10, n_top_words=10):
    tf, tf_vectorizer, tfidf, tfidf_vectorizer = get_words(text)
    tfidf_feature_names = tfidf_vectorizer.get_feature_names()
    lda, nmf = get_topics(tf, tfidf, n_components)

    print("For LDA:")
    print_top_words(lda, tfidf_feature_names, n_top_words)

    print("For NMA:")
    print_top_words(nmf, tfidf_feature_names, n_top_words)

    return
