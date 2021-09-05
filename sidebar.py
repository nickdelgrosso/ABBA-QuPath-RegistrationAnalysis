from pathlib import Path
from typing import List

from PyQt5.QtWidgets import QVBoxLayout, QWidget, QPushButton, QFileDialog

from model import AppState, read_detection_file
from utils import HasWidget


class Sidebar(HasWidget):

    def __init__(self, model: AppState):
        self.model = model

        self._widget = QWidget()
        HasWidget.__init__(self, widget=self._widget)

        layout = QVBoxLayout()
        self._widget.setLayout(layout)




