from PyQt5.QtWidgets import QVBoxLayout, QWidget

from model import AppState
from utils import HasWidget


class Sidebar(HasWidget):

    def __init__(self, model: AppState):
        self.model = model

        self._widget = QWidget()
        HasWidget.__init__(self, widget=self._widget)

        layout = QVBoxLayout()
        self._widget.setLayout(layout)




