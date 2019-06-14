"""日本語教育語彙表（http://jhlee.sakura.ne.jp/JEV.html）による難易度推定"""

import MeCab
import pandas as pd


def load_vocab(vocab_path: str = '../data/goi/goi.csv'):
    edu_vocab = pd.read_csv(vocab_path, encoding='shift_jis')
    print(edu_vocab)


def parse():
    parser = MeCab.Tagger()


if __name__ == '__main__':
    load_vocab()
