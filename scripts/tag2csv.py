from typing import Dict, List, Any

import pandas as pd
from mojimoji import zen_to_han

path = './data/毎日新聞コーパス/mai2018-utf8.txt'
data: List[Dict[str, Any]] = []

with open(path) as f:
    row = dict()
    for line in f:
        _, tag, value = line.split('＼')
        tag = zen_to_han(tag)
        value = zen_to_han(value, kana=False).rstrip()

        if tag == 'ID' and 'ID' in row:
            data.append(row)
            row = dict()

        if tag not in row:
            row[tag] = value
        else:
            # 区切り文字を';'とする
            row[tag] += ';' + value

mai = pd.DataFrame(data)
mai.to_csv('./data/毎日新聞コーパス/mai2018-utf8.csv', index=False)
