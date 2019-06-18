"""日本語テキスト難易度推定"""

import fileinput
import re

import jatr.vocab as jv


def main():
    text = ''.join([line.rstrip() for line in fileinput.input()])
    sentences = re.findall(r'[^。]+(?:[。]|$)', text)

    for sentence in sentences:
        v = jv.Vocab(sentence)
        print(v.sentence)
        print('文長:', v.len)
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
