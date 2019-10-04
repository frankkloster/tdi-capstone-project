import dill
import tweepy


def scrap_tweets(api, screen_name, tweet_count=3600000, save_as=None):
    """
    Scraps a user's followers on Twitter.

    Keyword Arguments:
    api            - The Twitter API, stored in Tweepy format.
    screen_name    - User's screen name.
    tweet_count    - Number of tweets to scrap information of.
    save_as        - Save information in Dill format.

    Returns:
    None
    """

    tweets = []
    for page in tweepy.Cursor(api.user_timeline, screen_name).pages():
        tweets.extend(page)
        if len(tweets) >= tweet_count:
            break

    if save_as:
        dill.dump(tweets, open(save_as, 'wb'))
    else:
        dill.dump(tweets, open(
            '../scrapped-data/twitter-data/{}-tweets.pkd'.format(screen_name), 'wb'))

if __name__ == '__main__':
    """
    Todo: Allow grabbing a screenname tweets via command line argument.
    """
    pass
