import threading

from PySide6 import QtWidgets
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QPixmap

from packages.logic import recommendations
from packages.ui.aesthetic import AestheticWindow


class RecPanel(AestheticWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Python Movie Manager - Movie Suggestions")
        self.setFixedSize(900, 460)
        self.recommendations: dict = recommendations.retrieve_information_from_files()

        ##################################################
        # Layouts.
        ##################################################

        self.main_layout = None
        self.header = None
        self.body = None
        self.rec_01 = None
        self.rec_02 = None
        self.rec_03 = None

        self.ui_manage_layouts()

        ##################################################
        # Widgets.
        ##################################################

        self.main_label = None

        self.lbl_titles: dict = {}
        self.pxp_posters: dict = {}
        self.mov_buttons: dict = {}
        self.mov_urls: dict = {}

        for index, (path, (title, url)) in enumerate(self.recommendations.items()):

            # Movie titles
            label = QtWidgets.QLabel(title.upper())
            label.setAlignment(Qt.AlignCenter)

            # Movie posters
            pixmap = QPixmap(path)
            pixmap_label = QtWidgets.QLabel()
            pixmap_label.setPixmap(pixmap)
            pixmap_label.setAlignment(Qt.AlignCenter)

            # Buttons
            button = QtWidgets.QPushButton("Watch Trailer")

            # Trailer links
            link = QUrl(url)

            key = f"Movie {index + 1}"

            self.lbl_titles[key] = label
            self.pxp_posters[key] = pixmap_label
            self.mov_buttons[key] = button
            self.mov_urls[key] = link

        self.ui_manage_widgets()

        ##################################################
        # Icons.
        ##################################################

        self.ui_manage_icons()

    def ui_manage_icons(self) -> None:
        """Icons are managed here.

        Returns:
            None: None.
        """

        super().ui_manage_icons()

    def ui_manage_layouts(self) -> None:
        """Layouts are managed here.

        Returns:
            None: None.
        """

        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.header = QtWidgets.QHBoxLayout()
        self.body = QtWidgets.QHBoxLayout()
        self.rec_01 = QtWidgets.QVBoxLayout()
        self.rec_02 = QtWidgets.QVBoxLayout()
        self.rec_03 = QtWidgets.QVBoxLayout()

        self.main_layout.addLayout(self.header)
        self.main_layout.addLayout(self.body)
        self.body.addLayout(self.rec_01)
        self.body.addLayout(self.rec_02)
        self.body.addLayout(self.rec_03)

    def ui_manage_widgets(self) -> None:
        """Widgets are managed here.

        Returns:
            None: None.
        """

        self.main_label = QtWidgets.QLabel("You might like these movies")
        self.main_label.setFont(self.default_font_big)
        self.main_label.setAlignment(Qt.AlignCenter)

        self.header.addWidget(self.main_label)
        self.rec_01.addWidget(self.lbl_titles.get('Movie 1'))
        self.rec_01.addWidget(self.pxp_posters.get('Movie 1'))
        self.rec_01.addWidget(self.mov_buttons.get('Movie 1'))
        self.rec_02.addWidget(self.lbl_titles.get('Movie 2'))
        self.rec_02.addWidget(self.pxp_posters.get('Movie 2'))
        self.rec_02.addWidget(self.mov_buttons.get('Movie 2'))
        self.rec_03.addWidget(self.lbl_titles.get('Movie 3'))
        self.rec_03.addWidget(self.pxp_posters.get('Movie 3'))
        self.rec_03.addWidget(self.mov_buttons.get('Movie 3'))
