from pathlib import Path

from PySide6 import QtWidgets
from PySide6.QtGui import QPixmap

BASE_DIR = Path(__file__).resolve().parent.parent.parent
RESOURCES_DIR = Path.joinpath(BASE_DIR, "resources")


class MovieTagDialog(QtWidgets.QWidget):

    def __init__(self):

        super(MovieTagDialog, self).__init__()

        self.setWindowTitle(f"Add a movie")
        self.setFixedSize(500, 250)
        self.ui_manage_layouts()
        self.ui_manage_widgets()
        self.ui_load_icons()
        self.ui_apply_style()

    def ui_manage_layouts(self):

        self.main_layout = QtWidgets.QVBoxLayout(self)

    def ui_manage_widgets(self):

        self.le_movie_title = QtWidgets.QLineEdit()
        self.le_movie_title.setPlaceholderText("Enter movie title here (Required)")
        self.year_label = QtWidgets.QLabel("Year of release is required in order to collect information from the internet")
        self.le_movie_year = QtWidgets.QLineEdit()
        self.le_movie_year.setPlaceholderText("Year the movie was released (Required)")
        self.movie_rating_label = QtWidgets.QLabel("Rate the movie (Optional)")
        self.cbb_movie_rating = QtWidgets.QComboBox()
        self.cbb_movie_rating.addItems(["---", '1', '2', '3', '4', '5'])
        self.btn_validate = QtWidgets.QPushButton("Validate")

        self.main_layout.addWidget(self.le_movie_title)
        self.main_layout.addWidget(self.year_label)
        self.main_layout.addWidget(self.le_movie_year)
        self.main_layout.addWidget(self.movie_rating_label)
        self.main_layout.addWidget(self.cbb_movie_rating)
        self.main_layout.addWidget(self.btn_validate)

    def ui_load_icons(self):

        application_logo = QPixmap(str(RESOURCES_DIR / "logo.png"))
        save_icon = QPixmap(str(RESOURCES_DIR / "icons" / "save.png"))

        self.setWindowIcon(application_logo)
        self.btn_validate.setIcon(save_icon)

    def ui_apply_style(self):

        style = Path.joinpath(RESOURCES_DIR, "style.qss")
        with open(style, 'r', encoding="UTF-8") as style_file:
            self.setStyleSheet(style_file.read())
