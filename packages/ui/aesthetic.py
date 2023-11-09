"""This module provides utility functions for managing the appearance of the user interface"""


from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QIcon


from packages.constants import constants


class AestheticWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.icons = {}
        self.ui_apply_style()

    def ui_manage_icons(self) -> None:
        """Icons are managed here.

        Returns:
            None: None.
        """

        for icn_name, icn_path in constants.STR_ICONS.items():
            icon = QIcon(icn_path)
            self.icons[icn_name] = icon

        self.setWindowIcon(self.icons.get('logo'))

    def ui_apply_style(self) -> None:
        """Style is managed here.

        Returns:
            None: None.
        """

        with open(constants.PATHS.get('style'), 'r', encoding="UTF-8") as style_file:
            self.setStyleSheet(style_file.read())
