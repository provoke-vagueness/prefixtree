import itertools
import operator
import pickle
import string

try:
    # python 2.x
    import unittest2 as unittest
except ImportError:
    # python 3.x
    import unittest

try:
    # python 2.x
    from itertools import ifilterfalse as filterfalse
except ImportError:
    # python 3.x
    from itertools import filterfalse

from prefixtree import PrefixSet


class TestPrefixSet(unittest.TestCase):

    def insert_search_delete(self, keys):
        pd = PrefixSet()
        for key in keys:
            pd.add(key)
        self.assertEqual(len(pd), len(set(keys)))
        for key in keys:
            self.assertIn(key, pd)
        for key in keys:
            pd.discard(key)
        self.assertEqual(len(pd), 0)
        for key in keys:
            self.assertFalse(key in pd)
        self.assertEqual(len(pd._root), 0)

    def test_zero_length_key(self):
        self.insert_search_delete([''])

    def test_one_byte_key(self):
        self.insert_search_delete(['a'])

    def test_all_bytes_key(self):
        key = ''.join(chr(i) for i in range(256))
        self.insert_search_delete([key])

    def test_every_byte_keys(self):
        keys = [chr(i) for i in range(256)]
        self.insert_search_delete(keys)

    def test_long_key(self):
        self.insert_search_delete([string.printable])

    def test_repeated_key(self):
        self.insert_search_delete(['\xFF', '\xFF'])

    def test_unicode_key(self):
        self.insert_search_delete([b"\xe2\x82\xac".decode("UTF-8")])

    def test_invalid_key(self):
        pd = PrefixSet()
        self.assertRaises(TypeError, operator.setitem, pd, 0)

    def test_init_iterable(self):
        pd = PrefixSet(['a'])
        self.assertIn('a', pd)

    def test_init_two_args(self):
        self.assertRaises(TypeError, PrefixSet, [], None)

    def test_init_invalid(self):
        self.assertRaises(TypeError, PrefixSet, None)

    def test_iterable(self):
        pd = PrefixSet()
        keys = [''.join(combo) for combo in itertools.product('abc', repeat=3)]
        for key in reversed(keys):
            pd.add(key)
        self.assertSequenceEqual(keys, list(iter(pd)))

    def test_reversed(self):
        pd = PrefixSet()
        keys = [''.join(combo) for combo in itertools.product('abc', repeat=3)]
        for key in keys:
            pd.add(key)
        self.assertSequenceEqual(list(reversed(keys)), list(reversed(pd)))

    def test_pickle(self):
        pd = PrefixSet()
        pd.add('a')
        pickle.dumps(pd, pickle.HIGHEST_PROTOCOL)

    def test_startswith(self):
        pd = PrefixSet()
        keys = [''.join(combo) for combo in itertools.product('abc', repeat=3)]
        for key in reversed(keys):
            pd.add(key)
        subset = [k for k in keys if k.startswith('ab')]
        self.assertSequenceEqual(subset, list(pd.startswith('ab')))

    def test_startswith(self):
        pd = PrefixSet()
        keys = [''.join(combo) for combo in itertools.product('abc', repeat=3)]
        for key in keys:
            pd.add(key)
        subset = [k for k in keys if k.startswith('ab')]
        self.assertSequenceEqual(list(reversed(subset)),
                list(pd.startswith('ab', reverse=True)))

    def test_startswith_empty(self):
        pd = PrefixSet()
        pd.add('a')
        self.assertSequenceEqual([], list(pd.startswith('b')))

    def test_sort_order(self):
        pd = PrefixSet()
        keys = ['', 'a', 'aa', 'ab', 'b', 'ba']
        for key in reversed(keys):
            pd.add(key)
        self.assertSequenceEqual(keys, list(iter(pd)))

    def test_commonprefix_empty(self):
        pd = PrefixSet(['abcd'])
        self.assertEqual(b'', pd.commonprefix('efgh'))

    def test_commonprefix_half(self):
        pd = PrefixSet(['abcd'])
        self.assertEqual(b'ab', pd.commonprefix('abef'))

    def test_commonprefix_full(self):
        pd = PrefixSet(['abcd'])
        self.assertEqual('abcd', pd.commonprefix('abcd'))

    def test_iter_post_el(self):
        pd = PrefixSet(['a', 'b', 'c'])
        pd.remove('b')
        list(pd)
