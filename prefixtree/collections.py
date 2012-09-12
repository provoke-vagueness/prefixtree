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

    def _build_slice(self, key):
        if key.start is not None:
            start = iord(self.prepare_key(key.start)[0])
        else:
            start = tuple()

        if key.stop is not None:
            stop = iord(self.prepare_key(key.stop)[0])
        else:
            stop = tuple()

        if key.step is None or key.step == 1:
            reverse = False
        elif key.step == -1:
            reverse = True
        else:
            raise ValueError("slice step must be 1, -1 or None")

        return slice(start, stop, reverse)

    def __delitem__(self, key):
        if not isinstance(key, slice):
            try:
                path, _ = self.prepare_key(key)
                leaf = self._delete(iord(path), self._root)
                del leaf.value, leaf.meta
                self._values -= 1
            except AttributeError:
                raise KeyError(key)
        else:
            cut = self._build_slice(key)
            for node in self._iter(self._root, cut.start, cut.stop, cut.step):
                if not hasattr(node, 'value'):
                    continue
                leaf = self._delete(iord(node.path), self._root)
                del leaf.value, leaf.meta
                self._values -= 1

    def __getitem__(self, key):
        if not isinstance(key, slice):
            try:
                path, _ = self.prepare_key(key)
                leaf = self._search(iord(path), self._root)
                return leaf.value
            except AttributeError:
                raise KeyError(key)
        else:
            cut = self._build_slice(key)
            return self._iter_values(self._root, cut.start, cut.stop, cut.step)

    def __setitem__(self, key, value):
        if not isinstance(key, slice):
            path, meta = self.prepare_key(key)
            leaf = self._insert(iord(path), self._root)
            if not hasattr(leaf, 'value'):
                self._values += 1
            leaf.value = value
            leaf.meta = meta
        else:
            cut = self._build_slice(key)
            values = iter(value)
            for node in self._iter(self._root, cut.start, cut.stop, cut.step):
                if not hasattr(node, 'value'):
                    continue
                try:
                    node.value = next(values)
                except StopIteration:
                    msg = "Fewer new elements to than slice length"
                    raise ValueError(msg)


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
        """Add an element to a set.

        This has no effect if the element is already present.
        """
        path, meta = self.prepare_key(key)
        leaf = self._insert(iord(path), self._root)
        if not hasattr(leaf, 'value'):
            self._values += 1
        leaf.value = None
        leaf.meta = meta

    def discard(self, key):
        """Remove an element from a set if it is a member.

        If the element is not a member, do nothing.
        """
        try:
            path, _ = self.prepare_key(key)
            leaf = self._delete(iord(path), self._root)
            del leaf.value, leaf.meta
            self._values -= 1
        except AttributeError:
            pass
