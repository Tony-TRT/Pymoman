"""
This module contains all the constants used in the application.
These constants can be imported and used throughout the project to maintain
consistency and ease of updates.
"""

from typing import final
from pathlib import Path


BASE: final(Path) = Path(__file__).resolve().parent.parent.parent
APP_HIDDEN_FOLDER: final(Path) = Path.joinpath(Path.home(), ".pymoman")

PATHS: final(dict) = {
    "settings": Path(APP_HIDDEN_FOLDER / "settings.json"),
    "cache": Path(APP_HIDDEN_FOLDER / "cache"),
    "collections": Path(APP_HIDDEN_FOLDER / "collections"),
    "recommendations": Path(APP_HIDDEN_FOLDER / "recommendations"),
    "resources": Path(BASE / "resources"),
    "default font": Path(BASE / "resources" / "fonts" / "default.ttf"),
    "cyber font": Path(BASE / "resources" / "fonts" / "cyber.ttf"),
    "default poster": Path(BASE / "resources" / "posters" / "default.jpg"),
    "wishlist": Path(BASE / "resources" / "posters" / "wishlist.jpg"),
    "default style": Path(BASE / "resources" / "styles" / "default.qss"),
    "cyber style": Path(BASE / "resources" / "styles" / "cyber.qss"),
    "icons": Path(BASE / "resources" / "icons")
}
STR_PATHS: final(dict) = {key: str(value) for key, value in PATHS.items()}

ICONS: final(dict) = {icon_path.stem: icon_path for icon_path in PATHS["icons"].iterdir()}
STR_ICONS: final(dict) = {key: str(value) for key, value in ICONS.items()}

MOVIE_GENRES: final(dict) = {
    "action": "action",
    "adventure": "adventure",
    "animation": "animated",
    "comedy": "comedy",
    "crime": "crime",
    "documentary": "biography",
    "drama": "drama",
    "experimental": "experimental",
    "fantasy": "fantasy",
    "historical": "historical",
    "horror": "horror",
    "martial arts": "martial arts",
    "mystery": "mystery",
    "romance": "romance",
    "science fiction": "sci-fi",
    "thriller": "thriller",
    "war": "war",
    "western": "western"
}

MOVIE_RATINGS: final(dict) = {
    "-": "☆☆☆☆☆",
    "1": "★☆☆☆☆",
    "2": "★★☆☆☆",
    "3": "★★★☆☆",
    "4": "★★★★☆",
    "5": "★★★★★"
}

CACHE_WARNING: final(str) = """
Regrettably, no data was found for this movie, or it seems
that an error occurred while attempting to copy cached information.
Rest assured, this situation merely necessitates a fresh
retrieval of the movie data from the internet.
"""

IMPORT_INFO: final(str) = """
In order to import a file as a movie, you must tag it first.
You can assign a title, a year and a rating in this window.
"""
