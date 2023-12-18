"""
This module encapsulates the logic for generating new movie recommendations.
It is designed to operate in the background.
"""

from random import choice
from pathlib import Path
import base64

from packages.constants import constants
from packages.logic.dataimport import load_all_movies
from packages.logic.dataretrieve import MovieScraper
from packages.logic.movie import Movie


SUGGESTED_MOVIES: dict = {
    "Movie 1": [],
    "Movie 2": [],
    "Movie 3": []
}


def update_dict(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if not (isinstance(result, tuple) and len(result) == 3):
            raise ValueError
        for index, key in enumerate(SUGGESTED_MOVIES):
            SUGGESTED_MOVIES[key].append(result[index])
        return result
    return wrapper


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


@update_dict
def collect_trailer_links(movies: tuple[Movie]) -> tuple:
    """Gathers the trailer links for the given input movies.

    Args:
        movies (tuple[Movie]): A tuple containing three Movie objects.

    Returns:
        tuple: A tuple containing three YouTube links for movie trailers.
    """

    links: list = []
    for movie in movies:
        scraper = MovieScraper(movie)
        links.append(scraper.get_youtube_link(year=False))

    return tuple(links)


def film_picker() -> list[Movie]:
    """Selects three random movies from the user's personal collection.
    These randomly chosen movies serve as the basis for obtaining recommendations.

    Returns:
        list[Movie]: A list containing the three selected movies.
    """

    all_movies: list[Movie] = load_all_movies()
    selected_movies: list[Movie] = []

    for _ in range(3):
        try:
            selected_movies.append(choice(all_movies))
        except IndexError:
            return []

    return selected_movies


@update_dict
def generate_image_filename(dictionary: dict) -> tuple:
    """Generates the filenames for movie posters.
    Trailer links and movie title are encoded in the filename using the base64 module for simplification.

    Args:
        dictionary (dict): A dictionary where values are links, and keys associated with these values are Movie objects.

    Returns:
        tuple: A tuple containing filenames for the posters of the three recommended movies.
    """

    separator: str = ':::'

    filenames: list = []
    for link, movie in dictionary.items():
        information: str = movie.title + separator + link
        information_bytes = information.encode('ascii')
        information_base64 = base64.b64encode(information_bytes)
        filenames.append(information_base64)

    return tuple(filenames)


@update_dict
def generate_recommendations(movies: list[Movie]) -> tuple:
    """Generates three Movie objects corresponding to film suggestions for the user using the web scraping module.

    Args:
        movies (list[Movie]): Movies to generate recommendations from.

    Returns:
        tuple: A tuple containing three Movie objects representing recommended films or nothing.
    """

    many_recommendations: set[str] = set()
    for movie in movies:
        scraper = MovieScraper(movie)
        many_recommendations.update(scraper.get_recommendations())

    if len(many_recommendations) < 3:
        return ()

    while len(many_recommendations) > 3:
        many_recommendations.pop()

    dummy_year: int = 2000  # Year is required to create a Movie object.
    # In this specific case, a wrong year is not problematic.

    recommended_movies: list = []
    for recommendation in many_recommendations:
        movie_object: Movie = Movie(title=recommendation, year=dummy_year)
        recommended_movies.append(movie_object)

    return tuple(recommended_movies)


def main() -> None:
    directory = check_folder()
    selected_movies = film_picker()

    if not (directory and selected_movies):
        return

    for file in constants.PATHS.get('recommendations').iterdir():
        file.unlink()  # Removes old recommendations which may have become obsolete.

    recommendations: tuple[Movie] = generate_recommendations(selected_movies)
    links: tuple[str] = collect_trailer_links(recommendations)
    generate_image_filename(dict(zip(links, recommendations)))
