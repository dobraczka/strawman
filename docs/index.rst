The strawman library provides simple dummy objects for fast prototyping and testing.

Usage
=====

Create a dummy DataFrame:

.. code-block:: python

    >>> from strawman import dummy_df
    >>> dummy_df((5,3))
             0    1    2
    0  Ass  wEB  jEx
    1  xxD  TtW  Xzs
    2  ITh  mpj  tgy
    3  rgN  ZyW  kzR
    4  FPO  XiY  ARn

Or create a triples DataFrame:

.. code-block:: python

    >>> from strawman import dummy_triples
    >>> dummy_triples(5)
      head relation tail
    0   e2     rel0   e1
    1   e1     rel0   e0
    2   e1     rel0   e2
    3   e0     rel0   e2
    4   e1     rel1   e0


Installation
============

You can install strawman via pip:

.. code-block:: bash
  
  pip install strawman


.. toctree::
   :maxdepth: 2
   :hidden:
   :caption: Documentation

   Installation <source/installation>
   strawman API <source/apidoc>
