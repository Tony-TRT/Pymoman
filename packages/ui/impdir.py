from pathlib import Path


from PySide6 import QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon


from ..logic.collection import Collection
from ..logic.dataimport import find_movie_files
from packages.constants import constants


class DirectoryImporter(QtWidgets.QWidget):

    def __init__(self, collection: Collection, path: Path):
        super().__init__()

        self.setWindowTitle("Python Movie Manager - Import files")
        self.setFixedSize(380, 470)
        self.collection = collection
        self.directory = path
        self.files_path = find_movie_files(path)

        ##################################################
        # Layouts.
        ##################################################

        self.main_layout = None
        self.top_layout = None
        self.bottom_layout = None

        self.ui_manage_layouts()

        ##################################################
        # Widgets.
        ##################################################

        self.le_title_tag = None
        self.le_year_tag = None
        self.lbl_info = None
        self.cbb_rating_tag = None
        self.lw_main = None
        self.btn_validate = None

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

        self.logic_initial_display()

    def ui_apply_style(self) -> None:
        """Style is managed here.

        Returns:
            None: None.
        """

        with open(constants.PATHS.get('style'), 'r', encoding="UTF-8") as style_file:
            self.setStyleSheet(style_file.read())

    def ui_manage_icons(self) -> None:
        """Icons are managed here.

        Returns:
            None: None.
        """

        for icn_name, icn_path in constants.STR_ICONS.items():
            icon = QIcon(icn_path)
            self.icons[icn_name] = icon

        self.setWindowIcon(self.icons.get('logo'))
        self.btn_validate.setIcon(self.icons.get('add'))

    def ui_manage_layouts(self) -> None:
        """Layouts are managed here.

        Returns:
            None: None.
        """

        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.top_layout = QtWidgets.QHBoxLayout()
        self.bottom_layout = QtWidgets.QVBoxLayout()

        self.main_layout.addLayout(self.top_layout)
        self.main_layout.addLayout(self.bottom_layout)

    def ui_manage_widgets(self) -> None:
        """Widgets are managed here.

        Returns:
            None: None.
        """

        self.le_title_tag = QtWidgets.QLineEdit()
        self.le_title_tag.setPlaceholderText("Enter title here")
        self.le_title_tag.setFixedHeight(30)
        self.le_year_tag = QtWidgets.QLineEdit()
        self.le_year_tag.setPlaceholderText("Enter release year here")
        self.le_year_tag.setFixedHeight(30)
        self.lbl_info = QtWidgets.QLabel(constants.IMPORT_INFO)
        self.lbl_info.setWordWrap(True)
        self.lbl_info.setAlignment(Qt.AlignCenter)
        self.cbb_rating_tag = QtWidgets.QComboBox()
        self.cbb_rating_tag.addItems(["-", '1', '2', '3', '4', '5'])
        self.lw_main = QtWidgets.QListWidget()
        self.lw_main.setAlternatingRowColors(True)
        self.lw_main.setFocusPolicy(Qt.NoFocus)
        self.btn_validate = QtWidgets.QPushButton("Add all tagged movies")

        self.top_layout.addWidget(self.le_title_tag)
        self.top_layout.addWidget(self.le_year_tag)
        self.bottom_layout.addWidget(self.lbl_info)
        self.bottom_layout.addWidget(self.cbb_rating_tag)
        self.bottom_layout.addWidget(self.lw_main)
        self.bottom_layout.addWidget(self.btn_validate)

    def logic_connect_widgets(self) -> None:
        """Connections are managed here.

        Returns:
            None: None.
        """

        self.le_title_tag.textChanged.connect(
            lambda: self.logic_update_item_attribute('title', self.le_title_tag))
        self.le_year_tag.textChanged.connect(
            lambda: self.logic_update_item_attribute('year', self.le_year_tag))
        self.cbb_rating_tag.currentTextChanged.connect(
            lambda: self.logic_update_item_attribute('rating', self.cbb_rating_tag))
        self.lw_main.itemClicked.connect(self.logic_single_click)

    def logic_initial_display(self) -> None:
        """Initial display logic for the list widget is managed here.

        Returns:
            None: None.
        """

        for path in self.files_path:
            lw_item = QtWidgets.QListWidgetItem(path)
            lw_item.title = None
            lw_item.year = None
            lw_item.rating = None
            lw_item.setTextAlignment(Qt.AlignCenter)
            self.lw_main.addItem(lw_item)

    def logic_single_click(self, clicked_item) -> None:
        """Handle a single click on items in the QListWidget.

        Returns:
            None: None.
        """

        attribute_mapping = {
            self.le_title_tag: "title",
            self.le_year_tag: "year",
            self.cbb_rating_tag: "rating"
        }

        for widget, attribute in attribute_mapping.items():
            value = getattr(clicked_item, attribute, None)
            if isinstance(widget, QtWidgets.QLineEdit):
                widget.setText(value if value is not None else '')
            else:
                widget.setCurrentIndex(int(value) if value is not None and value.isdigit() else 0)

    def logic_update_item_attribute(self, attr: str, sender) -> None:
        """Update a selected custom attribute of a QListWidgetItem.

        Args:
            attr (str): Attribute to modify.
            sender: Since self.sender() returns None when using lambda, we are directly passing the sender here.

        Returns:
            None: None.
        """

        selected_items = self.lw_main.selectedItems()

        if selected_items:
            selected_item = selected_items[0]

            if isinstance(sender, QtWidgets.QComboBox):
                new_value = sender.currentText()

            else:
                new_value = sender.text()

            setattr(selected_item, attr, new_value)
