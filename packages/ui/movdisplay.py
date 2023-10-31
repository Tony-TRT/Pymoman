from PySide6 import QtWidgets
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class MovieTagDisplay(QtWidgets.QWidget):

    def __init__(self):

        super(MovieTagDisplay, self).__init__()

        self.ui_manage_layouts()
        self.ui_manage_widgets()

    def ui_manage_layouts(self):

        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.info_layout = QtWidgets.QVBoxLayout()
        self.poster_layout = QtWidgets.QVBoxLayout()

        self.main_layout.addLayout(self.info_layout)
        self.main_layout.addLayout(self.poster_layout)

    def ui_manage_widgets(self):

        self.rating_label = QtWidgets.QLabel()
        self.rating_label.setAlignment(Qt.AlignRight)
        self.poster_label = QtWidgets.QLabel()
        self.title_label = QtWidgets.QLabel()
        self.title_label.setFont(QFont("Arial", 16))
        self.title_label.setAlignment(Qt.AlignTop)
        self.title_label.setWordWrap(True)
        self.summary_label = QtWidgets.QLabel()
        self.summary_label.setWordWrap(True)

        self.poster_layout.addWidget(self.rating_label)
        self.poster_layout.addWidget(self.poster_label)
        self.info_layout.addWidget(self.title_label)
        self.info_layout.addWidget(self.summary_label)
