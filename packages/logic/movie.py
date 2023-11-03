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
    def storage(self) -> Path:
        """Returns storage folder path

        Returns:
            Path: data storage folder path
        """

        m_folder = self.title.lower().replace(' ', '_')
        if m_folder.startswith('the_'):
            m_folder = m_folder[4:]

        return Path(constants.CACHE / m_folder)

    @property
    def data_file(self) -> Path:
        """Returns data file path

        Returns:
            Path: data file path
        """

        return Path(self.storage / 'data.json')

    @property
    def thumb(self) -> Path:
        """Returns thumbnail path

        Returns:
            Path: thumbnail path
        """

        return Path(self.storage / 'thumb.jpg')

    @property
    def official_title(self) -> str:
        """Returns official movie title

        Returns:
            str: official title
        """

        official_title = self.title.title()
        if not self.data_file.exists():
            return official_title

        data = dti.load_file_content(self.data_file)
        official_title = data.get('title', official_title)
        rem_expr = {
            '(film)': '', 'film': '', ' )': ')', '( ': '(', '()': '', '/': '', '\\': '', ': ': ' - ', '  ': ' '
        }

        for k, v in rem_expr.items():
            official_title = official_title.replace(k, v)

        return official_title.strip()

    @property
    def actors(self) -> list[str]:
        """Retrieves movie's actors from the data file

        Returns:
            list[str]: actors names
        """

        try:
            content = dti.load_file_content(self.data_file)
            actors_list = content.get('actors', [''])
        except FileNotFoundError:
            return ['']
        except json.JSONDecodeError:
            return ['']
        else:
            return actors_list

    @property
    def genre(self) -> str:
        """Retrieves the movie genre from data file

        Returns:
            str: movie genre
        """

        try:
            content = dti.load_file_content(self.data_file)
            genre = content.get("genre", "Other")
        except FileNotFoundError:
            return "Other"
        except json.JSONDecodeError:
            return "Other"
        else:
            return genre

    def rename(self, new_title: str) -> bool:

        old_storage = self.storage

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

    def remove_cache(self):

        if self.storage.exists():
            shutil.rmtree(self.storage)
