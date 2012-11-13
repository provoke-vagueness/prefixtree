import sys


"""
Simple prefix tree 


Reference:
    + http://en.wikipedia.org/wiki/Suffix_tree
    + http://en.wikipedia.org/wiki/Trie

[mjdorma@gmail.com]

"""

from prefixtree._trie import Node


def pprint_prefix(prefix, out = sys.stdout):
    """pretty print a prefix tree"""
    def _print_prefix(node, depth, key, forks, out):
        if depth != 0:
            pad = [" "] * (depth * 4)
            for fork in forks:
                pad[fork*4 - 1] = '|'
            pad = "".join(pad)
            out.write("%s\n" % pad)
            out.write("%s-->%s" % (pad, key[-1]))
            if hasattr(node,'value'):
                out.write(" (%s=%s)\n" % ("".join([chr(a) for a in key]), 
                                                    node.value))
            else:
                out.write("\n")
        if len(node) > 1:
            forks = forks + [depth + 1]
        for k, child in node:
            _print_prefix(child, depth + 1, key + [k], forks, out)

    print(" <root> (%s items)" % len(prefix))
    _print_prefix(prefix.root, 0, [], [0], out)


class Prefix:

    def __init__(self):
        self._root = Node()
        self._len = 0

    @property
    def root(self):
        return self._root

    def __str__(self):
        return str(self.root)
    
    def __setitem__(self, i, y):
        """x.__setitem__(i, y) <==> x[i]=y"""
        if i[0] not in self.root:
            self.root[i[0]] = Node()
        leaf = self.root[i[0]]
        for k in i[1:]:
            if k not in leaf:
                leaf[k] = Node()
            leaf = leaf[k]
        if not hasattr(leaf, 'value'):
            self._len += 1
        leaf.value = y

    def find_node(self, p):
        """D.find_node(p) -> Node for the prefix p"""
        try:
            leaf = self.root[p[0]]
            for k in p[1:]:
                leaf = leaf[k]
        except KeyError:
            raise KeyError(p)
        return leaf

    def __getitem__(self, y):
        """x.__getitem__(y) <==> x[y]"""
        leaf = self.find_node(y)
        try:
            v = leaf.value
        except AttributeError:
            raise KeyError(y)
        return v

    def __iter__(self):
        """x.__iter__() <==> iter(x)"""
        return self.itermkeys

    def __contains__(self, k):
        """D.__contains__(k) -> True if D has a key k, else False"""
        try:
            self[k]
        except KeyError:
            return False
        else:
            return True

    def __len__(self):
        """x.__len__() <==> len(x)"""
        return self._len

    def clear(self):
        """D.clear() -> None.  Remove all items from D"""
        sel._len = 0
        self._root = Node()

    def copy(self):
        """D.copy() -> a shallow copy of D"""
        raise NotImplemented()

    def fromkeys(self, s, *v):
        """
        dict.fromkeys(S[,v]) -> New dict with keys from S and values equal to
        v.  v defaults to None.
        """
        p = Prefix()
        val = None
        for i, k in enumerate(s):
            if v:
                val = v[0][i]
            p[k] = val
        return p

    def get(self, k, *d):
        """D.get(k[,d]) -> D[k] if k in D, else d.  d defaults to None."""
        try:
            v = self[k]
        except KeyError:
            if d:
                v = d[0]
            else:
                raise
        return v

    def has_key(self, k):
        """D.has_key(k) -> True if D has a key k, else False"""
        return k in self

    def items(self):
        """D.items() -> list of D's (key, value) pairs, as 2-tuples"""
        return [k for k in self.iteritems()]

    def values(self):
        """D.values() -> list of D's values"""
        return [k for k in self.itervalues()]

    def startswith(self, p):
        """D.startswith(p) -> an iterator over (key, value) where
        key.startwith(p)
        """
        try:
            leaf = self.find_node(p)
        except KeyError:
            return []
        return self.iteritems_from_node(leaf, 
                                        prefix=[ord(a) for a in p])

    def iteritems_from_node(self, node, prefix=[]):
        """D.iteritems_from_node(node) -> an iterator over (key, value) items
        from node
        """
        if hasattr(node, 'value'):
            yield ("".join([chr(a) for a in prefix]), node.value)

        node_stack = [(prefix, iter(node))]
        while True:
            key, node_iter = node_stack[-1]
            try:
                k, child = node_iter.__next__()
                new_key = key + [k]
                if hasattr(child, 'value'):
                    yield ("".join([chr(a) for a in new_key]), child.value)
                node_stack.append((new_key, iter(child)))
            except StopIteration:
                if len(node_stack) == 1:
                    raise StopIteration()
                else:
                    node_stack.pop(-1)
                    continue

    def iteritems(self):
        """D.iteritems() -> an iterator over the (key, value) items of D"""
        return self.iteritems_from_node(self.root)

    def iterkeys(self):
        """D.iterkeys() -> an iterator over the keys of D"""
        for k, _ in self.iteritems():
            yield k

    def itervalues(self):
        """D.itervalues() -> an iterator over the values of D"""
        for _, v in self.iteritems():
            yield v

    def keys(self):
        """D.keys() -> list of D's keys"""
        return [k for k in self.iterkeys()]

    def pop(self, k, *d):
        """
        D.pop(k[,d]) -> v, remove specified key and return the corresponding
        value.  If key is not found, d is returned if given, otherwise KeyError
        is raised
        """
        try:
            leaf = self.find_node(k)
            v = leaf.value
            delattr(leaf, 'value')
            self._len -= 1
        except (KeyError, ValueError, AttributeError) as err:
            if d:
                v = d[0]
            else:
                raise KeyError(k)
        return v

    def popitem(self):
        """
        D.popitem() -> (k, v), remove and return some (key, value) pair as a
        2-tuple; but raise KeyError if D is empty.
        """
        raise NotImplemented()







