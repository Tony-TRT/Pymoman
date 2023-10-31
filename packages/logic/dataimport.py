"""
This module only contains code used to organize data collected from the internet
"""

import json
from pathlib import Path

from .movie import Movie

BASE_DIR = Path(__file__).resolve().parent.parent.parent


def load_actors_list() -> list[str]:
    """Retrieves all actors from data.json files

    Returns:
        list[str]: actors names
    """

    root = Path.joinpath(BASE_DIR, 'cache')
    full_list = set()

    for file_path in root.glob('**/data.json'):
        try:
            with open(file_path, 'r', encoding="UTF-8") as data_file:
                content = json.load(data_file)
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

    root = Path.joinpath(BASE_DIR, 'collections')
    full_list = []

    for file_path in root.glob('**/*.json'):
        try:
            with open(file_path, 'r', encoding="UTF-8") as data_file:
                content = json.load(data_file)
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
