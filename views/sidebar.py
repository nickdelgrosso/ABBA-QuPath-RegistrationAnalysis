from enum import Enum, auto

from PyQt5.QtWidgets import QVBoxLayout, QWidget, QComboBox
from traitlets import HasTraits, UseEnum, Tuple, List, Unicode, All

from model import AppState
from .utils import HasWidget


class Colormap(Enum):
    tab20c = auto()
    viridis = auto()


class SidebarModel(HasTraits):
    colormap_options = List(Unicode, default_value=[cmap.name for cmap in Colormap])
    selected_colormap = Unicode(default_value=colormap_options.default_args[0][0])


class Sidebar(HasWidget):

    def __init__(self, model: SidebarModel):
        self.model = model

        self._widget = QWidget()
        HasWidget.__init__(self, widget=self._widget)

        layout = QVBoxLayout()
        self._widget.setLayout(layout)

        self.cmap_dropdown = QComboBox()
        self.cmap_dropdown.currentTextChanged.connect(self.select_cmap_from_dropdown)
        layout.addWidget(self.cmap_dropdown)
        self.model.observe(self.update_cmap_dropdown_values, ['colormap_options'], type=All)
        self.model.colormap_options  # does have effect: triggers a notification (note: find way to not need this)

    def update_cmap_dropdown_values(self, changed):
        self.cmap_dropdown.clear()
        for cmap in self.model.colormap_options:
            self.cmap_dropdown.addItem(cmap)
        self.cmap_dropdown.setCurrentText(self.model.selected_colormap)

    def select_cmap_from_dropdown(self, text):
        self.model.selected_colormap = text




