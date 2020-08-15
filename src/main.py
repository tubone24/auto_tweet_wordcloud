# -*- coding: utf-8 -*-
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from janome.tokenizer import Tokenizer
from wordcloud import WordCloud
import markovify
from utils import generate_exclude_list, remove_emoji, remove_url
from tweet import Tweet
from web import Web

FONT_PATH = "fonts/keifont.ttf"
BASE_URL = "https://blog.tubone-project24.xyz"
WEB_EXCLUDE_LIST = ["tag", "contact", "about", "sitemap", "pages", "rss", "photos", "privacy-policies", "header", "#"]


def generate_word_cloud(words, filename, alpha=False, mask=False):
    text = " ".join(words)
    font_path = FONT_PATH

    if mask == "rect":
        mask = None
    elif mask:
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


def wakati_text(texts):
    t = Tokenizer()
    words = []
    for text in texts:
        remove_url_text = remove_url(text)
        tokens = t.tokenize(remove_url_text)
        for token in tokens:
            words.append(token.base_form)
        words.append("\n")
    wakati_text = " ".join(words)
    return wakati_text


def textMakarov(text):
    sentence = None
    while sentence is None:
        text_model = markovify.NewlineText(text, state_size=3)

        sentence = text_model.make_sentence()

    with open("makarov_learned_data.json", "w") as f:
        f.write(text_model.to_json())

    with open("makarov_text.txt", "w") as f:
        f.write(''.join(sentence.split()))
    return ''.join(sentence.split())


def overdraw_image():
    im1 = Image.open("mask_photos/head-profile-of-young-male.png")
    im2 = Image.open(os.path.join(os.path.dirname(__file__), "word_cloud_tweet_face_profile_alpha.png")).convert("RGBA")
    im1.paste(im2, (1000, 500), im2)
    im1.save(os.path.join(os.path.dirname(__file__), "word_cloud_tweet_face_profile_overlay.png"), quality=95)


def main():
    tw = Tweet()
    tweets = tw.get_tweets()
    exclude_list = generate_exclude_list()
    words = word_count(tweets, exclude_list)
    generate_word_cloud(words, "word_cloud_tweet.png")
    generate_word_cloud(words, "word_cloud_tweet_alpha.png", alpha=True)
    generate_word_cloud(words, "word_cloud_tweet_face_profile.png", mask="mask_photos/head-profile-of-young-male.png")
    generate_word_cloud(words, "word_cloud_tweet_face_profile_alpha.png", alpha=True, mask="mask_photos/head-profile-of-young-male.png")
    generate_word_cloud(words, "word_cloud_tweet_twitter_bird.png", mask="mask_photos/twitter.png")
    generate_word_cloud(words, "word_cloud_tweet_twitter_bird_alpha.png", alpha=True, mask="mask_photos/twitter.png")
    overdraw_image()
    print("makarov: ")
    print(textMakarov(wakati_text(tweets)))
    generate_word_cloud(tw.get_trends_tokyo(), "trend_tokyo.png")
    web = Web(BASE_URL, WEB_EXCLUDE_LIST)
    blog_words = word_count(web.get_text_by_base_url(), exclude_list)
    generate_word_cloud(blog_words, "word_cloud_blog.png", alpha=True, mask="rect")


if __name__ == '__main__':
    main()
