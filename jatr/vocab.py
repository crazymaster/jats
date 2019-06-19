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
        self.len = len(self.text)
        self.vocab = self.load_vocab()
        self.words = self.split_into_words(self.text)
        self.level_list = self.calc_vocab_level(self.words)

        # TODO: 例外処理を関数化する
        try:
            self.max = max(self.level_list)
        except ValueError:
            self.max = math.nan

        try:
            self.mean = st.mean(self.level_list)
        except st.StatisticsError:
            self.mean = math.nan

        try:
            self.median = st.median(self.level_list)
        except st.StatisticsError:
            self.median = math.nan

        try:
            self.mode = st.mode(self.level_list)
        except st.StatisticsError:
            self.mode = math.nan

        try:
            self.stdev = st.stdev(self.level_list)
            self.variance = st.variance(self.level_list)
        except st.StatisticsError:
            self.stdev = math.nan
            self.variance = math.nan

    def load_vocab(self, vocab_path: str = abs_path('../data/goi/goi.csv')) -> pd.DataFrame:
        """日本語教育語彙表を読込み、語彙の難易度の列を数値に変換する"""
        # TODO: 教科書コーパス語彙表(https://pj.ninjal.ac.jp/corpus_center/bccwj/freq-list.html)も使えるようにする
        edu_vocab = pd.read_csv(vocab_path, encoding='shift_jis')
        edu_vocab['語彙の難易度'] = edu_vocab['語彙の難易度'].map(lambda s: s[0]).astype('int')
        return edu_vocab

    def split_into_words(self, text: str) -> List[str]:
        """分かち書きにしてリストで返す"""
        # TODO: ステミング(語形の変化を取り除く)を行う
        m = MeCab.Tagger("-Owakati")
        return m.parse(text).split(" ")

    def calc_vocab_level(self, words: List[str]) -> List[int]:
        level_list: List[int] = []
        for word in words:
            level_list += self.vocab[self.vocab['標準的な表記'] == word]['語彙の難易度'].to_list()
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
