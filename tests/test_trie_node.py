import unittest

from prefixtree import trie


class TestTrieNode(unittest.TestCase):

    def test_set_get(self):
        n = trie.Node()
        n[0] = Ellipsis
        self.assertIs(n[0], Ellipsis)

    def test_set_del(self):
        n = trie.Node()
        n[0] = Ellipsis
        del n[0]
        self.assertIs(n[0], None)

    def test_set_set(self):
        n = trie.Node()
        n[0] = False
        self.assertIs(n[0], False)
        n[0] = True
        self.assertIs(n[0], True)

    def test_contains(self):
        n = trie.Node()
        self.assertFalse(0 in n)
        n[0] = Ellipsis
        self.assertTrue(0 in n)

    def test_iterate(self):
        keys = [(k, Ellipsis) for k in range(128, 256)]
        n = trie.Node()
        for k, v in keys:
            n[k] = v
        self.assertSequenceEqual(list(iter(n)), keys)

    def test_len(self):
        keys = [(k, Ellipsis) for k in range(128, 256)]
        n = trie.Node()
        for k, v in keys:
            n[k] = v
        self.assertEqual(len(n), 128)
