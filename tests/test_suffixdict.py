import itertools

try:
    # python 2.x
    import unittest2 as unittest
except ImportError:
    # python 3.x
    import unittest

from prefixtree import PrefixDict


class SuffixDict(PrefixDict):

    def prepare_key(self, key):
        return PrefixDict.prepare_key(self, key[::-1])

    def restore_key(self, path, meta):
        key = PrefixDict.restore_key(self, path, meta)
        return key[::-1]

    def commonsuffix(self, key):
        path = PrefixDict.commonprefix(self, key, restore_key=False)
        return path[::-1]

    endswith = PrefixDict.startswith


class TestSuffixDict(unittest.TestCase):

    def test_commonsuffix_empty(self):
        sd = SuffixDict(abcd=None)
        self.assertEqual(b'', sd.commonsuffix('abc'))

    def test_commonsuffix_half(self):
        sd = SuffixDict(abcd=None)
        self.assertEqual(b'cd', sd.commonsuffix('..cd'))

    def test_commonsuffix_full(self):
        sd = SuffixDict(abcd=None)
        self.assertEqual(b'abcd', sd.commonsuffix('abcd'))

    def test_endswith(self):
        sd = SuffixDict()
        keys = [''.join(combo) for combo in itertools.product('ab', repeat=3)]
        for key in keys:
            sd[key] = None
        subset = [k for k in keys if k.endswith('a')]
        if hasattr(self, 'assertCountEqual'):
            self.assertCountEqual(subset, list(sd.endswith('a')))
        else:
            self.assertSetEqual(set(subset), set(sd.endswith('a')))
