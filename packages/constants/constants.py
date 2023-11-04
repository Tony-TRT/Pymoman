"""
This module contains all the constants used in the application.
These constants can be imported and used throughout the project to maintain
consistency and ease of updates.
"""

from typing import final
from pathlib import Path
from glob import glob


BASE_DIR: final(Path) = Path(__file__).resolve().parent.parent.parent

CACHE: final(Path) = Path.joinpath(BASE_DIR, "cache")

COLLECTIONS: final(Path) = Path.joinpath(BASE_DIR, "collections")
STR_COLLECTIONS: final(str) = str(COLLECTIONS)
COLLECTION_FILES: final(list[str]) = glob(str(Path.joinpath(COLLECTIONS, "*.json")))

RESOURCES: final(Path) = Path.joinpath(BASE_DIR, "resources")
STR_RESOURCES: final(str) = str(RESOURCES)

DEFAULT_POSTER: final(Path) = Path.joinpath(RESOURCES, "default.jpg")
STR_DEFAULT_POSTER: final(str) = str(DEFAULT_POSTER)

STYLE: final(Path) = Path.joinpath(RESOURCES, "style.qss")

ICONS_FOLDER: final(Path) = Path.joinpath(RESOURCES, "icons")
STR_ICONS_FOLDER: final(str) = str(ICONS_FOLDER)

ICONS: final(dict) = {
    'logo': Path.joinpath(RESOURCES, "logo.png"),
    'save': Path.joinpath(ICONS_FOLDER, "save.png"),
    'note': Path.joinpath(ICONS_FOLDER, "create_collection.png"),
    'folder': Path.joinpath(ICONS_FOLDER, "folder.png"),
    'collection': Path.joinpath(ICONS_FOLDER, "collection.png"),
    'movie': Path.joinpath(ICONS_FOLDER, "movie.png"),
    'add': Path.joinpath(ICONS_FOLDER, "add_item.png"),
    'rem': Path.joinpath(ICONS_FOLDER, "remove_item.png"),
    'search': Path.joinpath(ICONS_FOLDER, "search.png"),
    'previous': Path.joinpath(ICONS_FOLDER, "previous.png"),
    'export': Path.joinpath(ICONS_FOLDER, "export.png"),
    'delete': Path.joinpath(ICONS_FOLDER, "delete.png"),
    'official': Path.joinpath(ICONS_FOLDER, "official.png"),
    'star': Path.joinpath(ICONS_FOLDER, "star.png"),
    'trailer': Path.joinpath(ICONS_FOLDER, "trailer.png"),
    'wishlist': Path.joinpath(ICONS_FOLDER, "wishlist.png"),
    'new_poster': Path.joinpath(ICONS_FOLDER, "new_poster.png"),
    'default_poster': Path.joinpath(ICONS_FOLDER, "default_poster.png")
}

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
