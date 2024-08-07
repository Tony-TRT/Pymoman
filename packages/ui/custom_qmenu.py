from functools import partial

from PySide6.QtWidgets import QMenu
from PySide6.QtGui import QAction, QIcon


class CustomQMenu(QMenu):

    def __init__(self, parent=None, clicked_item=None):
        super().__init__(parent=parent)

        self.clicked_item = clicked_item
        self.menu_actions: dict = {}

    def new_action(self, *args) -> None:
        """Adds a new action to the menu.

        Args:
            *args: A variable length argument list containing:
                - key (str): The key to identify the action.
                - icon (QIcon): The icon to display for the action.
                - text (str): The text to display for the action.
                - function (callable): The function to call when the action is triggered.
        """

        is_collection: bool = hasattr(self.clicked_item, "name")
        key, icon, text = args[:3]
        function = args[3] if is_collection else None
        self.menu_actions[key] = QAction(icon, text)
        self.addAction(self.menu_actions[key])

        if is_collection and function:
            self.menu_actions[key].triggered.connect(partial(function, self.clicked_item))
