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

    if not many_recommendations:
        return
