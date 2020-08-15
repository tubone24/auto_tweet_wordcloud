import os
from time import sleep
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

    def __limit_handled(self, cursor):
        while True:
            try:
                yield cursor.next()
            except tweepy.RateLimitError:
                sleep(15 * 60)

    def get_tweets(self):
        all_tweets = []
        # new_tweets = self.api.user_timeline(screen_name=SCREEN_NAME, count=200, include_rts=False, exclude_replies=True)
        # all_tweets.extend(new_tweets)
        # oldest = all_tweets[-1].id - 1
        # while len(new_tweets) > 0:
        #     print("getting tweets before {}".format(oldest))
        #     new_tweets = self.api.user_timeline(screen_name=SCREEN_NAME, count=200, max_id=oldest, include_rts=False, exclude_replies=True)
        #     all_tweets.extend(new_tweets)
        #     oldest = all_tweets[-1].id - 1
        # print("Tweet Num {}".format(len(all_tweets)))
        for new_tweet in self.__limit_handled(tweepy.Cursor(self.api.user_timeline, screen_name=SCREEN_NAME, count=200, include_rts=False, exclude_replies=True).items()):
            all_tweets.append(new_tweet)
        print("Tweet Num {}".format(len(all_tweets)))
        return [remove_emoji(x.text) for x in all_tweets]

    def get_trends_tokyo(self):
        return [remove_emoji(x["name"]) for x in self.api.trends_place(1118285)[0]["trends"]]

    def get_followers(self):
        followers = []
        for follower in self.__limit_handled(tweepy.Cursor(self.api.followers).items()):
            followers.append(follower.screen_name)
