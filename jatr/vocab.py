"""日本語教育語彙表（http://jhlee.sakura.ne.jp/JEV.html）による難易度推定"""

import statistics as st
from typing import List, Tuple

import MeCab
import pandas as pd

from jatr.util import abs_path, safety_stat


class Vocab:
    def __init__(self, text: str):
        self.text = text
        self.n_chars = len(self.text)
        self.vocab = self.load_vocab()
        self.morph_list = self.tokenize(self.text)
        self.words = [word for word, _ in self.morph_list]
        self.n_words = len(self.words)
        self.level_list, self.matched_words = self.calc_vocab_level(self.morph_list)
        self.n_matched_words = len(self.matched_words)

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
        """分かち書きにしてリストで返す
        >>> Vocab.split_into_words('物理学は、自然科学の一分野である。')
        ['物理', '学', 'は', '、', '自然', '科学', 'の', '一', '分野', 'で', 'ある', '。', '\\n']
        """
        parser = MeCab.Tagger("-Owakati")
        return parser.parse(text).split(" ")

    @staticmethod
    def tokenize(text: str) -> List[Tuple[str, str]]:
        """形態素への分割とステミング(語形の変化を取り除く)を行う
        日本語教育語彙表はUniDicに基づいているので、UniDicを使う
        >>> Vocab.tokenize('物理学は、自然科学の一分野である。')
        [('物理', '名詞'), ('学', '接尾辞'), ('は', '助詞'), ('、', '補助記号'), ('自然', '名詞'), ('科学', '名詞'), ('の', '助詞'), ('一', '名詞'), ('分野', '名詞'), ('だ', '助動詞'), ('有る', '動詞'), ('。', '補助記号')]
        """

        unidic_path = '/var/lib/mecab/dic/unidic'
        parser = MeCab.Tagger("-d " + unidic_path)
        result: str = parser.parse(text)
        morph_list: List[Tuple[str, str]] = []
        for m in result.splitlines():
            if m == 'EOS':
                continue  # break でも可

            # タブで区切って、表層形と各種情報を得る
            surface, features = m.split('\t')

            feature_list = features.split(',')

            # (原形または表層形, 品詞) のタプルをリストに追加する
            # ipadicとunidicで辞書のフィールドが違うので注意
            morph_list.append((feature_list[7] if feature_list[7] != '*' else surface, feature_list[0]))

        return morph_list

    def calc_vocab_level(self, words: List[Tuple[str, str]]) -> Tuple[List[int], List[str]]:
        """
        >>> v = Vocab('')
        >>> v.calc_vocab_level([('物理', '名詞'), ('学', '接尾辞'), ('は', '助詞'), ('自然', '名詞'), ('科学', '名詞'), ('分野', '名詞')])
        ([4, 3, 4, 3, 3, 3, 4], ['物理', '学', '自然', '科学', '分野'])
        """
        level_list: List[int] = []
        matched_words: List[str] = []
        for word, pos in words:
            matched_level = self.vocab[(self.vocab['標準的な表記'] == word) &
                                       self.vocab['品詞1'].str.contains(pos)]['語彙の難易度'].to_list()
            level_list += matched_level
            if not matched_level == []:
                matched_words.append(word)
        return level_list, matched_words

    def show_metrics(self):
        print('マッチした単語:', ', '.join(self.matched_words))
        print('文字数:', self.n_chars)
        print('単語数:', self.n_words)
        print('マッチした単語数:', self.n_matched_words)
        print('語彙の難易度')
        print('平均値:', self.mean)
        print('最大値:', self.max)
        print('中央値:', self.median)
        print('最頻値:', self.mode)
        print('標準偏差:', self.stdev)
        print('分散:', self.variance)
        print()
