"""便利関数"""

import os
import statistics as st

import math


def abs_path(path: str) -> str:
    return os.path.join(os.path.dirname(__file__), path)


def safety_stat(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except st.StatisticsError:
        return math.nan
