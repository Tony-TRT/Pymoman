"""
This module contains the logic for new movie recommendations.
It is supposed to run in the background.
"""

from random import choice
from pathlib import Path
# from time import sleep

from packages.constants import constants
from packages.logic.dataimport import load_all_movies
from packages.logic.movie import Movie


def check_folder() -> bool:
    folder: Path = constants.PATHS.get("recommendations")
    folder.mkdir(exist_ok=True, parents=True)

    if folder.exists():
        return True
    return False


def film_picker() -> dict:
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
    # sleep(30)

    directory = check_folder()
    selected_movies = film_picker()

    if not (directory and selected_movies):
        return


# Get 3 recommendations for these 3 films, they cannot be identical or already present in a collection.
# Download the posters of these 3 recommendations in the recommendations directory.
# Obtain and organize the trailer links in a json file.
