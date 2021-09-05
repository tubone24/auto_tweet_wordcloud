# -*- coding: utf-8 -*-
from utils import generate_exclude_list
from tweet import Tweet
from web import Web
from makarov import run_makarov
from wc import WC
from convert_webp import conv_webp

FONT_PATH = "fonts/keifont.ttf"
BASE_URL = "https://blog.tubone-project24.xyz"
WEB_EXCLUDE_LIST = ["tag", "contact", "about", "sitemap", "pages", "rss", "photos", "privacy-policies", "header", "#"]


def main():
#     tw = Tweet()
#     tweets = tw.get_tweets()
#     print("get tweet")
    exclude_list = generate_exclude_list()
#     wordcloud_tweet = WC(tweets, exclude_list)
#     wordcloud_tweet.generate_word_cloud("word_cloud_tweet.png")
#     print("generate tweet cloud")
    # wordcloud_tweet.generate_word_cloud("word_cloud_tweet_alpha.png", alpha=True)
    # wordcloud_tweet.generate_word_cloud("word_cloud_tweet_face_profile.png", mask="mask_photos/head-profile-of-young-male.png")
    # wordcloud_tweet.generate_word_cloud("word_cloud_tweet_face_profile_alpha.png", alpha=True, mask="mask_photos/head-profile-of-young-male.png")
    # wordcloud_tweet.generate_word_cloud("word_cloud_tweet_twitter_bird.png", mask="mask_photos/twitter.png")
    # wordcloud_tweet.generate_word_cloud("word_cloud_tweet_twitter_bird_alpha.png", alpha=True, mask="mask_photos/twitter.png")
    # wordcloud_tweet.overdraw_image()
#     print("makarov: ")
#     print(run_makarov(tweets))
#     wordcloud_trend = WC(tw.get_trends_tokyo(), [])
#     wordcloud_trend.generate_word_cloud("trend_tokyo.png")
    web = Web(BASE_URL, WEB_EXCLUDE_LIST)
    wordcloud_blog_words = WC(web.get_text_by_base_url(), exclude_list)
    wordcloud_blog_words.generate_word_cloud("word_cloud_blog.png", alpha=False, mask="rect")
    wordcloud_blog_words.generate_word_cloud("word_cloud_blog_large.png", alpha=True, mask="rect_large")
    conv_webp("word_cloud_blog.png")
    # print(tw.get_followers_followers_list())


if __name__ == '__main__':
    main()
