from PySide2.QtCore import Qt
from PySide2.QtWidgets import QWidget, QHBoxLayout, QLabel, QSlider
from traitlets import HasTraits, Unicode, Int, observe

from regexport.views.utils import HasWidget


class LabelledSliderModel(HasTraits):
    label = Unicode()
    min = Int(default_value=0)
    max = Int()
    value = Int(default_value=1000)
    label2 = Unicode(allow_none=True)

    def __repr__(self):
        return f"{self.__class__.__name__}(label='{self.label}', min={self.min}, max={self.max}, value={self.value})"

    @observe('value')
    def _clamp_value_to_be_inside_bounded_range(self, change):
        value = change.new
        print(self)
        if value < self.min:
            self.value = 0
        elif value > self.max:
            self.value = self.max


class LabelledSliderView(HasWidget):

    def __init__(self, model: LabelledSliderModel):
        widget = QWidget()
        HasWidget.__init__(self, widget=widget)

        layout = QHBoxLayout()
        widget.setLayout(layout)

        self.label = QLabel()
        layout.addWidget(self.label)

        self.slider = QSlider()
        self.slider.setOrientation(Qt.Horizontal)

        layout.addWidget(self.slider)

        self.value_label = QLabel()
        layout.addWidget(self.value_label)

        self.model = model
        self.model.observe(self.render)
        self.slider.valueChanged.connect(self._update_model_value)
        self.render()

    def render(self, change=None):
        self.label.setText(self.model.label)
        self.slider.setMinimum(self.model.min)
        self.slider.setMaximum(self.model.max)
        self.value_label.setText(str(self.model.value))

    def _update_model_value(self, value: int):
        self.model.value = value
