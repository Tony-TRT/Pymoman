from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class Movie:

    def __init__(self, title: str, path=None, rating: int=0):

        self.title = title
        self.path = path
        self.rating = rating

    def __str__(self):

        return self.title

    def __repr__(self):

        return f"{self.title}, {self.path}, {self.rating}/5"
