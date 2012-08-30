import unittest

import prefixtree


class TestPrefixTree(unittest.TestCase):

    def test_has_version(self):
        self.assertTrue(prefixtree.__version__)

    def test_has_prefixdict(self):
        self.assertTrue(hasattr(prefixtree, 'PrefixDict'))
