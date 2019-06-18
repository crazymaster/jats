"""日本語テキスト難易度推定"""

import jatr.vocab as jv
import fileinput
import re


def main():
    text = re.split('[。！？!?]', ''.join([line.rstrip() for line in fileinput.input()]))
    print(text)

    for sentence in text:
        v = jv.Vocab(sentence)
        # v = jv.Vocab('李さんは毎日お酒をのんでいます。')
        print(v.sentence)
        print('語彙の難易度')
        print('平均値:', v.mean)
        print('最大値:', v.max)
        print('中央値:', v.median)
        print('最頻値:', v.mode)
        print('標準偏差:', v.stdev)
        print('分散:', v.variance)
        print()


if __name__ == '__main__':
    main()
