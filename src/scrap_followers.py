import dill
import tweepy


def get_followers(api, screen_name, follower_count=360000, save_as=None):
    """
    Scraps a user's followers on Twitter.

    Keyword Arguments:
    api            - The Twitter API, stored in Tweepy format.
    screen_name    - User's screen name.
    follower_count - Number of users to scrap information of.
    save_as        - Save information in Dill format.

    Returns:
    None
    """

    followers = []
    for page in tweepy.Cursor(api.followers, screen_name).pages():
        followers.extend(page)
        if len(followers) >= follower_count:
            break

    if save_as:
        dill.dump(followers, open(save_as, 'wb'))
    else:
        dill.dump(followers, open(
            '../scrapped-data/twitter-data/{}-followers.pkd'.format(screen_name), 'wb'))


if __name__ == '__main__':
    """
    Todo: Allow grabbing a screenname followers via command line argument.
    """
    pass
