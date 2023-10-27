import json
from pathlib import Path
from glob import glob

BASE_DIR = Path(__file__).resolve().parent.parent
COLLECTIONS_DIR = Path.joinpath(BASE_DIR, "collections")


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

        return Path.joinpath(COLLECTIONS_DIR, self.name.replace(' ', '_') + ".json")

    @staticmethod
    def retrieve_collections() -> list:

        collections = []
        files = glob(str(Path.joinpath(COLLECTIONS_DIR, "*.json")))
        for file in files:
            with open(file, 'r', encoding="UTF-8") as json_file:
                mov_list = json.load(json_file)
                name = Path(file).stem.replace('_', ' ')
                collection = Collection(name=name, mov_lst=mov_list)
                collections.append(collection)

        return collections

    def add_movie(self, movie):

        self.mov_lst.append(movie)

    def export_as_txt(self, output_file):

        with open(output_file, 'a', encoding="UTF-8") as text_file:
            for movie in self.mov_lst:
                text_file.write(f"- {movie}\n")

    def remove(self) -> bool:

        if self.path.exists():
            self.path.unlink()

        if self.path.exists():
            return False
        return True

    def remove_movie(self, movie):

        self.mov_lst.remove(movie)
        if self.path.exists():
            self.save()

    def rename(self, new_name: str):

        old_path = self.path
        self.name = new_name

        if old_path.exists():
            self.save()
            old_path.unlink()

    def save(self):

        COLLECTIONS_DIR.mkdir(exist_ok=True)

        with open(self.path, 'w', encoding="UTF-8") as save_file:
            json.dump(self.mov_lst, save_file, indent=4)
