from enum import Enum, auto

from PyQt5.QtWidgets import QComboBox
from traitlets import HasTraits, List as TList, Unicode, All

from views.utils import HasWidget


class Colormap(Enum):
    tab20c = auto()
    viridis = auto()


class ColormapSelectorModel(HasTraits):
    options = TList(Unicode, default_value=[cmap.name for cmap in Colormap])
    selected = Unicode(default_value=options.default_args[0][0])


class ColormapSelector(HasWidget):
    def __init__(self, model: ColormapSelectorModel):
        self.dropdown = QComboBox()
        HasWidget.__init__(self, widget=self.dropdown)

        self.model = model
        self.model.observe(self.update_cmap_dropdown_values, ['options'], type=All)
        self.model.options  # does have effect: triggers a notification (note: find way to not need this)
        self.dropdown.currentTextChanged.connect(self.select_cmap_from_dropdown)


    def update_cmap_dropdown_values(self, changed):
        self.dropdown.clear()
        for cmap in self.model.options:
            self.dropdown.addItem(cmap)
        self.dropdown.setCurrentText(self.model.selected)

    def select_cmap_from_dropdown(self, text):
        print('selected', text)
        self.model.selected = text