[![Gitpod ready-to-code](https://img.shields.io/badge/Gitpod-ready--to--code-blue?logo=gitpod)](https://gitpod.io/#https://github.com/tubone24/auto_tweet_wordcloud)

# auto_tweet_wordcloud
[![Generate Word Cloud](https://github.com/tubone24/auto_tweet_wordcloud/workflows/Generate%20Word%20Cloud/badge.svg)](https://github.com/tubone24/auto_tweet_wordcloud/actions)

This repos is auto action which generating a wordcloud made by Twitter.

## Preconditions

Install Python dependencies
```
pip install -r requirements.txt
```

Download neologd Dictionary

```
sh scripts/download_neologd_dict.sh
```

## Usage

```
python src/main.py
```

## Demo

Default

![img](https://raw.githubusercontent.com/tubone24/auto_tweet_wordcloud/master/src/word_cloud_tweet.png)

Default Alpha

![img](https://raw.githubusercontent.com/tubone24/auto_tweet_wordcloud/master/src/word_cloud_tweet_alpha.png)

Man Face in Profile

![img](https://raw.githubusercontent.com/tubone24/auto_tweet_wordcloud/master/src/word_cloud_tweet_face_profile.png)

Man Face in Profile Alpha

![imng](https://raw.githubusercontent.com/tubone24/auto_tweet_wordcloud/master/src/word_cloud_tweet_face_profile_alpha.png)

Twitter Bird

![img](https://raw.githubusercontent.com/tubone24/auto_tweet_wordcloud/master/src/word_cloud_tweet_twitter_bird.png)

Twitter Bird Alpha

![img](https://raw.githubusercontent.com/tubone24/auto_tweet_wordcloud/master/src/word_cloud_tweet_twitter_bird_alpha.png)
