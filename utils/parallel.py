from typing import Callable

from PyQt5.QtCore import QObject, pyqtSignal, QRunnable, QThread


class TaskSignals(QObject):
    finished = pyqtSignal(object)


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
        self._orig_thread_id = int(QThread.currentThreadId())
        self.fun = fun
        self.args = args
        self.kwargs = kwargs
        self.signals = TaskSignals()

    # @pyqtSlot
    def run(self):
        new_thread_id = int(QThread.currentThreadId())
        assert self._orig_thread_id != new_thread_id, "Worker not running in seperate thread, pointless."
        result = self.fun(*self.args, **self.kwargs)
        self.signals.finished.emit(result)