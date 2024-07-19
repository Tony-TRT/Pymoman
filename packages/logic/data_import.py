"""
This module is dedicated to the organization and classification of data.
It provides functions and utilities to parse, structure, and categorize information.
"""

import json
from pathlib import Path

from packages.constants import constants


def find_movie_files(directory: Path) -> list[Path]:
    """Finds the paths of video files within a directory and its subdirectories.

    Args:
        directory (Path): The path to the main directory from which to search for videos.

    Returns:
        list[Path]: A list containing the paths of video files.
    """

    if directory.exists():
        ok_files: set = {".avi", ".flv", ".m4v", ".mkv", ".mov", ".mp4", ".ogg", ".vob", ".wmv"}
        return [path for path in directory.rglob("*") if path.suffix.casefold() in ok_files]
    return []


def load_all_actors() -> list[str]:
    """Retrieves all actors from data.json files.

    Returns:
        list[str]: Actors names.
    """

    full_list: set[str] = set()

    for file_path in constants.PATHS["cache"].glob("**/data.json"):
        content: dict = load_file_content(file_path)
        actors: list[str] = content.get("actors", [])
        full_list.update(actors)
    return sorted(full_list, key=lambda x: str.casefold(x))


def load_all_movies() -> list:
    """Returns a list of Movie objects from all saved collections.

    Returns:
        list[Movie]: Movies.
    """

    full_list = []

    for file_path in constants.PATHS["collections"].glob("*.json"):
        full_list.extend(load_collection_movies(file_path))
    return full_list


def load_collection_movies(collection_path) -> list:
    """Returns a list of Movie objects from a collection's path.

    Args:
        collection_path: Collection's file's path.

    Returns
        list[Movie]: Collection's movies.
    """

    content: list[dict] = load_file_content(collection_path)

    if content:
        from packages.logic.movie import Movie
        movies = [Movie.no_errors(data["title"], data["year"], data["path"], data["rating"]) for data in content]
        return [movie for movie in movies if movie]
    return []


def load_file_content(input_file) -> dict | list[dict]:
    """Loads a json file and returns its content.

    Args:
        input_file: File's path.

    Returns:
        dict | list[dict]: File's content.
    """

    try:
        with open(input_file, "r", encoding="UTF-8") as file:
            return json.load(file)

    except (FileNotFoundError, json.JSONDecodeError):
        return {}
