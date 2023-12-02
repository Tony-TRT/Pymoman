import unittest

from packages.logic.collection import Collection


class CollectionTester(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.testcase = Collection("My collection")
        cls.testcase_complicated_name = Collection("My: /collection\\")

    def test_basic_name(self):
        self.assertEqual(self.testcase.name, "My collection")

    def test_filter_name(self):
        self.assertEqual(self.testcase_complicated_name.name, "My collection")

    def test_empty_name(self):
        self.assertRaises(ValueError, Collection, "")

    def test_only_spaces(self):
        self.assertRaises(ValueError, Collection, "   ")

    def test_only_specials(self):
        self.assertRaises(ValueError, Collection, "%$€#")

    def test_too_long(self):
        self.assertRaises(ValueError, Collection, "An excessively long and relatively boring collection name")

    def test_basic_list(self):
        self.assertEqual(self.testcase.movies, [])


if __name__ == '__main__':
    unittest.main()
