"Trie implementation in pure Python"
import array
from . import _trie

try:
    # python 2.x
    from itertools import chain, imap, repeat, tee
    iord = lambda s: imap(ord, s)
    char = chr
except ImportError:
    # python 3.x
    from itertools import chain, repeat, tee
    iord = iter
    char = lambda o: bytes(chr(o), encoding='latin1')

try:
    from collections import abc
except ImportError:
    import collections as abc

STRING_TYPE = bytes
UNICODE_TYPE = str if str is not bytes else unicode

class Node(_trie.Node):
    "Node object for Trie"

    def __init__(self, path=b''):
        self._path = path

    @property
    def path(self):
        return self._path

    def __reversed__(self):
        #TODO: make the items iterator compatible with a sequence so we can 
        #      place it straight into reversed
        for key, node in reversed([a for a in self.items()]):
            yield key, node


class TrieBase(object):
    "Base class for collection classes implemented using a Trie"

    def __init__(self):
        self._root = Node()
        self._values = 0

    def __iter__(self):
        return self._iter_keys(self._root)

    def __len__(self):
        return self._values

    def __reversed__(self):
        return self._iter_keys(self._root, reverse=True)

    def _delete(self, keys, node):
        try:
            index = next(keys)
            child = node.get(index)
            if child is None:
                raise AttributeError(index)
            leaf = self._delete(keys, child)
            if len(child) == 0:
                del node[index]
            return leaf
        except StopIteration:
            return node

    def _insert(self, keys, node):
        try:
            index = next(keys)
            child = node.get(index)
            if child is None:
                child = Node(node.path + char(index))
                node[index] = child
            return self._insert(keys, child)
        except StopIteration:
            return node

    def _iter(self, node, start=tuple(), stop=tuple(), reverse=False):
        start = chain(start, repeat(-1))
        stop = chain(stop, repeat(256))
        direction = iter if not reverse else reversed
        for node in self._walk(node, start, stop, iterate=direction):
            yield node

    def _iter_keys(self, node, start=tuple(), stop=tuple(), reverse=False):
        for node in self._iter(node, start, stop, reverse):
            if not hasattr(node, 'value'):
                continue
            yield self.restore_key(node.path, node.meta)

    def _iter_values(self, node, start=tuple(), stop=tuple(), reverse=False):
        for node in self._iter(node, start, stop, reverse):
            if not hasattr(node, 'value'):
                continue
            yield node.value

    def _search(self, keys, node, exact=True):
        try:
            index = next(keys)
            child = node.get(index)
            if child is None and exact:
                raise AttributeError(index)
            elif child is None:
                return node
            return self._search(keys, child, exact)
        except StopIteration:
            return node

    def _walk(self, root, start, stop, lower=-1, upper=256, iterate=iter):
        current = ord(root.path[-1:]) if len(root.path) > 0 else -1
        if not lower <= current <= upper:
            raise StopIteration
        yield root
        lower = next(start)
        upper = next(stop)
        #TODO: is root supposed to change size during this iteration?
        for key, child in list(iterate(root)): 
            for descendant in self._walk(child, start, stop,
                                        lower, upper, iterate):
                yield descendant

    def prepare_key(self, key):
        """Prepare key for use by Trie.

        Encodes unicode strings to byte strings. If key is not a byte or
        unicode string, raises ValueError.
        """
        encoded = False
        if isinstance(key, UNICODE_TYPE):
            encoded = True
            key = key.encode('UTF-8')
        if isinstance(key, STRING_TYPE):
            return key, encoded
        else:
            raise TypeError("key must be string or bytes")

    def restore_key(self, key, encoded):
        """Restores key to user supplied state.

        Decodes key if the key was originally provided as a unicode string.
        """
        return key.decode('UTF-8') if encoded else key

    def commonprefix(self, key, restore_key=True):
        "Return longest common prefix between key and current keys."
        path, _ = self.prepare_key(key)
        node = self._search(iord(path), self._root, exact=False)
        if hasattr(node, 'value') and restore_key:
            return self.restore_key(node.path, node.meta)
        return node.path

    def startswith(self, base, reverse=False):
        "Iterate over all keys with matching prefix."
        path, _ = self.prepare_key(base)
        start, stop = tee(iord(path))
        return self._iter_keys(self._root, start, stop, reverse)
