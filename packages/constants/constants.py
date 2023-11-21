"""
This module contains all the constants used in the application.
These constants can be imported and used throughout the project to maintain
consistency and ease of updates.
"""


from typing import final
from pathlib import Path


BASE: final(Path) = Path(__file__).resolve().parent.parent.parent
APP_HIDDEN_FOLDER: final(Path) = Path.joinpath(Path.home(), '.pymoman')

STR_PATHS = {}
PATHS: final(dict) = {
    'base': BASE,
    'cache': Path(APP_HIDDEN_FOLDER / "cache"),
    'collections': Path(APP_HIDDEN_FOLDER / "collections"),
    'resources': Path(BASE / "resources"),
    'font': Path(BASE / "resources" / "font" / "MerriweatherSans-Regular.ttf"),
    'default poster': Path(BASE / "resources" / "posters" / "default.jpg"),
    'wishlist': Path(BASE / "resources" / "posters" / "wishlist.jpg"),
    'style': Path(BASE / "resources" / "style.qss"),
    'icons': Path(BASE / "resources" / "icons")
}

for key, value in PATHS.items():
    STR_PATHS[key] = str(value)

STR_ICONS = {}
ICONS: final(dict) = {
    'logo': Path(PATHS.get('icons') / "logo.png"),
    'save': Path(PATHS.get('icons') / "save.png"),
    'note': Path(PATHS.get('icons') / "create_collection.png"),
    'folder': Path(PATHS.get('icons') / "folder.png"),
    'collection': Path(PATHS.get('icons') / "collection.png"),
    'movie': Path(PATHS.get('icons') / "movie.png"),
    'add': Path(PATHS.get('icons') / "add_item.png"),
    'rem': Path(PATHS.get('icons') / "remove_item.png"),
    'search': Path(PATHS.get('icons') / "search.png"),
    'previous': Path(PATHS.get('icons') / "previous.png"),
    'export': Path(PATHS.get('icons') / "export.png"),
    'delete': Path(PATHS.get('icons') / "delete.png"),
    'official': Path(PATHS.get('icons') / "official.png"),
    'star': Path(PATHS.get('icons') / "star.png"),
    'trailer': Path(PATHS.get('icons') / "trailer.png"),
    'wishlist': Path(PATHS.get('icons') / "wishlist.png"),
    'new_poster': Path(PATHS.get('icons') / "new_poster.png"),
    'default_poster': Path(PATHS.get('icons') / "default_poster.png")
}

for key, value in ICONS.items():
    STR_ICONS[key] = str(value)

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
    "Mystery",
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

IMPORT_INFO: final(str) = """
In order to import a file as a movie, you must tag it first.
You can assign a title, a year and a rating in this window.
"""
