from PySide2.QtCore import Qt
from PySide2.QtWidgets import QCheckBox, QLabel, QWidget, QHBoxLayout

from traitlets import HasTraits, Bool, link, Unicode

from regexport.model import AppState
from regexport.views.utils import HasWidget


class CheckboxModel(HasTraits):
    label = Unicode(default_value='')
    checked = Bool(default_value=True)

    def register(self, model: AppState, model_property: str):
        link(
            (self, 'checked'),
            (model, model_property)
        )

    def click(self):

        self.checked = not self.checked
        print('checked:', self.checked)


class CheckboxView(HasWidget):

    def __init__(self, model: CheckboxModel):
        self.checkbox = QCheckBox(model.label)
        HasWidget.__init__(self, widget=self.checkbox)

        self.checkbox.setChecked(model.checked)
        self.checkbox.clicked.connect(model.click)

        model.observe(self.render, 'checked')

    def render(self, changed):
        self.checkbox.setChecked(changed.new)


