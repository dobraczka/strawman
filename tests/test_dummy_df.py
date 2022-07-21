import pytest

from strawman import dummy_df, dummy_triples
from strawman.dummy_pandas import TRIPLES_COL


def test_dummy_df():
    shape = (10, 3)
    assert dummy_df(shape).shape == shape

    seed = 17
    assert dummy_df(shape, seed=seed).equals(dummy_df(shape, seed=seed))


def test_dummy_df_bad_inputs():
    with pytest.raises(ValueError):
        dummy_df((10, 3), columns=["a", "b", "c", "d"])


@pytest.mark.parametrize("length", [5, 10, 20])
def test_dummy_triples(length):
    prefix = "e"
    num_entities = 5
    trips = dummy_triples(
        length=length,
        num_entities=num_entities,
        num_rel=3,
        entity_prefix=prefix,
        seed=8039,
    )
    columns = trips.columns
    assert list(columns) == TRIPLES_COL
    assert trips.shape == (length, 3)
    # assert no self relations
    assert not trips[columns[0]].eq(columns[2]).any()
    # assert entities start with prefix
    assert trips[columns[0]].str.startswith(prefix).all()
    assert trips[columns[2]].str.startswith(prefix).all()
    # no duplicates
    assert not trips.duplicated().any()
    unique_ents = set(trips[columns[0]]).union(trips[columns[2]])
    assert len(unique_ents) == num_entities

    seed = 17
    assert dummy_triples(length=length, seed=seed).equals(
        dummy_triples(length=length, seed=seed)
    )

    # test attributes
    trips = dummy_triples(length=length, relation_triples=False, columns=columns)
    # assert no overlap between entities and attributes
    assert set(trips[columns[0]]).intersection(trips[columns[2]]) == set()


def test_predefined():
    entity_ids = ["e1", "e2", "e3", "e4"]
    relation_ids = ["rel1", "rel2", "rel3"]
    trips = dummy_triples(10, entity_ids=entity_ids, relation_ids=relation_ids)
    columns = trips.columns
    assert set(trips[columns[0]]) == set(entity_ids)
    assert set(trips[columns[1]]) == set(relation_ids)


def test_dummy_triples_bad_inputs():
    with pytest.raises(ValueError):
        dummy_triples(length=1, num_entities=100, num_rel=2)
    with pytest.raises(ValueError):
        dummy_triples(length=10, num_entities=1, num_rel=20)
    with pytest.raises(ValueError):
        dummy_triples(length=10, num_entities=1, num_rel=2)
    with pytest.raises(ValueError):
        dummy_triples(length=-10, num_entities=1, num_rel=2)
    with pytest.raises(ValueError):
        dummy_triples(length=10, columns=["too", "many", "values", "for", "triples"])
