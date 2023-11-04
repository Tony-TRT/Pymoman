import json
import shutil
from pathlib import Path
from datetime import datetime

from . import dataimport as dti
from ..constants import constants


class Movie:

    def __init__(self, title: str, year: int, path=None, rating=None):

        if len(title) < 2:
            raise ValueError

        if not isinstance(year, int) or not 1900 <= year <= (datetime.now().year + 5):
            raise ValueError

        self.title = title.strip()
        self.year = year
        self.path = path
        self.rating = rating

        for key, value in constants.MOVIE_RATINGS.items():
            if rating == key:
                self.aesthetic_rating = value

    def __str__(self):

        return self.title

    def __repr__(self):

        return f"{self.title}, {self.year}, {self.path}, {self.rating}/5"

    @property
    def actors(self) -> list[str]:
        """Retrieves movie's actors from the data file.

        Returns:
            list[str]: Actors names.
        """

        content: dict = self.load_data_file()
        return content.get('actors', [])

    @property
    def data_file(self) -> Path:
        """Returns the data file's path.

        Returns:
            Path: Data file's path.
        """

        return Path(self.storage / 'data.json')

    @property
    def genre(self) -> list[str]:
        """Retrieves the movie genre(s) from data file.

        Returns:
            list[str]: Movie genre(s).
        """

        content: dict = self.load_data_file()
        return content.get('genre', [])

    def load_data_file(self) -> dict:
        """Loads data file and returns its content.

        Returns:
            dict: Data file's content.
        """

        try:
            content: dict = dti.load_file_content(self.data_file)
        except FileNotFoundError:
            return {}
        except json.JSONDecodeError:
            return {}
        else:
            return content

    @property
    def official_title(self) -> str:
        """Returns official movie title.

        Returns:
            str: Official title.
        """

        official_title: str = self.title.title()
        if not self.data_file.exists():
            return official_title

        content: dict = self.load_data_file()
        official_title = content.get('title', official_title)
        rem_expr = {
            '(film)': '', 'film': '', ' )': ')', '( ': '(', '()': '', '/': '', '\\': '', ': ': ' - ', '  ': ' '
        }

        for key, value in rem_expr.items():
            official_title = official_title.replace(key, value)

        return official_title.strip()

    def remove_cache(self):
        """Remove cached data.
        """

        if self.storage.exists():
            shutil.rmtree(self.storage)

    def rename(self, new_title: str) -> bool:
        """Changes the movie title.

        Returns:
            bool: True or False depending on whether the cache folder was moved successfully or not.
            Can also return False if the title contains prohibited characters.
        """

        old_storage: Path = self.storage

        b_char = '&"(-_='
        if any(new_title.startswith(char) or new_title.endswith(char) for char in b_char):
            return False

        self.title = new_title.strip()
        try:
            shutil.copytree(old_storage, self.storage)
        except FileNotFoundError:
            return False
        except FileExistsError:
            return True
        except shutil.Error:
            return False
        return True

    @property
    def storage(self) -> Path:
        """Returns storage folder's path.

        Returns:
            Path: Data storage folder's path.
        """

        folder_name = self.title.lower().replace(' ', '_')
        folder_name = folder_name[4:] if folder_name.startswith('the_') else folder_name

        return Path(constants.CACHE / folder_name)

    @property
    def thumb(self) -> Path:
        """Returns thumbnail's path.

        Returns:
            Path: Thumbnail's path.
        """

        return Path(self.storage / 'thumb.jpg')
