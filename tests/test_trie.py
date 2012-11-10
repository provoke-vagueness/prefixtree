import sys

try:
    # python 2.x
    import unittest2 as unittest
except ImportError:
    # python 3.x
    import unittest

from prefixtree import trie
from prefixtree import _trie

class TestCNode(unittest.TestCase):

    def test_parsekey(self):
        n = _trie.Node()
        self.assertRaises(ValueError, n.__setitem__, b'aa', 0)
        self.assertRaises(ValueError, n.__setitem__, 'aa', 0)
        self.assertRaises(ValueError, n.__setitem__, dict(), 0)
        self.assertRaises(ValueError, n.__setitem__, dict(), -1)
        self.assertRaises(ValueError, n.__setitem__, dict(), 256)
        n[b'a'] = 0
        n['a'] = 0
        n[0] = 0
        n[255] = 0

    def test_subscript(self):
        n = _trie.Node()
        n[0] = 0
        self.assertEqual(n[0], 0)
        n[1] = 10
        self.assertEqual(n[1], 10)

    def test_ass_subscript(self):
        n = _trie.Node()
        n[0] = 0
        self.assertEqual(n[0], 0)
        del n[0]
        n[1] = 10
        self.assertEqual(n[1], 10)

    def test_itervalues(self):
        pass

    def test_iterkeys(self):
        pass
    
    def test_iteritems(self):
        pass
    
                        

class TestNode(unittest.TestCase):

    def test_set_get(self):
        n = trie.Node()
        n[0] = Ellipsis
        self.assertIs(n[0], Ellipsis)

    def test_set_del(self):
        n = trie.Node()
        n[0] = Ellipsis
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
        keys = [(chr(k), Ellipsis) for k in range(128, 256)]
        print(keys)
        n = trie.Node()
        for k, v in keys:
            n[k] = v
        self.assertEqual(len(n), 128)

    def test_set_path(self):
        n = trie.Node('a')
        self.assertEqual(n.path, 'a')

    def test_path_readonly(self):
        with self.assertRaises(AttributeError):
            n = trie.Node()
            n.path = 'a'

    @unittest.skipIf(sys.version_info[:2] < (3, 3),
            "slots unsupported before Py 3.3")
    def test_slots(self):
        with self.assertRaises(AttributeError):
            n = trie.Node()
            n.data = None


class TestTrie(unittest.TestCase):

    def test_byte_path(self):
        t = trie.TrieBase()
        path, encoded = t.prepare_key(b'ab')
        self.assertFalse(encoded)
        self.assertSequenceEqual(list(trie.iord(path)), [97, 98])

    def test_unicode_path(self):
        t = trie.TrieBase()
        path, encoded = t.prepare_key(b'ab'.decode('UTF-8'))
        self.assertTrue(encoded)
        self.assertSequenceEqual(list(trie.iord(path)), [97, 98])

    def test_invalid_path(self):
        t = trie.TrieBase()
        self.assertRaises(TypeError, t.prepare_key, 0)

    def test_restore_bytes(self):
        t = trie.TrieBase()
        self.assertEqual(b'ab', t.restore_key(b'ab', False))

    def test_restore_unicode(self):
        t = trie.TrieBase()
        self.assertEqual(b'ab'.decode('UTF-8'), t.restore_key(b'ab', True))
