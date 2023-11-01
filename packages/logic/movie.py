import json
from shutil import rmtree
from datetime import datetime
from pathlib import Path

from ..constants import constants


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
    def storage(self) -> Path:
        """Returns storage folder path

        Returns:
            Path: data storage folder path
        """

        m_folder = self.title.strip().lower()
        if m_folder.startswith('the '):
            m_folder = m_folder[4:]
        m_folder = m_folder.replace(' ', '_')

        return Path(constants.CACHE / m_folder)

    @property
    def actors(self) -> list[str]:
        """Retrieves movie's actors from the data file

        Returns:
            list[str]: actors names
        """

        from .dataimport import load_file_content
        try:
            content = load_file_content(Path(self.storage / "data.json"))
            actors_list = content.get('actors', [''])
        except FileNotFoundError:
            return ['']
        except json.JSONDecodeError:
            return ['']
        else:
            return actors_list

    def remove_cache(self):

        if self.storage.exists():
            rmtree(self.storage)
