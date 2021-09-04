from PyQt5.QtWidgets import QVBoxLayout, QWidget, QPushButton, QFileDialog
from bg_atlasapi import BrainGlobeAtlas

from model import AppState, read_detection_file
from utils import HasWidget


class Sidebar(HasWidget):

    def __init__(self, model: AppState):
        self.model = model

        self._widget = QWidget()
        HasWidget.__init__(self, widget=self._widget)

        layout = QVBoxLayout()
        self._widget.setLayout(layout)

        button = QPushButton('Load Cells')
        layout.addWidget(button)
        button.clicked.connect(self.load_data)

    def load_data(self):
        filenames, filetype = QFileDialog.getOpenFileNames(
            parent=self._widget,
            caption="Load Cell Points from File",
            # dir="D:/QuPath Projects/Project3/export2",
            filter="TSV Files (*.tsv)"
        )

        if not filenames:
            return
        filename, *other_filenames = filenames
        if other_filenames:
            raise NotImplementedError("Multiple Filenames not yet implemented")

        df = read_detection_file(filename=filename, atlas=self.model.atlas)
        self.model.cells = df




