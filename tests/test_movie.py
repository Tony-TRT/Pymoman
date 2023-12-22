import unittest

from packages.logic.movie import Movie


class NameChecker(unittest.TestCase):

    def test_valid_name(self):
        movie = Movie(title="Movie", year=2000)
        self.assertEqual(movie.title, "Movie")

    def test_filter_special_characters(self):
        movie = Movie(title="My: /movie\\", year=2000)
        self.assertEqual(movie.title, "My movie")

    def test_empty_name_raises_value_error(self):
        with self.assertRaises(ValueError):
            Movie(title="", year=2000)

    def test_name_with_only_spaces_raises_value_error(self):
        with self.assertRaises(ValueError):
            Movie(title="   ", year=2000)

    def test_name_with_only_special_characters_raises_value_error(self):
        with self.assertRaises(ValueError):
            Movie(title="%$€", year=2000)

    def test_too_long_name_raises_value_error(self):
        title = 'a' * 65
        with self.assertRaises(ValueError):
            Movie(title=title, year=2000)


class YearChecker(unittest.TestCase):

    def test_too_old_year_raises_value_error(self):
        with self.assertRaises(ValueError):
            Movie(title="Movie", year=1850)

    def test_too_far_year_raises_value_error(self):
        from datetime import datetime
        year = datetime.now().year + 10
        with self.assertRaises(ValueError):
            Movie(title="Movie", year=year)

    def test_year_is_not_int_raises_value_error(self):
        with self.assertRaises(ValueError):
            Movie(title="Movie", year="2000")  # type: ignore


class MethodsChecker(unittest.TestCase):

    def test_aesthetic_rating_is_str(self):
        movie = Movie(title="Movie", year=2000, rating='5')
        self.assertTrue(type(movie.aesthetic_rating) is str)

    def test_aesthetic_rating_default_when_rating_not_specified(self):
        movie = Movie(title="Movie", year=2000)
        self.assertEqual(movie.aesthetic_rating, "☆☆☆☆☆")

    def test_storage_path(self):
        from pathlib import Path
        expected_a: Path = Path.joinpath(Path.home(), '.pymoman', 'cache', 'my_movie')
        expected_b: Path = Path.joinpath(Path.home(), '.pymoman', 'cache', 'best_movie')
        expected_c: Path = Path.joinpath(Path.home(), '.pymoman', 'cache', 'movie_of_the_year')
        movie_a = Movie(title="My Movie", year=2000)
        movie_b = Movie(title="The Best Movie", year=2000)
        movie_c = Movie(title="The Movie of The Year", year=2000)
        self.assertEqual(movie_a.storage, expected_a)
        self.assertEqual(movie_b.storage, expected_b)
        self.assertEqual(movie_c.storage, expected_c)


if __name__ == '__main__':
    unittest.main()
