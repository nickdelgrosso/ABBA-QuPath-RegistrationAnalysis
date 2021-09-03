from typing import List, Union

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QWidget, QSplitter

from utils import HasWidget


class MainWindow(QMainWindow):

    def __init__(self, main_widgets: List[Union[QWidget, HasWidget]]):
        super().__init__()
        self._widgets = main_widgets  # keep reference to these widgets, so they aren't garbage collected.

        self._splitter = QSplitter(Qt.Horizontal)
        self.setCentralWidget(self._splitter)
        for widget in self._widgets:
            self._splitter.addWidget(widget.widget if hasattr(widget, 'widget') else widget)
