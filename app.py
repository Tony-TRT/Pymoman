from pathlib import Path
from functools import partial
from time import sleep

from PySide6 import QtWidgets
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtGui import QPixmap, QIcon, QAction
from PySide6.QtCore import Qt, QEvent

from package.collection import Collection
from package.movie import Movie

CURRENT_DIR = Path(__file__).resolve().parent
RESOURCES_DIR = Path.joinpath(CURRENT_DIR, "resources")
ICONS_DIR = Path.joinpath(RESOURCES_DIR, "icons")


class PyMoman(QtWidgets.QWidget):
    all_collections: list[Collection] = Collection.retrieve_collections()
    last_collection_opened: list[Collection] = []

    def __init__(self):

        super().__init__()

        self.setWindowTitle("PyMoman")
        self.setFixedSize(950, 450)
        self.ui_manage_layouts_and_frames()
        self.ui_manage_widgets()
        self.ui_load_icons()
        self.ui_apply_style()
        self.logic_connect_widgets()
        self.logic_display_collections()

    def ui_manage_layouts_and_frames(self):

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

    def ui_manage_widgets(self):

        self.btn_create_col = QtWidgets.QPushButton("Create collection")
        self.btn_save_col = QtWidgets.QPushButton("Save all collections")
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
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setFixedHeight(5)
        self.progress_bar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.le_search = QtWidgets.QLineEdit()
        self.le_search.setClearButtonEnabled(True)
        self.le_search.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.le_search.setPlaceholderText("Search")
        self.lw_main = QtWidgets.QListWidget()
        self.lw_main.installEventFilter(self)
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

    def ui_load_icons(self):

        application_logo = QPixmap(str(RESOURCES_DIR / "logo.png"))
        self.note_icon = QPixmap(str(ICONS_DIR / "create_collection.png"))
        self.save_icon = QPixmap(str(ICONS_DIR / "save.png"))
        self.open_icon = QPixmap(str(ICONS_DIR / "folder.png"))
        self.collection_icon = QPixmap(str(ICONS_DIR / "collection.png"))
        self.movie_icon = QPixmap(str(ICONS_DIR / "movie.png"))
        btn_add_movie_icon = QPixmap(str(ICONS_DIR / "add_item.png"))
        btn_remove_movie_icon = QPixmap(str(ICONS_DIR / "remove_item.png"))
        le_search_icon = QIcon(str(ICONS_DIR / "search.png"))
        self.previous_icon = QIcon(str(ICONS_DIR / "previous.png"))
        self.export_icon = QIcon(str(ICONS_DIR / "export.png"))
        self.delete_icon = QIcon(str(ICONS_DIR / "delete.png"))

        self.setWindowIcon(application_logo)
        self.btn_create_col.setIcon(self.note_icon)
        self.btn_save_col.setIcon(self.save_icon)
        self.btn_scan_dir.setIcon(self.open_icon)
        self.btn_add_movie.setIcon(btn_add_movie_icon)
        self.btn_remove_movie.setIcon(btn_remove_movie_icon)
        self.le_search.addAction(le_search_icon, self.le_search.ActionPosition.LeadingPosition)

    def ui_apply_style(self):

        style = Path.joinpath(RESOURCES_DIR, "style.qss")
        with open(style, 'r', encoding="UTF-8") as style_file:
            self.setStyleSheet(style_file.read())

    def logic_connect_widgets(self):

        self.btn_create_col.clicked.connect(self.logic_create_collection)
        self.btn_save_col.clicked.connect(self.logic_save_collection)
        self.btn_add_movie.clicked.connect(self.logic_add_movie)
        self.btn_remove_movie.clicked.connect(self.logic_remove_movie)
        self.lw_main.itemClicked.connect(self.logic_go_back)

    def logic_create_collection(self):

        name, val = QtWidgets.QInputDialog.getText(self, "New collection", "Enter name:")
        if name and name not in [col.name for col in PyMoman.all_collections] and val:
            new_collection = Collection(name)
            PyMoman.all_collections.append(new_collection)
            self.logic_display_collections()

    def logic_open_collection(self, open_collection: Collection):

        PyMoman.last_collection_opened.clear()
        PyMoman.last_collection_opened.append(open_collection)
        self.logic_display_movies(open_collection)

    def logic_save_collection(self, collection_to_save: Collection):

        self.progress_bar.setValue(50)
        sleep(0.3)

        if isinstance(self.sender(), QtWidgets.QPushButton):
            for collection in PyMoman.all_collections:
                collection.save()
        else:
            collection_to_save.save()

        self.logic_display_collections()

        self.progress_bar.setValue(100)
        sleep(0.4)
        self.progress_bar.setValue(0)

    def logic_rename_collection(self, collection_to_rename: Collection):

        n_name, val = QtWidgets.QInputDialog.getText(self, "Rename collection", "Enter new name:")
        if n_name and n_name not in [col.name for col in PyMoman.all_collections] and val:
            collection_to_rename.rename(n_name)
            self.logic_display_collections()

    def logic_export_collection(self, collection_to_export: Collection):

        dialog = QtWidgets.QFileDialog.getSaveFileName(self, 'PyMoman - Save text file')
        if dialog[0]:
            collection_to_export.export_as_txt(Path(f"{dialog[0]}.txt"))

    def logic_delete_collection(self, collection_to_delete: Collection):

        val = collection_to_delete.remove()

        if val:
            PyMoman.all_collections.remove(collection_to_delete)
            del collection_to_delete

            self.logic_display_collections()

    def logic_display_collections(self):

        self.lw_main.clear()
        self.last_collection_opened.clear()
        for collection in PyMoman.all_collections:
            lw_item = QtWidgets.QListWidgetItem(collection.name)
            lw_item.attr = collection
            lw_item.setTextAlignment(Qt.AlignCenter)
            if lw_item.attr.path.exists():
                lw_item.setIcon(self.collection_icon)
            self.lw_main.addItem(lw_item)

    def logic_go_back(self, clicked_item):

        if clicked_item.text() == "GO BACK":
            self.logic_display_collections()

    def logic_add_movie(self) -> bool:

        if not PyMoman.last_collection_opened:
            return False

        collection = PyMoman.last_collection_opened[0]
        title, val = QtWidgets.QInputDialog.getText(self, f"{collection} - Add a movie", "Enter movie title:")
        if title and title not in collection.mov_lst and val:
            collection.add_movie(title)
            self.logic_display_movies(collection)
            return True

    def logic_remove_movie(self) -> bool:

        if not PyMoman.last_collection_opened:
            return False

        collection = PyMoman.last_collection_opened[0]

        try:
            movie_to_remove = self.lw_main.selectedItems()[0].attr
        except AttributeError:
            return False
        except IndexError:
            return False
        else:
            if isinstance(movie_to_remove, Movie):
                collection.remove_movie(movie_to_remove.title)
                del movie_to_remove
                self.logic_display_movies(collection)
                return True

    def logic_display_movies(self, open_collection: Collection):

        self.lw_main.clear()
        previous_item = QtWidgets.QListWidgetItem("GO BACK")
        previous_item.setTextAlignment(Qt.AlignCenter)
        previous_item.setIcon(self.previous_icon)
        self.lw_main.addItem(previous_item)

        for movie in open_collection.mov_lst:
            movie = Movie(movie)
            lw_item = QtWidgets.QListWidgetItem(movie.title)
            lw_item.attr = movie
            lw_item.setTextAlignment(Qt.AlignCenter)
            lw_item.setIcon(self.movie_icon)
            self.lw_main.addItem(lw_item)

    def eventFilter(self, watched, event: QEvent) -> bool:

        if event.type() == QEvent.ContextMenu and watched is self.lw_main:
            list_item = watched.itemAt(event.pos())

            try:
                list_item.attr
            except AttributeError:
                # Prevents harmless console errors
                list_item = QtWidgets.QListWidgetItem("")
                list_item.attr = None

            collection_menu = QtWidgets.QMenu(self)

            open_col = QAction(self.open_icon, "Open")
            open_col.triggered.connect(partial(self.logic_open_collection, list_item.attr))

            save = QAction(self.save_icon, "Save")
            save.triggered.connect(partial(self.logic_save_collection, list_item.attr))

            rename = QAction(self.note_icon, "Rename")
            rename.triggered.connect(partial(self.logic_rename_collection, list_item.attr))

            export = QAction(self.export_icon, "Export as text")
            export.triggered.connect(partial(self.logic_export_collection, list_item.attr))

            delete = QAction(self.delete_icon, "Delete")
            delete.triggered.connect(partial(self.logic_delete_collection, list_item.attr))

            collection_menu.addAction(open_col)
            collection_menu.addAction(save)
            collection_menu.addAction(rename)
            collection_menu.addAction(export)
            collection_menu.addAction(delete)

            if isinstance(list_item.attr, Collection):
                collection_menu.exec(event.globalPos())
                return True

        return super().eventFilter(watched, event)


if __name__ == '__main__':
    root = QtWidgets.QApplication()
    application = PyMoman()
    application.show()
    root.exec()
