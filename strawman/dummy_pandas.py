import string
from typing import List, Tuple

import numpy as np
import pandas as pd

from .utils import random_string_generator, split_seq


def dummy_df(
    size: Tuple[int, int],
    content_length=3,
    allowed_chars: str = string.ascii_letters,
    columns: List[str] = None,
):
    df = pd.DataFrame(np.full(size, np.nan), columns=columns)
    return df.applymap(
        lambda x, content_length, allowed_chars: random_string_generator(
            str_size=content_length, allowed_chars=allowed_chars
        ),
        content_length=content_length,
        allowed_chars=allowed_chars,
    )


def unique_columns_df(
    size: Tuple[int, int],
    content_length=1,
    allowed_chars: str = string.ascii_letters,
    columns: List[str] = None,
):
    if size[0] > len(allowed_chars):
        raise ValueError("Cannot make unique columns with less allowed characters than length of column!")

    df = pd.DataFrame(np.full(size, np.nan), columns=columns)
    return df.applymap(
        lambda x, content_length, allowed_chars: random_string_generator(
            str_size=content_length, allowed_chars=allowed_chars
        ),
        content_length=content_length,
        allowed_chars=allowed_chars,
    )
