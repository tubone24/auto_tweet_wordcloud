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

    @staticmethod
    def __limit_handled(cursor):
        wait_seconds = 1
        while True:
            try:
                yield cursor.next()
            except tweepy.RateLimitError as e:
                print(e)
                print("wait {} seconds".format(wait_seconds))
                sleep(wait_seconds)
                wait_seconds *= 2  # Retries with Exponential Backoff

    def get_tweets(self):
        all_tweets = []
        try:
            for new_tweet in self.__limit_handled(tweepy.Cursor(self.api.user_timeline, screen_name=SCREEN_NAME, include_rts=False, exclude_replies=True).items()):
                all_tweets.append(new_tweet)
        except RuntimeError as e:  # RuntimeError: generator raised StopIteration
            print(e)
        print("Tweet Num {}".format(len(all_tweets)))
        return [remove_emoji(x.text) for x in all_tweets]

    def get_trends_tokyo(self):
        return [remove_emoji(x["name"]) for x in self.api.trends_place(1118285)[0]["trends"]]

    def get_followers(self, user):
        followers = []
        try:
            for follower in self.__limit_handled(tweepy.Cursor(self.api.followers, user).items()):
                followers.append(follower)
        except RuntimeError as e:  # RuntimeError: generator raised StopIteration
            print(e)
        return followers

    def get_followers_followers_list(self):
        followers_followers_list = []
        my_followers = self.get_followers(SCREEN_NAME)
        followers_followers_list.append([follower.screen_name for follower in my_followers])
        for follower in my_followers:
            print(follower.screen_name)
            if follower.followers_count > 300:
                print("many friends may be a spam: {}".format(follower.friends_count))
                continue
            others_followers = self.get_followers(follower.screen_name)
            followers_followers_list.append([follower.screen_name for follower in others_followers])
        return followers_followers_list
