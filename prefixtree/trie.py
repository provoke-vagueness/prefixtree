"Trie implementation in pure Python"
import array
import itertools

try:
    from collections import abc
except ImportError:
    import collections as abc


class Node(abc.MutableMapping):
    "Node object for Trie"

    def __init__(self):
        self._branches = array.array('B', itertools.repeat(0xFF, 256))
        self._children = 0
        self._nodes = []

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
