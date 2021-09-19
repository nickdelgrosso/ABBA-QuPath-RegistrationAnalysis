from typing import List

from PyQt5.QtWidgets import QVBoxLayout, QWidget
from traitlets import HasTraits

from .utils import HasWidget


class SidebarModel(HasTraits):
    pass


class Sidebar(HasWidget):

    def __init__(self, model: SidebarModel, widgets: List[HasWidget] = []):
        self.model = model

        self._widget = QWidget()
        HasWidget.__init__(self, widget=self._widget)

        layout = QVBoxLayout()
        self._widget.setLayout(layout)

        self.widgets = widgets
        for widget in widgets:
            layout.addWidget(widget.widget)





