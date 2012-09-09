import doctest

try:
    # python 2.x
    import unittest2 as unittest
except ImportError:
    # python 3.x
    import unittest

import prefixtree


class TestPrefixTree(unittest.TestCase):

    def test_has_version(self):
        self.assertTrue(prefixtree.__version__)

    def test_readme(self):
        doctest.testfile('../README.rst')

    def test_has_prefixdict(self):
        self.assertTrue(hasattr(prefixtree, 'PrefixDict'))
