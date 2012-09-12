prefixtree
==========

This package provides ``PrefixDict``, a dictionary like object, and
``PrefixSet``, set like object, that are implemented using using `prefix
trees`_, or tries. Using tries provides the following unique features when
compared to the builtin dict and set objects.

* Keys are returned in sorted order.
* Slice operations for getting, setting and deleting values.

Trie based collections are useful when ordered access to key and values is a
requirement.

Usage
-----

``PrefixDict`` and ``PrefixSet`` behave like the builtin dict and set objects.
They are implementations of the ``MutableMapping`` and ``MutableSet`` `abstract
base classes`. They also support the same constructors as the builtins. ::

    >>> from prefixtree import PrefixDict
    >>> pd = PrefixDict(a=0, b=1)
    >>> pd['c'] = 2
    >>> 'a' in pd
    True
    >>> 'd' in pd
    False

The only incompatible API difference between *prefixtree* collections and the
builtins is that ``PrefixDict`` and ``PrefixSet`` only support strings as keys.
Unicode strings will be encoded to byte strings before and after use.

Unlike the bultins, it's possible to use slices when getting, setting and
deleting values from *prefixtree* collecionts. ::

    >>> list(pd['a':'c'])
    [0, 1, 2]
    >>> pd[:'b'] = [4, 3]
    >>> list(pd['a':'c':-1])
    [2, 3, 4]

``PrefixDict`` also has additional methods not present on builtin ``dicts``.

* ``commonprefix(key)``, to find the longest comment prefix with current keys.
* ``startswith(prefix)``, iterates over current keys with matching prefix.

Refer to the full *prefixtree* documentation on `Read The Docs`_ for details.

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

Source code for ``prefixtree`` is hosted on `GitHub`_. Any bug reports or
feature requests can be made using GitHub's `issues system`_.

|build_status|

Further Reading
---------------

Full documentation for *prefixtree* is hosted by `Read The Docs`_.

.. _GitHub: https://github.com/aliles/prefixtree
.. _Read The Docs: http://prefixtree.readthedocs.org/
.. _Travis CI: http://travis-ci.org/
.. _abstract base classes: http://docs.python.org/py3k/library/collections.html#abcs-abstract-base-classes
.. _issues system: https://github.com/aliles/prefixtree/issues
.. _prefix trees: http://en.wikipedia.org/wiki/Trie

.. |build_status| image:: https://secure.travis-ci.org/aliles/prefixtree.png?branch=master
   :target: http://travis-ci.org/#!/aliles/prefixtree
