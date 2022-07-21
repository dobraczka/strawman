import string
from typing import List, Optional, Sequence, Union

import numpy as np


def sequence_choice(seq: Sequence, rng: np.random.Generator):
    """Choose an element randomly from the sequence.

    :param seq: sequence to choose from
    :param rng: rng to control randomness
    """
    return seq[rng.integers(0, len(seq))]


def shuffle(
    mylist: List,
    rng: np.random.Generator,
) -> List:
    """Return a new shuffled list.

    :param mylist: List to shuffle
    :param rng: rng to control randomness
    """
    return [mylist[i] for i in rng.permutation(len(mylist))]


def shuffled_overlong(mylist: List, length: int,rng: np.random.Generator) -> List:
    """Return a shuffled list which can be longer or shorter (containing the same elements).

    :param mylist: The list from which to choose elements
    :param length: length of output
    :param rng: rng to control randomness
    """
    res: List = []
    while len(res) < length:
        for i in rng.permutation(len(mylist)):
            res.append(mylist[i])
            if len(res) == length:
                break
    return res


def random_string_generator(
    str_size: int,
    allowed_chars: str = string.ascii_letters,
    rng: np.random.Generator = None,
):
    if rng is None:
        rng = np.random.default_rng()
    return "".join(sequence_choice(allowed_chars,rng) for x in range(str_size))


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
