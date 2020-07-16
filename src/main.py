# -*- coding: utf-8 -*-
import emoji
import numpy as np
import os
import re
import codecs
from PIL import Image, ImageDraw, ImageFilter
from janome.tokenizer import Tokenizer
from wordcloud import WordCloud
import tweepy

API_KEY = os.environ['API_KEY']
API_SECRET_KEY = os.environ['API_SECRET_KEY']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']
FONT_PATH = "fonts/keifont.ttf"
SCREEN_NAME = "@meitante1conan"


def generate_exclude_list():
    exclude_list = []
    with codecs.open(os.path.join(os.path.dirname(__file__), "stop_words.txt"), "r", "UTF-8") as lines:
        for line in lines:
            exclude_list.append(line.replace("\n", "").replace("\r", ""))
    return exclude_list


def generate_word_cloud(words, filename, alpha=False, mask=False):
    text = ' '.join(words)
    font_path = FONT_PATH

    if mask:
        mask = np.array(Image.open(mask))
    else:
        x, y = np.ogrid[:450, :900]
        mask = ((x - 225) ** 2 / 5 ** 2) + ((y - 450) ** 2 / 10 ** 2) > 40 ** 2
        mask = 255 * mask.astype(int)

    if alpha:
        wordcloud = WordCloud(background_color=None,
                              colormap="viridis",
                              font_path=font_path,
                              mode="RGBA",
                              mask=mask
                              ).generate(text)
        wordcloud.to_file(os.path.join(
            os.path.dirname(__file__), filename))
    else:
        wordcloud = WordCloud(background_color="white",
                              colormap="viridis",
                              font_path=font_path,
                              mask=mask
                              ).generate(text)
        wordcloud.to_file(os.path.join(
            os.path.dirname(__file__), filename))


def get_tweets():
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    all_tweets = []
    new_tweets = api.user_timeline(screen_name=SCREEN_NAME, count=200, include_rts=False, exclude_replies=True)
    all_tweets.extend(new_tweets)
    oldest = all_tweets[-1].id - 1
    while len(new_tweets) > 0:
        print("getting tweets before {}".format(oldest))
        new_tweets = api.user_timeline(screen_name=SCREEN_NAME, count=200, max_id=oldest, include_rts=False, exclude_replies=True)
        all_tweets.extend(new_tweets)
        oldest = all_tweets[-1].id - 1
    return [remove_emoji(x.text) for x in all_tweets]


def get_trends():
    auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    api = tweepy.API(auth)
    return api.trends_available()


def remove_emoji(src_str):
    return ''.join(c for c in src_str if c not in emoji.UNICODE_EMOJI)


def word_count(texts, exclude_list):
    t = Tokenizer()
    words = []
    for text in texts:
        remove_url_text = remove_url(text)
        tokens = t.tokenize(remove_url_text)
        for token in tokens:
            part_of_speech = token.part_of_speech.split(',')[0]
            part_of_speech2 = token.part_of_speech.split(',')[1]
            if part_of_speech in ['名詞']:
                if (part_of_speech2 != "非自立") and (part_of_speech2 != "代名詞") and (part_of_speech2 != "数"):
                    if token.base_form not in exclude_list:
                        print("{}: {} {}".format(token.base_form, part_of_speech, part_of_speech2))
                        words.append(token.base_form)
    return words


def remove_url(text):
    return re.sub(r"(https?|ftp)(:\/\/[-_\.!~*\'()a-zA-Z0-9;\/?:\@&=\+$,%#]+)", "", text)


def overdraw_image():
    im1 = Image.open("mask_photos/head-profile-of-young-male.png")
    im2 = Image.open(os.path.join(os.path.dirname(__file__), "word_cloud_tweet_face_profile_alpha.png")).convert("RGBA")
    im1.paste(im2, (1000, 500), im2)
    im1.save(os.path.join(os.path.dirname(__file__), "word_cloud_tweet_face_profile_overlay.png"), quality=95)


def main():
    tweets = get_tweets()
    exclude_list = generate_exclude_list()
    words = word_count(tweets, exclude_list)
    generate_word_cloud(words, "word_cloud_tweet.png")
    generate_word_cloud(words, "word_cloud_tweet_alpha.png", alpha=True)
    generate_word_cloud(words, "word_cloud_tweet_face_profile.png", mask="mask_photos/head-profile-of-young-male.png")
    generate_word_cloud(words, "word_cloud_tweet_face_profile_alpha.png", alpha=True, mask="mask_photos/head-profile-of-young-male.png")
    generate_word_cloud(words, "word_cloud_tweet_twitter_bird.png", mask="mask_photos/twitter.png")
    generate_word_cloud(words, "word_cloud_tweet_twitter_bird_alpha.png", alpha=True, mask="mask_photos/twitter.png")
    overdraw_image()
    print(get_trends())


if __name__ == '__main__':
    main()
