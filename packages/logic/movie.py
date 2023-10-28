from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent.parent


class Movie:

    def __init__(self, title: str, year: int, path=None, rating=None):

        if len(title) < 2:
            raise ValueError

        if not isinstance(year, int) or not 1900 <= year <= (datetime.now().year + 5):
            raise ValueError

        self.title = title
        self.year = year
        self.path = path
        self.rating = rating

    def __str__(self):

        return self.title

    def __repr__(self):

        return f"{self.title}, {self.year}, {self.path}, {self.rating}/5"
