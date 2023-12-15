"""
This module is dedicated to the organization and classification of data.
It provides functions and utilities to parse, structure, and categorize information.
"""

import json
from pathlib import Path
from typing import TYPE_CHECKING

from packages.constants import constants
if TYPE_CHECKING:
    from packages.logic.movie import Movie


def find_movie_files(directory: Path) -> list[Path]:
    """Finds the paths of video files within a directory and its subdirectories.

    Args:
        directory (Path): The path to the main directory from which to search for videos.

    Returns:
        list[Path]: A list containing the paths of video files.
    """

    if directory.exists():
        ok_files = {'.avi', '.flv', '.m4v', '.mkv', '.mov', '.mp4', '.ogg', '.vob', '.wmv'}
        return [file for file in directory.rglob('*') if file.suffix.casefold() in ok_files]
    return []


def load_all_actors() -> list[str]:
    """Retrieves all actors from data.json files.

    Returns:
        list[str]: Actors names.
    """

    full_list: set[str] = set()

    for file_path in constants.PATHS.get('cache').glob('**/data.json'):
        content: dict = load_file_content(file_path)
        actors: list[str] = content.get('actors', [])
        full_list.update(actors)

    return sorted(list(full_list), key=lambda x: str.casefold(x))


def load_all_movies() -> list["Movie"]:
    """Returns a list of Movie objects from all saved collections.

    Returns:
        list[Movie]: Movies.
    """

    full_list = []

    for file_path in constants.PATHS.get('collections').glob('*.json'):
        full_list.extend(load_collection_movies(file_path))
    return full_list


def load_collection_movies(collection_path) -> list["Movie"]:
    """Returns a list of Movie objects from a collection's path.

    Args:
        collection_path: Collection's file's path.

    Returns
        list[Movie]: Collection's movies.
    """

    content: list[dict] = load_file_content(collection_path)

    if not content:
        return []

    movies = [make_movie(
        title=element.get('title'),
        year=element.get('year'),
        path=element.get('path'),
        rating=element.get('rating'))[0] for element in content]
    return [movie for movie in movies if movie]


def load_file_content(input_file) -> dict | list[dict]:
    """Loads a json file and returns its content.

    Args:
        input_file: File's path.

    Returns:
        dict | list[dict]: File's content.
    """

    try:
        with open(input_file, 'r', encoding="UTF-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}


def make_movie(title: str, year: int, path, rating) -> tuple:
    """Creates Movie object in a tuple.

    Args:
        title (str): Movie title.
        year (int): Release year.
        path: File's path if any.
        rating: Personal rating.

    Returns:
        tuple: Tuple containing Movie object or False.
    """

    from packages.logic.movie import Movie
    movie = (False,)

    try:
        movie = (Movie(title=title, year=year, path=path, rating=rating),)
    except ValueError:
        pass

    return movie
