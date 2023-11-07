from PySide6 import QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon


from packages.constants import constants


class DirectoryImporter(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Python Movie Manager - Import files")
        self.setFixedSize(380, 470)

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
        self.btn_validate = QtWidgets.QPushButton("Add all tagged movies")

        self.top_layout.addWidget(self.le_title_tag)
        self.top_layout.addWidget(self.le_year_tag)
        self.bottom_layout.addWidget(self.lbl_info)
        self.bottom_layout.addWidget(self.cbb_rating_tag)
        self.bottom_layout.addWidget(self.lw_main)
        self.bottom_layout.addWidget(self.btn_validate)
