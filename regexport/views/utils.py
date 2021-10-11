from abc import ABC

from PySide2.QtWidgets import QWidget


class HasWidget(ABC):

    def __init__(self, widget: QWidget):
        self.__widget = widget

    @property
    def widget(self) -> QWidget:
        return self.__widget


