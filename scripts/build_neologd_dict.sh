#!/usr/bin/env bash
git clone https://github.com/neologd/mecab-ipadic-neologd.git
xz -dkv mecab-ipadic-neologd/seed/*.csv.xz
cat mecab-ipadic-neologd/seed/*.csv > neologd.csv
python src/build_neologd_dict.py
