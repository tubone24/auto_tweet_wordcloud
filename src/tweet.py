import os
import tweepy
from utils import remove_emoji

API_KEY = os.environ['API_KEY']
API_SECRET_KEY = os.environ['API_SECRET_KEY']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']
SCREEN_NAME = "@meitante1conan"


class Tweet:
    def __init__(self):
        auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
        auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
        self.api = tweepy.API(auth)

    def get_tweets(self):
        all_tweets = []
        new_tweets = self.api.user_timeline(screen_name=SCREEN_NAME, count=200, include_rts=False, exclude_replies=True)
        all_tweets.extend(new_tweets)
        oldest = all_tweets[-1].id - 1
        while len(new_tweets) > 0:
            print("getting tweets before {}".format(oldest))
            new_tweets = self.api.user_timeline(screen_name=SCREEN_NAME, count=200, max_id=oldest, include_rts=False, exclude_replies=True)
            all_tweets.extend(new_tweets)
            oldest = all_tweets[-1].id - 1
        print("Tweet Num {}".format(len(all_tweets)))
        return [remove_emoji(x.text) for x in all_tweets]

    def get_trends_tokyo(self):
        return [remove_emoji(x["name"]) for x in self.api.trends_place(1118285)[0]["trends"]]
