from abc import ABC
from typing import Callable

from PyQt5.QtCore import QObject, pyqtSignal
from qtpy.QtWidgets import QWidget


class HasWidget(ABC):

    def __init__(self, widget: QWidget):
        self.__widget = widget

    @property
    def widget(self) -> QWidget:
        return self.__widget


class Worker(QObject):
    start = pyqtSignal()
    started = pyqtSignal(str)
    finished = pyqtSignal(object)

    def __init__(self, fun: Callable, *args, **kwargs):
        super().__init__()
        self.fun = fun
        self.args = args
        self.kwargs = kwargs
        self.start.connect(self.run)

    # @pyqtSlot
    def run(self):
        self.finished.connect(self.deleteLater)
        print('started working...')
        self.started.emit("started run")
        result = self.fun(*self.args, **self.kwargs)
        print('finished working...')
        self.finished.emit(result)