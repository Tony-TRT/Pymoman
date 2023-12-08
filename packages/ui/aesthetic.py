"""
This module provides utility functions for managing the appearance of the user interface.
"""

import json

from PySide6.QtWidgets import QWidget, QApplication
from PySide6.QtGui import QIcon, QFontDatabase, QFont

from packages.constants import constants
from packages.logic.dataimport import load_file_content


def save_settings(settings: dict) -> None:
    """Saves settings in a file.

    Args:
        settings (dict): Settings dictionary.

    Returns:
        None:None.
    """

    with open(constants.PATHS.get("settings"), "w", encoding="UTF-8") as settings_file:
        json.dump(obj=settings, fp=settings_file, indent=4)


class AestheticWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.icons = {}
        self.settings: dict = load_file_content(constants.PATHS.get('settings'))
        self.default_font = None
        self.cyber_font = None
        self.default_font_big = None
        self.default_font_small = None

        if self.settings.get("theme") == "cyber":
            self.ui_apply_style("cyber")
        else:
            self.ui_apply_style("default")

        self.ui_load_fonts()

        if self.settings.get("font") == "cyber":
            self.ui_apply_font("cyber")
        else:
            self.ui_apply_font("default")

    def ui_apply_font(self, style: str) -> None:
        """Loads application font.

        Args:
            style (str): Font style (default or cyber).

        Returns:
            None: None.
        """

        if style == "default" and self.default_font:
            self.setFont(self.default_font)
            QApplication.instance().setFont(self.default_font)
        elif style == "cyber" and self.cyber_font:
            self.setFont(self.cyber_font)
            QApplication.instance().setFont(self.cyber_font)

        self.settings['font'] = style
        save_settings(self.settings)

    def ui_apply_style(self, style: str) -> None:
        """Loads application style.

        Args:
            style (str): Application style (default or cyber).

        Returns:
            None: None.
        """

        if style == "default":
            with open(constants.PATHS.get("default style"), "r", encoding="UTF-8") as style_file:
                self.setStyleSheet(style_file.read())
        else:
            with open(constants.PATHS.get("cyber style"), "r", encoding="UTF-8") as style_file:
                self.setStyleSheet(style_file.read())

        self.settings['theme'] = style
        save_settings(self.settings)

    def ui_load_fonts(self) -> None:
        """Loads the application fonts.

        Returns:
            None: None.
        """

        default_font = QFontDatabase.addApplicationFont(constants.STR_PATHS.get('default font'))
        default_font_family = QFontDatabase.applicationFontFamilies(default_font)[0]
        cyber_font = QFontDatabase.addApplicationFont(constants.STR_PATHS.get('cyber font'))
        cyber_font_family = QFontDatabase.applicationFontFamilies(cyber_font)[0]

        self.default_font = QFont(default_font_family)
        self.default_font.setPointSize(10)
        self.cyber_font = QFont(cyber_font_family)
        self.cyber_font.setPointSize(11)

        self.default_font_big = QFont(default_font_family)
        self.default_font_big.setPointSize(12)

        self.default_font_small = QFont(default_font_family)
        self.default_font_small.setPointSize(8)

    def ui_manage_icons(self) -> None:
        """Icons are managed here.

        Returns:
            None: None.
        """

        for icn_name, icn_path in constants.STR_ICONS.items():
            icon = QIcon(icn_path)
            self.icons[icn_name] = icon

        self.setWindowIcon(self.icons.get('logo'))
