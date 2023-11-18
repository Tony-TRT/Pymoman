"""
This module is dedicated to retrieving information from the internet.
It provides functions and tools to access and gather data from various online sources.
The information retrieved and the manner in which it is retrieved is legal and tries as much as possible
to respect the source websites by deliberately slowing down the program.
"""


import json
import re
from random import shuffle
from time import sleep


import requests
import wikipedia
from bs4 import BeautifulSoup


from packages.constants import constants
from packages.logic.dataprocess import modify_raw_poster
from packages.logic.movie import Movie


class MovieScraper(Movie):
    """MovieScraper object can process input and retrieve information"""

    sources_websites: dict = {
        "SA": "http://www.impawards.com/",
        "SB": "https://www.movieposterdb.com/",
        "SC": "https://www.cinematerial.com/",
        "SD": "https://www.youtube.com/"
    }

    def __init__(self, movie: Movie):
        super().__init__(movie.title, movie.year)

        self.headers: dict = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/114.0.0.0 Mobile Safari/537.36'
        }

        self.storage.mkdir(exist_ok=True, parents=True)

    def download_info(self) -> None:
        """Gathers information about the movie, such as title, summary, actors, genre and trailer link.

        Returns:
            None: None.
        """

        if self.data_file.exists():
            return

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
        data = {
            "title": official_title,
            "summary": summary,
            "actors": actors,
            "genre": genres,
            "trailer": self.get_youtube_link()
        }

        with open(self.data_file, 'w', encoding="UTF-8") as file:
            json.dump(data, file, indent=4)

    def download_poster(self, override=False) -> None:
        """Downloads movie poster.

        Args:
            override (bool): True = replace current poster, False = do not replace current poster.

        Returns:
            None: None.
        """

        if self.thumb.exists() and not override:
            return

        links = self.generate_cnm_link() + self.generate_imp_links() + self.generate_movie_pdb_link()
        shuffle(links)

        for link in links:
            response = requests.get(link, headers=self.headers, timeout=10)
            if response.status_code == 200:
                self._write_img_to_disk(response)
                break
            else:
                sleep(3)
                continue

    def generate_cnm_link(self) -> list[str]:
        """Generates CineMaterial download link.

        Returns:
            list[str]: Link in a list.
        """

        sanitized_title: str = self.title.lower().replace(' ', '+')
        results_page_link: str = f"{self.sources_websites.get('SC')}search?q={sanitized_title}"
        results_page = requests.get(results_page_link, headers=self.headers, timeout=10)

        if results_page.status_code == 200:
            cnm_soup = BeautifulSoup(results_page.text, 'html.parser')
            div_element = cnm_soup.find('div', class_='table-responsive')
            td_element = div_element.find_all('td')[1] if div_element and len(div_element.find_all('td')) >= 2 else None
            page_link = td_element.find('a')['href'] if td_element and td_element.find('a') else ''
            full_link: str = f"{self.sources_websites.get('SC')}{page_link[1:] if page_link else ''}"
            posters_page = requests.get(full_link, headers=self.headers, timeout=10)

            if full_link != self.sources_websites.get('SC') and posters_page.status_code == 200:
                soup = BeautifulSoup(posters_page.text, 'html.parser')
                cont_poster_link = soup.find('img', class_="lazy")
                return [cont_poster_link.get('data-src')] if cont_poster_link else []
        return []

    def generate_imp_links(self) -> list[str]:
        """Generates IMP Awards download links.

        Returns:
            list[str]: Links in a list.
        """

        imp_suffixes: set = {
            "_ver2", "_ver3", "_ver4",
            "_ver5", "_ver6", "_ver7",
            "_ver8", "_ver9", "_ver10",
            "_xlg", "_xxlg"
        }
        sanitized_title: str = self.title.strip().lower().replace(' ', '_')
        sanitized_title: str = sanitized_title[4:] if sanitized_title.startswith('the_') else sanitized_title
        def_imp_link: str = f"{MovieScraper.sources_websites.get('SA')}{self.year}/posters/{sanitized_title}.jpg"
        links: list[str] = [f"{def_imp_link[:-4]}{suffix}.jpg" for suffix in imp_suffixes]
        links.insert(0, def_imp_link)

        return links

    def generate_movie_pdb_link(self) -> list[str]:
        """Generates MoviePosterDB download link.

        Returns:
            list[str]: Link in a list.
        """

        sanitized_title: str = self.title.lower().replace(' ', '%20')
        url: str = f"{MovieScraper.sources_websites.get('SB')}search?q={sanitized_title}&imdb=0"

        page = requests.get(url, headers=self.headers, timeout=10)

        if page.status_code == 200:
            pdb_soup = BeautifulSoup(page.text, 'html.parser')
            img_cont = pdb_soup.find(class_='vertical-image img-responsive poster_img lazyload')
            return [img_cont.get('data-src')] if img_cont else []
        return []

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

    def get_youtube_link(self) -> str:
        """Generates an embedded YouTube link corresponding to the movie trailer.
        Regex used here comes from a YouTube video by CodeFather.

        Returns:
            str: Embedded YouTube link.
        """

        sanitized_query = f"{self.title.strip().replace(' ', '+')}+{self.year}"
        base_link = f"{self.sources_websites.get('SD')}embed/"
        page = f"{self.sources_websites.get('SD')}results?search_query={sanitized_query}+trailer"

        response = requests.get(page, timeout=10)

        if response.status_code == 200:
            identifiers: list[str] = re.findall(r"watch\?v=(\S{11})", response.text)
        else:
            identifiers: list[str] = []

        if not (identifiers and len(identifiers[0]) == 11):
            return ""

        return base_link + identifiers[0]

    def _write_img_to_disk(self, url: requests.Response) -> None:
        """Writes image to disk.

        Args:
            url (requests.Response): Image link.

        Returns:
            None: None.
        """

        with open(self.thumb, "wb") as poster:
            poster.write(url.content)

        modify_raw_poster(self.thumb)
