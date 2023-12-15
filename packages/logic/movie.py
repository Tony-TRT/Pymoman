"""
This module is dedicated to the creation and management of movies.
"""

import shutil
from datetime import datetime
from pathlib import Path

from packages.constants import constants
from packages.logic.dataimport import load_file_content
from packages.logic.dataprocess import filter_name


class Movie:

    def __init__(self, title: str, year: int, path=None, rating=None):

        if len(title) < 2 or not isinstance(year, int) or not 1900 <= year <= (datetime.now().year + 5):
            raise ValueError

        self.title = filter_name(title, limit=60)
        self.year = year
        self.path = path
        self.rating = rating

    def __str__(self):

        return self.title

    def __repr__(self):

        return f"{self.title}, {self.year}, {self.path}, {self.rating}/5"

    def __eq__(self, other):

        if isinstance(other, Movie):
            return self.storage == other.storage and self.year == other.year
        return False

    def __lt__(self, other):

        if isinstance(other, Movie):
            return self.title.casefold() < other.title.casefold()
        return False

    @property
    def actors(self) -> list[str]:
        """Retrieves movie's actors from the data file.

        Returns:
            list[str]: Actors names.
        """

        content: dict = self.load_data_file()
        return content.get('actors', [])

    @property
    def aesthetic_rating(self) -> str:
        """Displays the movie rating in a nice way.

        Returns:
            str: Aesthetic movie rating.
        """

        for key, value in constants.MOVIE_RATINGS.items():
            if self.rating == key:
                return value

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

        return load_file_content(self.data_file)

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

    def remove_cache(self) -> None:
        """Remove cached data.

        Returns:
            None: None.
        """

        if self.storage.exists():
            shutil.rmtree(self.storage)

    def rename(self, new_title: str) -> bool:
        """Changes the movie title.

        Args:
            new_title (str): New movie title.

        Returns:
            bool: True or False depending on whether the cache folder was moved successfully or not.
            Can also return False if the title contains prohibited characters.
        """

        old_storage: Path = self.storage

        self.title = filter_name(new_title, limit=60)

        if self.storage == old_storage:
            return True

        try:
            shutil.copytree(old_storage, self.storage)
        except FileNotFoundError:
            return False
        except FileExistsError:
            return False
        except shutil.Error:
            return False
        return True

    def set_default_poster(self) -> None:
        """Set default poster.

        Returns:
            None: None.
        """

        if self.thumb.exists():
            self.thumb.unlink()

        self.storage.mkdir(exist_ok=True, parents=True)
        shutil.copy(constants.PATHS.get('default poster'), self.thumb)

    @property
    def storage(self) -> Path:
        """Returns storage folder's path.

        Returns:
            Path: Data storage folder's path.
        """

        folder_name = self.title.lower().replace(' ', '_')
        folder_name = folder_name[4:] if folder_name.startswith('the_') else folder_name

        return Path(constants.PATHS.get('cache') / folder_name)

    @property
    def thumb(self) -> Path:
        """Returns thumbnail's path.

        Returns:
            Path: Thumbnail's path.
        """

        return Path(self.storage / 'thumb.jpg')
