"""日本語教育語彙表（http://jhlee.sakura.ne.jp/JEV.html）による難易度推定"""

import statistics as st
from typing import List

import MeCab
import pandas as pd

from jatr.util import abs_path, safety_stat


class Vocab:
    def __init__(self, text: str):
        self.text = text
        self.n_chars = len(self.text)
        self.vocab = self.load_vocab()
        self.words = self.tokenize(self.text)
        self.n_words = len(self.words)
        self.level_list = self.calc_vocab_level(self.words)

        try:
            self.max = max(self.level_list)
        except ValueError:
            self.max = 0

        self.mean = safety_stat(st.mean, self.level_list)
        self.median = safety_stat(st.median, self.level_list)
        self.mode = safety_stat(st.mode, self.level_list)
        self.stdev = safety_stat(st.stdev, self.level_list)
        self.variance = safety_stat(st.variance, self.level_list)

    @classmethod
    def load_vocab(cls, vocab_path: str = abs_path('../data/goi/goi.csv')) -> pd.DataFrame:
        """日本語教育語彙表を読込み、語彙の難易度の列を数値に変換する"""
        # TODO: 教科書コーパス語彙表(https://pj.ninjal.ac.jp/corpus_center/bccwj/freq-list.html)も使えるようにする
        edu_vocab = pd.read_csv(vocab_path, encoding='shift_jis')
        edu_vocab['語彙の難易度'] = edu_vocab['語彙の難易度'].map(lambda s: s[0]).astype('int')
        return edu_vocab

    @staticmethod
    def split_into_words(text: str) -> List[str]:
        """分かち書きにしてリストで返す"""
        parser = MeCab.Tagger("-Owakati")
        return parser.parse(text).split(" ")

    @staticmethod
    def tokenize(text: str) -> List[str]:
        """形態素への分割とステミング(語形の変化を取り除く)を行う"""
        parser = MeCab.Tagger()
        result: str = parser.parse(text)
        morph_list: List[str] = []
        for m in result.splitlines():
            if m == 'EOS':
                continue  # break でも可

            # タブで区切って、表層形と各種情報を得る
            surface, features = m.split('\t')

            feature_list = features.split(',')

            # 原形または表層形をリストに追加する
            morph_list.append(feature_list[6] if feature_list[6] != '*' else surface)

        return morph_list

    def calc_vocab_level(self, words: List[str]) -> List[int]:
        level_list: List[int] = []
        for word in words:
            level_list += self.vocab[self.vocab['標準的な表記'] == word]['語彙の難易度'].to_list()
        return level_list

    def show_metrics(self):
        print('文字数:', self.n_chars)
        print('単語数:', self.n_words)
        print('語彙の難易度')
        print('平均値:', self.mean)
        print('最大値:', self.max)
        print('中央値:', self.median)
        print('最頻値:', self.mode)
        print('標準偏差:', self.stdev)
        print('分散:', self.variance)
        print()
