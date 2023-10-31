"""
This module is dedicated to retrieving information from the internet.
It provides functions and tools to access and gather data from various online sources.
"""

import json
from pathlib import Path
from time import sleep

import wikipedia
from bs4 import BeautifulSoup
import requests

from ..constants import constants
from .dataprocess import modify_raw_poster


class MovieScraper:
    """MovieScraper object can process input and retrieve information"""

    sources_websites = {
        "SA": "http://www.impawards.com/",
        "SB": "https://www.movieposterdb.com/search?q={}&imdb=0"
    }

    def __init__(self, movie_title: str, movie_year: int):

        self.movie_title = movie_title
        self.movie_year = movie_year
        self.imp_suffixes = (
            "_ver2",
            "_ver3",
            "_ver4",
            "_ver5",
            "_ver6",
            "_ver7",
            "_xlg",
            "_xxlg"
        )

        self.storage.mkdir(exist_ok=True, parents=True)

    @property
    def sanitized_title(self) -> str:
        """Returns sanitized title

        Returns:
            str: sanitized title
        """

        sanitized_title = self.movie_title.strip().lower()
        if sanitized_title.startswith('the '):
            sanitized_title = sanitized_title[4:]

        return sanitized_title.replace(' ', '_')

    @property
    def storage(self) -> Path:
        """Returns storage folder path

        Returns:
            Path: data storage folder path
        """

        return Path(constants.CACHE / self.sanitized_title)

    @property
    def thumb(self) -> Path:
        """Returns thumbnail path

        Returns:
            Path: thumbnail path
        """

        return Path(self.storage / 'thumb.jpg')

    @property
    def data_file(self) -> Path:
        """Returns data file path

        Returns:
            Path: data file path
        """

        return Path(self.storage / 'data.json')

    def generate_imp_links(self) -> list[str]:
        """Generates download links

        Returns:
            list[str]: links in a list
        """

        def_imp_link = f"{MovieScraper.sources_websites.get('SA')}{self.movie_year}/posters/{self.sanitized_title}.jpg"
        links = [f"{def_imp_link[:-4]}{suffix}.jpg" for suffix in self.imp_suffixes]
        links.insert(0, def_imp_link)
        return links

    def generate_movie_pdb_link(self) -> list[str]:
        """Generates download link

        Returns:
            list[str]: download link
        """

        movie_pdb_title = self.movie_title.replace(' ', '%20')
        url = MovieScraper.sources_websites.get('SB').format(movie_pdb_title)

        page = requests.get(url, timeout=10)
        soup = BeautifulSoup(page.text, 'html.parser')
        img_cont = soup.find(class_='vertical-image img-responsive poster_img lazyload')
        links = [img_cont['data-src']]
        return links

    def _write_img_on_disk(self, url: requests.Response) -> bool:
        """Writes image to disk

        Returns:
            bool: success or failure
        """

        with open(self.thumb, "wb") as poster:
            poster.write(url.content)

        res = modify_raw_poster(self.thumb)
        if not res:
            return False
        return True

    @staticmethod
    def get_actors(page: wikipedia.WikipediaPage) -> list[str]:
        """Retrieves movie's actors from the wikipedia page

        Returns:
            list[str]: actors names
        """

        soup = BeautifulSoup(page.html(), 'html.parser')
        starring_element = soup.find('th', string='Starring')

        if starring_element:
            starring_element_parent = starring_element.parent
            return [a.text for a in starring_element_parent.find_all('a')]
        return []

    def download_poster(self) -> bool:
        """Downloads movie poster

        Returns:
            bool: success or failure
        """

        if self.thumb.exists():
            return True

        imp_links = self.generate_imp_links()
        movie_pdb_link = self.generate_movie_pdb_link()
        every_links = imp_links + movie_pdb_link

        value = None
        for lnk in every_links:
            resp = requests.get(lnk, timeout=7)
            if resp.ok:
                value = self._write_img_on_disk(resp)
                break
            else:
                value = False
                sleep(1)
                continue

        return value

    def download_info(self) -> bool:
        """Downloads movie info using wikipedia module

        Returns:
            bool: success or failure
        """

        if self.data_file.exists():
            return True

        official_title = None
        summary = None
        actors = []

        query = f"{self.movie_title} {self.movie_year}"
        wikipedia.set_lang("en")

        # Let's try 2 times
        for _ in range(2):
            try:
                page = wikipedia.page(query)
            except wikipedia.exceptions.DisambiguationError:
                query = f"{self.movie_title} film"
                continue
            except wikipedia.exceptions.HTTPTimeoutError:
                break
            except wikipedia.exceptions.PageError:
                query = f"{self.movie_title} film"
                continue
            except wikipedia.exceptions.RedirectError:
                query = f"{self.movie_title} film"
                continue
            else:
                official_title = page.title
                actors = self.get_actors(page)
                break

        query = f"{self.movie_title} {self.movie_year}"
        # Let's try 2 times again
        for _ in range(2):
            try:
                summary = wikipedia.summary(query, 2)
            except wikipedia.exceptions.DisambiguationError:
                query = f"{self.movie_title} film"
                continue
            except wikipedia.exceptions.HTTPTimeoutError:
                break
            except wikipedia.exceptions.PageError:
                query = f"{self.movie_title} film"
                continue
            except wikipedia.exceptions.RedirectError:
                query = f"{self.movie_title} film"
                continue
            else:
                if len(summary) < 230:
                    summary = wikipedia.summary(query, 3)

        if official_title is None:
            official_title = f"{self.movie_title.title()} ({self.movie_year})"

        if summary is None:
            summary = "The summary could not be retrieved, movie title may be incomplete, incorrect or too vague"

        data = {"title": official_title, "summary": summary, "actors": actors}

        with open(self.data_file, 'w', encoding="UTF-8") as file:
            json.dump(data, file, indent=4)

        if not self.data_file.exists():
            return False
        return True
