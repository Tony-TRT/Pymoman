"""This module contains a custom window.

Features:
    - Allows users to add movies to their collection.
    - Provides options for tagging movies to facilitate organization.
"""

from PySide6 import QtWidgets

from packages.ui.aesthetic import AestheticWindow


class MovieAppender(AestheticWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Add a movie")
        self.setFixedSize(500, 250)

        ##################################################
        # Layouts.
        ##################################################

        self.main_layout = QtWidgets.QVBoxLayout(self)

        ##################################################
        # Widgets.
        ##################################################

        self.le_movie_title = None
        self.lbl_year = None
        self.le_movie_year = None
        self.lbl_movie_rating = None
        self.cbb_movie_rating = None
        self.btn_validate = None

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
        self.btn_validate.setIcon(self.icons.get('save'))

    def ui_manage_widgets(self) -> None:
        """Widgets are managed here.

        Returns:
            None: None.
        """

        self.le_movie_title = QtWidgets.QLineEdit()
        self.le_movie_title.setPlaceholderText("Enter movie title here (Required)")
        self.lbl_year = QtWidgets.QLabel("Release year is essential for internet data collection")
        self.le_movie_year = QtWidgets.QLineEdit()
        self.le_movie_year.setPlaceholderText("Year the movie was released (Required)")
        self.lbl_movie_rating = QtWidgets.QLabel("Rate the movie (Optional)")
        self.cbb_movie_rating = QtWidgets.QComboBox()
        self.cbb_movie_rating.addItems(["-", '1', '2', '3', '4', '5'])
        self.btn_validate = QtWidgets.QPushButton("Validate")

        self.main_layout.addWidget(self.le_movie_title)
        self.main_layout.addWidget(self.lbl_year)
        self.main_layout.addWidget(self.le_movie_year)
        self.main_layout.addWidget(self.lbl_movie_rating)
        self.main_layout.addWidget(self.cbb_movie_rating)
        self.main_layout.addWidget(self.btn_validate)

    def closeEvent(self, event):

        self.le_movie_title.clear()
        self.le_movie_year.clear()
        self.cbb_movie_rating.setCurrentIndex(0)
        super().closeEvent(event)
