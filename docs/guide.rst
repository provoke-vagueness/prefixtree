Guide
=====

Introduction
------------

*prefixtree* provides both
:class:`~prefixtree.PrefixDict`,
a :term:`dictionary` like object,
and :class:`~prefixtree.PrefixSet`,
a set like object.
Both are implemented
using `prefix trees`_,
or tries.

Tries
^^^^^

Tries,
also known as `prefix trees`_,
are an ordered tree data structure.
Trie minimise the ammount
of memory required
to store keys if
the keys frequently share
the same prefix.

In addition to
minimising memory,
the keys in tries
are ordered.
This allows prefix tree based
dicts and sets to
support slicing operations.

.. note::

   Memory minimisation is
   an academic property of
   the data structure.
   Comparing a
   pure Python trie to
   an optimised C hash table may
   not demonstrate any
   memory savings.

Keys
^^^^

The keys used in
*prefixtree* collections
must be a :class:`str` or
:class:`bytes` object.
Unicode strings will
be encoded to bytes
before storage and
after retrieval.
Because of this
``'\u2641'`` and
``b'\xe2\x99\x81'`` are
equivalent keys.

Installation
------------

Use `pip`_ to
install *prefixtree* from
`PyPI`_. ::

    $ pip install --use-mirrors filemagic

The ``--use-mirrors``
argument is optional.
However,
it is a good idea to
use this option as
it both reduces the
load on `PyPI`_ as well as
continues to work if
`PyPI`_ is unavailable.

The :mod:`prefixtree` module
should now be
availabe from
the Python shell.

.. doctest::

    >>> import prefixtree

The sections bellow will
describe how to use
:class:`~prefixtree.PrefixDict` and
:class:`~prefixtree.PrefixSet`.

PrefixDict
----------

This dictionary like object,
implemented using a trie,
is an implementation of
the :class:`~collections.abc.MutableMapping`
:mod:`Abstract Base Class<abc>`.
:class:`~prefixtree.PrefixDict` supports
the same construction methods as
the builtin :class:`dict` object.

.. doctest::

    >>> from prefixtree import PrefixDict
    >>> pd = PrefixDict()
    >>> pd['a'] = Ellipsis
    >>> 'a' in pd
    True

The most significant difference between
:class:`~prefixtree.PrefixDict` and
builtin :class:`dict` object is
that :class:`~prefixtree.PrefixDict` supports
using a :class:`slice` when
getting, setting and deleting keys.
When a :class:`slice` is used to
get values an
:term:`iterator` is returned.

.. doctest::

    >>> pd.update([('a', 0), ('b', 1), ('c', 2)])
    >>> list(pd['a':'b'])
    [0, 1]

Unlike slices for
:term:`sequence` objects,
such as :class:`list`
and :class:`tuple`,
slices on :class:`~prefixtree.PrefixDict` are
inclusive of both
the start and
the stop values.
Step values of
1 and -1 are
supported.
Indicating forward and
reverse iteration.

.. doctest::

    >>> list(pd['a':'c':-1])
    [2, 1, 0]

When setting a range
of values using
a slice from
a :class:`~prefixtree.PrefixDict`,
the new values are
iterated over in order,
replacing the current values from
the slice.

.. doctest::

    >>> pd[:'b'] = [3, 4]
    >>> pd['a']
    3
    >>> pd['b']
    4

If there are
fewer new values than
there are values in
the slice an
:class:`ValueError` exception is raised.
The exception i
raised after
updating all
possible values from
the :class:`~prefixtree.PrefixDict`.

.. doctest::

    >>> pd['b':] = [5]
    Traceback (most recent call last):
        ...
    ValueError: Fewer new elements to than slice length
    >>> pd['b']
    5

Deleting slices works
similar to
getting slices.
They are also
inclusive of both
the start and
the stop value.

.. doctest::

    >>> del pd['b':'b']
    >>> 'b' in pd
    False

In addition to
the standard :class:`dict` interface,
a :class:`~prefixtree.PrefixDict` has
the following additional
methods.

* :meth:`~prefixtree.PrefixDict.commonprefix`
* :meth:`~prefixtree.PrefixDict.startswith`

:meth:`~prefixtree.PrefixDict.commonprefix`` returns
the longest common prefix between
the supplied key and
the keys already in
the :class:`~prefixtree.PrefixDict`.

.. doctest::

    >>> pd.commonprefix('aa')
    'a'

:meth:`~prefixtree.PrefixDict.startswith` iterates
over all keys that
begin with
the supplied prefix.

.. doctest::

    >>> pd = PrefixDict(aa=0, ab=1, ac=2)
    >>> list(pd.startswith('a'))
    ['aa', 'ab', 'ac']

Matching keys are
returned in order.
The order can
be reversed by
passing ``True`` for
the ``reverse`` parameter.

PrefixSet
---------

This set like object,
implemented using a trie,
is an implementation of
the :class:`collections.MutableSet`.
:mod:`Abstract Base Class<abc>`.

.. doctest::

    >>> from prefixtree import PrefixSet
    >>> ps = PrefixSet()
    >>> ps.add('abc')
    >>> 'abc' in ps
    True

:class:`~prefixtree.PrefixSet` supports
the same construction methods as
the builtin :class:`set` object.

.. _PyPI: http://pypi.python.org
.. _pip: http://pypi.python.org/pypi/pip
.. _prefix trees: http://en.wikipedia.org/wiki/Trie
