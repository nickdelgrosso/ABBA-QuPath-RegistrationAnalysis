from abc import ABC
from typing import Callable

from PyQt5.QtCore import QObject, pyqtSignal, QThread, QRunnable
from qtpy.QtWidgets import QWidget


class HasWidget(ABC):

    def __init__(self, widget: QWidget):
        self.__widget = widget

    @property
    def widget(self) -> QWidget:
        return self.__widget


class Signals(QObject):
    finished = pyqtSignal(object)


class Worker(QRunnable):

    def __init__(self, fun: Callable, *args, **kwargs):
        super().__init__()
        self._orig_thread_id = int(QThread.currentThreadId())
        self.fun = fun
        self.args = args
        self.kwargs = kwargs
        self.signals = Signals()

    # @pyqtSlot
    def run(self):
        new_thread_id = int(QThread.currentThreadId())
        assert self._orig_thread_id != new_thread_id, "Worker not running in seperate thread, pointless."
        result = self.fun(*self.args, **self.kwargs)
        self.signals.finished.emit(result)
