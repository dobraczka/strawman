from strawman import dummy_df


def test_dummy_df():
    shape = (10, 3)
    assert dummy_df(shape).shape == shape
