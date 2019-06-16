"""日本語教育語彙表（http://jhlee.sakura.ne.jp/JEV.html）による難易度推定"""

import statistics as st
from typing import List

import MeCab
import math
import pandas as pd

from jatr.util import abs_path


class Vocab:
    def __init__(self, text: str):
        self.text = text
        self.vocab = self.load_vocab()
        self.words = self.split_into_words(self.text)
        self.level_list = self.calc_vocab_level(self.words)
        self.mean = st.mean(self.level_list)
        self.max = max(self.level_list)
        self.median = st.median(self.level_list)

        try:
            self.mode = st.mode(self.level_list)
        except st.StatisticsError:
            self.mode = math.nan

        try:
            self.stdev = st.stdev(self.level_list)
        except st.StatisticsError:
            self.stdev = math.nan

        try:
            self.variance = st.variance(self.level_list)
        except st.StatisticsError:
            self.variance = math.nan

    def load_vocab(self, vocab_path: str = abs_path('../data/goi/goi.csv')) -> pd.DataFrame:
        """日本語教育語彙表を読込み、語彙の難易度の列を数値に変換する"""
        edu_vocab = pd.read_csv(vocab_path, encoding='shift_jis')
        edu_vocab['語彙の難易度'] = edu_vocab['語彙の難易度'].map(lambda s: s[0]).astype('int')
        return edu_vocab

    def split_into_words(self, text: str) -> List[str]:
        """分かち書きにしてリストで返す"""
        m = MeCab.Tagger("-Owakati")
        return m.parse(text).split(" ")

    def calc_vocab_level(self, words: List[str]) -> List[int]:
        level_list: List[int] = []
        for word in words:
            level_list += self.vocab[self.vocab['標準的な表記'] == word]['語彙の難易度'].to_list()
        return level_list
