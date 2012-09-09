"Prefix tree base dictionary object"
from __future__ import absolute_import
import itertools

try:
    # python 3.3+
    from collections import abc
except ImportError:
    # python 3.2 
    import collections as abc

from prefixtree.trie import TrieBase, iord


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
            path, _ = self.prepare_key(key)
            leaf = self._delete(iord(path), self._root)
            del leaf.value, leaf.meta
            self._values -= 1
        except AttributeError:
            raise KeyError(key)

    def __getitem__(self, key):
        if not isinstance(key, slice):
            try:
                path, _ = self.prepare_key(key)
                leaf = self._search(iord(path), self._root)
                return leaf.value
            except AttributeError:
                raise KeyError(key)
        else:
            if key.step is None or key.step == 1:
                reverse = False
            elif key.step == -1:
                reverse = True
            else:
                raise ValueError("slice step must be 1, -1 or None")
            start = iord(self.prepare_key(key.start)[0])
            stop = iord(self.prepare_key(key.stop)[0])
            return self._iter_values(self._root, start, stop, reverse)

    def __setitem__(self, key, value):
        path, meta = self.prepare_key(key)
        leaf = self._insert(iord(path), self._root)
        if not hasattr(leaf, 'value'):
            self._values += 1
        leaf.value = value
        leaf.meta = meta


class PrefixSet(TrieBase, abc.MutableSet):
    "Set object using prefix trie"

    def __init__(self, *args):
        TrieBase.__init__(self)
        if len(args) > 1:
            msg = "{0} expected at most 1 arguments, got 2"
            raise TypeError(msg.format(self.__class__.__name__))
        if len(args) == 1:
            if isinstance(args[0], abc.Sequence):
                for key in args[0]:
                    self.add(key)
            else:
                msg = "{0} object is not iterable"
                raise TypeError(msg.format(args[0].__class__.__name__))

    def __contains__(self, key):
        try:
            path, _ = self.prepare_key(key)
            leaf = self._search(iord(path), self._root)
            if hasattr(leaf, 'value'):
                return True
        except AttributeError:
            return False

    def add(self, key):
        path, meta = self.prepare_key(key)
        leaf = self._insert(iord(path), self._root)
        if not hasattr(leaf, 'value'):
            self._values += 1
        leaf.value = None
        leaf.meta = meta

    def discard(self, key):
        try:
            path, _ = self.prepare_key(key)
            leaf = self._delete(iord(path), self._root)
            del leaf.value, leaf.meta
            self._values -= 1
        except AttributeError:
            pass
