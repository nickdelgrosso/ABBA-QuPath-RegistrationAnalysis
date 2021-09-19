from PyQt5.QtWidgets import QComboBox
from traitlets import HasTraits, List as TList, Unicode, directional_link

from model import AppState
from views.utils import HasWidget


class TextSelectorModel(HasTraits):
    options = TList(Unicode, default_value=["Unknown", "Unknown2"])
    selected = Unicode(default_value="Unknown")

    def register(self, model: AppState, options_attr: str, selected_attr: str):
        directional_link(
            (model, options_attr),
            (self, 'options'),
        )
        self.selected = model.selected_colormap
        directional_link(
            (self, 'selected'),
            (model, selected_attr),
        )


class DropdownTextSelectorView(HasWidget):
    def __init__(self, model: TextSelectorModel):
        self.dropdown = QComboBox()
        HasWidget.__init__(self, widget=self.dropdown)

        self.model = model
        self.model.observe(self.update_cmap_dropdown_values, ['options'])
        self.model.observe(self.update_selected, ['selected'])
        self.update_cmap_dropdown_values(None)
        self.dropdown.currentTextChanged.connect(self.select_cmap_from_dropdown)


    def update_cmap_dropdown_values(self, changed):
        self.dropdown.clear()
        for cmap in self.model.options:
            self.dropdown.addItem(cmap)
        self.dropdown.setCurrentText(self.model.selected)

    def update_selected(self, changed):
        self.dropdown.setCurrentText(self.model.selected)

    def select_cmap_from_dropdown(self, text):
        print('selected', text)
        self.model.selected = text