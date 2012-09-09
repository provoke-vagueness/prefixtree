"Trie implementation in pure Python"
import array

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


class Node(abc.MutableMapping):
    "Node object for Trie"

    __slots__ = ('value', 'meta', '_branches', '_children', '_nodes', '_path')

    def __init__(self, path=b''):
        self._branches = array.array('B', repeat(0xFF, 256))
        self._children = 0
        self._nodes = []
        self._path = path

    @property
    def path(self):
        return self._path

    def __contains__(self, key):
        offset = self._branches[key]
        if offset >= len(self._nodes):
            return False
        return self._branches[key] is not None

    def __delitem__(self, key):
        offset = self._branches[key]
        if offset < len(self._nodes):
            self._nodes[offset] = None
            self._children -= 1

    def __getitem__(self, key):
        offset = self._branches[key]
        return self._nodes[offset] if offset < len(self._nodes) else None

    def __iter__(self):
        for key, offset in enumerate(self._branches):
            if offset >= len(self._nodes):
                continue
            yield (key, self._nodes[offset])

    def __len__(self):
        return self._children

    def __setitem__(self, key, node):
        current = self._branches[key]
        if current < len(self._nodes):
            self._nodes[current] = node
        else:
            leaf = len(self._nodes)
            self._nodes.append(node)
            self._branches[key] = leaf
            self._children += 1


class TrieBase(object):

    def __init__(self):
        self._root = Node()
        self._values = 0

    def __iter__(self):
        return self._iter(self._root)

    def __len__(self):
        return self._values

    def _delete(self, keys, node):
        try:
            index = next(keys)
            child = node[index]
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
            child = node[index]
            if child is None:
                child = Node(node.path + char(index))
                node[index] = child
            return self._insert(keys, child)
        except StopIteration:
            return node

    def _iter(self, node, start=tuple(), stop=tuple()):
        start = chain(start, repeat(-1))
        stop = chain(stop, repeat(256))
        for node in self._walk(node, start, stop):
            if not hasattr(node, 'value'):
                continue
            yield self.restore_key(node.path, node.meta)

    def _search(self, keys, node, exact=True):
        try:
            index = next(keys)
            child = node[index]
            if child is None and exact:
                raise AttributeError(index)
            elif child is None:
                return node
            return self._search(keys, child, exact)
        except StopIteration:
            return node

    def _walk(self, root, start, stop, lower=-1, upper=256):
        current = ord(root.path[-1:]) if len(root.path) > 0 else -1
        if not lower <= current <= upper:
            raise StopIteration
        yield root
        lower = next(start)
        upper = next(stop)
        for key, child in root:
            for descendant in self._walk(child, start, stop, lower, upper):
                yield descendant

    def prepare_key(self, key):
        encoded = False
        if isinstance(key, UNICODE_TYPE):
            encoded = True
            key = key.encode('UTF-8')
        if isinstance(key, STRING_TYPE):
            return key, encoded
        else:
            raise TypeError("key must be string or bytes")

    def restore_key(self, key, encoded):
        return key.decode('UTF-8') if encoded else key

    def commonprefix(self, key, restore=True):
        path, _ = self.prepare_key(key)
        node = self._search(iord(path), self._root, exact=False)
        if hasattr(node, 'value') and restore:
            return self.restore_key(node.path, node.meta)
        return node.path

    def startswith(self, base):
        path, _ = self.prepare_key(base)
        start, stop = tee(iord(path))
        return self._iter(self._root, start, stop)
