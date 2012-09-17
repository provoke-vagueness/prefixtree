API
===

.. module:: prefixtree
   :noindex:

Collection classes implemented
using `prefix trees`_.

PrefixDict
----------

.. class:: PrefixDict([arg])

   Implementation of
   :class:`~collections.abc.MutableMapping`
   that conforms to
   the interface of
   :class:`dict`.
   
   A *PrefixDict* has
   some extensions to
   the interface of
   :class:`dict`.

   .. describe:: d[i:j:k]

      Return iterable from
      *i* to *j* in
      the direction *k*.

      If *i* or *j* is
      *None* the slice is
      open ended.
      *k* may be
      -1 or 1.
      If -1 the
      values are returned
      in reverse order.

   .. method:: commonprefix(key)

      Find the
      longest common prefix between
      the key provided
      and the keys in
      the *PrefixDict*.

   .. method:: startswith(prefix)

      Iterate over
      all keys that
      begin with
      the supplied prefix.

PrefixSet
---------

.. class:: PrefixSet([iterable])

   Implementation of
   :class:`~collections.abc.MutableSet`
   that conforms to
   the interface of
   :class:`set`.

.. _prefix trees: http://en.wikipedia.org/wiki/Trie
