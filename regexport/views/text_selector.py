from PyQt5.QtWidgets import QComboBox
from traitlets import HasTraits, List as TList, Unicode, directional_link, observe

from regexport.model import AppState
from regexport.views.utils import HasWidget


class TextSelectorModel(HasTraits):
    options = TList(Unicode(), default_value=["Unknown", "Unknown2"])
    selected = Unicode(default_value="Unknown")

    def register(self, model: AppState, options_attr: str, selected_attr: str):
        directional_link(
            (model, options_attr),
            (self, 'options'),
        )
        self.selected = getattr(model, selected_attr)
        directional_link(
            (self, 'selected'),
            (model, selected_attr),
        )

    @observe('options')
    def reset_selected(self, changed):
        self.selected = self.options[0]

    def select(self, option: str):
        if option not in self.options:
            raise ValueError(f"'{option}' not in {self.options}")
        self.selected = option


class DropdownTextSelectorView(HasWidget):
    def __init__(self, model: TextSelectorModel):
        self.dropdown = QComboBox()
        HasWidget.__init__(self, widget=self.dropdown)

        self.model = model
        self.model.observe(self.render, ['options'])
        self.model.observe(self.update_selected, ['selected'])
        self.dropdown.currentTextChanged.connect(self.select_text_from_dropdown)
        self.render(None)

    def render(self, changed=None):
        self.dropdown.currentTextChanged.disconnect()  # clearin
        self.dropdown.clear()
        for option in self.model.options:
            self.dropdown.addItem(option)
        self.dropdown.setCurrentText(self.model.selected)
        self.dropdown.currentTextChanged.connect(self.select_text_from_dropdown)

    def update_selected(self, changed):
        self.dropdown.setCurrentText(self.model.selected)

    def select_text_from_dropdown(self, text):
        print('selected', text)
        self.model.selected = text
