from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).resolve().parent.parent.parent
RATINGS = {
    "-": "☆☆☆☆☆",
    "1": "★☆☆☆☆",
    "2": "★★☆☆☆",
    "3": "★★★☆☆",
    "4": "★★★★☆",
    "5": "★★★★★"
}


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

        for key, value in RATINGS.items():
            if rating == key:
                self.aesthetic_rating = value

    def __str__(self):

        return self.title

    def __repr__(self):

        return f"{self.title}, {self.year}, {self.path}, {self.rating}/5"
