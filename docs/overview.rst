Overview
========

Duck Typing
-----------

*prefixtree* provides
two container classes,
:class:`~prefixtree.PrefixDict` and
:class:`~prefixtree.PrefixSet`.
They are implementations of the
:class:`~collections.abc.MutableMapping` and
:class:`~collections.abc.MutableSet`
:mod:`Abstract Base Classes<abc>`.
Any modules that
adhere to the
principle of :term:`duck-typing`
should be able to accept a
:class:`~prefixtree.PrefixtDict` or
:class:`~prefixtree.PrefixSet` in place of
a :class:`dict`
or :class:`set`.

Compatability
-------------

*prefixtree* is implemented
to be compatible with
Python 2.x and Python 3.x.
It has been tested
against the following
Python implementations:

* CPython 2.6
* CPython 2.7
* CPython 3.2
* PyPy 1.9.0

Continuous integration testing
is provided by `Travis CI`_.

Benchmarks
----------

Benchmarks show
that *prefixtree* is
200 times slower than
the builtin :class:`dict` and requires
10 times the memory.

============== ====== ========
Collection     Memory Run Time
============== ====== ========
**dict**       40MB   0.34s
**PrefixDict** 453MB  67s
============== ====== ========

The following script was
used to benchmark the
memory usage and
cpu utilisation of
:class:`~prefixtree.PrefixDict`.

.. literalinclude:: benchmark_trie.py
   :emphasize-lines: 9,14,17

They are compared to
the results for
the following script
testing the builtin :class:`dict`:

.. literalinclude:: benchmark_dict.py
   :emphasize-lines: 12,15

The benchmarks where run using:

* CPython 3.2, 64-bit
* Max OSX 10.7.4
* 2010 Macbook Pro

The benchamrks values were
averaged from three runs of
each benchmark script.

.. _Travis CI: http://travis-ci.org/#!/aliles/prefixtree
