<p align="center">
<img src="https://github.com/dobraczka/strawman/raw/main/docs/assets/logo.png" alt="strawman logo", width=200/>
<h2 align="center"> strawman</h2>
</p>


<p align="center">
<a href="https://github.com/dobraczka/strawman/actions/workflows/main.yml"><img alt="Actions Status" src="https://github.com/dobraczka/strawman/actions/workflows/main.yml/badge.svg?branch=main"></a>
<a href='https://strawman.readthedocs.io/en/latest/?badge=latest'><img src='https://readthedocs.org/projects/strawman/badge/?version=latest' alt='Documentation Status' /></a>
<a href="https://codecov.io/gh/dobraczka/strawman"><img src="https://codecov.io/gh/dobraczka/strawman/branch/main/graph/badge.svg"/></a>
<a href="https://pypi.org/project/strawman"/><img alt="Stable python versions" src="https://img.shields.io/pypi/pyversions/strawman"></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
</p>

Usage
=====

Create a dummy DataFrame:

```python
    >>> from strawman import dummy_df
    >>> dummy_df((5,3))
             0    1    2
    0  Ass  wEB  jEx
    1  xxD  TtW  Xzs
    2  ITh  mpj  tgy
    3  rgN  ZyW  kzR
    4  FPO  XiY  ARn
```

Or create a triples DataFrame:

```python
    >>> from strawman import dummy_triples
    >>> dummy_triples(5)
      head relation tail
    0   e2     rel0   e1
    1   e1     rel0   e0
    2   e1     rel0   e2
    3   e0     rel0   e2
    4   e1     rel1   e0
```

Installation
============

Via pip:

```bash
pip install strawman
```
