"""
This module is designed for the processing of data.
"""

import re
from pathlib import Path
from shutil import rmtree, copy

from PIL import Image

from packages.constants import constants
from packages.logic import data_import


def clear_cache() -> None:
    """Clear unused cache data."""

    if not constants.PATHS["cache"].exists():
        return
    saved_movies_cache_paths = [movie.storage for movie in data_import.load_all_movies()]

    for path in constants.PATHS["cache"].iterdir():
        if path not in saved_movies_cache_paths and path.is_dir():
            rmtree(path)


def filter_name(name: str, limit: int = 25) -> str:
    """Filters collection or movie name and raises a ValueError if it is not suitable.

    Args:
        name (str): Name to filter.
        limit (int): Maximal number of characters.

    Returns:
        str: Filtered name.
    """

    forbidden_names: dict = {
        r"^$": "Name cannot be empty.",
        r"^ +$": "Name cannot contain only spaces.",
        r"^\W+$": "Name cannot contain only special characters.",
        f".{{{limit},}}": f"Name cannot exceed {limit} characters."
    }

    for regex, error_message in forbidden_names.items():
        if re.match(regex, name):
            raise ValueError(error_message)

    unwanted_characters: str = '/\\:;"'

    for unwanted_character in unwanted_characters:
        name = name.replace(unwanted_character, "")
    name = name.strip()

    if name:
        return name
    raise ValueError("An unknown error has occurred.")


def modify_raw_poster(poster: Path) -> None:
    """Prepares movie poster to be displayed.

    Args:
        poster (Path): Raw file's path.

    Returns:
        None: None.
    """

    if not poster.exists():
        return

    movie_poster = Image.open(poster)
    movie_poster_resized = movie_poster.resize((185, 275))
    movie_poster_resized.save(poster)


def set_local_poster(file, movie) -> None:
    """Assigns a poster to a movie from a local file.

    Args:
        file: Image file's path.
        movie (Movie): Concerned movie.

    Returns:
        None: None.
    """

    try:
        copy(file, movie.thumb)
    except FileNotFoundError:
        return
    except FileExistsError:
        movie.thumb.unlink()
        set_local_poster(file, movie)

    modify_raw_poster(movie.thumb)
