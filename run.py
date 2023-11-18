"""Main application file."""


import threading
from functools import partial
from pathlib import Path
from time import sleep


from PySide6 import QtWidgets
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtGui import QPixmap, QAction
from PySide6.QtCore import Qt, QEvent


from packages.constants import constants
from packages.logic import dataimport
from packages.logic import dataprocess
from packages.logic import dataretrieve
from packages.logic.collection import Collection
from packages.logic.movie import Movie
from packages.ui.aesthetic import AestheticWindow
from packages.ui.displaypanel import DisplayPanel
from packages.ui.impdir import DirectoryImporter
from packages.ui.movtag import MovieTagDialog
from packages.ui.minib import MiniBrowser


class MainWindow(AestheticWindow):
    all_collections: list[Collection] = Collection.retrieve_collections()
    last_collection_opened: list[Collection] = []

    def __init__(self):
        super().__init__()

        dataprocess.clear_cache()  # Remove unused cache folders before loading anything.

        self.setWindowTitle("Python Movie Manager")
        self.setFixedSize(950, 450)

        ##################################################
        # Frames and layouts.
        ##################################################

        self.pnl_frm = None
        self.main_layout = None
        self.header_layout = None
        self.body_layout = None
        self.menu_layout = None
        self.list_layout = None
        self.global_movie_layout = None
        self.pnl_frm_layout = None

        self.ui_manage_layouts_and_frames()

        ##################################################
        # Widgets.
        ##################################################

        self.btn_create_col = None
        self.btn_save_col = None
        self.btn_scan_dir = None
        self.btn_add_movie = None
        self.btn_remove_movie = None
        self.lbl_filter = None
        self.cbb_genre = None
        self.cbb_actors = None
        self.prg_bar = None
        self.le_search = None
        self.lw_main = None
        self.cst_dialog = None
        self.panel = None
        self.imp_dir = None
        self.mini_browser = None

        self.ui_manage_widgets()

        ##################################################
        # Icons.
        ##################################################

        self.ui_manage_icons()

        ##################################################
        # Connections.
        ##################################################

        self.logic_connect_widgets()

        ##################################################
        # Display.
        ##################################################

        self.logic_list_display(MainWindow.all_collections)

    def ui_information_panel(self, item) -> None:
        """Right information panel that displays information about the selected item.

        Args:
            item: Collection or Movie object.

        Returns:
            None: None.
        """

        image = QPixmap(constants.STR_PATHS.get('default poster'))

        if isinstance(item, Collection):
            title = f"→ {item.name.upper()}"
            summary = "\n".join([f"- {movie.title}" for movie in item.mov_lst[:7]] + ['...'])
            top_right_text = f"{len(item.mov_lst)} movie{'s' if len(item.mov_lst) > 1 else ''}."

        else:
            if item.thumb.exists():
                image = QPixmap(str(item.thumb))

            title = f"{item.title.title()} ({item.year})"
            summary = "The summary could not be retrieved, movie title may be incomplete, incorrect or too vague"
            top_right_text = item.aesthetic_rating

            if item.data_file.exists():
                content = item.load_data_file()
                title = content.get('title')
                summary = content.get('summary')

        self.panel.lbl_image.setPixmap(image)
        self.panel.lbl_top_right.setText(top_right_text)
        self.panel.lbl_title.setText(title)
        self.panel.te_summary.setText(summary)

    def ui_manage_icons(self) -> None:
        """Icons are managed here.

        Returns:
            None: None.
        """

        super().ui_manage_icons()
        self.btn_create_col.setIcon(self.icons.get('note'))
        self.btn_save_col.setIcon(self.icons.get('save'))
        self.btn_scan_dir.setIcon(self.icons.get('folder'))
        self.btn_add_movie.setIcon(self.icons.get('add'))
        self.btn_remove_movie.setIcon(self.icons.get('rem'))
        self.le_search.addAction(self.icons.get('search'), self.le_search.ActionPosition.LeadingPosition)

    def ui_manage_layouts_and_frames(self) -> None:
        """Frames and layouts are managed here.

        Returns:
            None: None.
        """

        self.pnl_frm = QtWidgets.QFrame()
        self.pnl_frm.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.header_layout = QtWidgets.QHBoxLayout()
        self.body_layout = QtWidgets.QHBoxLayout()
        self.menu_layout = QtWidgets.QVBoxLayout()
        self.list_layout = QtWidgets.QVBoxLayout()
        self.list_layout.setContentsMargins(10, 0, 0, 0)
        self.global_movie_layout = QtWidgets.QHBoxLayout()
        self.pnl_frm_layout = QtWidgets.QHBoxLayout(self.pnl_frm)

        self.main_layout.addLayout(self.header_layout)
        self.main_layout.addLayout(self.body_layout)
        self.body_layout.addLayout(self.menu_layout)
        self.body_layout.addLayout(self.list_layout)
        self.body_layout.addLayout(self.global_movie_layout)
        self.global_movie_layout.addWidget(self.pnl_frm)

    def ui_manage_widgets(self) -> None:
        """Widgets are managed here.

        Returns:
            None: None.
        """

        self.btn_create_col = QtWidgets.QPushButton("Create collection")
        self.btn_save_col = QtWidgets.QPushButton("Save all collections")
        self.btn_scan_dir = QtWidgets.QPushButton("Scan directory")
        self.btn_add_movie = QtWidgets.QPushButton("Add movie")
        self.btn_add_movie.setEnabled(False)
        self.btn_remove_movie = QtWidgets.QPushButton("Remove movie")
        self.btn_remove_movie.setEnabled(False)
        self.lbl_filter = QtWidgets.QLabel(f"{12 * '-'} Filter {12 * '-'}")
        self.lbl_filter.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.cbb_genre = QtWidgets.QComboBox()
        self.cbb_genre.setMaxVisibleItems(5)
        self.cbb_genre.addItems(["Genre"] + constants.MOVIE_GENRES)
        self.cbb_actors = QtWidgets.QComboBox()
        self.cbb_actors.setMaxVisibleItems(5)
        self.clr_reload_cbb_actors()
        self.prg_bar = QtWidgets.QProgressBar()
        self.prg_bar.setTextVisible(False)
        self.prg_bar.setFixedHeight(5)
        self.prg_bar.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.le_search = QtWidgets.QLineEdit()
        self.le_search.setClearButtonEnabled(True)
        self.le_search.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.le_search.setPlaceholderText("Search")
        self.lw_main = QtWidgets.QListWidget()
        self.lw_main.installEventFilter(self)
        self.lw_main.setAlternatingRowColors(True)
        self.lw_main.setFocusPolicy(Qt.NoFocus)
        self.lw_main.setWordWrap(True)
        self.lw_main.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.cst_dialog = MovieTagDialog()
        self.panel = DisplayPanel()

        self.header_layout.addWidget(self.btn_create_col)
        self.header_layout.addWidget(self.btn_save_col)
        self.header_layout.addWidget(self.btn_scan_dir)
        self.menu_layout.addWidget(self.btn_add_movie)
        self.menu_layout.addWidget(self.btn_remove_movie)
        self.menu_layout.addWidget(self.lbl_filter)
        self.menu_layout.addWidget(self.cbb_genre)
        self.menu_layout.addWidget(self.cbb_actors)
        self.menu_layout.addWidget(self.prg_bar)
        self.list_layout.addWidget(self.le_search)
        self.list_layout.addWidget(self.lw_main)
        self.pnl_frm_layout.addWidget(self.panel)

    def ui_progress_bar_animation(self) -> None:
        """Creates a small animation for the progress bar.

        Returns:
            None: None.
        """

        for i in range(1, 101):         # The interface freezes for
            self.prg_bar.setValue(i)    # such a short time that using a
            sleep(0.003)                # thread here seems unnecessary.

        sleep(0.3)
        self.prg_bar.reset()

    def logic_add_movie(self) -> None:
        """Opens the window which allows to add a movie.

        Returns:
            None: None.
        """

        if not MainWindow.last_collection_opened:
            return

        self.cst_dialog.show()

    def logic_add_movie_validation(self) -> None:
        """Validate whether to add the movie or not based on whether the user input is correct or incorrect.

        Returns:
            None: None.
        """

        collection = MainWindow.last_collection_opened[0]
        try:
            movie = Movie(
                title=self.cst_dialog.le_movie_title.text(),
                year=int(self.cst_dialog.le_movie_year.text()),
                rating=self.cst_dialog.cbb_movie_rating.currentText())
        except ValueError:
            self.cst_dialog.close()
        else:
            if movie.title not in [mov.title for mov in collection.mov_lst]:
                collection.add_movie(movie)
                self.cst_dialog.close()
                self.logic_list_display(collection.mov_lst)
            else:
                self.cst_dialog.close()

        self.clr_reset_cst_dialog()

    def logic_add_to_wishlist(self, movie: Movie) -> None:

        pass

    def logic_connect_widgets(self) -> None:
        """Connections are managed here.

        Returns:
            None: None.
        """

        self.btn_create_col.clicked.connect(self.logic_create_collection)
        self.btn_save_col.clicked.connect(self.logic_save_collection)
        self.btn_scan_dir.clicked.connect(self.logic_scan_dir)
        self.btn_add_movie.clicked.connect(self.logic_add_movie)
        self.cst_dialog.btn_validate.clicked.connect(self.logic_add_movie_validation)
        self.btn_remove_movie.clicked.connect(self.logic_remove_movie)
        self.cbb_genre.currentTextChanged.connect(self.logic_filter)
        self.cbb_actors.currentTextChanged.connect(self.logic_filter)
        self.le_search.textChanged.connect(self.logic_search_bar)
        self.lw_main.itemClicked.connect(self.logic_single_click)

    def logic_create_collection(self) -> None:
        """Creates a new collection.

        Returns:
            None: None.
        """

        name, value = QtWidgets.QInputDialog.getText(self, "New collection", "Enter name:")
        if name and name not in [c.name for c in MainWindow.all_collections] and value:
            new_collection = Collection(name)
            MainWindow.all_collections.append(new_collection)

            self.logic_list_display(MainWindow.all_collections)

    def logic_create_collection_menu(self, pos, item: Collection) -> None:
        """Create a context menu for collections.

        This method generates a context menu with specific actions for collections
        within the QListWidget. It is triggered by a right-click event at the given
        position 'pos' within the list widget.

        Args:
            pos: Event position.
            item (Collection): Clicked item.

        Returns:
            None: None.
        """

        collection_menu = QtWidgets.QMenu(self)

        open_collection = QAction(self.icons.get('folder'), "Open")
        open_collection.triggered.connect(partial(self.logic_open_collection, item))
        save_collection = QAction(self.icons.get('save'), "Save")
        save_collection.triggered.connect(partial(self.logic_save_collection, item))
        rename_collection = QAction(self.icons.get('note'), "Rename")
        rename_collection.triggered.connect(partial(self.logic_rename_collection, item))
        export_collection = QAction(self.icons.get('export'), "Export as text")
        export_collection.triggered.connect(partial(self.logic_export_collection, item))
        delete_collection = QAction(self.icons.get('delete'), "Delete")
        delete_collection.triggered.connect(partial(self.logic_delete_collection, item))

        collection_menu.addAction(open_collection)
        collection_menu.addAction(save_collection)
        collection_menu.addAction(rename_collection)
        collection_menu.addAction(export_collection)
        collection_menu.addAction(delete_collection)

        collection_menu.exec(pos)
        collection_menu.deleteLater()

    def logic_create_movie_menu(self, pos, item: Movie) -> None:
        """Create a context menu for movies.

        This method generates a context menu with specific actions for movies
        within the QListWidget. It is triggered by a right-click event at the given
        position 'pos' within the list widget.

        Args:
            pos: Event position.
            item (Movie): Clicked item.

        Returns:
            None: None.
        """

        movie_menu = QtWidgets.QMenu(self)

        rename_movie = QAction(self.icons.get('note'), "Rename")
        rename_movie.triggered.connect(partial(self.logic_rename_movie, item, True))
        official_title = QAction(self.icons.get('official'), "Assign official title")
        official_title.triggered.connect(partial(self.logic_rename_movie, item, False))
        edit_rating = QAction(self.icons.get('star'), "Edit rating")
        edit_rating.triggered.connect(partial(self.logic_edit_movie_rating, item))
        load_new_poster = QAction(self.icons.get('new_poster'), "Load new poster")
        load_new_poster.triggered.connect(partial(self.logic_modify_poster, item))
        load_default_poster = QAction(self.icons.get('default_poster'), "Set default poster")
        load_default_poster.triggered.connect(partial(self.logic_modify_poster, item, True))
        wishlist = QAction(self.icons.get('wishlist'), "Add to Wishlist")
        wishlist.triggered.connect(partial(self.logic_add_to_wishlist, item))
        watch_trailer = QAction(self.icons.get('trailer'), "Watch trailer")
        watch_trailer.triggered.connect(partial(self.logic_watch_trailer, item))
        delete_cache = QAction(self.icons.get('delete'), "Delete cached data")
        delete_cache.triggered.connect(partial(self.logic_delete_movie_cache, item))

        movie_menu.addAction(official_title)
        movie_menu.addAction(rename_movie)
        movie_menu.addAction(edit_rating)
        movie_menu.addAction(load_new_poster)
        movie_menu.addAction(load_default_poster)
        movie_menu.addAction(wishlist)
        movie_menu.addAction(watch_trailer)
        movie_menu.addAction(delete_cache)

        movie_menu.exec(pos)
        movie_menu.deleteLater()

    def logic_delete_collection(self, collection: Collection) -> None:
        """Allows to delete a collection.

        Args:
            collection (Collection): Collection to delete.

        Returns:
            None: None.
        """

        value = collection.remove()

        if value:
            MainWindow.all_collections.remove(collection)
            self.logic_list_display(MainWindow.all_collections)

    @staticmethod
    def logic_delete_movie_cache(movie: Movie) -> None:

        movie.remove_cache()

    def logic_edit_movie_rating(self, movie: Movie) -> None:

        pass

    def logic_export_collection(self, collection: Collection) -> None:
        """Allows to export a collection.

        Args:
            collection (Collection): Collection to export.

        Returns:
            None: None.
        """

        dialog = QtWidgets.QFileDialog.getSaveFileName(self, 'Python Movie Manager - Save text file')
        if dialog[0]:
            collection.export_as_txt(Path(f"{dialog[0]}.txt"))

    def logic_filter(self) -> None:
        """Filters logic is managed here.

        Returns:
            None: None.
        """

        all_movies = [mov for col in MainWindow.all_collections for mov in col.mov_lst]
        query_g = self.cbb_genre.currentText()
        query_a = self.cbb_actors.currentText()

        if query_g == "Genre" and query_a != "Actors":
            matching_movies = [mov for mov in all_movies if query_a in mov.actors]
        elif query_g != "Genre" and query_a == "Actors":
            matching_movies = [mov for mov in all_movies if query_g in mov.genre]
        elif query_g != "Genre" and query_a != "Actors":
            matching_movies = [mov for mov in all_movies if (query_g in mov.genre) and (query_a in mov.actors)]
        else:
            matching_movies = all_movies

        self.logic_list_display(matching_movies)

    def logic_generate_list_item(self, item) -> QtWidgets.QListWidgetItem:
        """Generates a QListWidgetItem from the received object.

        Args:
            item: Collection or Movie object.

        Returns:
            QtWidgets.QListWidgetItem: Item ready for display.
        """

        if isinstance(item, Collection):
            lw_item = QtWidgets.QListWidgetItem(item.name)
            if item.path.exists():
                lw_item.setIcon(self.icons.get('collection'))

        else:
            lw_item = QtWidgets.QListWidgetItem(item.title)
            lw_item.setIcon(self.icons.get('movie'))

        lw_item.setTextAlignment(Qt.AlignCenter)
        lw_item.attr = item
        return lw_item

    def logic_import_directory(self) -> None:
        """Retrieves scanned movies from a folder and add them to a collection.

        Returns:
            None: None.
        """

        qlw_items = [self.imp_dir.lw_main.item(i) for i in range(self.imp_dir.lw_main.count())]
        conv_items = [dataimport.make_movie(
            title=qlw_item.title,
            year=int(qlw_item.year) if qlw_item.year and isinstance(qlw_item.year, str) else qlw_item.year,
            path=qlw_item.text(),
            rating=qlw_item.rating) for qlw_item in qlw_items]
        movies = [item[0] for item in conv_items if item[0]]

        for movie in movies:
            self.imp_dir.collection.add_movie(movie)

        if self.imp_dir.collection.name not in [c.name for c in MainWindow.all_collections]:
            MainWindow.all_collections.append(self.imp_dir.collection)
        self.imp_dir.close()

        self.logic_list_display(self.imp_dir.collection.mov_lst)

    def logic_list_display(self, items: list) -> None:
        """All display logic for the list widget is managed here.

        Args:
            items (list): List of Collection objects or Movie objects.

        Returns:
            None: None.
        """

        previous_item = QtWidgets.QListWidgetItem("GO BACK")
        previous_item.attr = None
        previous_item.setTextAlignment(Qt.AlignCenter)
        previous_item.setIcon(self.icons.get('previous'))
        self.lw_main.clear()

        if not items and not MainWindow.all_collections:
            display_list = []
        elif not items and MainWindow.all_collections:
            display_list = [previous_item]
        elif all(isinstance(item, Collection) for item in items):
            self.last_collection_opened.clear()
            display_list = [self.logic_generate_list_item(collection) for collection in items]
        else:
            display_list = [previous_item] + [self.logic_generate_list_item(movie) for movie in items]

        for item in display_list:
            self.lw_main.addItem(item)

    def logic_modify_poster(self, movie: Movie, use_default=False) -> None:
        """Allows the user to display a new image for the movie,
        (for example if they don't like the current image.)

        Args:
            movie (Movie): Movie to work on.
            use_default (bool): True to use default image, False to scrape a new image.

        Returns:
            None: None.
        """

        if use_default:
            movie.set_default_poster()
        else:
            scraper = dataretrieve.MovieScraper(movie)
            threading.Thread(target=scraper.download_poster, args=(True,), daemon=True).start()
            self.ui_progress_bar_animation()

        self.ui_information_panel(movie)

    def logic_open_collection(self, collection: Collection) -> None:
        """Allows to open a collection.

        Args:
            collection (Collection): Collection to open.

        Returns:
            None: None.
        """

        self.last_collection_opened.clear()
        self.last_collection_opened.append(collection)
        self.logic_list_display(collection.mov_lst)
        self.btn_add_movie.setEnabled(True)
        self.btn_remove_movie.setEnabled(True)

    def logic_remove_movie(self) -> None:
        """Allows to remove a movie.

        Returns:
            None: None.
        """

        if not MainWindow.last_collection_opened:
            return

        collection = MainWindow.last_collection_opened[0]

        try:
            movie_to_remove = self.lw_main.selectedItems()[0].attr
        except AttributeError:
            pass
        except IndexError:
            pass
        else:
            if isinstance(movie_to_remove, Movie):
                collection.remove_movie(movie_to_remove)
                movie_to_remove.remove_cache()
                del movie_to_remove
                self.logic_list_display(collection.mov_lst)

    def logic_rename_collection(self, collection: Collection) -> None:
        """Allows to rename a collection.

        Args:
            collection (Collection): Collection to rename.

        Returns:
            None: None.
        """

        new_name, value = QtWidgets.QInputDialog.getText(self, "Rename collection", "Enter new name:")
        if new_name and new_name not in [c.name for c in MainWindow.all_collections] and value:
            collection.rename(new_name)
            self.logic_update_list_widget()

    def logic_rename_movie(self, movie: Movie, user_choice: bool) -> None:
        """Allows to rename a movie.

        Args:
            movie (Movie): Movie to rename.
            user_choice (bool): True for personal renaming, False to automatically rename with the official title.

        Returns:
            None: None.
        """

        res = True
        if user_choice:
            new_name, value = QtWidgets.QInputDialog.getText(self, "Rename movie", "Enter new title:")

            if new_name and value:              # Users can use a title that already exists when renaming.
                res = movie.rename(new_name)    # However they cannot when adding a new movie.

        else:
            res = movie.rename(movie.official_title)

        if not res:
            QtWidgets.QMessageBox.about(self, "Warning", constants.CACHE_WARNING)

        self.logic_update_list_widget()

    def logic_save_collection(self, collection_to_save: Collection) -> None:
        """Saves the created collections.

        Args:
            collection_to_save (Collection): Collection to save.

        Returns:
            None: None.
        """

        if not MainWindow.all_collections:
            return

        if self.sender() is self.btn_save_col:
            for collection in MainWindow.all_collections:
                collection.save()
        else:
            collection_to_save.save()

        self.ui_progress_bar_animation()
        self.logic_update_list_widget()

    def logic_scan_dir(self) -> None:
        """Creates all variables needed to scan a folder.

        Returns:
            None: None.
        """

        dialog = QtWidgets.QFileDialog.getExistingDirectory(self, "Python Movie Manager - Select Directory")

        if not dialog:
            return

        dir_path = Path(dialog).resolve()
        dir_name = dir_path.stem
        suffix = 0

        while dir_name in [collection.name for collection in MainWindow.all_collections]:
            dir_name = f"{dir_name}_{suffix}"
            suffix += 1

        # Define the collection in which to add the scanned files
        collection = MainWindow.last_collection_opened[0] \
            if MainWindow.last_collection_opened else Collection(dir_name)

        self.imp_dir = DirectoryImporter(collection, dir_path)
        self.imp_dir.btn_validate.clicked.connect(self.logic_import_directory)
        self.imp_dir.show()

    def logic_search_bar(self) -> None:
        """Search bar logic is here.

        Returns:
            None: None.
        """

        query: str = self.le_search.text().strip().lower()

        if MainWindow.last_collection_opened:
            collection = MainWindow.last_collection_opened[0]
            requested_items = [movie for movie in collection.mov_lst if movie.title.casefold().startswith(query)]
        else:
            requested_items = [col for col in MainWindow.all_collections if col.name.casefold().startswith(query)]

        self.logic_list_display(requested_items)

    def logic_single_click(self, clicked_item) -> None:
        """Handle a single click on items in the QListWidget.

        Returns:
            None: None.
        """

        if isinstance(clicked_item.attr, Collection):
            self.ui_information_panel(clicked_item.attr)

        elif isinstance(clicked_item.attr, Movie):
            self.clr_reload_cbb_actors()
            scraper = dataretrieve.MovieScraper(clicked_item.attr)
            threading.Thread(target=scraper.download_poster, daemon=True).start()
            threading.Thread(target=scraper.download_info, daemon=True).start()
            self.ui_information_panel(clicked_item.attr)

        else:  # clicked_item is 'GO BACK'
            self.logic_list_display(MainWindow.all_collections)
            self.btn_add_movie.setEnabled(False)
            self.btn_remove_movie.setEnabled(False)

    def logic_update_list_widget(self) -> None:
        """Refreshes the current items in the list widget.

        Returns:
            None: None.
        """

        selected_item_row = self.lw_main.row(self.lw_main.currentItem())

        items = [self.lw_main.item(i) for i in range(self.lw_main.count())]
        items = [item.attr for item in items if item.attr is not None]
        self.logic_list_display(items)

        if selected_item_row:
            self.lw_main.scrollToItem(self.lw_main.item(selected_item_row))

    def logic_watch_trailer(self, movie: Movie) -> None:
        """Allows trailer viewing.

        Returns:
            None: None.
        """

        self.mini_browser = MiniBrowser(movie)
        self.mini_browser.show()

    def clr_reload_cbb_actors(self) -> None:
        """Reloads a list of all actors in the combobox.

        Returns:
            None: None.
        """

        self.cbb_actors.blockSignals(True)
        self.cbb_actors.clear()
        self.cbb_actors.addItems(["Actors"] + dataimport.load_all_actors())
        self.cbb_actors.blockSignals(False)

    def clr_reset_cst_dialog(self) -> None:
        """Reset the fields of cst_dialog.

        Returns:
            None: None.
        """

        self.cst_dialog.le_movie_title.clear()
        self.cst_dialog.le_movie_year.clear()
        self.cst_dialog.cbb_movie_rating.setCurrentIndex(0)

    def eventFilter(self, watched, event: QEvent) -> bool:

        if event.type() == QEvent.ContextMenu and watched is self.lw_main:
            list_item = watched.itemAt(event.pos())

            if list_item is None:
                return False

            if isinstance(list_item.attr, Collection):
                self.logic_create_collection_menu(event.globalPos(), list_item.attr)

            elif isinstance(list_item.attr, Movie):  # Can't put 'else' because of previous_item
                self.logic_create_movie_menu(event.globalPos(), list_item.attr)

        return super().eventFilter(watched, event)


if __name__ == '__main__':
    root = QtWidgets.QApplication()
    application = MainWindow()
    application.show()
    root.exec()
