"""
This module contains the definition of ScraperThread, a QThread subclass designed
to execute methods on a MovieScraper object in a separate thread. The thread signals
when it finishes or encounters an error.
"""


from typing import List, Tuple, Any

from PySide6.QtCore import QThread, Signal

from packages.logic.dataretrieve import MovieScraper


class ScraperThread(QThread):

    thread_finished = Signal()
    thread_failed = Signal(str)

    def __init__(self):
        super().__init__()

        self._movie_scraper_object = None
        self._methods_to_call: List[Tuple[str, Any]] = []

    def define_thread_settings(self, *args: Any) -> None:
        """Configure the thread settings.

        Args:
            *args: The first argument should be an instance of MovieScraper.
                   Subsequent arguments should be tuples (method_name, argument).

        Raises:
            ValueError: If the arguments are not correctly formatted.
        """

        if not len(args) >= 2 and all(isinstance(item, tuple) for item in args[1:]):
            raise ValueError("At least two arguments are required, with methods in tuple form (method, argument).")

        self._movie_scraper_object = args[0] if isinstance(args[0], MovieScraper) else None
        self._methods_to_call = list(filter(lambda x: hasattr(self._movie_scraper_object, x[0]), args[1:]))

    def run(self) -> None:

        if self._movie_scraper_object is None:
            self.thread_failed.emit("MovieScraper object is not defined.")
            return

        processes: list = [(getattr(self._movie_scraper_object, method), arg) for method, arg in self._methods_to_call]

        for process, argument in processes:

            try:
                process(argument) if argument is not None else process()

            except Exception as error:
                self.thread_failed.emit(str(error))
                return

        self.thread_finished.emit()
