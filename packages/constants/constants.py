"""
This module contains all the constants used in the application.
These constants can be imported and used throughout the project to maintain
consistency and ease of updates.
"""

from typing import final
from pathlib import Path
from glob import glob


BASE_DIR: final(Path) = Path(__file__).resolve().parent.parent.parent
STR_BASE_DIR: final(str) = str(BASE_DIR)

CACHE: final(Path) = Path.joinpath(BASE_DIR, "cache")
STR_CACHE: final(str) = str(CACHE)

COLLECTIONS: final(Path) = Path.joinpath(BASE_DIR, "collections")
STR_COLLECTIONS: final(str) = str(COLLECTIONS)
COLLECTION_FILES: final(list[str]) = glob(str(Path.joinpath(COLLECTIONS, "*.json")))

RESOURCES: final(Path) = Path.joinpath(BASE_DIR, "resources")
STR_RESOURCES: final(str) = str(RESOURCES)

DEFAULT_POSTER: final(Path) = Path.joinpath(RESOURCES, "default.jpg")
STR_DEFAULT_POSTER: final(str) = str(DEFAULT_POSTER)

LOGO: final(str) = str(Path.joinpath(RESOURCES, "logo.png"))

STR_STYLE: final(str) = str(Path.joinpath(RESOURCES, "style.qss"))

ICONS: final(Path) = Path.joinpath(RESOURCES, "icons")
STR_ICONS: final(str) = str(ICONS)

SAVE: final(str) = str(Path.joinpath(ICONS, "save.png"))
NOTE: final(str) = str(Path.joinpath(ICONS, "create_collection.png"))
FOLDER: final(str) = str(Path.joinpath(ICONS, "folder.png"))
COLLECTION_ICN: final(str) = str(Path.joinpath(ICONS, "collection.png"))
MOVIE_ICN: final(str) = str(Path.joinpath(ICONS, "movie.png"))
ADD_ICN: final(str) = str(Path.joinpath(ICONS, "add_item.png"))
REM_ICN: final(str) = str(Path.joinpath(ICONS, "remove_item.png"))
SEARCH: final(str) = str(Path.joinpath(ICONS, "search.png"))
PREVIOUS: final(str) = str(Path.joinpath(ICONS, "previous.png"))
EXPORT: final(str) = str(Path.joinpath(ICONS, "export.png"))
DELETE: final(str) = str(Path.joinpath(ICONS, "delete.png"))
OFFICIAL: final(str) = str(Path.joinpath(ICONS, "official.png"))
STAR: final(str) = str(Path.joinpath(ICONS, "star.png"))
TRAILER: final(str) = str(Path.joinpath(ICONS, "trailer.png"))
WISHLIST: final(str) = str(Path.joinpath(ICONS, "wishlist.png"))
LOAD_NEW_POSTER: final(str) = str(Path.joinpath(ICONS, "new_poster.png"))
LOAD_DEFAULT_POSTER: final(str) = str(Path.joinpath(ICONS, "default_poster.png"))

MOVIE_GENRES: final(list[str]) = [
    "Action",
    "Adventure",
    "Animation",
    "Comedy",
    "Crime",
    "Documentary",
    "Drama",
    "Experimental",
    "Fantasy",
    "Historical",
    "Horror",
    "Martial Arts",
    "Mistery",
    "Romance",
    "Science Fiction",
    "Thriller",
    "War",
    "Western",
]
