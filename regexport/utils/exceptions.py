import sys

from PySide2.QtWidgets import QMessageBox


def _show_exception_dialog(t, value, traceback):
    QMessageBox.critical(None, "An Exception was Raised", f'Value: {value}')


def show_dialog_box_on_uncaught_exception():
    """
        Set sys.excepthook to this function so that a dialog box appears when exceptions are raised.
        from https://www.youtube.com/watch?v=hhRKiMceaeY
    """
    sys.excepthook = _show_exception_dialog

