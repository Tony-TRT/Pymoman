import unittest

from packages.logic.collection import Collection
from packages.logic.movie import Movie


class NameChecker(unittest.TestCase):

    def test_normal_name(self):
        collection = Collection(name="My collection")
        self.assertEqual(collection.name, "My collection")

    def test_filter_name(self):
        collection = Collection(name="My: /collection\\")
        self.assertEqual(collection.name, "My collection")

    def test_empty_name(self):
        self.assertRaises(ValueError, Collection, "")

    def test_only_spaces(self):
        self.assertRaises(ValueError, Collection, "   ")

    def test_only_specials(self):
        self.assertRaises(ValueError, Collection, "%$€")

    def test_too_long(self):
        self.assertRaises(ValueError, Collection, "An excessively long and relatively boring collection name")


class MovieListChecker(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.collection = Collection("My collection")

    def test_default_list(self):
        self.assertEqual(self.collection.movies, [])

    def test_movie_list_is_not_list_object(self):
        collection = Collection(name="My collection", movies=("string_01", "string_02"))
        self.assertEqual(collection.movies, [])

    def test_movie_list_without_movie_object(self):
        collection = Collection(name="My collection", movies=["string_01", "string_02"])
        self.assertEqual(collection.movies, [])

    def test_add_one_movie(self):
        one_movie = Movie(title="Movie", year=2000)
        self.collection.add_movie(one_movie)
        self.assertEqual(len(self.collection.movies), 1)
        self.collection.movies.clear()

    def test_add_1000_movies(self):
        for i in range(1000):
            self.collection.add_movie(Movie(title="Movie " + str(i), year=2000))
        self.assertEqual(len(self.collection.movies), 1000)
        self.collection.movies.clear()


if __name__ == '__main__':
    unittest.main()
