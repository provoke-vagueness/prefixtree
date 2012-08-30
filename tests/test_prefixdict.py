import itertools
import operator
import pickle
import string
import unittest

try:
    from itertools import filterfalse
except ImportError:
    from itertools import ifilterfalse as filterfalse

from prefixtree.mapping import PrefixDict


class TestPrefixDict(unittest.TestCase):

    def insert_search_delete(self, keys, value=None):
        pd = PrefixDict()
        for key in keys:
            val = key if value is None else value
            pd[key] = val
        self.assertEqual(len(pd), len(set(keys)))
        for key in keys:
            val = key if value is None else value
            self.assertIn(key, pd)
            self.assertEqual(pd[key], val)
        seen = set()
        for key in filterfalse(seen.__contains__, keys):
            seen.add(key)
            del pd[key]
        self.assertEqual(len(pd), 0)
        self.assertRaises(KeyError, operator.delitem, pd, '')
        for key in keys:
            self.assertRaises(KeyError, operator.getitem, pd, key)
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
        pd = PrefixDict()
        self.assertRaises(TypeError, operator.setitem, pd, 0, None)

    def test_init_iterable(self):
        pd = PrefixDict([('a', None)])
        self.assertIn('a', pd)
        self.assertIs(pd['a'], None)

    def test_init_mapping(self):
        pd = PrefixDict({'a': None})
        self.assertIn('a', pd)
        self.assertIs(pd['a'], None)

    def test_init_kwargs(self):
        pd = PrefixDict(a=None)
        self.assertIn('a', pd)
        self.assertIs(pd['a'], None)

    def test_init_two_args(self):
        self.assertRaises(TypeError, PrefixDict, [], None)

    def test_init_invalid(self):
        self.assertRaises(TypeError, PrefixDict, None)

    def test_iterable(self):
        pd = PrefixDict()
        keys = [''.join(combo) for combo in itertools.product('abc', repeat=3)]
        for key in reversed(keys):
            pd[key] = None
        self.assertSequenceEqual(keys, list(iter(pd)))

    def test_pickle(self):
        pd = PrefixDict()
        pd['a'] = None
        pickle.dumps(pd, pickle.HIGHEST_PROTOCOL)

    def test_startswith(self):
        pd = PrefixDict()
        keys = [''.join(combo) for combo in itertools.product('abc', repeat=3)]
        for key in reversed(keys):
            pd[key] = None
        subset = [k for k in keys if k.startswith('ab')]
        self.assertSequenceEqual(subset, list(pd.startswith('ab')))
