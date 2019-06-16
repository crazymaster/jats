"""便利関数"""

import os


def abs_path(path: str) -> str:
    return os.path.join(os.path.dirname(__file__), path)
