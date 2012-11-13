import unittest

from prefix import Prefix
from prefix import pprint_prefix


class TestPrefixBasics(unittest.TestCase):

    def test_get_set(self):
        """prefix - set and get"""
        prefix = Prefix()
        prefix['dog'] = 4
        prefix['dogma'] = 5
        prefix['dogmatix'] = 6
        prefix['dogfood'] = 6
        prefix['tudo'] = 7
        print ()
        pprint_prefix(prefix)
        self.assertTrue(prefix['dog'] == 4)
        self.assertTrue(prefix['dogma'] == 5)
        self.assertTrue(prefix['dogmatix'] == 6)
        self.assertTrue(prefix['tudo'] == 7)

    def test_contains_len(self):
        """prefix - contains and len"""
        prefix = Prefix()
        prefix['mundo'] = 3
        self.assertTrue('mundo' in prefix)
        self.assertTrue('dogma' not in prefix)
        self.assertTrue(len(prefix) == 1)
        prefix['mundo'] = 4
        self.assertTrue(prefix['mundo'] == 4)
        self.assertTrue(len(prefix) == 1)
        print ()
        pprint_prefix(prefix)

    def test_pop(self):
        """prefix - test pop"""
        prefix = Prefix()
        prefix['amazed'] = 4
        self.assertTrue(prefix.pop('amazed') == 4)
        self.assertTrue(prefix.pop('amazed', 34) == 34)
        self.assertTrue('amazed' not in prefix)
        self.assertTrue(len(prefix) == 0)
        print ()
        pprint_prefix(prefix)

class TestPrefixIters(unittest.TestCase):

    def setUp(self):
        prefix = Prefix()
        prefix['dog'] = 4
        prefix['dogma'] = 5
        prefix['dogmatix'] = 6
        prefix['dogfood'] = 6
        prefix['tudo'] = 7
        prefix['tudobom'] = 8
        self.prefix = prefix

    def test_startswith(self):
        """prefix - startswith prefix iteration"""
        items = [a for a in self.prefix.startswith('dog')]
        self.assertTrue(len(items) == 4)

    def test_iteritems(self):
        """prefix - iteritems prefix iteration"""
        items = [a for a in self.prefix.iteritems()]
        self.assertTrue(len(items) == 6)

    def test_iterkeys(self):
        """prefix - iterkeys prefix iteration"""
        keys = [k for k in self.prefix.iterkeys()]
        self.assertTrue(len(keys) == 6)


if __name__ == "__main__":
    unittest.main()
