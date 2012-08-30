"Prefix tree base dictionary object"
from __future__ import absolute_import

try:
    from collections import abc
except ImportError:
    import collections as abc

from prefixtree.trie import TrieBase


class PrefixDict(TrieBase, abc.MutableMapping):
    "Dictionary object using prefix trie"

    def __init__(self, *args, **kwargs):
        TrieBase.__init__(self)
        if len(args) > 1:
            msg = "{0} expected at most 1 arguments, got 2"
            raise TypeError(msg.format(self.__class__.__name__))
        if len(args) == 1:
            if isinstance(args[0], abc.Sequence):
                iterable = args[0]
            elif isinstance(args[0], abc.Mapping):
                iterable = args[0].items()
            else:
                msg = "{0} object is not iterable"
                raise TypeError(msg.format(args[0].__class__.__name__))
            for key, value in iterable:
                self[key] = value
        for key, value in kwargs.items():
            self[key] = value

    def __delitem__(self, key):
        try:
            path, encoded = self._make_path(key)
            leaf = self._delete(path, self._root)
            del leaf.value, leaf.encoded
            self._values -= 1
        except AttributeError:
            raise KeyError(key)

    def __getitem__(self, key):
        try:
            path, encoded = self._make_path(key)
            leaf = self._search(path, self._root)
            return leaf.value
        except AttributeError:
            raise KeyError(key)

    def __setitem__(self, key, value):
        path, encoded = self._make_path(key)
        leaf = self._insert(path, self._root)
        if not hasattr(leaf, 'value'):
            self._values += 1
        leaf.value = value
        leaf.encoded = encoded
