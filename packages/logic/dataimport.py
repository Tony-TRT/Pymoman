"""
This module is dedicated to the organization and classification of data.
It provides functions and utilities to parse, structure, and categorize information.
"""


import json
from glob import glob
from pathlib import Path


from packages.constants import constants
from packages.logic.movie import Movie


def find_movie_files(directory: Path) -> list[Path]:
    """Finds the paths of video files within a directory and its subdirectories.

    Args:
        directory (Path): The path to the main directory from which to search for videos.

    Returns:
        list[Path]: A list containing the paths of video files.
    """

    if directory.exists():
        ok_files = {'.mkv', '.avi', '.mp4', '.flv', '.wmv', '.mov'}
        return [file for file in directory.rglob('*') if file.suffix in ok_files]
    return []


def load_all_actors() -> list[str]:
    """Retrieves all actors from data.json files

    Returns:
        list[str]: actors names
    """

    full_list = set()

    for file_path in constants.PATHS.get('cache').glob('**/data.json'):
        try:
            content = load_file_content(file_path)
            actors = content.get('actors', ['Unknown'])
            full_list.update(actors)
        except json.JSONDecodeError:
            continue

    full_list = list(full_list)
    full_list = sorted(full_list, key=str.casefold)
    return full_list


def load_all_movies() -> list[Movie]:
    """Returns a list of Movie objects from all saved collections

    Returns:
        list[Movie]: movies
    """

    full_list = []

    for file_path in glob(str(Path.joinpath(constants.PATHS.get('collections'), "*.json"))):
        full_list.extend(load_collection_movies(file_path))
    return full_list


def load_collection_movies(c_path: str) -> list[Movie]:
    """Returns a list of Movie objects from a collection's path

    Returns
        list[Movie]: movies
    """

    content = load_file_content(c_path)
    mvs = [make_movie(el.get('title'), el.get('year'), el.get('path'), el.get('rating'))[0] for el in content]
    return [mov for mov in mvs if mov]


def load_file_content(input_file):
    """Loads a json file and returns its content
    """

    with open(input_file, 'r', encoding="UTF-8") as file:
        return json.load(file)


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
