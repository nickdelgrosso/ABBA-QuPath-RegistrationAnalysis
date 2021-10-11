from pathlib import Path
from typing import Union, Tuple

from PIL import ImageGrab
from PySide2.QtCore import Qt, QThreadPool
from PySide2.QtWidgets import QMainWindow, QWidget, QSplitter, QToolBar, QAction

from .utils import HasWidget


class MainWindow(QMainWindow):

    def __init__(self, main_widgets: Tuple[Union[QWidget, HasWidget], ...] = (),
                 menu_actions: Tuple[QAction, ...] = ()):
        super().__init__()
        self._widgets = main_widgets  # keep reference to these widgets, so they aren't garbage collected.

        self._splitter = QSplitter(Qt.Horizontal)
        self.setCentralWidget(self._splitter)
        for widget in self._widgets:
            self._splitter.addWidget(widget.widget if hasattr(widget, 'widget') else widget)

        self._actions = menu_actions
        tool_bar = QToolBar()
        for action in menu_actions:
            tool_bar.addAction(action)
        self.addToolBar(Qt.TopToolBarArea, tool_bar)

