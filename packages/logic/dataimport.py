"""
This module is dedicated to the organization and classification of data.
It provides functions and utilities to parse, structure, and categorize information.
"""

import json

from .movie import Movie
from ..constants import constants


def make_movie(title: str, year: int, path, rating) -> tuple:
    """Creates Movie object in a tuple

    Returns:
        tuple: tuple containing Movie object or False
    """

    movie = (False,)
    try:
        movie = (Movie(title, year, path, rating),)
    except ValueError:
        movie = (False,)
    finally:
        return movie


def load_file_content(input_file):
    """Loads a json file and returns its content
    """

    with open(input_file, 'r', encoding="UTF-8") as file:
        return json.load(file)


def load_all_actors() -> list[str]:
    """Retrieves all actors from data.json files

    Returns:
        list[str]: actors names
    """

    full_list = set()

    for file_path in constants.CACHE.glob('**/data.json'):
        try:
            content = load_file_content(file_path)
            actors = content.get('actors', ['Unknown'])
            full_list.update(actors)
        except json.JSONDecodeError:
            continue

    full_list = list(full_list)
    full_list = sorted(full_list, key=str.casefold)
    return full_list


def load_collection_movies(c_path: str) -> list[Movie]:
    """Returns a list of Movie objects from a collection's path

    Returns
        list[Movie]: movies
    """

    content = load_file_content(c_path)
    mvs = [make_movie(el.get('title'), el.get('year'), el.get('path'), el.get('rating'))[0] for el in content]
    return [mov for mov in mvs if mov]


def load_all_movies() -> list[Movie]:
    """Returns a list of Movie objects from all saved collections

    Returns:
        list[Movie]: movies
    """

    full_list = []

    for file_path in constants.COLLECTION_FILES:
        full_list.extend(load_collection_movies(file_path))
    return full_list
