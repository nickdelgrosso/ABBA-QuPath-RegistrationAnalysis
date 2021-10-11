from typing import Callable

from PySide2.QtCore import QObject, Signal, QRunnable, QThread, Slot


class TaskSignals(QObject):
    finished = Signal(object)


class Task(QRunnable):

    def __init__(self, fun: Callable, *args, **kwargs):
        """
        Runs function with args and kwargs when Task.run() is called, outputting to the Task.signals.finished signal.

        Meant to be used with QThreadPool.start(my_task)

        Resources:
          - https://www.pythonguis.com/tutorials/multithreading-pyqt-applications-qthreadpool/
          - https://realpython.com/python-pyqt-qthread/#using-qthread-to-prevent-freezing-guis
        """

        super().__init__()
        self._orig_thread = QThread.currentThread()
        self.fun = fun
        self.args = args
        self.kwargs = kwargs
        self.signals = TaskSignals()

    def run(self):
        assert self._orig_thread != QThread.currentThread(), "Worker not running in seperate thread, pointless."
        result = self.fun(*self.args, **self.kwargs)
        self.signals.finished.emit(result)
