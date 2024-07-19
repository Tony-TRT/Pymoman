"""
This module contains the Collection class which allows the creation and management of movie collections.
"""

import json
from pathlib import Path
from typing import Self

from packages.constants import constants
from packages.logic.data_import import load_collection_movies
from packages.logic.dataprocess import filter_name
from packages.logic.movie import Movie


class Collection:

    def __init__(self, name: str, movies=None):

        if not (type(movies) is list and all(isinstance(item, Movie) for item in movies)):
            movies = []

        self.name: str = filter_name(name)
        self.movies: list[Movie] = movies

    def __str__(self):

        return self.name

    def __repr__(self):

        return f"Collection -> '{self.name}' with {len(self.movies)} movie{'s' if len(self.movies) > 1 else ''}"

    def add_movie(self, movie: Movie) -> None:
        """Add a movie to the collection.

        Args:
            movie (Movie): Movie to add.

        Returns:
            None: None.
        """

        if isinstance(movie, Movie) and not any(movie == other for other in self.movies):
            self.movies.append(movie)

    def export_as_txt(self, output_file: str | Path) -> None:
        """Export the collection to a text file.

        Args:
            output_file: Output file's path.

        Returns:
            None: None.
        """

        with open(output_file, 'w', encoding="UTF-8") as file:
            for movie in self.movies:
                file.write(f"- {movie.title}{f' ({movie.year})' if str(movie.year) not in movie.title else ''}\n")

    @property
    def path(self) -> Path:
        """Returns the path of the instance's file on disk.

        Returns:
            Path: File's path.
        """

        return Path.joinpath(constants.PATHS.get('collections'), self.name.replace(' ', '_') + ".json")

    def remove(self) -> bool:
        """Remove saved collection from disk.

        Returns:
            bool: True = good, False = something went wrong.
        """

        if self.path.exists():
            self.path.unlink()

        if self.path.exists():
            return False
        return True

    def remove_movie(self, movie: Movie) -> None:
        """Remove a movie from the collection.

        Args:
            movie (Movie): Movie to remove.

        Returns:
            None: None.
        """

        self.movies.remove(movie)

    def rename(self, new_name: str) -> None:
        """Renames a collection both on disk and in memory.

        Args:
            new_name (str): New collection name.

        Returns:
            None: None.
        """

        old_path = self.path
        self.name = filter_name(new_name)

        if old_path.exists():
            self.save()
            old_path.unlink()

    @classmethod
    def retrieve_collections(cls) -> list[Self]:
        """Recovers all collections saved on the disk.

        Returns:
            list[self]: List of all saved collections.
        """

        collections = []
        for file in constants.PATHS.get('collections').glob('*.json'):
            movies = load_collection_movies(file)
            name = Path(file).stem.replace('_', ' ')
            collections.append(Collection(name=name, movies=movies))
        return collections

    def save(self) -> None:
        """Saves a collection to disk.

        Returns:
            None: None.
        """

        constants.PATHS.get('collections').mkdir(exist_ok=True)
        data_to_dump: list[dict] = []

        for movie in self.movies:
            dictionary = {
                'title': movie.title,
                'year': movie.year,
                'path': movie.path,
                'rating': movie.rating
            }
            data_to_dump.append(dictionary)

        with open(self.path, 'w', encoding="UTF-8") as save_file:
            json.dump(data_to_dump, save_file, indent=4)
