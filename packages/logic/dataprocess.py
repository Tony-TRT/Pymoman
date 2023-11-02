"""
This module is designed for the processing of data obtained from the internet.
"""

from pathlib import Path
from shutil import rmtree

from PIL import Image

from . import dataimport as dti
from ..constants import constants


def modify_raw_poster(poster: Path) -> bool:
    """Prepares movie poster to be displayed

    Args:
        poster (Path): raw file path

    Returns:
        bool: success or failure
    """

    if not poster.exists():
        return False

    movie_poster = Image.open(poster)
    movie_poster_resized = movie_poster.resize((185, 275))
    movie_poster_resized.save(poster)
    return True


def clear_cache():
    """Clear unused cache data
    """

    if not constants.CACHE.exists():
        return

    saved_movies = dti.load_all_movies()
    saved_movies_c_path = [movie.storage for movie in saved_movies]

    for directory in constants.CACHE.iterdir():
        if directory not in saved_movies_c_path:
            rmtree(directory)
