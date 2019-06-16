"""日本語テキスト難易度推定"""

if __name__ == '__main__':
    import jatr.vocab as jv

    v = jv.Vocab('李さんは毎日お酒をのんでいます。')
    print('語彙の難易度')
    print('平均値:', v.mean)
    print('最大値:', v.max)
    print('中央値:', v.median)
    print('最瀕値:', v.mode)
    print('標準偏差:', v.stdev)
    print('分散:', v.variance)
