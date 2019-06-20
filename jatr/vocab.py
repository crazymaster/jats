"""日本語教育語彙表（http://jhlee.sakura.ne.jp/JEV.html）による難易度推定"""

import statistics as st
from typing import List

import MeCab
import pandas as pd

from jatr.util import abs_path, safety_stat


class Vocab:
    vocab = pd.DataFrame()

    def __init__(self, text: str):
        self.text = text
        self.len = len(self.text)
        self.load_vocab()
        self.words = self.split_into_words(self.text)
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
    def load_vocab(cls, vocab_path: str = abs_path('../data/goi/goi.csv')):
        """日本語教育語彙表を読込み、語彙の難易度の列を数値に変換する"""
        # TODO: 教科書コーパス語彙表(https://pj.ninjal.ac.jp/corpus_center/bccwj/freq-list.html)も使えるようにする
        cls.vocab = pd.read_csv(vocab_path, encoding='shift_jis')
        cls.vocab['語彙の難易度'] = cls.vocab['語彙の難易度'].map(lambda s: s[0]).astype('int')

    @staticmethod
    def split_into_words(text: str) -> List[str]:
        """分かち書きにしてリストで返す"""
        # TODO: ステミング(語形の変化を取り除く)を行う
        m = MeCab.Tagger("-Owakati")
        return m.parse(text).split(" ")

    @classmethod
    def calc_vocab_level(cls, words: List[str]) -> List[int]:
        level_list: List[int] = []
        for word in words:
            level_list += cls.vocab[cls.vocab['標準的な表記'] == word]['語彙の難易度'].to_list()
        return level_list

    def show_metrics(self):
        print('文字数:', self.len)
        print('語彙の難易度')
        print('平均値:', self.mean)
        print('最大値:', self.max)
        print('中央値:', self.median)
        print('最頻値:', self.mode)
        print('標準偏差:', self.stdev)
        print('分散:', self.variance)
        print()
