from pathlib import Path

from PySide6 import QtWidgets
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtGui import QPixmap, QIcon


CURRENT_DIR = Path(__file__).resolve().parent
RESOURCES_DIR = Path.joinpath(CURRENT_DIR, "resources")
ICONS_DIR = Path.joinpath(RESOURCES_DIR, "icons")


class PyMoman(QtWidgets.QWidget):

    def __init__(self):

        super().__init__()

        self.setWindowTitle("PyMoman")
        self.setFixedSize(950, 450)
        self.manage_layouts_and_frames()
        self.manage_widgets()
        self.load_icons()
        self.apply_style()


    def manage_layouts_and_frames(self):

        self.mov_frm = QtWidgets.QFrame()
        self.mov_frm.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.header_layout = QtWidgets.QHBoxLayout()
        self.body_layout = QtWidgets.QHBoxLayout()
        self.menu_layout = QtWidgets.QVBoxLayout()
        self.list_layout = QtWidgets.QVBoxLayout()
        self.list_layout.setContentsMargins(10, 0, 0, 0)
        self.gmovie_layout = QtWidgets.QHBoxLayout()
        self.mov_frm_layout = QtWidgets.QHBoxLayout(self.mov_frm)

        self.main_layout.addLayout(self.header_layout)
        self.main_layout.addLayout(self.body_layout)
        self.body_layout.addLayout(self.menu_layout)
        self.body_layout.addLayout(self.list_layout)
        self.body_layout.addLayout(self.gmovie_layout)
        self.gmovie_layout.addWidget(self.mov_frm)


    def manage_widgets(self):

        self.btn_create_col = QtWidgets.QPushButton("Create collection")
        self.btn_save_col = QtWidgets.QPushButton("Save collection")
        self.btn_scan_dir = QtWidgets.QPushButton("Scan directory")
        self.btn_add_movie = QtWidgets.QPushButton("Add movie")
        self.btn_remove_movie = QtWidgets.QPushButton("Remove movie")
        self.label_filter = QtWidgets.QLabel(f"{12 * '-'} Filter {12 * '-'}")
        self.label_filter.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.cbb_genre = QtWidgets.QComboBox()
        self.cbb_genre.addItem('Genre')
        self.cbb_actors = QtWidgets.QComboBox()
        self.cbb_actors.addItem('Actors')
        self.progress_bar = QtWidgets.QProgressBar()
        self.progress_bar.setFixedHeight(5)
        self.progress_bar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.le_search = QtWidgets.QLineEdit()
        self.le_search.setClearButtonEnabled(True)
        self.le_search.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.le_search.setPlaceholderText("Search")
        self.lw_main = QtWidgets.QListWidget()
        self.lw_main.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

        self.header_layout.addWidget(self.btn_create_col)
        self.header_layout.addWidget(self.btn_save_col)
        self.header_layout.addWidget(self.btn_scan_dir)
        self.menu_layout.addWidget(self.btn_add_movie)
        self.menu_layout.addWidget(self.btn_remove_movie)
        self.menu_layout.addWidget(self.label_filter)
        self.menu_layout.addWidget(self.cbb_genre)
        self.menu_layout.addWidget(self.cbb_actors)
        self.menu_layout.addWidget(self.progress_bar)
        self.list_layout.addWidget(self.le_search)
        self.list_layout.addWidget(self.lw_main)


    def load_icons(self):

        application_logo = QPixmap(str(RESOURCES_DIR / "logo.png"))
        btn_create_col_icon = QPixmap(str(ICONS_DIR / "create_collection.png"))
        btn_save_col_icon = QPixmap(str(ICONS_DIR / "save.png"))
        btn_scan_dir_icon = QPixmap(str(ICONS_DIR / "scan_folder.png"))
        btn_add_movie_icon = QPixmap(str(ICONS_DIR / "add_item.png"))
        btn_remove_movie_icon = QPixmap(str(ICONS_DIR / "remove_item.png"))
        le_search_icon = QIcon(str(ICONS_DIR / "search.png"))

        self.setWindowIcon(application_logo)
        self.btn_create_col.setIcon(btn_create_col_icon)
        self.btn_save_col.setIcon(btn_save_col_icon)
        self.btn_scan_dir.setIcon(btn_scan_dir_icon)
        self.btn_add_movie.setIcon(btn_add_movie_icon)
        self.btn_remove_movie.setIcon(btn_remove_movie_icon)
        self.le_search.addAction(le_search_icon, self.le_search.ActionPosition.LeadingPosition)


    def apply_style(self):

        style = Path.joinpath(RESOURCES_DIR, "style.qss")
        with open(style, 'r', encoding="UTF-8") as style_file:
            self.setStyleSheet(style_file.read())


if __name__ == '__main__':

    root = QtWidgets.QApplication()
    application = PyMoman()
    application.show()
    root.exec()
