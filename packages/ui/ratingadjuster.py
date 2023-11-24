"""
Window to modify the rating of the movie.
"""


from PySide6 import QtWidgets


from packages.ui.aesthetic import AestheticWindow


class RatingAdjuster(AestheticWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Change rating")
        self.setFixedSize(300, 100)

        ##################################################
        # Layouts.
        ##################################################

        self.main_layout = QtWidgets.QVBoxLayout(self)

        ##################################################
        # Widgets.
        ##################################################

        self.cbb_movie_rating = None

        self.ui_manage_widgets()

        ##################################################
        # Icons.
        ##################################################

        self.ui_manage_icons()

    def ui_manage_widgets(self) -> None:
        """Widgets are managed here.

        Returns:
            None: None.
        """

        self.cbb_movie_rating = QtWidgets.QComboBox()
        self.cbb_movie_rating.addItems(["-", '1', '2', '3', '4', '5'])

        self.main_layout.addWidget(self.cbb_movie_rating)
