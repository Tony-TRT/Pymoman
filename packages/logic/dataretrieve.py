"""
This module is dedicated to retrieving information from the internet.
It provides functions and tools to access and gather data from various online sources.
"""

import json
from pathlib import Path
from time import sleep

import requests
import wikipedia
from bs4 import BeautifulSoup

from .dataprocess import modify_raw_poster
from .movie import Movie


class MovieScraper(Movie):
    """MovieScraper object can process input and retrieve information"""

    sources_websites = {
        "SA": "http://www.impawards.com/",
        "SB": "https://www.movieposterdb.com/search?q={}&imdb=0"
    }

    def __init__(self, movie: Movie):
        super().__init__(movie.title, movie.year)

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

        sanitized_title = self.title.strip().lower()
        if sanitized_title.startswith('the '):
            sanitized_title = sanitized_title[4:]

        return sanitized_title.replace(' ', '_')

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

        def_imp_link = f"{MovieScraper.sources_websites.get('SA')}{self.year}/posters/{self.sanitized_title}.jpg"
        links = [f"{def_imp_link[:-4]}{suffix}.jpg" for suffix in self.imp_suffixes]
        links.insert(0, def_imp_link)
        return links

    def generate_movie_pdb_link(self) -> list[str]:
        """Generates download link

        Returns:
            list[str]: download link
        """

        movie_pdb_title = self.title.replace(' ', '%20')
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
            ul_element = starring_element.find_next('ul')
        else:
            return []

        try_a = [a.text for a in starring_element_parent.find_all('a')]
        try_a = [el for el in try_a if not any(char.isdigit() for char in el)]
        if not ul_element:
            return sorted(try_a, key=str.casefold)

        try_b = [li.text for li in ul_element.find_all('li')]
        try_b = [el for el in try_b if not any(char.isdigit() for char in el)]
        final_try: set[str] = set().union(try_a, try_b)

        return sorted([actor for actor in final_try], key=str.casefold)

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

        query = f"{self.title} {self.year}"
        wikipedia.set_lang("en")

        # Let's try 2 times
        for _ in range(2):
            try:
                page = wikipedia.page(query)
            except wikipedia.exceptions.DisambiguationError:
                query = f"{self.title} film"
                continue
            except wikipedia.exceptions.HTTPTimeoutError:
                break
            except wikipedia.exceptions.PageError:
                query = f"{self.title} film"
                continue
            except wikipedia.exceptions.RedirectError:
                query = f"{self.title} film"
                continue
            else:
                official_title = page.title
                actors = self.get_actors(page)
                break

        query = f"{self.title} {self.year}"
        # Let's try 2 times again
        for _ in range(2):
            try:
                summary = wikipedia.summary(query, 2)
            except wikipedia.exceptions.DisambiguationError:
                query = f"{self.title} film"
                continue
            except wikipedia.exceptions.HTTPTimeoutError:
                break
            except wikipedia.exceptions.PageError:
                query = f"{self.title} film"
                continue
            except wikipedia.exceptions.RedirectError:
                query = f"{self.title} film"
                continue
            else:
                if len(summary) < 230:
                    summary = wikipedia.summary(query, 3)

        if official_title is None:
            official_title = f"{self.title.title()} ({self.year})"

        if summary is None:
            summary = "The summary could not be retrieved, movie title may be incomplete, incorrect or too vague"

        data = {"title": official_title, "summary": summary, "actors": actors}

        with open(self.data_file, 'w', encoding="UTF-8") as file:
            json.dump(data, file, indent=4)

        if not self.data_file.exists():
            return False
        return True
