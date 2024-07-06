"""Main application file."""

from functools import partial
from pathlib import Path
from time import sleep

from PySide6 import QtWidgets
from PySide6.QtWidgets import QSizePolicy
from PySide6.QtGui import QPixmap, QAction
from PySide6.QtCore import Qt, QEvent

from packages.constants import constants
from packages.logic import dataimport, dataprocess, dataretrieve
from packages.logic.qthread import ScraperThread
from packages.logic.collection import Collection
from packages.logic.movie import Movie
from packages.ui.aesthetic import AestheticWindow
from packages.ui.displaypanel import DisplayPanel
from packages.ui.dirimporter import DirectoryImporter
from packages.ui.movieappender import MovieAppender
from packages.ui.ratingadjuster import RatingAdjuster
from packages.ui.minibrowser import MiniBrowser
from packages.ui.suggester import RecPanel


class MainWindow(AestheticWindow):
    all_collections: list[Collection] = Collection.retrieve_collections()
    last_collection_opened = last_movie_displayed = None

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Python Movie Manager")
        self.setFixedSize(950, 450)
        self.setAcceptDrops(True)
        self.thread = ScraperThread()
        self.commands: dict = {
            "/set_default_theme": partial(self.ui_apply_style, "default"),
            "/set_cyber_theme": partial(self.ui_apply_style, "cyber"),
            "/set_default_font": partial(self.ui_apply_font, "default"),
            "/set_cyber_font": partial(self.ui_apply_font, "cyber"),
            "/sort_collection": self.logic_sort_collection
        }

        ##################################################
        # Frames and layouts.
        ##################################################

        self.pnl_frame = self.gnr_layout = None
        self.hdr_layout = self.crp_layout = None
        self.men_layout = self.lst_layout = None
        self.inf_layout = self.frm_layout = None

        self.ui_manage_layouts_and_frames()

        ##################################################
        # Widgets.
        ##################################################

        self.btn_cr_cl = self.btn_sv_cl = self.btn_sc_dr = self.btn_ad_mv = self.btn_rm_mv = None
        self.lbl_fl_tx = self.cbb_ls_gn = self.cbb_ls_ac = self.prg_br_wg = self.lne_sr_cm = None
        self.lsw_mn_wg = self.mov_ap_wn = self.dsp_pn_wn = self.dir_im_wn = self.rtg_st_wn = None
        self.min_br_wn = self.rec_pn_wn = None

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

    def dragEnterEvent(self, event):

        event.accept()

    def dropEvent(self, event):

        event.accept()
        dropped_file = event.mimeData().urls()[0].toLocalFile()

        if MainWindow.last_movie_displayed and dropped_file.split('.')[-1].casefold() in ['jpg', 'jpeg', 'png', 'bmp']:
            dataprocess.set_local_poster(file=dropped_file, movie=MainWindow.last_movie_displayed)
            self.ui_information_panel(MainWindow.last_movie_displayed)

    def ui_information_panel(self, item: Collection | Movie) -> None:
        """Displays information about the received item.

        Args:
            item: Collection or Movie object.
        """

        is_collection: bool = isinstance(item, Collection)
        MainWindow.last_movie_displayed = None if is_collection else item
        img_path = constants.STR_PATHS["wishlist" if is_collection and item.name == "My Wishlist" else "default poster"]
        image = QPixmap(img_path if is_collection else str(item.thumb))

        if is_collection:
            title: str = f"→ {item.name.upper()}"
            summary: str = "\n".join([f"- {movie.title}" for movie in item.movies[:7]] + ["..."])
            top_right_text: str = f"{len(item.movies)} movie{'s' if len(item.movies) > 1 else ''}."

        else:
            content = item.load_data_file()
            title = content.get("title", f"{item.title.title()} ({item.year})")
            summary = content.get("summary", "Summary is being retrieved...")
            top_right_text = item.aesthetic_rating
        self.dsp_pn_wn.lbl_top_right.setText(top_right_text)
        self.dsp_pn_wn.lbl_image.setPixmap(image)
        self.dsp_pn_wn.lbl_title.setText(title)
        self.dsp_pn_wn.te_summary.setText(summary)

    def ui_manage_icons(self) -> None:
        """Icons are managed here."""

        super().ui_manage_icons()
        self.lne_sr_cm.addAction(self.icons["search"], self.lne_sr_cm.ActionPosition.LeadingPosition)
        self.btn_cr_cl.setIcon(self.icons["note"])
        self.btn_sv_cl.setIcon(self.icons["save"])
        self.btn_sc_dr.setIcon(self.icons["folder"])
        self.btn_ad_mv.setIcon(self.icons["add"])
        self.btn_rm_mv.setIcon(self.icons["rem"])

    def ui_manage_layouts_and_frames(self) -> None:
        """Frames and layouts are managed here."""

        self.pnl_frame = QtWidgets.QFrame()
        self.gnr_layout = QtWidgets.QVBoxLayout(self)
        self.hdr_layout = QtWidgets.QHBoxLayout()
        self.crp_layout = QtWidgets.QHBoxLayout()
        self.men_layout = QtWidgets.QVBoxLayout()
        self.lst_layout = QtWidgets.QVBoxLayout()
        self.inf_layout = QtWidgets.QHBoxLayout()
        self.frm_layout = QtWidgets.QHBoxLayout(self.pnl_frame)

        self.pnl_frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.lst_layout.setContentsMargins(10, 0, 0, 0)

        self.gnr_layout.addLayout(self.hdr_layout)
        self.gnr_layout.addLayout(self.crp_layout)
        self.crp_layout.addLayout(self.men_layout)
        self.crp_layout.addLayout(self.lst_layout)
        self.crp_layout.addLayout(self.inf_layout)
        self.inf_layout.addWidget(self.pnl_frame)

    def ui_manage_widgets(self) -> None:
        """Widgets are managed here."""

        self.btn_cr_cl = QtWidgets.QPushButton("Create collection")
        self.btn_sv_cl = QtWidgets.QPushButton("Save all collections")
        self.btn_sc_dr = QtWidgets.QPushButton("Scan directory")
        self.btn_ad_mv = QtWidgets.QPushButton("Add movie")
        self.btn_rm_mv = QtWidgets.QPushButton("Remove movie")
        self.lbl_fl_tx = QtWidgets.QLabel("Filter".center(30, "-"))
        self.cbb_ls_gn = QtWidgets.QComboBox()
        self.cbb_ls_ac = QtWidgets.QComboBox()
        self.prg_br_wg = QtWidgets.QProgressBar()
        self.lne_sr_cm = QtWidgets.QLineEdit()
        self.lsw_mn_wg = QtWidgets.QListWidget()
        self.mov_ap_wn = MovieAppender()
        self.rtg_st_wn = RatingAdjuster()
        self.dsp_pn_wn = DisplayPanel()
        self.rec_pn_wn = RecPanel()

        self.btn_ad_mv.setEnabled(False)
        self.btn_rm_mv.setEnabled(False)
        self.lbl_fl_tx.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.cbb_ls_gn.setMaxVisibleItems(5)
        self.cbb_ls_gn.addItems(["Genre"] + [genre.title() for genre in constants.MOVIE_GENRES])
        self.cbb_ls_ac.setMaxVisibleItems(5)
        self.clr_reload_cbb_actors()
        self.prg_br_wg.setTextVisible(False)
        self.prg_br_wg.setFixedHeight(5)
        self.prg_br_wg.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.lne_sr_cm.setClearButtonEnabled(True)
        self.lne_sr_cm.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        self.lne_sr_cm.setPlaceholderText("Search  or  run  '/'  commands.")
        self.lsw_mn_wg.installEventFilter(self)
        self.lsw_mn_wg.setAlternatingRowColors(True)
        self.lsw_mn_wg.setFocusPolicy(Qt.NoFocus)
        self.lsw_mn_wg.setWordWrap(True)
        self.lsw_mn_wg.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)

        self.hdr_layout.addWidget(self.btn_cr_cl)
        self.hdr_layout.addWidget(self.btn_sv_cl)
        self.hdr_layout.addWidget(self.btn_sc_dr)
        self.men_layout.addWidget(self.btn_ad_mv)
        self.men_layout.addWidget(self.btn_rm_mv)
        self.men_layout.addWidget(self.lbl_fl_tx)
        self.men_layout.addWidget(self.cbb_ls_gn)
        self.men_layout.addWidget(self.cbb_ls_ac)
        self.men_layout.addWidget(self.prg_br_wg)
        self.lst_layout.addWidget(self.lne_sr_cm)
        self.lst_layout.addWidget(self.lsw_mn_wg)
        self.frm_layout.addWidget(self.dsp_pn_wn)

    def ui_progress_bar_animation(self, flag: bool = None) -> None:
        """Creates a small animation for the progress bar."""

        if flag is None:

            for i in range(1, 101):              # The interface freezes for
                self.prg_br_wg.setValue(i)    # such a short time that using a
                sleep(0.003)                     # thread here seems unnecessary.

            sleep(0.3)
            self.prg_br_wg.reset()

        elif flag:

            self.prg_br_wg.setValue(100)
            sleep(0.3)
            self.prg_br_wg.reset()

        else:

            ...

    def logic_add_movie(self) -> None:
        """Opens the window which allows to add a movie."""

        if MainWindow.last_collection_opened:
            self.mov_ap_wn.show()

    def logic_add_movie_validation(self) -> None:
        """Attempts to create a 'Movie' object from the information entered
        by the user and adds this object to the currently open collection.
        """

        title: str = self.mov_ap_wn.le_movie_title.text()
        year: str = self.mov_ap_wn.le_movie_year.text()
        rating: str = self.mov_ap_wn.cbb_movie_rating.currentText()
        collection: Collection = MainWindow.last_collection_opened
        movie: Movie = Movie(title=title, year=year, rating=rating)

        if collection:
            collection.add_movie(movie)
            self.logic_list_display(collection.movies)
        self.mov_ap_wn.close()

    def logic_add_to_wishlist(self, movie: Movie) -> None:
        """Adds a movie to a special collection called 'My Wishlist'.

        Args:
            movie (Movie): Movie to add.
        """

        wishlist = next((item for item in MainWindow.all_collections if item.name == 'My Wishlist'), None)

        if wishlist is None:
            wishlist = Collection(name='My Wishlist')
            MainWindow.all_collections.append(wishlist)
        wishlist.add_movie(movie)
        self.ui_progress_bar_animation()

    def logic_commands(self) -> None:
        """Search bar commands logic is managed here."""

        function = self.commands.get(self.lne_sr_cm.text())

        if function:
            self.lne_sr_cm.clear()
            function()

    def logic_connect_widgets(self) -> None:
        """Connections are managed here."""

        self.btn_cr_cl.clicked.connect(self.logic_create_collection)
        self.btn_sv_cl.clicked.connect(self.logic_save_collection)
        self.btn_sc_dr.clicked.connect(self.logic_scan_dir)
        self.btn_ad_mv.clicked.connect(self.logic_add_movie)
        self.mov_ap_wn.btn_validate.clicked.connect(self.logic_add_movie_validation)
        self.btn_rm_mv.clicked.connect(self.logic_remove_movie)
        self.cbb_ls_gn.currentTextChanged.connect(self.logic_filter)
        self.cbb_ls_ac.currentTextChanged.connect(self.logic_filter)
        self.lne_sr_cm.textChanged.connect(self.logic_search_bar)
        self.lne_sr_cm.returnPressed.connect(self.logic_commands)
        self.lsw_mn_wg.itemClicked.connect(self.logic_single_click)
        self.rtg_st_wn.cbb_movie_rating.currentTextChanged.connect(self.logic_edit_movie_rating)
        self.thread.thread_finished.connect(partial(self.ui_progress_bar_animation, True))
        self.thread.thread_failed.connect(partial(self.ui_progress_bar_animation, False))

    def logic_create_collection(self) -> None:
        """Creates a new collection.

        Returns:
            None: None.
        """

        name, value = QtWidgets.QInputDialog.getText(self, "New collection", "Enter name:")
        if name and name not in [c.name for c in MainWindow.all_collections] and value:
            MainWindow.all_collections.append(Collection(name=name))
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

        official_title = QAction(self.icons.get('official'), "Assign official title")
        official_title.triggered.connect(partial(self.logic_rename_movie, item, False))
        rename_movie = QAction(self.icons.get('note'), "Rename")
        rename_movie.triggered.connect(partial(self.logic_rename_movie, item, True))
        edit_rating = QAction(self.icons.get('star'), "Edit rating")
        edit_rating.triggered.connect(partial(self.logic_show_rating_modifier))
        load_new_poster = QAction(self.icons.get('new_poster'), "Load new poster")
        load_new_poster.triggered.connect(partial(self.logic_modify_poster, item))
        load_default_poster = QAction(self.icons.get('default_poster'), "Set default poster")
        load_default_poster.triggered.connect(partial(self.logic_modify_poster, item, True))
        wishlist = QAction(self.icons.get('wishlist'), "Add to Wishlist")
        wishlist.triggered.connect(partial(self.logic_add_to_wishlist, item))
        watch_trailer = QAction(self.icons.get('trailer'), "Watch trailer")
        watch_trailer.triggered.connect(partial(self.logic_mini_browser, item, 'trailer'))
        see_on_imdb = QAction(self.icons.get('imdb'), "See on IMDb")
        see_on_imdb.triggered.connect(partial(self.logic_mini_browser, item, 'imdb'))
        delete_cache = QAction(self.icons.get('delete'), "Delete cached data")
        delete_cache.triggered.connect(item.remove_cache)

        movie_menu.addAction(official_title)
        movie_menu.addAction(rename_movie)
        movie_menu.addAction(edit_rating)
        movie_menu.addAction(load_new_poster)
        movie_menu.addAction(load_default_poster)
        movie_menu.addAction(wishlist)
        movie_menu.addAction(watch_trailer)
        movie_menu.addAction(see_on_imdb)
        movie_menu.addAction(delete_cache)

        movie_menu.exec(pos)
        movie_menu.deleteLater()

    def logic_delete_collection(self, collection: Collection) -> None:
        """Deletes a collection.

        Args:
            collection (Collection): Collection to delete.

        Returns:
            None: None.
        """

        if collection.remove():
            MainWindow.all_collections.remove(collection)
            self.logic_list_display(MainWindow.all_collections)

    def logic_edit_movie_rating(self) -> None:
        """Lets the user change their rating of the selected movie.

        Returns:
            None: None.
        """

        if self.lsw_mn_wg.selectedItems() and isinstance(self.lsw_mn_wg.selectedItems()[0].attr, Movie):
            selected_movie: Movie = self.lsw_mn_wg.selectedItems()[0].attr
            selected_movie.rating = self.rtg_st_wn.cbb_movie_rating.currentText()
            self.ui_information_panel(selected_movie)

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

        all_movies: list[Movie] = [movie for collection in MainWindow.all_collections for movie in collection.movies]
        query_g, query_a = self.cbb_ls_gn.currentText(), self.cbb_ls_ac.currentText()

        if query_g == "Genre" and query_a != "Actors":
            matching_movies = [movie for movie in all_movies if query_a in movie.actors]
        elif query_g != "Genre" and query_a == "Actors":
            matching_movies = [movie for movie in all_movies if query_g in movie.genre]
        elif query_g != "Genre" and query_a != "Actors":
            matching_movies = [movie for movie in all_movies if (query_g in movie.genre) and (query_a in movie.actors)]
        else:
            matching_movies = all_movies

        self.logic_list_display(matching_movies)

    def logic_generate_list_item(self, item: Collection | Movie) -> QtWidgets.QListWidgetItem:
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

        collection: Collection = self.dir_im_wn.collection
        number_of_files: int = self.dir_im_wn.lw_main.count()
        list_of_files: list = [self.dir_im_wn.lw_main.item(i) for i in range(number_of_files)]

        for item in list_of_files:
            title: str = item.title
            year: int = int(item.year) if item.year and item.year.isdigit() else 0
            path: str = item.text()
            rating: str = item.rating
            result: tuple = dataimport.make_movie(title=title, year=year, path=path, rating=rating)

            if result[0]:
                collection.add_movie(result[0])

        if collection not in MainWindow.all_collections:
            MainWindow.all_collections.append(collection)

        self.logic_list_display(collection.movies)
        self.dir_im_wn.close()

    def logic_list_display(self, items: list[Collection] | list[Movie]) -> None:
        """All display logic for the list widget is managed here.

        Args:
            items: List of Collection objects or Movie objects.

        Returns:
            None: None.
        """

        self.lsw_mn_wg.clear()
        previous_item = QtWidgets.QListWidgetItem("GO BACK")
        previous_item.attr = None
        previous_item.setIcon(self.icons.get('previous'))
        previous_item.setTextAlignment(Qt.AlignCenter)

        display_list = [self.logic_generate_list_item(item) for item in items]
        if (not items and MainWindow.all_collections) or (items and all(isinstance(item, Movie) for item in items)):
            display_list.insert(0, previous_item)
        else:  # When displaying collections.
            MainWindow.last_collection_opened = None

        for item in display_list:
            self.lsw_mn_wg.addItem(item)

    def logic_mini_browser(self, movie: Movie, content: str) -> None:
        """Instantiates a small browser that loads a link.

        Args:
            movie (Movie): The movie whose user wants to open a corresponding link.
            content (str): The link that should be loaded; 'trailer' or 'imdb'.

        Returns:
            None: None.
        """

        self.min_br_wn = MiniBrowser(movie=movie, content=content)
        self.min_br_wn.show()

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
            self.thread.define_thread_settings(dataretrieve.MovieScraper(movie), ("download_poster", True))
            self.thread.start()
            self.ui_progress_bar_animation()

        self.ui_information_panel(movie)

    def logic_open_collection(self, collection: Collection) -> None:
        """Allows to open a collection.

        Args:
            collection (Collection): Collection to open.

        Returns:
            None: None.
        """

        MainWindow.last_collection_opened = collection
        self.logic_list_display(collection.movies)
        self.btn_ad_mv.setEnabled(True)
        self.btn_rm_mv.setEnabled(True)

    def logic_remove_movie(self) -> None:
        """Removes a selected movie.

        Returns:
            None: None.
        """

        collection = MainWindow.last_collection_opened
        selected_items = self.lsw_mn_wg.selectedItems()

        if collection and selected_items and isinstance(selected_items[0].attr, Movie):
            movie_to_remove: Movie = selected_items[0].attr
            collection.remove_movie(movie_to_remove)
            movie_to_remove.remove_cache()
            del movie_to_remove
            self.logic_list_display(collection.movies)

    def logic_rename_collection(self, collection: Collection) -> None:
        """Renames a collection.

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
        """Renames a movie.

        Args:
            movie (Movie): Movie to rename.
            user_choice (bool): True for personal renaming, False to automatically rename with the official title.

        Returns:
            None: None.
        """

        if user_choice:
            new_name, value = QtWidgets.QInputDialog.getText(self, "Rename movie", "Enter new title:")
            success: bool = movie.rename(new_name) if new_name and value else True
        else:
            success: bool = movie.rename(movie.official_title)

        if not success:
            QtWidgets.QMessageBox.about(self, "Warning", constants.CACHE_WARNING)

        self.logic_update_list_widget()

    def logic_save_collection(self, collection: Collection) -> None:
        """Saves the created collections.

        Args:
            collection (Collection): Collection to save.
        """

        if self.sender() is self.btn_sv_cl:
            for item in MainWindow.all_collections:
                item.save()

        else:
            collection.save()

        self.ui_progress_bar_animation()
        self.logic_update_list_widget()

    def logic_scan_dir(self) -> None:
        """This method is called after clicking the button to scan a folder."""

        dialog = QtWidgets.QFileDialog.getExistingDirectory(self, caption="Python Movie Manager - Select Directory")

        if dialog:
            directory_path: Path = Path(dialog).resolve()
            directory_name: str = directory_path.stem
            suffix: int = 0

            while directory_name in [collection.name for collection in MainWindow.all_collections]:
                directory_name: str = directory_name.rsplit(sep='_', maxsplit=1)[0] + f"_{str(suffix).zfill(3)}"
                suffix += 1
            collection: Collection = MainWindow.last_collection_opened or Collection(name=directory_name)
            self.dir_im_wn = DirectoryImporter(collection, directory_path)
            self.dir_im_wn.btn_validate.clicked.connect(self.logic_import_directory)
            self.dir_im_wn.show()

    def logic_search_bar(self) -> None:
        """Search bar logic is managed here."""

        completer = QtWidgets.QCompleter(self.commands, self)
        theme: dict = dataimport.load_file_content(constants.PATHS["settings"])
        color: str = "color: #FFA500;" if theme["theme"] == "default" else "color: #EF745C;"
        background: str = "background: #3F3F3F" if theme["theme"] == "default" else "background: #531942"
        completer.popup().setStyleSheet(color + background)
        self.lne_sr_cm.setCompleter(completer)
        query: str = self.lne_sr_cm.text().strip().casefold()

        if not query.startswith("/"):
            box: list = self.last_collection_opened.movies if self.last_collection_opened else self.all_collections
            attribute: str = "title" if self.last_collection_opened else "name"
            items: list = [x for x in box if getattr(x, attribute).casefold().startswith(query)]
            self.logic_list_display(items)

    def logic_show_rating_modifier(self) -> None:
        """Shows rating modification dialog."""

        self.rtg_st_wn.cbb_movie_rating.setCurrentIndex(0)
        self.rtg_st_wn.show()

    def logic_single_click(self, clicked_item) -> None:
        """Handle a single click on items in the QListWidget."""

        if clicked_item.attr is None:
            self.logic_list_display(MainWindow.all_collections)
            self.btn_ad_mv.setEnabled(False)
            self.btn_rm_mv.setEnabled(False)
            return

        elif isinstance(clicked_item.attr, Movie):
            self.clr_reload_cbb_actors()
            scraper: dataretrieve.MovieScraper = dataretrieve.MovieScraper(clicked_item.attr)
            self.thread.define_thread_settings(scraper, ("download_poster", None), ("download_info", None))
            self.thread.start()
        self.ui_information_panel(clicked_item.attr)

    def logic_sort_collection(self) -> None:
        """Sorts a collection alphabetically."""

        if MainWindow.last_collection_opened:
            movies: list[Movie] = MainWindow.last_collection_opened.movies
            movies.sort()
            self.logic_list_display(movies)

    def logic_update_list_widget(self) -> None:
        """Refreshes the current items in the list widget."""

        selected_item_row: int = self.lsw_mn_wg.row(self.lsw_mn_wg.currentItem())
        items = [self.lsw_mn_wg.item(i).attr for i in range(self.lsw_mn_wg.count()) if self.lsw_mn_wg.item(i).attr]
        self.logic_list_display(items)

        if selected_item_row:
            self.lsw_mn_wg.scrollToItem(self.lsw_mn_wg.item(selected_item_row))

    def clr_reload_cbb_actors(self) -> None:
        """Reloads a list of all actors in the combobox."""

        self.cbb_ls_ac.blockSignals(True)
        self.cbb_ls_ac.clear()
        self.cbb_ls_ac.addItems(["Actors"] + dataimport.load_all_actors())
        self.cbb_ls_ac.blockSignals(False)

    def closeEvent(self, event):

        dataprocess.clear_cache()

    def eventFilter(self, watched, event: QEvent) -> bool:

        if event.type() == QEvent.ContextMenu and watched is self.lsw_mn_wg:
            list_item = watched.itemAt(event.pos())

            if list_item and isinstance(list_item.attr, Collection):
                self.logic_create_collection_menu(event.globalPos(), list_item.attr)

            elif list_item and isinstance(list_item.attr, Movie):
                self.logic_create_movie_menu(event.globalPos(), list_item.attr)

            else:
                return False
        return super().eventFilter(watched, event)


if __name__ == '__main__':
    constants.APP_HIDDEN_FOLDER.mkdir(exist_ok=True)
    dataprocess.clear_cache()
    root = QtWidgets.QApplication()
    application = MainWindow()
    application.show()
    root.exec()
