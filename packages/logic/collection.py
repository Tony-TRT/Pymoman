"""
This module contains the Collection class which allows the creation and management of movie collections.
"""


import json
from glob import glob
from pathlib import Path
from typing import Self


from packages.constants import constants
from packages.logic.dataimport import load_collection_movies
from packages.logic.movie import Movie


class Collection:

    def __init__(self, name: str, mov_lst=None):

        if mov_lst is None:
            mov_lst = []

        self.name = self._name_filter(name)
        self.mov_lst = mov_lst

    def __str__(self):

        return self.name

    def __repr__(self):

        return f"{self.name} {self.mov_lst}"

    @staticmethod
    def _name_filter(name: str) -> str:
        """Filter unwanted characters.

        Args:
            name (str): Collection's name.

        Returns:
            str: Filtered name.
        """

        return "".join(char for char in name if char not in "/\\:'\"")

    @property
    def path(self) -> Path:
        """Returns the path of the instance's file on disk.

        Returns:
            Path: File's path.
        """

        return Path.joinpath(constants.PATHS.get('collections'), self.name.replace(' ', '_') + ".json")

    @classmethod
    def retrieve_collections(cls) -> list[Self]:
        """Recovers all collections saved on the disk.

        Returns:
            list[self]: List of all saved collections.
        """

        collections = []
        for file in glob(str(Path.joinpath(constants.PATHS.get('collections'), "*.json"))):
            mov_lst = load_collection_movies(file)
            name = Path(file).stem.replace('_', ' ')
            collections.append(Collection(name=name, mov_lst=mov_lst))
        return collections

    def add_movie(self, movie: Movie) -> None:
        """Add a movie to the collection.

        Args:
            movie (Movie): Movie to add.

        Returns:
            None: None.
        """

        self.mov_lst.append(movie)

    def export_as_txt(self, output_file) -> None:
        """Export the collection to a text file.

        Args:
            output_file: Output file's path.

        Returns:
            None: None.
        """

        with open(output_file, 'a', encoding="UTF-8") as text_file:
            for movie in self.mov_lst:
                text_file.write(f"- {movie.title} ({movie.year})\n")

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

        self.mov_lst.remove(movie)

    def rename(self, new_name: str) -> None:
        """Renames a collection both on disk and in memory.

        Args:
            new_name (str): New collection name.

        Returns:
            None: None.
        """

        old_path = self.path
        self.name = self._name_filter(new_name)

        if old_path.exists():
            self.save()
            old_path.unlink()

    def save(self) -> None:
        """Saves a collection to disk.

        Returns:
            None: None.
        """

        constants.PATHS.get('collections').mkdir(exist_ok=True)
        data_to_dump = []

        for movie in self.mov_lst:
            dictionary = {
                'title': movie.title,
                'year': movie.year,
                'path': movie.path,
                'rating': movie.rating
            }
            data_to_dump.append(dictionary)

        with open(self.path, 'w', encoding="UTF-8") as save_file:
            json.dump(data_to_dump, save_file, indent=4)
