prefixtree
==========

This package implements dictionary and set like objects using `prefix trees`_.

Tries
-----

Tries, also known as `prefix trees`_, are an ordered tree data structure. Using
a tries minimises the ammount of memory required to store keys the keys
frequently share the same prefix.

In addition to minimising memory, tries are ordered. This allows prefix tree
based dicitonaries and sets to support slicing operations.

Status
------

*prefixtree* is still in an early stage of development, the trove classifier
has for development status has been set to "Pre-Alpha". The most significant
feature missing is the support for slices. Currently the only feature expoiting
the trie is the *startswith()* method.

PrefixDict
----------

This dictionary like object, implemented using a trie, is an implementation of
the *MutableMapping* `abstract base class`_. ::

    >>> from prefixtree import PrefixDict
    >>> pd = PrefixDict()
    >>> pd['abc'] = Ellipsis
    >>> 'abc' in pd
    True

*PrefixDict* supports the same construction methods as the builtin *dict*
object.

PrefixSet
---------

This set like object, implemented using a trie, is an implementation of the
*MutableSet* `abstract base class`_. ::

    >>> from prefixtree import PrefixSet
    >>> ps = PrefixSet()
    >>> ps.add('abc')
    >>> 'abc' in pd
    True

*PrefixSet* supports the same construction methods as the builtin *set*
object.

Compatability
-------------

*prefixtree* is implemented to be compatible with Python 2.x and Python 3.x. It
has been tested against the following Python implementations:

* CPython 2.6
* CPython 2.7
* CPython 3.2
* PyPy 1.9.0

|build_status|

Continuous integration testing is provided by `Travis CI`_.

Issues
------

Source code for *prefixtree* is hosted on `GitHub`_. Please file `bug reports`_
with GitHub's issues system.

.. _GitHub: https://github.com/aliles/prefixtree
.. _Travis CI: http://travis-ci.org/
.. _abstract base class: http://docs.python.org/py3k/library/collections.html#abcs-abstract-base-classes
.. _bug reports: https://github.com/aliles/prefixtree/issues
.. _prefix trees: http://en.wikipedia.org/wiki/Trie

.. |build_status| image:: https://secure.travis-ci.org/aliles/prefixtree.png?branch=master
   :target: http://travis-ci.org/#!/aliles/prefixtree
