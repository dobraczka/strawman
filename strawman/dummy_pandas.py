import logging
import random
import string
from typing import List, Optional, Set, Tuple

import numpy as np
import pandas as pd

from .utils import (
    coherence_check_non_negative,
    random_string_generator,
    sequence_choice,
)

TRIPLES_COL = ["head", "relation", "tail"]

logger = logging.getLogger(__name__)


def dummy_df(
    size: Tuple[int, int],
    content_length=3,
    allowed_chars: str = string.ascii_letters,
    columns: List[str] = None,
    seed: int = None,
):
    if seed is None:
        seed = np.random.default_rng().integers(0, 10000)
        logger.debug(f"Selected seed {seed}")
    rng = np.random.default_rng(seed=seed)
    df = pd.DataFrame(np.full(size, np.nan), columns=columns)
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
    coherence_check_non_negative(length)
    coherence_check_non_negative(num_entities)
    coherence_check_non_negative(num_rel)
    coherence_check_non_negative(content_length)
    if num_entities and num_entities > length:
        raise ValueError(
            f"num_entities={num_entities} cannot be larger than length={length}"
        )
    if num_rel and num_rel > length:
        raise ValueError(f"num_rel={num_rel} cannot be larger than length={length}")
    if columns is None:
        columns = TRIPLES_COL
    elif len(columns) != 3:
        raise ValueError(f"Columns can only be length of 3 but got {columns}")
    if relation_triples:
        if num_entities and num_rel:
            possible_unique = num_entities * num_rel * num_entities
            if possible_unique < length:
                raise ValueError(
                    f"Cannot create {length} unique rows with {num_entities} entities and {num_rel} relations"
                )


def _choose_rel_tail(
    head: str, rel_values: List[str], tail_values: List[str], rng: np.random.Generator
):
    rel = sequence_choice(rng, rel_values)
    tail = sequence_choice(rng, tail_values)
    while head == tail and not len(tail_values) == 1:
        tail = sequence_choice(rng, tail_values)
    return rel, tail


def dummy_triples(
    length: int,
    num_entities: int = None,
    num_rel: int = None,
    entity_prefix: str = "e",
    relation_triples: bool = True,
    columns: List[str] = None,
    content_length: int = 3,
    allowed_chars: str = string.ascii_letters,
    seed: int = None,
):
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

    if num_entities is None:
        num_entities = int(length * 0.7)
    if num_rel is None:
        minimum_rel = int(length / (num_entities * num_entities)) + 1
        num_rel = max(minimum_rel, num_entities // 2)

    if seed is None:
        seed = np.random.default_rng().integers(0, 10000)
        logger.debug(f"Selected seed {seed}")
    rng = np.random.default_rng(seed=seed)
    head_values = ["e" + str(i) for i in range(num_entities)]
    rel_values = [
        random_string_generator(str_size=content_length, rng=rng)
        for _ in range(num_rel)
    ]
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
            for head in head_values:
                rel, tail = _choose_rel_tail(
                    head=head, rel_values=rel_values, tail_values=tail_values, rng=rng
                )
                rows.add((head, rel, tail))
            ensured_all_entities = True
        else:
            rel, tail = _choose_rel_tail(
                head=head, rel_values=rel_values, tail_values=tail_values, rng=rng
            )
            rows.add((head, rel, tail))
    return pd.DataFrame(rows, columns=columns)
