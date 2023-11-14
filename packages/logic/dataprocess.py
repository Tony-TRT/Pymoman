"""
This module is designed for the processing of data obtained from the internet.
"""


from pathlib import Path
from shutil import rmtree


from PIL import Image


from packages.constants import constants
from packages.logic import dataimport


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


def clear_cache() -> None:
    """Clear unused cache data.

    Returns:
        None: None.
    """

    if not constants.PATHS.get('cache').exists():
        return

    saved_movies = dataimport.load_all_movies()
    saved_movies_c_path = [movie.storage for movie in saved_movies]

    for path in constants.PATHS.get('cache').iterdir():
        if path not in saved_movies_c_path and path.is_dir():
            rmtree(path)
