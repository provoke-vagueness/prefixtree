Introducing prefixtree
======================

*prefixtree* implements
Python :class:`dict` and
:class:`set` like objects using
a `trie`_ or
prefix tree.
Tries are ordered,
tree based data structures.
Using tries adds
unique features to
dict and set like
objects:

* Keys are returned in sorted order.
* Slice operations for getting, setting and deleting values.

Python's builtin :class:`dict` is
implemented using a hash table.
While they are
an excellent,
general purpose container
that have been
heavily optimised.
There are use cases where
tree based containers
are a better solution.

Table of Contents
=================

.. toctree::
   :maxdepth: 2

   overview
   guide
   issues
   api

.. _trie: http://en.wikipedia.org/wiki/Trie
.. _hash table: http://en.wikipedia.org/wiki/Hash_table
