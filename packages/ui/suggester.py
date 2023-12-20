import threading
from functools import partial

from PySide6 import QtWidgets
from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QPixmap

from packages.logic import recommendations
from packages.ui.aesthetic import AestheticWindow
from packages.ui.minibrowser import MiniBrowser


class RecPanel(AestheticWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Python Movie Manager - Movie Suggestions")
        self.setFixedSize(900, 420)
        self.recommendations: dict = recommendations.retrieve_information_from_files()

        ##################################################
        # Layouts.
        ##################################################

        self.main_layout = None
        self.header_layout = None
        self.titles_layout = None
        self.posters_layout = None
        self.buttons_layout = None

        ##################################################
        # Widgets.
        ##################################################

        self.mini_browser = None
        self.main_label = None

        self.images: dict = {}
        self.buttons: dict = {}

        for index, (path, (title, url)) in enumerate(self.recommendations.items()):

            # Movie posters
            image = QPixmap(path)
            image_label = QtWidgets.QLabel()
            image_label.setPixmap(image)
            image_label.setToolTip(title)
            image_label.setAlignment(Qt.AlignCenter)

            # Buttons
            button = QtWidgets.QPushButton("Watch Trailer")
            button.link = QUrl(url)

            key: str = "Movie {}".format(index + 1)
            self.images[key] = image_label
            self.buttons[key] = button

        ##################################################

        if self.recommendations:
            self.ui_manage_layouts()
            self.ui_manage_widgets()
            self.ui_manage_icons()
            self.logic_connect_widgets()
            self.show()

        threading.Thread(target=recommendations.main, daemon=True).start()

    def logic_connect_widgets(self) -> None:
        """Connections are managed here.

        Returns:
            None: None.
        """

        for button in self.buttons.values():
            button.clicked.connect(partial(self.logic_mini_browser, button.link))

    def logic_mini_browser(self, url: QUrl) -> None:
        """Instantiates a small browser that loads a link.

        Args:
            url (QUrl): Link to load.

        Returns:
            None: None.
        """

        self.mini_browser = MiniBrowser(one_url=url)
        self.mini_browser.show()

    def ui_manage_icons(self) -> None:
        """Icons are managed here.

        Returns:
            None: None.
        """

        super().ui_manage_icons()
        for button in self.buttons.values():
            button.setIcon(self.icons.get('trailer'))

    def ui_manage_layouts(self) -> None:
        """Layouts are managed here.

        Returns:
            None: None.
        """

        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.header_layout = QtWidgets.QHBoxLayout()
        self.titles_layout = QtWidgets.QHBoxLayout()
        self.posters_layout = QtWidgets.QHBoxLayout()
        self.buttons_layout = QtWidgets.QHBoxLayout()

        self.main_layout.addLayout(self.header_layout)
        self.main_layout.addLayout(self.titles_layout)
        self.main_layout.addLayout(self.posters_layout)
        self.main_layout.addLayout(self.buttons_layout)

    def ui_manage_widgets(self) -> None:
        """Widgets are managed here.

        Returns:
            None: None.
        """

        self.main_label = QtWidgets.QLabel("You might like these movies!\n(hover to see title)")
        self.main_label.setFont(self.default_font_big)
        self.main_label.setAlignment(Qt.AlignCenter)

        self.header_layout.addWidget(self.main_label)
        for i in range(1, 4):
            self.posters_layout.addWidget(self.images.get(f'Movie {i}'))
            self.buttons_layout.addWidget(self.buttons.get(f'Movie {i}'))
