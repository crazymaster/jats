"""日本語テキスト難易度推定"""

import fileinput
import re
from typing import List

import jatr.vocab as jv


def main():
    text: str = ''.join([line.strip() for line in fileinput.input()])

    # TODO: 文分割の改良を行う 例:「」への対応
    sentences: List[str] = re.findall(r'[^。]+(?:[。]|$)', text)

    vt = jv.Vocab(text)
    print('文章全体')
    print('文数:', len(sentences))
    vt.show_metrics()

    for sentence in sentences:
        v = jv.Vocab(sentence)
        print(sentence)
        v.show_metrics()
