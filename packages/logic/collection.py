import json
from glob import glob
from pathlib import Path
from typing import Self


from .dataimport import load_collection_movies
from ..constants import constants
from .movie import Movie


class Collection:

    def __init__(self, name: str, mov_lst=None):

        if mov_lst is None:
            mov_lst = []
        self.name = name
        self.mov_lst = mov_lst

    def __str__(self):

        return self.name

    def __repr__(self):

        return f"{self.name} {self.mov_lst}"

    @property
    def path(self):

        return Path.joinpath(constants.PATHS.get('collections'), self.name.replace(' ', '_') + ".json")

    @classmethod
    def retrieve_collections(cls) -> list[Self]:

        collections = []
        for file in glob(str(Path.joinpath(constants.PATHS.get('collections'), "*.json"))):
            mov_lst = load_collection_movies(file)
            name = Path(file).stem.replace('_', ' ')
            collections.append(Collection(name=name, mov_lst=mov_lst))
        return collections

    def add_movie(self, movie: Movie):

        self.mov_lst.append(movie)

    def export_as_txt(self, output_file):

        with open(output_file, 'a', encoding="UTF-8") as text_file:
            for movie in self.mov_lst:
                text_file.write(f"- {movie.title} ({movie.year})\n")

    def remove(self) -> bool:

        if self.path.exists():
            self.path.unlink()

        if self.path.exists():
            return False
        return True

    def remove_movie(self, movie: Movie):

        self.mov_lst.remove(movie)

    def rename(self, new_name: str):

        old_path = self.path
        self.name = new_name

        if old_path.exists():
            self.save()
            old_path.unlink()

    def save(self):

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
