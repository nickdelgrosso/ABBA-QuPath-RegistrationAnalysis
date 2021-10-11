from functools import partial

from PySide2.QtCore import QThreadPool
from PySide2.QtWidgets import QAction
from bg_atlasapi import BrainGlobeAtlas
from traitlets import HasTraits, Unicode, Instance, directional_link

from regexport.model import AppState
from regexport.utils.parallel import Task


class LoadAtlasActionModel(HasTraits):
    text = Unicode("1. Load Brainglobe Atlas")
    atlas = Instance(BrainGlobeAtlas, allow_none=True)

    def register(self, model: AppState):
        directional_link((self, "atlas"), target=(model, "atlas"))

    def click(self):
        self.atlas = self.load_brainglobe_atlas()

    @staticmethod
    def load_brainglobe_atlas() -> BrainGlobeAtlas:
        # Static method used for multithreading
        return BrainGlobeAtlas("allen_mouse_25um")


class LoadAtlasAction(QAction):

    def __init__(self, model: LoadAtlasActionModel, *args, **kwargs):
        self.model = model
        super().__init__(*args, **kwargs)
        self.setText(self.model.text)
        self.triggered.connect(self.click)

    def click(self):
        task = Task(self.model.load_brainglobe_atlas)
        task.signals.finished.connect(partial(setattr, self.model, 'atlas'))
        QThreadPool.globalInstance().start(task)

