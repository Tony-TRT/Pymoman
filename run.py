from functools import partial
from pathlib import Path
from time import sleep


from PySide6 import QtWidgets
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtGui import QIcon, QAction
from PySide6.QtCore import Qt, QEvent


from packages.logic import dataimport
from packages.logic import dataprocess
from packages.logic.collection import Collection
from packages.logic.movie import Movie
from packages.ui.movdisplay import MovieTagDisplay
from packages.ui.movtag import MovieTagDialog
from packages.constants import constants


class MainWindow(QtWidgets.QWidget):
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

        self.mov_frm = None
        self.main_layout = None
        self.header_layout = None
        self.body_layout = None
        self.menu_layout = None
        self.list_layout = None
        self.global_movie_layout = None
        self.mov_frm_layout = None

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
        self.mvt_display = None

        self.ui_manage_widgets()

        ##################################################
        # Icons.
        ##################################################

        self.icons = {}

        self.ui_manage_icons()

        ##################################################
        # Style.
        ##################################################

        self.ui_apply_style()

        ##################################################
        # Connections.
        ##################################################

        self.logic_connect_widgets()

        ##################################################
        # Display.
        ##################################################

        self.logic_list_display(self.all_collections, show_previous_icn=False)

    def ui_apply_style(self) -> None:
        """Style is managed here.

        Returns:
            None: None.
        """

        with open(constants.STYLE, 'r', encoding="UTF-8") as style_file:
            self.setStyleSheet(style_file.read())

    def ui_manage_icons(self) -> None:
        """Icons are managed here.

        Returns:
            None: None.
        """

        for icn_name, icn_path in constants.ICONS.items():
            icon = QIcon(str(icn_path))
            self.icons[icn_name] = icon

        self.setWindowIcon(self.icons.get('logo'))
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

    def ui_manage_widgets(self) -> None:
        """Widgets are managed here.

        Returns:
            None: None.
        """

        self.btn_create_col = QtWidgets.QPushButton("Create collection")
        self.btn_save_col = QtWidgets.QPushButton("Save all collections")
        self.btn_scan_dir = QtWidgets.QPushButton("Scan directory")
        self.btn_add_movie = QtWidgets.QPushButton("Add movie")
        self.btn_remove_movie = QtWidgets.QPushButton("Remove movie")
        self.lbl_filter = QtWidgets.QLabel(f"{12 * '-'} Filter {12 * '-'}")
        self.lbl_filter.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.cbb_genre = QtWidgets.QComboBox()
        self.cbb_genre.addItems(["Genre"] + constants.MOVIE_GENRES)
        self.cbb_actors = QtWidgets.QComboBox()
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
        self.lw_main.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
        self.cst_dialog = MovieTagDialog()
        self.mvt_display = MovieTagDisplay()

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
        self.mov_frm_layout.addWidget(self.mvt_display)

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

    def logic_add_to_wishlist(self, movie: Movie) -> None:

        pass

    def logic_connect_widgets(self) -> None:
        """Connections are managed here.

        Returns:
            None: None.
        """

        self.btn_create_col.clicked.connect(self.logic_create_collection)
        self.btn_save_col.clicked.connect(self.logic_save_collection)

    def logic_create_collection(self) -> None:
        """Creates a new collection.

        Returns:
            None: None.
        """

        name, value = QtWidgets.QInputDialog.getText(self, "New collection", "Enter name:")
        if name and name not in [c.name for c in self.all_collections] and value:
            new_collection = Collection(name)
            self.all_collections.append(new_collection)

            self.logic_list_display(self.all_collections, show_previous_icn=False)

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
        rename_movie.triggered.connect(partial(self.logic_rename_movie, item, False))
        official_title = QAction(self.icons.get('official'), "Assign official title")
        official_title.triggered.connect(partial(self.logic_rename_movie, item, True))
        edit_rating = QAction(self.icons.get('star'), "Edit rating")
        edit_rating.triggered.connect(partial(self.logic_edit_movie_rating, item))
        load_new_poster = QAction(self.icons.get('new_poster'), "Load new poster")
        load_new_poster.triggered.connect(partial(self.logic_modify_poster, item))
        load_default_poster = QAction(self.icons.get('default_poster'), "Set default poster")
        load_default_poster.triggered.connect(partial(self.logic_modify_poster, item))
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
            self.all_collections.remove(collection)
            self.logic_list_display(self.all_collections, show_previous_icn=False)

    def logic_delete_movie_cache(self, movie: Movie) -> None:

        pass

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

    def logic_list_display(self, items: list, show_previous_icn: bool = True) -> None:
        """All display logic for the list widget is managed here.

        Args:
            items (list): List of Collection objects or Movie objects.
            show_previous_icn (bool, optional): Whether to display the previous item. Defaults to True.

        Returns:
            None: None.
        """

        previous_item = QtWidgets.QListWidgetItem("GO BACK")
        previous_item.attr = None
        previous_item.setTextAlignment(Qt.AlignCenter)
        previous_item.setIcon(self.icons.get('previous'))
        self.lw_main.clear()

        if not items and show_previous_icn:
            display_list = [previous_item]

        elif all(isinstance(item, Collection) for item in items):
            self.last_collection_opened.clear()
            display_list = [self.logic_generate_list_item(collection) for collection in items]

        else:
            display_list = [previous_item] + [self.logic_generate_list_item(movie) for movie in items]

        for item in display_list:
            self.lw_main.addItem(item)

    def logic_modify_poster(self, movie: Movie) -> None:

        pass

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

    def logic_rename_collection(self, collection: Collection) -> None:
        """Allows to rename a collection.

        Args:
            collection (Collection): Collection to rename.

        Returns:
            None: None.
        """

        new_name, value = QtWidgets.QInputDialog.getText(self, "Rename collection", "Enter new name:")
        if new_name and new_name not in [c.name for c in self.all_collections] and value:
            collection.rename(new_name)
            self.logic_update_list_widget()

    def logic_rename_movie(self, movie: Movie) -> None:

        pass

    def logic_save_collection(self, collection_to_save: Collection) -> None:
        """Saves the created collections.

        Args:
            collection_to_save (Collection): Collection to save.

        Returns:
            None: None.
        """

        if not self.all_collections:
            return

        if self.sender() is self.btn_save_col:
            for collection in self.all_collections:
                collection.save()
        else:
            collection_to_save.save()

        self.ui_progress_bar_animation()
        self.logic_update_list_widget()

    def logic_update_list_widget(self) -> None:
        """Refreshes the current items in the list widget.

        Returns:
            None: None.
        """

        items = [self.lw_main.item(i) for i in range(self.lw_main.count())]
        items = [it.attr for it in items if it.attr is not None]
        self.logic_list_display(items)

    def logic_watch_trailer(self, movie: Movie) -> None:

        pass

    def clr_reload_cbb_actors(self) -> None:
        """Reloads a list of all actors in the combobox.

        Returns:
            None: None.
        """

        self.cbb_actors.blockSignals(True)
        self.cbb_actors.clear()
        self.cbb_actors.addItems(["Actors"] + dataimport.load_all_actors())
        self.cbb_actors.blockSignals(False)

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
