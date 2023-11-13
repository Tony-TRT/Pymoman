"""
This module is dedicated to retrieving information from the internet.
It provides functions and tools to access and gather data from various online sources.
"""


import json
from time import sleep


import requests
import wikipedia
from bs4 import BeautifulSoup


from packages.constants import constants
from packages.logic.dataprocess import modify_raw_poster
from packages.logic.movie import Movie


class MovieScraper(Movie):
    """MovieScraper object can process input and retrieve information"""

    sources_websites = {
        "SA": "http://www.impawards.com/",
        "SB": "https://www.movieposterdb.com/search?q={}&imdb=0",
        "SC": "https://www.cinematerial.com"
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
    def imp_sanitized_title(self) -> str:
        """Returns sanitized title for IMP Awards.

        Returns:
            str: Sanitized title.
        """

        sanitized_title = self.title.strip().lower()
        if sanitized_title.startswith('the '):
            sanitized_title = sanitized_title[4:]

        return sanitized_title.replace(' ', '_')

    def generate_imp_links(self) -> list[str]:
        """Generates IMP Awards download links.

        Returns:
            list[str]: Links in a list.
        """

        def_imp_link = f"{MovieScraper.sources_websites.get('SA')}{self.year}/posters/{self.imp_sanitized_title}.jpg"
        links = [f"{def_imp_link[:-4]}{suffix}.jpg" for suffix in self.imp_suffixes]
        links.insert(0, def_imp_link)
        return links

    def generate_movie_pdb_link(self) -> list[str]:
        """Generates MoviePosterDB download link.

        Returns:
            list[str]: Link in a list.
        """

        movie_pdb_title = self.title.replace(' ', '%20')
        url = MovieScraper.sources_websites.get('SB').format(movie_pdb_title)

        page = requests.get(url, timeout=10)
        soup = BeautifulSoup(page.text, 'html.parser')
        img_cont = soup.find(class_='vertical-image img-responsive poster_img lazyload')
        return [img_cont['data-src']] if img_cont else []

    def generate_cnm_link(self) -> str:
        """Generates CineMaterial download link.

        Returns:
            str: Download link.
        """

        sanitized_query = self.title.replace(' ', '+')
        results_link = f"{self.sources_websites.get('SC')}/search?q={sanitized_query}"

        results_page = requests.get(results_link, timeout=5)
        if results_page.ok:
            soup = BeautifulSoup(results_page.text, 'html.parser')
            div_element = soup.find('div', class_='table-responsive')
            td_element = div_element.find_all('td')[1]
            page_link = td_element.find('a')['href']
            full_link = f"{self.sources_websites.get('SC')}{page_link}"
        else:
            return ""

        posters_page = requests.get(full_link, timeout=5)
        if posters_page.ok:
            soup = BeautifulSoup(posters_page.text, 'html.parser')
            cont_poster_link = soup.find('img', class_="lazy")
            return cont_poster_link['data-src'] if cont_poster_link else ""

    def _write_img_on_disk(self, url: requests.Response) -> bool:
        """Writes image to disk.

        Args:
            url (requests.Response): Image link.

        Returns:
            bool: Success or failure.
        """

        with open(self.thumb, "wb") as poster:
            poster.write(url.content)

        res = modify_raw_poster(self.thumb)
        if not res:
            return False
        return True

    @staticmethod
    def get_actors(page: wikipedia.WikipediaPage) -> list[str]:
        """Retrieves movie's actors from the wikipedia page.

        Args:
            page (wikipedia.WikipediaPage): Wikipedia page.

        Returns:
            list[str]: Actors in a list.
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
        """Downloads movie poster.

        Returns:
            bool: Success or failure.
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

    def download_cnm_poster(self) -> bool:
        """Downloads movie poster.

        Returns:
            bool: Success or failure.
        """

        cnm_link = self.generate_cnm_link()
        if not cnm_link:
            return False

        resp = requests.get(cnm_link, timeout=7)
        if resp.ok:
            value = self._write_img_on_disk(resp)
            return value

    def download_info(self) -> bool:
        """Downloads movie info using wikipedia module.

        Returns:
            bool: Success or failure.
        """

        if self.data_file.exists():
            return True

        official_title = f"{self.title.title()} ({self.year})"
        summary = "The summary could not be retrieved, movie title may be incomplete, incorrect or too vague"
        movie_gse = None
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
                summary = wikipedia.summary(query, 3)
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
                movie_gse = summary.split('.')[0].casefold().replace(self.title.casefold(), '')

        genres = [mov_genre for mov_genre in constants.MOVIE_GENRES if movie_gse and mov_genre.casefold() in movie_gse]
        data = {"title": official_title, "summary": summary, "actors": actors, "genre": genres}

        with open(self.data_file, 'w', encoding="UTF-8") as file:
            json.dump(data, file, indent=4)

        if not self.data_file.exists():
            return False
        return True
