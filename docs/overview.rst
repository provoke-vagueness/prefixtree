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

.. _Travis CI: http://travis-ci.org/#!/aliles/prefixtree
