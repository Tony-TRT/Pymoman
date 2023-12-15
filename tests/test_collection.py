import unittest

from packages.logic.collection import Collection
from packages.logic.movie import Movie


class NameChecker(unittest.TestCase):

    def test_valid_name(self):
        collection = Collection(name="My collection")
        self.assertEqual(collection.name, "My collection")

    def test_filter_special_characters(self):
        collection = Collection(name="My: /collection\\")
        self.assertEqual(collection.name, "My collection")

    def test_empty_name_raises_value_error(self):
        with self.assertRaises(ValueError):
            Collection(name="")

    def test_name_with_only_spaces_raises_value_error(self):
        with self.assertRaises(ValueError):
            Collection(name="   ")

    def test_name_with_only_special_characters_raises_value_error(self):
        with self.assertRaises(ValueError):
            Collection(name="%$€")

    def test_too_long_name_raises_value_error(self):
        name = 'a' * 30
        with self.assertRaises(ValueError):
            Collection(name=name)


class MovieListChecker(unittest.TestCase):

    def setUp(self):
        self.collection = Collection(name="My collection")

    def tearDown(self):
        self.collection.movies.clear()

    def test_default_list(self):
        self.assertEqual(self.collection.movies, [])

    def test_movie_list_argument_is_not_list_object(self):
        collection = Collection(name="My collection", movies=("string_01", "string_02"))
        self.assertEqual(collection.movies, [])

    def test_movie_list_without_movie_object(self):
        collection = Collection(name="My collection", movies=["string_01", "string_02"])
        self.assertEqual(collection.movies, [])

    def test_add_one_movie(self):
        one_movie = Movie(title="Movie", year=2000)
        self.collection.add_movie(one_movie)
        self.assertEqual(len(self.collection.movies), 1)

    def test_add_1000_movies(self):
        for i in range(1000):
            self.collection.add_movie(Movie(title="Movie " + str(i), year=2000))
        self.assertEqual(len(self.collection.movies), 1000)

    def test_add_same_movie(self):
        for _ in range(3):
            self.collection.add_movie(Movie(title="Movie", year=2000))
        self.assertEqual(len(self.collection.movies), 1)

    def test_add_movies_with_same_title_but_different_year(self):
        for i in range(3):
            self.collection.add_movie(Movie(title="Movie", year=2000 + i))
        self.assertEqual(len(self.collection.movies), 3)

    def test_add_not_a_movie(self):
        self.collection.add_movie("string_01")  # type: ignore
        self.collection.add_movie(123)  # type: ignore
        self.assertListEqual(self.collection.movies, [])


class MethodsChecker(unittest.TestCase):

    def setUp(self):
        self.collection = Collection(name="My collection")
        self.movie = Movie(title="Movie", year=2000)
        self.collection.add_movie(self.movie)

    def tearDown(self):
        self.collection.movies.clear()
        self.collection.add_movie(self.movie)

    def test_remove_movie(self):
        self.collection.remove_movie(self.movie)
        self.assertListEqual(self.collection.movies, [])


if __name__ == '__main__':
    unittest.main()
