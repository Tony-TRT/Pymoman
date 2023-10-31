import json
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

    @property
    def actors(self) -> list[str]:
        """Retrieves movie's actors from the data file

        Returns:
            list[str]: actors names
        """

        movie_folder = self.title.strip().lower().replace(' ', '_')
        if movie_folder.startswith('the_'):
            movie_folder = movie_folder[4:]

        try:
            with open(Path.joinpath(BASE_DIR, "cache", movie_folder, "data.json"), 'r', encoding="UTF-8") as f:
                content = json.load(f)
                actors_list = content.get('actors', [''])
        except FileNotFoundError:
            return ['']
        except json.JSONDecodeError:
            return ['']
        else:
            return actors_list
