"""
This module is dedicated to the creation and management of movies.
"""

from __future__ import annotations

import shutil
from datetime import datetime
from pathlib import Path
from typing import Any, Optional, Union

from packages.constants import constants
from packages.logic.dataimport import load_file_content
from packages.logic.dataprocess import filter_name


class Movie:

    def __init__(self, title: str, year: Union[int, str], path: Optional[str] = None, rating: str = "-"):

        self.title: str = self.check_title(title=title)
        self.year: int = self.check_year(year=year)
        self.path: str = self.check_path(path=path)
        self.rating: str = self.check_rating(rating=rating)

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
        return content.get("actors", [])

    @property
    def aesthetic_rating(self) -> str:
        """Displays the movie rating in a nice way.

        Returns:
            str: Aesthetic movie rating.
        """

        return constants.MOVIE_RATINGS[self.rating]

    @staticmethod
    def check_path(path: Any) -> str:
        """Validates and converts the path to a string.

        Args:
            path (Any): The path to validate.

        Returns:
            str: The validated path as a string.
        """

        if path is None:
            return ""

        if not isinstance(path, (str, Path)):
            raise ValueError("Path must be a string or a Path object.")
        path_str = str(path)

        if not Path(path_str).exists():
            raise FileNotFoundError("The specified path does not exist.")
        return path_str

    @staticmethod
    def check_rating(rating: Any) -> str:
        """Validates the rating of the movie.

        Args:
            rating (Any): The rating to validate.

        Returns:
            str: The validated rating.
        """

        if not isinstance(rating, str):
            raise ValueError("Rating must be a string.")

        elif rating not in constants.MOVIE_RATINGS:
            raise ValueError("Unknown value for rating.")
        return rating

    @staticmethod
    def check_title(title: Any) -> str:
        """Validates the title of the movie and processes it.

        Args:
            title (Any): The title to validate.

        Returns:
            str: The processed title.
        """

        if not isinstance(title, str):
            raise ValueError("Title must be a string.")

        elif len(title) < 2:
            raise ValueError("Title must be at least 2 characters long.")
        return filter_name(name=title, limit=60)

    @staticmethod
    def check_year(year: Any) -> int:
        """Validates and converts the year to an integer.

        Args:
            year (Any): The year to validate.

        Returns:
            int: The validated and converted year.
        """

        year: int = int(year) if isinstance(year, str) and year.isdigit() else year

        if not isinstance(year, int):
            raise ValueError("Year must be an integer or a string that can be converted to an integer.")

        elif not 1900 <= year <= (datetime.now().year + 5):
            raise ValueError(f"Year must be between 1900 and {datetime.now().year + 5}.")
        return year

    @property
    def data_file(self) -> Path:
        """Returns the data file's path.

        Returns:
            Path: Data file's path.
        """

        return Path(self.storage / "data.json")

    @property
    def genre(self) -> list[str]:
        """Retrieves the movie genre(s) from data file.

        Returns:
            list[str]: Movie genre(s).
        """

        content: dict = self.load_data_file()
        return content.get("genre", [])

    def load_data_file(self) -> dict:
        """Loads data file and returns its content.

        Returns:
            dict: Data file's content.
        """

        return load_file_content(self.data_file)

    @staticmethod
    def no_errors(*args) -> "Movie" | None:
        """Creates a Movie instance if no exceptions are raised during instantiation.
        If a ValueError or FileNotFoundError is encountered during the creation process,
        the method returns None instead of raising the exception.

        Args:
            *args: Variable length argument list used to initialize the Movie object.

        Returns:
            Movie | None: A new Movie instance if creation is successful, None if a
            ValueError or FileNotFoundError is raised.
        """

        try:
            movie = Movie(*args)

        except (ValueError, FileNotFoundError):
            return None
        return movie

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
        official_title = content.get("title", official_title)
        rem_expr: dict = {
            '(film)': '', 'film': '', ' )': ')', '( ': '(', '()': '', '/': '', '\\': '', ': ': ' - ', '  ': ' '
        }

        for key, value in rem_expr.items():
            official_title = official_title.replace(key, value)
        return official_title.strip()

    def remove_cache(self) -> None:
        """Remove cached data."""

        if self.storage.exists():
            shutil.rmtree(self.storage)

    def rename(self, new_title: str) -> bool:
        """Changes the movie title.

        Args:
            new_title (str): New movie title.

        Returns:
            bool: True or False depending on whether the cache folder was moved successfully or not.
        """

        old_storage: Path = self.storage
        self.title = self.check_title(title=new_title)

        if self.storage == old_storage:
            return True

        try:
            shutil.copytree(old_storage, self.storage)

        except (FileNotFoundError, FileExistsError, shutil.Error):
            return False
        return True

    def set_default_poster(self) -> None:
        """Set default poster."""

        if self.thumb.exists():
            self.thumb.unlink()

        self.storage.mkdir(exist_ok=True, parents=True)
        shutil.copy(constants.PATHS["default poster"], self.thumb)

    @property
    def storage(self) -> Path:
        """Returns storage folder's path.

        Returns:
            Path: Data storage folder's path.
        """

        folder_name = self.title.lower().replace(' ', '_')
        folder_name = folder_name[4:] if folder_name.startswith("the_") else folder_name
        return Path(constants.PATHS["cache"] / folder_name)

    @property
    def thumb(self) -> Path:
        """Returns thumbnail's path.

        Returns:
            Path: Thumbnail's path.
        """

        return Path(self.storage / "thumb.jpg")
