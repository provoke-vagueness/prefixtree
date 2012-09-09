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

from prefixtree import PrefixDict


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

    def test_reversed(self):
        pd = PrefixDict()
        keys = [''.join(combo) for combo in itertools.product('abc', repeat=3)]
        for key in keys:
            pd[key] = None
        self.assertSequenceEqual(list(reversed(keys)), list(reversed(pd)))

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

    def test_startswith_empty(self):
        pd = PrefixDict()
        pd['a'] = None
        self.assertSequenceEqual([], list(pd.startswith('b')))

    def test_startswith_reversed(self):
        pd = PrefixDict()
        keys = [''.join(combo) for combo in itertools.product('abc', repeat=3)]
        for key in keys:
            pd[key] = None
        subset = [k for k in keys if k.startswith('ab')]
        self.assertSequenceEqual(list(reversed(subset)),
                list(pd.startswith('ab', reverse=True)))

    def test_sort_order(self):
        pd = PrefixDict()
        keys = ['', 'a', 'aa', 'ab', 'b', 'ba']
        for key in reversed(keys):
            pd[key] = None
        self.assertSequenceEqual(keys, list(iter(pd)))

    def test_commonprefix_empty(self):
        pd = PrefixDict(abcd=None)
        self.assertEqual(b'', pd.commonprefix('efgh'))

    def test_commonprefix_half(self):
        pd = PrefixDict(abcd=None)
        self.assertEqual(b'ab', pd.commonprefix('abef'))

    def test_commonprefix_full(self):
        pd = PrefixDict(abcd=None)
        self.assertEqual('abcd', pd.commonprefix('abcd'))

    def test_slice_get_narrow(self):
        pd = PrefixDict()
        keys = [''.join(combo) for combo in itertools.product('abc', repeat=3)]
        for key in reversed(keys):
            pd[key] = key.upper()
        subset = [k.upper() for k in keys if k.startswith('ab')]
        self.assertSequenceEqual(subset, list(pd['ab':'ab']))

    def test_slice_get_wide(self):
        pd = PrefixDict()
        keys = [''.join(combo) for combo in itertools.product('abc', repeat=3)]
        for key in reversed(keys):
            pd[key] = key.upper()
        subset = [k.upper() for k in keys if not k.startswith('c')]
        self.assertSequenceEqual(subset, list(pd['a':'b']))

    def test_slice_get_empty(self):
        pd = PrefixDict()
        keys = [''.join(combo) for combo in itertools.product('abc', repeat=3)]
        for key in reversed(keys):
            pd[key] = key.upper()
        self.assertSequenceEqual([], list(pd['d':'z']))

    def test_slice_get_reverse(self):
        pd = PrefixDict()
        keys = [''.join(combo) for combo in itertools.product('abc', repeat=3)]
        for key in reversed(keys):
            pd[key] = key.upper()
        subset = [k.upper() for k in keys if not k.startswith('c')]
        self.assertSequenceEqual(list(reversed(subset)), list(pd['a':'b':-1]))

    def test_slice_invalid_positive_step(self):
        pd = PrefixDict()
        with self.assertRaises(ValueError):
            pd[::2]

    def test_slice_invalid_negative_step(self):
        pd = PrefixDict()
        with self.assertRaises(ValueError):
            pd[::-2]

    def test_slice_open_start(self):
        pd = PrefixDict()
        keys = [''.join(combo) for combo in itertools.product('abc', repeat=3)]
        for key in reversed(keys):
            pd[key] = key.upper()
        subset = [k.upper() for k in keys if not k.startswith('c')]
        self.assertSequenceEqual(subset, list(pd[:'b']))

    def test_slice_open_end(self):
        pd = PrefixDict()
        keys = [''.join(combo) for combo in itertools.product('abc', repeat=3)]
        for key in reversed(keys):
            pd[key] = key.upper()
        subset = [k.upper() for k in keys if not k.startswith('a')]
        self.assertSequenceEqual(subset, list(pd['b':]))

    def test_slice_del(self):
        pd = PrefixDict()
        keys = [''.join(combo) for combo in itertools.product('abc', repeat=3)]
        for key in keys:
            pd[key] = None
        del pd['ab':'ab']
        for key in keys:
            if not key.startswith('ab'):
                continue
            self.assertNotIn(key, pd)

    def test_slice_del_empty(self):
        pd = PrefixDict()
        keys = [''.join(combo) for combo in itertools.product('abc', repeat=3)]
        for key in keys:
            pd[key] = None
        del pd['e':]
        self.assertSequenceEqual(keys, list(pd))

    def test_slice_set(self):
        pd = PrefixDict()
        keys = [''.join(combo) for combo in itertools.product('abc', repeat=3)]
        for key in reversed(keys):
            pd[key] = key
        newvalues = [k for k in keys if k.startswith('ab')]
        pd['ab':'ab'] = newvalues
        self.assertSequenceEqual(newvalues, list(pd['ab':'ab']))

    def test_slice_set_short(self):
        pd = PrefixDict()
        keys = [''.join(combo) for combo in itertools.product('abc', repeat=3)]
        for key in reversed(keys):
            pd[key] = key
        newvalues = [k for k in keys if k.startswith('ab')]
        with self.assertRaises(ValueError):
            pd['ab':'ab'] = newvalues[:-1]

    def test_slice_set_long(self):
        pd = PrefixDict()
        keys = [''.join(combo) for combo in itertools.product('abc', repeat=3)]
        for key in reversed(keys):
            pd[key] = key
        newvalues = [k for k in keys if k.startswith('ab')]
        pd['ab':'ab'] = newvalues + [None]
        self.assertNotIn(None, pd['ab':'ab'])

    def test_iter_post_del(self):
        pd = PrefixDict(a=0, b=1, c=2)
        del pd['b']
        list(pd)
