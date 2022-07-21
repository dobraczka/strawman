import pytest
import numpy as np

from strawman.utils import random_string_generator, split_seq, shuffled_overlong

INPUT_SEQ = "abcdefghijklmnopqrstuvwxyz"
INPUT_SEQ2 = list("abcdefghijklmnopqrstuvwxyz")
EXPECTED = ["abcdefgh", "ijklmnop", "qrstuvwxyz"]
EXPECTED2 = [list("abcdefgh"), list("ijklmnop"), list("qrstuvwxyz")]


@pytest.mark.parametrize(
    "input_seq,expected", [(INPUT_SEQ, EXPECTED), (INPUT_SEQ2, EXPECTED2)]
)
def test_split_seq(input_seq, expected):
    assert split_seq(input_seq, 3) == expected


def test_random_string_generator():
    res = random_string_generator(3, allowed_chars=INPUT_SEQ)
    for char in res:
        assert char in INPUT_SEQ


@pytest.mark.parametrize("length", [2,4,10,20])
def test_overlong(length):
    mylist = ["a","b","c","d"]
    res = shuffled_overlong(mylist,length,np.random.default_rng(17))
    assert len(res) == length
    if length >= len(mylist):
        assert set(mylist) == set(res)
