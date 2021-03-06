"""日本語テキスト難易度推定"""

import fileinput
import re
from typing import List

import jatr.vocab as jv


def load_text(txt_path: str):
    with open(txt_path) as t:
        text: str = ''.join([line.strip().replace('「', '').replace('」', '') for line in t])

    return text


def main():
    text: str = ''.join([line.strip().replace('「', '').replace('」', '') for line in fileinput.input()])

    # TODO: 文分割の改良を行う 例: !?への対応
    sentences: List[str] = re.findall(r'[^。]+(?:[。]|$)', text)

    for sentence in sentences:
        v = jv.Vocab(sentence)
        print(sentence)
        v.show_metrics()

    vt = jv.Vocab(text)
    print('文章全体')
    print('文数:', len(sentences))
    print('1文あたりの平均文字数:', vt.n_chars / len(sentences))
    print('1文あたりの平均単語数:', vt.n_words / len(sentences))
    vt.show_metrics()
