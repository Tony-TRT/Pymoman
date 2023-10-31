"""
This module is dedicated to the organization and classification of data.
It provides functions and utilities to parse, structure, and categorize information.
"""

import json

from .movie import Movie
from ..constants import constants


def load_file_content(input_file):
    """Loads a json file and returns its content
    """

    with open(input_file, 'r', encoding="UTF-8") as file:
        return json.load(file)


def load_actors_list() -> list[str]:
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


def load_movies() -> list[Movie]:
    """Retrieves all movies from collections folder

    Returns:
        list[Movie]: movies
    """

    full_list = []

    for file_path in constants.COLLECTIONS.glob('**/*.json'):
        try:
            content = load_file_content(file_path)
            for stored_movie in content:
                mov = Movie(
                    title=stored_movie.get('title'),
                    year=stored_movie.get('year'),
                    path=stored_movie.get('path'),
                    rating=stored_movie.get('rating')
                )
                full_list.append(mov)
        except json.JSONDecodeError:
            continue

    return full_list
