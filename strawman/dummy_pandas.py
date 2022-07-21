import logging
import random
import string
from typing import List, Optional, Set, Tuple

import numpy as np
import pandas as pd

from .utils import (
    _coherence_check_non_negative,
    _init_rng,
    random_string_generator,
    sequence_choice,
    shuffle,
    shuffled_overlong,
)

TRIPLES_COL = ["head", "relation", "tail"]

logger = logging.getLogger(__name__)


def dummy_df(
    shape: Tuple[int, int],
    content_length: int = 3,
    allowed_chars: str = string.ascii_letters,
    columns: List[str] = None,
    seed: int = None,
) -> pd.DataFrame:
    """Create a dummy DataFrame.

    :param shape: Dimensions of the DataFrame
    :param content_length: length of the strings in the cells
    :param allowed_chars: string containing the allowed chars
    :param columns: columns names
    :param seed: seed for reproducibility
    :return: Randomly generated DataFrame
    :raises ValueError: if length of columns does not match shape

    Example:

    >>> from strawman import dummy_df
    >>> dummy_df((10,3))
             0    1    2
    0  Ass  wEB  jEx
    1  xxD  TtW  Xzs
    2  ITh  mpj  tgy
    3  rgN  ZyW  kzR
    4  FPO  XiY  ARn
    5  gCh  ArF  QlR
    6  AxL  PMg  oMG
    7  cBo  NEN  ljX
    8  mpT  rjh  smJ
    9  lZe  Krw  TRs
    """
    if columns and len(columns) != shape[1]:
        raise ValueError(
            f"Length of columns ({len(columns)}) does not match shape ({shape})!"
        )
    rng = _init_rng(seed=seed)
    df = pd.DataFrame(np.full(shape, np.nan), columns=columns)
    return df.applymap(
        lambda x, content_length, allowed_chars, rng: random_string_generator(
            str_size=content_length, allowed_chars=allowed_chars, rng=rng
        ),
        content_length=content_length,
        allowed_chars=allowed_chars,
        rng=rng,
    )


def _coherence_check(
    length: int,
    num_entities: Optional[int],
    num_rel: Optional[int],
    entity_prefix: str,
    relation_triples: bool,
    columns: Optional[List[str]],
    content_length: int,
    allowed_chars: str,
):
    _coherence_check_non_negative(length)
    _coherence_check_non_negative(num_entities)
    _coherence_check_non_negative(num_rel)
    _coherence_check_non_negative(content_length)
    if num_entities and num_entities > length:
        raise ValueError(
            f"num_entities={num_entities} cannot be larger than length={length}"
        )
    if num_rel and num_rel > length:
        raise ValueError(f"num_rel={num_rel} cannot be larger than length={length}")
    if columns is not None and len(columns) != 3:
        raise ValueError(f"Columns can only be length of 3 but got {columns}")
    if relation_triples:
        if num_entities and num_rel:
            possible_unique = num_entities * num_rel * (num_entities - 1)
            if possible_unique < length:
                raise ValueError(
                    f"Cannot create {length} unique rows with {num_entities} entities and {num_rel} relations"
                )


def _choose_tail(head: str, tail_values: List[str], rng: np.random.Generator):
    tail = sequence_choice(tail_values, rng)
    while head == tail and not len(tail_values) == 1:
        tail = sequence_choice(tail_values, rng)
    return tail


def _choose_rel_tail(
    head: str, rel_values: List[str], tail_values: List[str], rng: np.random.Generator
) -> Tuple[str, str]:
    """Choose relation and tail where tail is not equal to head.

    :param head: head value
    :param rel_values: possible relation values
    :param tail_values: possible tail values
    :param rng: rng to control randomness
    :return: relation, tail
    """
    rel = sequence_choice(rel_values, rng)
    tail = _choose_tail(head=head, tail_values=tail_values, rng=rng)
    return rel, tail


