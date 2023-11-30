"""
This module provides utility functions for managing the appearance of the user interface.
"""

from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtGui import QIcon, QFontDatabase, QFont

from packages.constants import constants


class AestheticWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.icons = {}
        self.application_font = None
        self.application_font_big = None
        self.application_font_small = None

        self.ui_load_font()
        self.ui_apply_style()
        self.ui_apply_font()

    def ui_apply_font(self) -> None:
        """Applies the application font.

        Returns:
            None: None.
        """

        if self.application_font:
            self.setFont(self.application_font)
            QApplication.instance().setFont(self.application_font)

    def ui_apply_style(self) -> None:
        """Style is managed here.

        Returns:
            None: None.
        """

        with open(constants.PATHS.get('default style'), 'r', encoding="UTF-8") as style_file:
            self.setStyleSheet(style_file.read())

    def ui_load_font(self) -> None:
        """Loads the application font.

        Returns:
            None: None.
        """

        font = QFontDatabase.addApplicationFont(constants.STR_PATHS.get('font'))
        font_family = QFontDatabase.applicationFontFamilies(font)[0]

        self.application_font = QFont(font_family)
        self.application_font.setPointSize(10)

        self.application_font_big = QFont(font_family)
        self.application_font_big.setPointSize(12)

        self.application_font_small = QFont(font_family)
        self.application_font_small.setPointSize(8)

    def ui_manage_icons(self) -> None:
        """Icons are managed here.

        Returns:
            None: None.
        """

        for icn_name, icn_path in constants.STR_ICONS.items():
            icon = QIcon(icn_path)
            self.icons[icn_name] = icon

        self.setWindowIcon(self.icons.get('logo'))
