import random
import string
from typing import Sequence


def random_string_generator(str_size: int, allowed_chars: str = string.ascii_letters):
    return "".join(random.choice(allowed_chars) for x in range(str_size))


def split_seq(seq: Sequence, parts: int):
    split_size = len(seq) // parts
    start = 0
    res = []
    for offset_mult in range(1, parts):
        res.append(seq[start : split_size * offset_mult])
        start += split_size
    res.append(seq[split_size * offset_mult :])
    return res
