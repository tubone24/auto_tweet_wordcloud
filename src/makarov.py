from janome.tokenizer import Tokenizer
import markovify
from utils import remove_url


def run_makarov(texts):
    return __textMakarov(__wakati_text(texts))


def __wakati_text(texts):
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


def __textMakarov(text):
    sentence = None
    while sentence is None:
        text_model = markovify.NewlineText(text, state_size=3)

        sentence = text_model.make_sentence()

    with open("makarov_learned_data.json", "w") as f:
        f.write(text_model.to_json())

    with open("makarov_text.txt", "w") as f:
        f.write(''.join(sentence.split()))
    return ''.join(sentence.split())
