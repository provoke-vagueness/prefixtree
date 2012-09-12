import doctest

try:
    # python 2.x
    import unittest2 as unittest
except ImportError:
    # python 3.x
    import unittest

import prefixtree

PEP386 = r"""^(?P<version>\d+\.\d+)(?P<extraversion>(?:\.\d+)*)(?:(?P<prerel>[abc]|rc)(?P<prerelversion>\d+(?:\.\d+)*))?(?P<postdev>(\.post(?P<post>\d+))?(\.dev(?P<dev>\d+))?)?$"""


class TestPrefixTree(unittest.TestCase):

    def test_valid_version(self):
        if hasattr(self, 'assertRegex'):
            self.assertRegex(prefixtree.__version__, PEP386)
        else:
            self.assertRegexpMatches(prefixtree.__version__, PEP386)

    def test_readme(self):
        doctest.testfile('../README.rst')

    def test_has_prefixdict(self):
        self.assertTrue(hasattr(prefixtree, 'PrefixDict'))
