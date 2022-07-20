import string
from typing import Optional, Sequence, Union

import numpy as np


def sequence_choice(rng: np.random.Generator, seq: Sequence):
    return seq[rng.integers(0, len(seq))]


def random_string_generator(
    str_size: int,
    allowed_chars: str = string.ascii_letters,
    rng: np.random.Generator = None,
):
    if rng is None:
        rng = np.random.default_rng()
    return "".join(sequence_choice(rng, allowed_chars) for x in range(str_size))


def split_seq(seq: Sequence, parts: int):
    split_size = len(seq) // parts
    start = 0
    res = []
    for offset_mult in range(1, parts):
        res.append(seq[start : split_size * offset_mult])
        start += split_size
    res.append(seq[split_size * offset_mult :])
    return res


def coherence_check_non_negative(variable: Optional[Union[int, float]]):
    if variable is not None and variable < 0:
        # https://stackoverflow.com/a/69219928
        var_name = f"{variable=}".partition("=")[0]
        raise ValueError(f"{var_name} must be >= 0 but was {variable}")
