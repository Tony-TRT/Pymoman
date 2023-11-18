"""
This module allows loading an embedded YouTube video in a QWebEngineView.
"""


from PySide6.QtWidgets import QGridLayout
from PySide6.QtCore import QUrl
from PySide6.QtWebEngineWidgets import QWebEngineView


from packages.logic.movie import Movie
from packages.ui.aesthetic import AestheticWindow


class MiniBrowser(AestheticWindow):

    def __init__(self, movie: Movie):
        super().__init__()

        self.setWindowTitle("Python Movie Manager - Trailer Viewer")
        self.setFixedSize(900, 400)

        url = ''
        if movie.data_file.exists():
            url = movie.load_data_file().get('trailer')

        self.url = QUrl(url) if url else None

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
