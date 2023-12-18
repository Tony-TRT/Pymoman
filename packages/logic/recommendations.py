"""
This module contains the logic for new movie recommendations.
It is supposed to run in the background.
"""

from random import choice
from pathlib import Path

from packages.constants import constants
from packages.logic.dataimport import load_all_movies
from packages.logic.dataretrieve import MovieScraper
from packages.logic.movie import Movie


def check_folder() -> bool:
    """Checks that the recommendations directory exists, if not creates it.

    Returns:
        bool: True if it exists, False if not.
    """

    folder: Path = constants.PATHS.get("recommendations")
    folder.mkdir(exist_ok=True, parents=True)

    if folder.exists():
        return True
    return False


def collect_trailer_links(recommendations_dictionary: dict) -> dict:
    """Adds trailer links to movies in the dictionary.

    Args:
        recommendations_dictionary (dict): str keys paired with Movie objects.

    Returns:
        dict: str keys paired with a tuple containing Movie and str objects.
    """

    for key, value in recommendations_dictionary.items():
        scraper = MovieScraper(value)
        recommendations_dictionary[key] = (value, scraper.get_youtube_link(year=False))

    return recommendations_dictionary


def film_picker() -> dict:
    """Chooses three random movies from the user's personal collections.
    These movies will be the ones used to get recommendations.

    Returns:
        dict: The three chosen films each paired with a key.
    """

    all_movies: list[Movie] = load_all_movies()
    lucky_movies: dict = {
        "Movie A": None,
        "Movie B": None,
        "Movie C": None
    }

    for movie in lucky_movies:
        try:
            lucky_movies[movie] = choice(all_movies)
        except IndexError:
            return {}

    return lucky_movies


def str_to_movie(recommendations_dictionary: dict) -> dict:
    """Converts strings into Movie objects.
    This operation is necessary in order to be able to use web scraping module which needs a Movie object.

    Args:
        recommendations_dictionary (dict): str keys paired with str objects.

    Returns:
        dict: str keys paired with Movie objects.
    """

    dummy_year: int = 2000  # Year is required to create a Movie object.
    # In this specific case, a wrong year is not problematic.

    for key, value in recommendations_dictionary.items():
        movie_object: Movie = Movie(title=value, year=dummy_year)
        recommendations_dictionary[key] = movie_object

    return recommendations_dictionary


def main() -> None:
    directory = check_folder()
    selected_movies = film_picker()

    if not (directory and selected_movies):
        return

    for file in constants.PATHS.get('recommendations').iterdir():
        file.unlink()  # Removes old recommendations which may have become obsolete.

    many_recommendations: set[str] = set()
    for movie in selected_movies.values():
        scraper = MovieScraper(movie)
        many_recommendations.update(scraper.get_recommendations())

    if len(many_recommendations) < 3:
        return

    for movie in selected_movies:
        selected_movies[movie] = many_recommendations.pop()

    selected_movies: dict = str_to_movie(selected_movies)
    selected_movies: dict = collect_trailer_links(selected_movies)
