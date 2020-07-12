# -*- coding: utf-8 -*-
import emoji
import numpy as np
import os
import re
import codecs
from PIL import Image
from janome.tokenizer import Tokenizer
from requests_oauthlib import OAuth1Session
from wordcloud import WordCloud

API_KEY = os.environ['API_KEY']
API_SECRET_KEY = os.environ['API_SECRET_KEY']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_TOKEN_SECRET = os.environ['ACCESS_TOKEN_SECRET']
FONT_PATH = "fonts/MPLUSRounded1c-Regular.ttf"
SCREEN_NAME = "@meitante1conan"


def generate_exclude_list():
    exclude_list = []
    with codecs.open(os.path.join(os.path.dirname(__file__), "stop_words.txt"), "r", "UTF-8") as lines:
        for line in lines:
            exclude_list.append(line.replace("\n", "").replace("\r", ""))
    return exclude_list


def generate_word_cloud(words, alpha=False, mask=False):
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
            os.path.dirname(__file__), "word_cloud_tweet_alpha.png"))
    else:
        wordcloud = WordCloud(background_color="white",
                              colormap="viridis",
                              font_path=font_path,
                              mask=mask
                              ).generate(text)
        wordcloud.to_file(os.path.join(
            os.path.dirname(__file__), "word_cloud_tweet.png"))


def get_tweets():
    twitter = OAuth1Session(API_KEY, API_SECRET_KEY, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
    params = {
        'count': 200,
        'exclude_replies': True,
        'include_rts': False,
        'screen_name': SCREEN_NAME,
    }
    res = twitter.get(url, params=params)

    if res.status_code == 200:
        tweets = []
        res_body = res.json()
        for line in res_body:
            tweets.append(remove_emoji(line['text']))
    else:
        print("Failed Status Code: {}".format(res.status_code))
        raise res.raise_for_status()
    return tweets


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


def main():
    tweets = get_tweets()
    exclude_list = generate_exclude_list()
    words = word_count(tweets, exclude_list)
    generate_word_cloud(words)
    generate_word_cloud(words, alpha=True)


if __name__ == '__main__':
    main()
