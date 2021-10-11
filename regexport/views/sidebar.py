from typing import Tuple

from PySide2.QtWidgets import QVBoxLayout, QWidget, QHBoxLayout

from .utils import HasWidget


class Layout(HasWidget):

    def __init__(self, widgets: Tuple[HasWidget, ...] = (), horizontal=False):
        self._widget = QWidget()
        HasWidget.__init__(self, widget=self._widget)

        layout = QHBoxLayout() if horizontal else QVBoxLayout()
        self._widget.setLayout(layout)

        self.widgets = widgets
        for widget in widgets:
            layout.addWidget(widget.widget)
