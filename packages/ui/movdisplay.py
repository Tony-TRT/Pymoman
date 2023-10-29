from pathlib import Path

import wikipedia
from PySide6 import QtWidgets

BASE_DIR = Path(__file__).resolve().parent.parent.parent
RESOURCES_DIR = Path.joinpath(BASE_DIR, "resources")


class MovieTagDisplay(QtWidgets.QWidget):

    def __init__(self):

        super(MovieTagDisplay, self).__init__()

        self.ui_manage_layouts()
        self.ui_manage_widgets()

    def ui_manage_layouts(self):

        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.poster_layout = QtWidgets.QVBoxLayout()
        self.info_layout = QtWidgets.QVBoxLayout()

        self.main_layout.addLayout(self.poster_layout)
        self.main_layout.addLayout(self.info_layout)

    def ui_manage_widgets(self):

        self.poster_label = QtWidgets.QLabel()
        self.rating_label = QtWidgets.QLabel()
        self.cbb_lang = QtWidgets.QComboBox()
        self.cbb_lang.addItem("Choose language")
        self.cbb_lang.addItems(wikipedia.languages())
        self.title_label = QtWidgets.QLabel()
        self.summary_label = QtWidgets.QLabel()

        self.poster_layout.addWidget(self.poster_label)
        self.poster_layout.addWidget(self.rating_label)
        self.info_layout.addWidget(self.cbb_lang)
        self.info_layout.addWidget(self.title_label)
        self.info_layout.addWidget(self.summary_label)
