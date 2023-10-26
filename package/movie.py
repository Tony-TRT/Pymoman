import json
from pathlib import Path
from glob import glob


BASE_DIR = Path(__file__).resolve().parent.parent
COLLECTIONS_DIR = Path.joinpath(BASE_DIR, "collections")


class Movie:

    def __init__(self):

        pass


    def __str__(self):

        pass


    def __repr__(self):

        pass


    @staticmethod
    def save_collection() -> bool:

        pass


    @staticmethod
    def remove_collection() -> bool:

        pass


    @staticmethod
    def retrieve_collections() -> list[str]:

        files = glob(str(Path.joinpath(COLLECTIONS_DIR, "*.json")))
        return [Path(file).stem.replace('_', ' ') for file in files]
