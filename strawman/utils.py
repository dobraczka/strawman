import logging
import string
from typing import List, Optional, Sequence, Union

import numpy as np

logger = logging.getLogger(__name__)


def _init_rng(seed: int = None):
    if seed is None:
        seed = np.random.default_rng().integers(0, 10000)
        logger.debug(f"Selected seed {seed}")
    return np.random.default_rng(seed=seed)


def sequence_choice(seq: Sequence, rng: np.random.Generator = None):
    """Choose an element randomly from the sequence.

    :param seq: sequence to choose from
    :param rng: rng to control randomness

    Example:

    >>> from strawman.utils import sequence_choice
    >>> sequence_choice([1,2,3,4])
    2
    >>> sequence_choice("abcdef")
    'f'
    >>>
    """
    if rng is None:
        rng = _init_rng()
    return seq[rng.integers(0, len(seq))]


def shuffle(
    mylist: List,
    rng: np.random.Generator = None,
) -> List:
    """Return a new shuffled list.

    :param mylist: List to shuffle
    :param rng: rng to control randomness

    Example:

    >>> from strawman.utils import shuffle
    >>> shuffle([1,2,3,4])
    [2, 1, 3, 4]

    """
    if rng is None:
        rng = _init_rng()
    return [mylist[i] for i in rng.permutation(len(mylist))]


def shuffled_overlong(
    mylist: List, length: int, rng: np.random.Generator = None
) -> List:
    """Return a shuffled list which can be longer or shorter (containing the same elements).

    :param mylist: The list from which to choose elements
    :param length: length of output
    :param rng: rng to control randomness

    Example:

    >>> from strawman.utils import shuffled_overlong
    >>> shuffled_overlong([1,2,3,4],length=10)
    [4, 3, 1, 2, 1, 2, 4, 3, 3, 4]
    """
    if rng is None:
        rng = _init_rng()
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
) -> str:
    """Generate random strings from allowed charactes with specified size.

    :param str_size: Size of output string
    :param allowed_chars: chars from which to pick
    :param rng: rng to control randomness

    Example:

    >>> from strawman.utils import random_string_generator
    >>> random_string_generator(10)
    'rhVShtnDZw'
    """
    if rng is None:
        rng = _init_rng()
    return "".join(sequence_choice(allowed_chars, rng) for x in range(str_size))


def split_seq(seq: Sequence, parts: int):
    """Split a sequence into :obj:`parts` (which are not necessarily the same size).

    :param seq: Sequence to split
    :param parts: Number of parts

    Example:

    >>> from strawman.utils import split_seq
    >>> split_seq("abcdefgh",parts=3)
    ['ab', 'cd', 'efgh']
    """
    split_size = len(seq) // parts
    start = 0
    res = []
    for offset_mult in range(1, parts):
        res.append(seq[start : split_size * offset_mult])
        start += split_size
    res.append(seq[split_size * offset_mult :])
    return res


def _coherence_check_non_negative(variable: Optional[Union[int, float]]):
    if variable is not None and variable < 0:
        # https://stackoverflow.com/a/69219928
        var_name = f"{variable=}".partition("=")[0]
        raise ValueError(f"{var_name} must be >= 0 but was {variable}")
