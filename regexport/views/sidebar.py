from typing import Tuple

from PySide2.QtWidgets import QVBoxLayout, QWidget

from .utils import HasWidget


class Sidebar(HasWidget):

    def __init__(self, widgets: Tuple[HasWidget, ...] = ()):
        self._widget = QWidget()
        HasWidget.__init__(self, widget=self._widget)

        layout = QVBoxLayout()
        self._widget.setLayout(layout)

        self.widgets = widgets
        for widget in widgets:
            layout.addWidget(widget.widget)
