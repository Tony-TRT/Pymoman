"""
This module loads a link in a small browser.
"""

from PySide6.QtWidgets import QGridLayout
from PySide6.QtCore import QUrl, Qt
from PySide6.QtWebEngineWidgets import QWebEngineView

from packages.logic.movie import Movie
from packages.ui.aesthetic import AestheticWindow


class MiniBrowser(AestheticWindow):

    def __init__(self, movie: Movie = None, content: str = "trailer", one_url: QUrl = None):
        super().__init__()

        self.setWindowTitle("Python Movie Manager - Mini Browser")
        self.setFixedSize(900, 400)
        self.setAttribute(Qt.WA_DeleteOnClose)

        url = ''
        if one_url:
            url = one_url
        elif movie and movie.data_file.exists():
            url = QUrl(movie.load_data_file().get(content))

        self.url = url if url else None

        ##################################################
        # Layouts.
        ##################################################

        self.main_layout = QGridLayout(self)

        ##################################################
        # Widgets.
        ##################################################

        self.browser = QWebEngineView()

        if self.url is not None:
            self.browser.load(self.url)

        ##################################################

        self.main_layout.addWidget(self.browser, 0, 0, 1, 1)
        self.ui_manage_icons()
