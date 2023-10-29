"""
This module retrieves movies information
"""

import json
from pathlib import Path

import wikipedia
from PIL import Image
import requests


BASE_DIR = Path(__file__).resolve().parent.parent.parent
DEFAULT_POSTER = Path.joinpath(BASE_DIR, "resources", "default.jpg")
CACHE = Path.joinpath(BASE_DIR, "cache")


def perfect_resize(poster: Path) -> bool:
    """Resize movie poster to the perfect display size

    Args:
        poster (Path): file path

    Returns:
        bool: True = succes, False = problem
    """

    if not poster.exists():
        return False

    image = Image.open(str(poster))
    resized = image.resize((200, 300))
    resized.save(str(poster))
    return True


class MovieScrapper:
    """MovieScrapper object can process input and retrieve information"""

    pic_website = "http://www.impawards.com/"

    def __init__(self, movie_title: str, movie_year: int):

        self.movie_title = movie_title
        self.movie_year = movie_year
        self.some_suffixes = {
            "_ver2",
            "_ver3",
            "_ver4",
            "_ver5"
            "_xlg",
            "_xxlg"
        }

    @property
    def sanitized_title(self) -> str:
        """Return sanitized title

        Returns:
            str: sanitized title
        """

        sanitized_title = self.movie_title.strip().lower()
        if sanitized_title.startswith('the '):
            sanitized_title = sanitized_title[4:]

        return sanitized_title.replace(' ', '_')

    @property
    def default_download_link(self) -> str:
        """Return default download link

        Returns:
            str: default download link
        """

        return f"{MovieScrapper.pic_website}{self.movie_year}/posters/{self.sanitized_title}.jpg"

    def generate_links(self) -> list[str]:
        """Generate possible links

        Returns:
            list[str]: links in a list
        """

        links = [f"{self.default_download_link[:-4]}{suffix}.jpg" for suffix in self.some_suffixes]
        return links

    def download_poster(self) -> bool:
        """Downloads movie poster

        Returns:
            bool: True = succes, False = problem
        """

        storage = Path(CACHE / self.sanitized_title)
        storage.mkdir(exist_ok=True, parents=True)

        if Path(storage / 'thumb.jpg').exists():
            return True

        response = requests.get(self.default_download_link, timeout=8)

        if response.ok:
            with open(storage / 'thumb.jpg', "wb") as poster:
                poster.write(response.content)
                res = perfect_resize(storage / 'thumb.jpg')
                if res:
                    return True
        else:
            links = self.generate_links()
            for link in links:
                response = requests.get(link, timeout=8)
                if response.ok:
                    with open(storage / 'thumb.jpg', "wb") as poster:
                        poster.write(response.content)
                        res = perfect_resize(storage / 'thumb.jpg')
                        if res:
                            return True

        return False

    def download_info(self) -> bool:

        data_file = Path(CACHE / self.sanitized_title / 'data.json')
        data_file.parent.mkdir(exist_ok=True, parents=True)

        if data_file.exists():
            return True

        try:
            page = wikipedia.page(f"{self.movie_title} {self.movie_year}")
        except :
            title = self.movie_title
        else:
            title = page.title

        wikipedia.set_lang("en")
        try:
            summary = wikipedia.summary(f"{self.movie_title} {self.movie_year}", 2)
        except :
            summary = "The summary could not be retrieved, movie title may be incomplete, incorrect or too vague"

        data = {"title": title, "summary": summary}

        with open(data_file, 'w', encoding="UTF-8") as file:
            json.dump(data, file)

        if not data_file.exists():
            return False
        return True