def dummy_triples(
    length: int,
    num_entities: int = None,
    num_rel: int = None,
    entity_prefix: str = "e",
    relation_prefix: str = "rel",
    relation_triples: bool = True,
    entity_ids: List[str] = None,
    relation_ids: List[str] = None,
    columns: List[str] = None,
    content_length: int = 3,
    allowed_chars: str = string.ascii_letters,
    seed: int = None,
) -> pd.DataFrame:
    """Create dummy DataFrame in form of triples.

    The default columns are ["head","relation","tail"].
    Entries in the head column have an :obj:`entity_prefix` ("e" by default),
    with numbers as suffix. This is analagously done for the entries
    in the relation column but with the :obj:`relation_prefix`.

    All entities show up at least once. Self-links (e.g. ["e1", "rel1", "e1"]) are avoided.

    If :obj:`relation_triples` is False, the last column contains randomly generated strings.

    :param length: Length of the DataFrame
    :param num_entities: Number of unique entities
    :param num_rel: Number of unique relations
    :param entity_prefix: Prefix for entity strings
    :param relation_prefix: Prefix for relation strings
    :param relation_triples: If True the last column contains entities, else randomly generated string
    :param entity_ids: Predefined entity ids
    :param relation_ids: Predefined relation ids
    :param columns: Column names ["head","relation","tail"] by default
    :param content_length: Length of randomly generated string
    :param allowed_chars: Allowed characters in randomly generated string
    :param seed: Seed for reproducibility.
    :return: randomly generated triple DataFrame

    Example:

    >>> from strawman import dummy_triples
    >>> df = dummy_triples(10)
    >>> df
          head relation tail
    0   e4     rel1   e0
    1   e3     rel1   e1
    2   e0     rel1   e5
    3   e6     rel2   e3
    4   e6     rel0   e4
    5   e1     rel1   e0
    6   e2     rel1   e0
    7   e5     rel1   e3
    8   e6     rel2   e0
    9   e6     rel0   e2

    Create an attribute triple DataFrame with predefined entities

    >>> dummy_triples(10, entity_ids=set(df["head"]), relation_triples=False)
          head relation tail
    0   e5     rel1  LOR
    1   e6     rel1  rmM
    2   e4     rel2  rmM
    3   e0     rel2  LOR
    4   e1     rel0  rmM
    5   e5     rel2  Mda
    6   e2     rel1  yhf
    7   e3     rel2  ata
    8   e5     rel2  gHk
    9   e5     rel0  rmM

    """
    _coherence_check(
        length=length,
        num_entities=num_entities,
        num_rel=num_rel,
        entity_prefix=entity_prefix,
        relation_triples=relation_triples,
        columns=columns,
        content_length=content_length,
        allowed_chars=allowed_chars,
    )

    if columns is None:
        columns = TRIPLES_COL
    if num_entities is None:
        num_entities = int(length * 0.7)
    if num_rel is None:
        minimum_rel = int(length / (num_entities * num_entities)) + 1
        num_rel = max(minimum_rel, int(num_entities * 0.7))

    if seed is None:
        seed = np.random.default_rng().integers(0, 10000)
        logger.debug(f"Selected seed {seed}")
    rng = np.random.default_rng(seed=seed)
    head_values = (
        [entity_prefix + str(i) for i in range(num_entities)]
        if entity_ids is None
        else entity_ids
    )
    rel_values = (
        [relation_prefix + str(i) for i in range(num_rel)]
        if relation_ids is None
        else relation_ids
    )
    tail_values = (
        head_values
        if relation_triples
        else [
            random_string_generator(str_size=content_length, rng=rng)
            for _ in range(num_entities)
        ]
    )
    rows: Set[Tuple[str, str, str]] = set()
    ensured_all_entities = False
    while len(rows) < length:
        # ensure all entities show up
        if not ensured_all_entities:
            longest = max(len(head_values), len(rel_values))
            for head, rel in zip(
                shuffled_overlong(head_values, longest, rng),
                shuffled_overlong(rel_values, longest, rng),
            ):
                tail = _choose_tail(head=head, tail_values=tail_values, rng=rng)
                rows.add((head, rel, tail))
            ensured_all_entities = True
        else:
            head = sequence_choice(head_values, rng)
            rel, tail = _choose_rel_tail(
                head=head, rel_values=rel_values, tail_values=tail_values, rng=rng
            )
            rows.add((head, rel, tail))
    return pd.DataFrame(rows, columns=columns)
