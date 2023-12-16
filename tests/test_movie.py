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


if __name__ == '__main__':
    unittest.main()
