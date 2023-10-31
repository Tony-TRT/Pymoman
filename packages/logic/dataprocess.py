"""
This module is designed for the processing of data obtained from the internet.
"""

from pathlib import Path

from PIL import Image


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
