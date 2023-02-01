from importlib.metadata import version  # pragma: no cover

from .dummy_pandas import dummy_df, dummy_triples

__all__ = ["dummy_df", "dummy_triples"]

__version__ = version(__package__)
