prefixtree
==========

This package provides ``PrefixDict``, a dictionary like object, and
``PrefixSet``, set like object, that are implemented using  using `prefix
trees`_.

|build_status|

Tries
-----

Tries, also known as `prefix trees`_, are an ordered tree data structure. Using
a trie minimises the ammount of memory required to store keys if the keys
frequently share the same prefix.

In addition to minimising memory, tries are ordered. This allows prefix tree
based dicitonaries and sets to support slicing operations.

PrefixDict
----------

This dictionary like object, implemented using a trie, is an implementation of
the ``MutableMapping`` `abstract base class`_.  ``PrefixDict`` supports the
same construction methods as the builtin ``dict`` object. ::

    >>> from prefixtree import PrefixDict
    >>> pd = PrefixDict()
    >>> pd['a'] = Ellipsis
    >>> 'a' in pd
    True

The most significant difference between ``PrefixDict`` and the builtin ``dict``
object is that ``PrefixDict`` supports slices when getting, setting and
deleting keys. The use of slices when getting returns an iterator over
values.  ::

    >>> pd.update([('a', 0), ('b', 1), ('c', 2)])
    >>> list(pd['a':'b'])
    [0, 1]

Observe that, unlike lists and tuples, slices on ``PrefixDict`` are inclusive
of both the start and stop values. Step values of 1 and -1 are supported,
indicating forward and reverse iteration respectively. ::

    >>> list(pd['a':'c':-1])
    [2, 1, 0]

When settings a slice from a ``PrefixDict`` the new values are iterated over in
order, replacing the current value from the slice. ::

    >>> pd[:'b'] = [3, 4]
    >>> pd['a']
    3
    >>> pd['b']
    4

If there are fewer new values than there are values in the slice an exception
will be raised. The exception is raised after updating all possible values from
``PrefixDict``. ::

    >>> pd['b':] = [5]
    Traceback (most recent call last):
        ...
    ValueError: Fewer new elements to than slice length
    >>> pd['b']
    5

Deleting slices works similarily to getting slices. They are also inclusive of
both the start and stop value. ::

    >>> del pd['b':'b']
    >>> 'b' in pd
    False

In addition to the standard ``dict`` API, a ``PrefixDict`` has the following new
methods.

* ``commonprefix(key)``
* ``startswith(key, reverse=False)``

``commonprefix()`` returns the longest common prefix between the supplied key
and the keys already in the ``PrefixDict``. ::

    >>> pd.commonprefix('aa')
    'a'

``startswith()`` iterates over all key that begin with the supplied prefix. ::

    >>> pd = PrefixDict(aa=0, ab=1, ac=2)
    >>> list(pd.startswith('a'))
    ['aa', 'ab', 'ac']

Matching keys are returned in order. The order can be reversed by passing
``True`` for the ``reverse`` parameter.

PrefixSet
---------

This set like object, implemented using a trie, is an implementation of the
``MutableSet`` `abstract base class`_. ::

    >>> from prefixtree import PrefixSet
    >>> ps = PrefixSet()
    >>> ps.add('abc')
    >>> 'abc' in ps
    True

``PrefixSet`` supports the same construction methods as the builtin ``set``
object.

Compatability
-------------

``prefixtree`` is implemented to be compatible with Python 2.x and Python 3.x.
It has been tested against the following Python implementations:

* CPython 2.6
* CPython 2.7
* CPython 3.2
* PyPy 1.9.0

Continuous integration testing is provided by `Travis CI`_.

Issues
------

Source code for ``prefixtree`` is hosted on `GitHub`_. Please file `bug
reports`_ with GitHub's issues system.

.. _GitHub: https://github.com/aliles/prefixtree
.. _Travis CI: http://travis-ci.org/
.. _abstract base class: http://docs.python.org/py3k/library/collections.html#abcs-abstract-base-classes
.. _bug reports: https://github.com/aliles/prefixtree/issues
.. _prefix trees: http://en.wikipedia.org/wiki/Trie

.. |build_status| image:: https://secure.travis-ci.org/aliles/prefixtree.png?branch=master
   :target: http://travis-ci.org/#!/aliles/prefixtree
