"""
This module is dedicated to retrieving information from the internet.
It provides functions and tools to access and gather data from various online sources.
The information retrieved and the manner in which it is retrieved is legal and tries as much as possible
to respect the source websites by deliberately slowing down the program.
"""

import re
import json
from pathlib import Path
from random import shuffle
from time import sleep

import requests
import wikipedia as wiki
from bs4 import BeautifulSoup

from packages.constants import constants
from packages.logic.data_process import modify_raw_poster
from packages.logic.movie import Movie


class MovieScraper(Movie):
    """MovieScraper object can process input and retrieve information"""

    sources_websites: dict = {
        "SA": "http://www.impawards.com/",
        "SB": "https://www.movieposterdb.com/",
        "SC": "https://www.cinematerial.com/",
        "SD": "https://www.youtube.com/",
        "SE": "https://tastedive.com/"
    }

    def __init__(self, movie: Movie):
        super().__init__(movie.title, movie.year)

        self.headers: dict = {
            'User-Agent': 'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/114.0.0.0 Mobile Safari/537.36'
        }

        self.storage.mkdir(exist_ok=True, parents=True)

    def download_info(self) -> None:
        """Gathers information about the movie. This information is then stored in a json file.

        Returns:
            None: None.
        """

        if self.load_data_file():
            return

        title: str = f"{self.title.title()} ({self.year})"
        summary: str = "The summary could not be retrieved."
        actors: list[str] = []
        genre: list[str] = []
        trailer: str = self.get_youtube_link()
        imdb: str = ''

        wiki.set_lang("en")

        search_query: str = f"{self.title} {self.year}"
        page = None
        for _ in range(2):
            try:
                page = wiki.page(search_query) if page is None else page
                if summary == "The summary could not be retrieved.":
                    summary = wiki.summary(search_query, 3)
            except (wiki.exceptions.DisambiguationError, wiki.exceptions.PageError, wiki.exceptions.RedirectError):
                search_query = f"{self.title} film"
                continue
            except wiki.exceptions.HTTPTimeoutError:
                break
            else:
                title = page.title
                actors = self.get_actors(page)
                break

        sentence_containing_genres: str = summary.split('.')[0].casefold().replace(self.title.casefold(), '')
        for key, value in constants.MOVIE_GENRES.items():
            if key in sentence_containing_genres or value in sentence_containing_genres:
                genre.append(key.title())

        for link in self.generate_imp_links(end='html'):
            imdb: str = self.get_imdb_page_link(link)
            if imdb:
                sleep(1)
                break

        data_to_store: dict = {
            "title": title,
            "summary": summary,
            "actors": actors,
            "genre": genre,
            "trailer": trailer,
            "imdb": imdb
        }

        with open(self.data_file, 'w', encoding="UTF-8") as file:
            json.dump(data_to_store, file, indent=4)

    def download_poster(self, override: bool = False, dir_path=None, filename="thumb.jpg", year: bool = True) -> None:
        """Downloads movie poster.

        Args:
            override (bool): Set to True to replace existing images.
            dir_path (Path): Allows specifying a destination path for the downloaded image.
            filename (str): Allows specifying a filename for the downloaded image.
            year (bool): Set to True to include the release year in the queries. If year is uncertain, set it to False.

        Returns:
            None: None.
        """

        dir_path: Path = self.storage if dir_path is None else dir_path
        path: Path = Path.joinpath(dir_path, filename)

        if path.exists() and not override:
            return

        if year:
            links = self.generate_cnm_link() + self.generate_imp_links(end='jpg') + self.generate_movie_pdb_link()
        else:
            links = self.generate_cnm_link() + self.generate_movie_pdb_link()
        shuffle(links)

        for link in links:
            response = requests.get(link, headers=self.headers, timeout=10)
            if response.status_code == 200:
                self._write_img_to_disk(url=response, path=path)
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

    def generate_imp_links(self, end: str) -> list[str]:
        """Generates IMP Awards links.

        Args:
            end (str): End link extension, 'html' for web pages and 'jpg' for image links.

        Returns:
            list[str]: Links in a list.
        """

        imp_suffixes: set = {
            "_ver2", "_ver3", "_ver4", "_ver5", "_ver6", "_ver7",
            "_ver8", "_ver9", "_ver10", "_xlg", "_xxlg"
        }

        # Cached folder treats the movie title the same as http://www.impawards.com/ does.
        sanitized_title: str = self.storage.stem

        def_imp_link: str = f"{MovieScraper.sources_websites.get('SA')}{self.year}/posters/{sanitized_title}.{end}"
        links: list[str] = [f"{def_imp_link[:def_imp_link.index(end) - 1]}{suffix}.{end}" for suffix in imp_suffixes]
        links.insert(0, def_imp_link)

        if end == 'html':
            return [link.replace('posters/', '') for link in links]
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
    def get_actors(page: wiki.WikipediaPage) -> list[str]:
        """Retrieves movie's actors from the wikipedia page.

        Args:
            page (wikipedia.WikipediaPage): Wikipedia page.

        Returns:
            list[str]: Actors in a list.
        """

        actors: list[str] = []
        soup = BeautifulSoup(page.html(), 'html.parser')
        starring_element = soup.find('th', string='Starring')

        if starring_element:
            starring_element_parent: str = str(starring_element.parent)
            regex_pattern_a = r"title=\"[A-zÀ-ú -\.]+\">(.+?)<\/a>"
            regex_pattern_b = r"<li>([A-zÀ-ú -\.]+)<\/li>"
            regex = regex_pattern_a + '|' + regex_pattern_b
            actors: list[tuple] = re.findall(regex, starring_element_parent)
            actors: list[str] = ["".join(element) for element in actors]

        return actors

    def get_imdb_page_link(self, imp_url: str) -> str:
        """Get the movie IMDb page using http://www.impawards.com/ URL.
        (Since IMDb does not allow scripts to browse its pages.)

        Args:
            imp_url (str): http://www.impawards.com/ URL.

        Returns:
            str: IMDb link.
        """

        imdb_base_url: str = "https://www.imdb.com/title/{}/"

        response = requests.get(imp_url, headers=self.headers, timeout=10)
        if response.status_code != 200:
            return ""

        soup = BeautifulSoup(response.text, 'html.parser')
        div_elements = soup.find_all(name='div', class_="rightsidesmallbordered")
        regex = r"title/(\w{9})\""

        imdb_identifier = None
        for element in div_elements:
            element = str(element)
            if "www.imdb.com" not in element:
                continue

            imdb_identifier = re.search(regex, element)

        if imdb_identifier is not None:
            return imdb_base_url.format(imdb_identifier[1])
        return ""

    def get_recommendations(self) -> list[str]:
        """Retrieves movie titles that the user might like.

        Returns:
            list[str]: Recommendations in a list.
        """

        sanitized_title: list[str] = self.title.replace(f"({self.year})", '').strip().split()
        sanitized_title: str = '-'.join([item.title() for item in sanitized_title])
        queries: list[str] = [f"{sanitized_title}-Movie", f"{sanitized_title}-{self.year}", sanitized_title]

        response = ""
        for attempt in queries:
            url = f"{self.sources_websites.get('SE')}movies/like/{attempt}"
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code != 200:
                continue
            else:
                break

        regex = r'"recommendations":"(.*?), (.*?)?, (.*?)?"'
        recommendations = re.search(regex, response.text)

        if recommendations is None:
            return []

        valid_recommendations: list[str] = []
        for i in range(1, 4):
            suggestion: str = recommendations.group(i)
            if suggestion:
                valid_recommendations.append(suggestion.strip())

        return valid_recommendations

    def get_youtube_link(self, year: bool = True) -> str:
        """Generates an embedded YouTube link corresponding to the movie trailer.

        Args:
            year (bool): Decide whether to include the year in the YouTube query or not.

        Returns:
            str: Embedded YouTube link.
        """

        sanitized_query: str = f"{self.title.strip().replace(' ', '+')}{f'+{self.year}' if year else ''}"
        base_link: str = f"{self.sources_websites.get('SD')}embed/"
        page: str = f"{self.sources_websites.get('SD')}results?search_query={sanitized_query}+trailer"

        response = requests.get(page, timeout=10)
        if response.status_code == 200:
            regex = r"watch\?v=(\S{11})"
            identifier = re.search(regex, response.text)
        else:
            identifier = None

        if identifier:
            return base_link + identifier[1]
        return ""

    @staticmethod
    def _write_img_to_disk(url: requests.Response, path: Path) -> None:
        """Writes image to disk.

        Args:
            url (requests.Response): Image link.
            path (Path): Destination path.

        Returns:
            None: None.
        """

        with open(path, "wb") as poster:
            poster.write(url.content)

        modify_raw_poster(path)
