"""This module contains the right display panel."""


from PySide6 import QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


from packages.ui.aesthetic import AestheticWindow


class DisplayPanel(AestheticWindow):

    def __init__(self):
        super().__init__()

        ##################################################
        # Layouts.
        ##################################################

        self.main_layout = None
        self.info_layout = None
        self.image_layout = None

        self.ui_manage_layouts()

        ##################################################
        # Widgets.
        ##################################################

        self.lbl_title = None
        self.lbl_top_right = None
        self.lbl_summary = None
        self.lbl_image = None

        self.ui_manage_widgets()

    def ui_manage_layouts(self) -> None:
        """Layouts are managed here.

        Returns:
            None: None.
        """

        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.info_layout = QtWidgets.QVBoxLayout()
        self.image_layout = QtWidgets.QVBoxLayout()

        self.main_layout.addLayout(self.info_layout)
        self.main_layout.addLayout(self.image_layout)

    def ui_manage_widgets(self) -> None:
        """Widgets are managed here.

        Returns:
            None: None.
        """

        self.lbl_top_right = QtWidgets.QLabel()
        self.lbl_top_right.setAlignment(Qt.AlignRight)
        self.lbl_image = QtWidgets.QLabel()
        self.lbl_title = QtWidgets.QLabel()
        self.lbl_title.setFont(QFont("Arial", 16))
        self.lbl_title.setAlignment(Qt.AlignTop)
        self.lbl_title.setWordWrap(True)
        self.lbl_summary = QtWidgets.QLabel()
        self.lbl_summary.setWordWrap(True)

        self.image_layout.addWidget(self.lbl_top_right)
        self.image_layout.addWidget(self.lbl_image)
        self.info_layout.addWidget(self.lbl_title)
        self.info_layout.addWidget(self.lbl_summary)
