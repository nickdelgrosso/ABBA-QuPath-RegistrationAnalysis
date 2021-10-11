from os import path

from PIL import ImageGrab
from PySide2.QtWidgets import QWidget


def save_screenshot(widget: QWidget, filename: str, use_pil=True) -> None:
    if use_pil:
        ImageGrab.grab(bbox=widget.geometry().getCoords()).save(filename)
    else:
        widget.grab().save(filename, path.splitext(filename)[-1][1:])
