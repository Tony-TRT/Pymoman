import threading
from functools import partial
from pathlib import Path
from time import sleep

from PySide6 import QtWidgets
from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QPixmap, QIcon, QAction
from PySide6.QtWidgets import QSizePolicy

import packages.logic.dataimport as dti
import packages.logic.dataretrieve as dtr
import packages.logic.dataprocess as dtp
from packages.constants import constants
from packages.logic.collection import Collection
from packages.logic.movie import Movie
from packages.ui.movdisplay import MovieTagDisplay
from packages.ui.movtag import MovieTagDialog


class PyMoman(QtWidgets.QWidget):
    all_collections: list[Collection] = Collection.retrieve_collections()
    last_collection_opened: list[Collection] = []

    def __init__(self):

        super().__init__()

        dtp.clear_cache()

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
        self.global_movie_layout = QtWidgets.QHBoxLayout()
        self.mov_frm_layout = QtWidgets.QHBoxLayout(self.mov_frm)

        self.main_layout.addLayout(self.header_layout)
        self.main_layout.addLayout(self.body_layout)
        self.body_layout.addLayout(self.menu_layout)
        self.body_layout.addLayout(self.list_layout)
        self.body_layout.addLayout(self.global_movie_layout)
        self.global_movie_layout.addWidget(self.mov_frm)

    def ui_manage_widgets(self):

        self.btn_create_col = QtWidgets.QPushButton("Create collection")
        self.btn_save_col = QtWidgets.QPushButton("Save all collections")
        self.btn_scan_dir = QtWidgets.QPushButton("Scan directory")
        self.btn_add_movie = QtWidgets.QPushButton("Add movie")
        self.btn_remove_movie = QtWidgets.QPushButton("Remove movie")
        self.label_filter = QtWidgets.QLabel(f"{12 * '-'} Filter {12 * '-'}")
        self.label_filter.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.cbb_genre = QtWidgets.QComboBox()
        self.cbb_genre.addItems(["Genre"] + constants.MOVIE_GENRES)
        self.cbb_actors = QtWidgets.QComboBox()
        self.clr_reload_cbb_actors()
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
        self.custom_dialog = MovieTagDialog()
        self.movie_tag_display = MovieTagDisplay()

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
        self.mov_frm_layout.addWidget(self.movie_tag_display)

    def ui_load_icons(self):

        application_logo = QPixmap(constants.LOGO)
        self.note_icon = QPixmap(constants.NOTE)
        self.save_icon = QPixmap(constants.SAVE)
        self.open_icon = QPixmap(constants.FOLDER)
        self.collection_icon = QPixmap(constants.COLLECTION_ICN)
        self.movie_icon = QPixmap(constants.MOVIE_ICN)
        btn_add_movie_icon = QPixmap(constants.ADD_ICN)
        btn_remove_movie_icon = QPixmap(constants.REM_ICN)
        le_search_icon = QIcon(constants.SEARCH)
        self.previous_icon = QIcon(constants.PREVIOUS)
        self.export_icon = QIcon(constants.EXPORT)
        self.delete_icon = QIcon(constants.DELETE)
        self.official_icon = QIcon(constants.OFFICIAL)
        self.star_icon = QIcon(constants.STAR)

        self.setWindowIcon(application_logo)
        self.btn_create_col.setIcon(self.note_icon)
        self.btn_save_col.setIcon(self.save_icon)
        self.btn_scan_dir.setIcon(self.open_icon)
        self.btn_add_movie.setIcon(btn_add_movie_icon)
        self.btn_remove_movie.setIcon(btn_remove_movie_icon)
        self.le_search.addAction(le_search_icon, self.le_search.ActionPosition.LeadingPosition)

    def ui_apply_style(self):

        with open(constants.STR_STYLE, 'r', encoding="UTF-8") as style_file:
            self.setStyleSheet(style_file.read())

    def logic_connect_widgets(self):

        self.btn_create_col.clicked.connect(self.logic_create_collection)
        self.btn_save_col.clicked.connect(self.logic_save_collection)
        self.btn_add_movie.clicked.connect(self.logic_add_movie)
        self.btn_remove_movie.clicked.connect(self.logic_remove_movie)
        self.cbb_genre.currentTextChanged.connect(self.logic_filter)
        self.cbb_actors.currentTextChanged.connect(self.logic_filter)
        self.lw_main.itemClicked.connect(self.logic_single_click)
        self.custom_dialog.btn_validate.clicked.connect(self.logic_get_returned_movie)

    def logic_create_collection(self):

        name, val = QtWidgets.QInputDialog.getText(self, "New collection", "Enter name:")
        if name and name not in [col.name for col in PyMoman.all_collections] and val:
            new_collection = Collection(name)
            PyMoman.all_collections.append(new_collection)
            self.logic_display_collections()

    def logic_open_collection(self, open_collection: Collection):

        PyMoman.last_collection_opened.clear()
        PyMoman.last_collection_opened.append(open_collection)
        self.logic_display_movies(open_collection.mov_lst)

    def logic_save_collection(self, collection_to_save: Collection):

        self.progress_bar.setValue(50)
        sleep(0.3)

        if self.sender() is self.btn_save_col:
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
        self.btn_add_movie.setEnabled(True)
        self.btn_remove_movie.setEnabled(True)

        for collection in PyMoman.all_collections:
            lw_item = QtWidgets.QListWidgetItem(collection.name)
            lw_item.attr = collection
            lw_item.setTextAlignment(Qt.AlignCenter)
            if lw_item.attr.path.exists():
                lw_item.setIcon(self.collection_icon)
            self.lw_main.addItem(lw_item)

    def logic_single_click(self, clicked_item):

        try:
            clicked_item.attr
        except AttributeError:  # clicked_item is necessarily 'GO BACK'
            self.logic_display_collections()
        else:
            if isinstance(clicked_item.attr, Movie):
                self.clr_reload_cbb_actors()
                scraper = dtr.MovieScraper(clicked_item.attr)
                threading.Thread(target=scraper.download_poster).start()
                threading.Thread(target=scraper.download_info).start()
                self.logic_display_panel(clicked_item.attr, scraper)

    def logic_add_movie(self) -> bool:

        if not PyMoman.last_collection_opened:
            return False

        self.custom_dialog.show()

    def logic_get_returned_movie(self) -> bool:

        collection = PyMoman.last_collection_opened[0]
        try:
            movie = Movie(
                title=self.custom_dialog.le_movie_title.text(),
                year=int(self.custom_dialog.le_movie_year.text()),
                rating=self.custom_dialog.cbb_movie_rating.currentText())
        except ValueError:
            self.custom_dialog.close()
            self.clr_reset_custom_dialog()
            return False
        else:
            if movie.title not in [mov.title for mov in collection.mov_lst]:
                collection.add_movie(movie)
                self.custom_dialog.close()
                self.clr_reset_custom_dialog()
                self.logic_display_movies(collection.mov_lst)
                return True
            else:
                self.custom_dialog.close()
                self.clr_reset_custom_dialog()
                return False

    def logic_rename_movie(self, movie: Movie):

        pass

    def logic_edit_movie_rating(self, movie: Movie):

        pass

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
                collection.remove_movie(movie_to_remove)
                movie_to_remove.remove_cache()
                del movie_to_remove
                self.logic_display_movies(collection.mov_lst)
                return True

    def logic_filter(self):

        all_movies = [mov for col in PyMoman.all_collections for mov in col.mov_lst]

        if self.sender() is self.cbb_genre and self.cbb_actors.currentText() == "Actors":
            query = self.cbb_genre.currentText()
            matching_movies = [mov for mov in all_movies if query == mov.genre]
        elif self.sender() is self.cbb_genre and self.cbb_actors.currentText() != "Actors":
            query = self.cbb_genre.currentText()
            actor_filter = self.cbb_actors.currentText()
            filtered_movies = [mov for mov in all_movies if actor_filter in mov.actors]
            matching_movies = [mov for mov in filtered_movies if query == mov.genre]
        elif self.sender() is self.cbb_actors and self.cbb_genre.currentText() == "Genre":
            query = self.cbb_actors.currentText()
            matching_movies = [mov for mov in all_movies if query in mov.actors]
        else:
            query = self.cbb_actors.currentText()
            genre_filter = self.cbb_genre.currentText()
            filtered_movies = [mov for mov in all_movies if genre_filter == mov.genre]
            matching_movies = [mov for mov in filtered_movies if query in mov.actors]

        if query == "Genre" or query == "Actors":
            self.logic_display_collections()
            return

        self.btn_add_movie.setEnabled(False)
        self.btn_remove_movie.setEnabled(False)

        self.logic_display_movies(matching_movies)

    def logic_display_movies(self, mov_lst: list[Movie]):

        self.lw_main.clear()
        list_to_display: list[QtWidgets.QListWidgetItem] = []

        previous_item = QtWidgets.QListWidgetItem("GO BACK")
        previous_item.setTextAlignment(Qt.AlignCenter)
        previous_item.setIcon(self.previous_icon)
        list_to_display.append(previous_item)

        for movie in mov_lst:
            lw_item = QtWidgets.QListWidgetItem(movie.title)
            lw_item.attr = movie
            lw_item.setTextAlignment(Qt.AlignCenter)
            lw_item.setIcon(self.movie_icon)
            list_to_display.append(lw_item)

        for item in list_to_display:
            self.lw_main.addItem(item)

    def logic_display_panel(self, movie: Movie, scraper: dtr.MovieScraper):

        if scraper.thumb.exists():
            movie_poster = QPixmap(str(scraper.thumb))
        else:
            movie_poster = QPixmap(constants.STR_DEFAULT_POSTER)

        if scraper.data_file.exists():
            data = dti.load_file_content(scraper.data_file)
            title = data.get('title')
            summary = data.get('summary')
        else:
            title = f"{movie.title.title()} ({movie.year})"
            summary = "The summary could not be retrieved, movie title may be incomplete, incorrect or too vague"

        self.movie_tag_display.poster_label.setPixmap(movie_poster)
        self.movie_tag_display.rating_label.setText(movie.aesthetic_rating)
        self.movie_tag_display.title_label.setText(title)
        self.movie_tag_display.title_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.movie_tag_display.summary_label.setText(summary)
        self.movie_tag_display.summary_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def clr_reset_custom_dialog(self):

        self.custom_dialog.le_movie_title.clear()
        self.custom_dialog.le_movie_year.clear()
        self.custom_dialog.cbb_movie_rating.setCurrentIndex(0)

    def clr_reload_cbb_actors(self):

        self.cbb_actors.blockSignals(True)
        self.cbb_actors.clear()
        self.cbb_actors.addItems(["Actors"] + dti.load_all_actors())
        self.cbb_actors.blockSignals(False)

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

            movie_menu = QtWidgets.QMenu(self)

            rename_mov = QAction(self.note_icon, "Rename")
            rename_mov.triggered.connect(partial(self.logic_rename_movie, list_item.attr))

            official_title = QAction(self.official_icon, "Assign official title")
            official_title.triggered.connect(partial(self.logic_rename_movie, list_item.attr))

            edit_rating = QAction(self.star_icon, "Edit rating")
            edit_rating.triggered.connect(partial(self.logic_edit_movie_rating, list_item.attr))

            movie_menu.addAction(official_title)
            movie_menu.addAction(rename_mov)
            movie_menu.addAction(edit_rating)

            if isinstance(list_item.attr, Collection):
                collection_menu.exec(event.globalPos())
            elif isinstance(list_item.attr, Movie):
                movie_menu.exec(event.globalPos())

        return super().eventFilter(watched, event)


if __name__ == '__main__':
    root = QtWidgets.QApplication()
    application = PyMoman()
    application.show()
    root.exec()
