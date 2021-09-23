from functools import partial

from PyQt5.QtCore import QThreadPool
from PyQt5.QtWidgets import QAction
from bg_atlasapi import BrainGlobeAtlas
from traitlets import HasTraits, Unicode, Instance, directional_link

from regexport.model import AppState
from regexport.utils.parallel import Task


class LoadAtlasActionModel(HasTraits):
    text = Unicode("&Load Brainglobe Atlas")
    atlas = Instance(BrainGlobeAtlas, allow_none=True)

    def register(self, model: AppState):
        directional_link((self, "atlas"), target=(model, "atlas"))

    def run(self):
        task = Task(BrainGlobeAtlas, "allen_mouse_25um")
        task.signals.finished.connect(partial(setattr, self, 'atlas'))
        pool = QThreadPool.globalInstance()
        pool.start(task)


class LoadAtlasAction(QAction):

    def __init__(self, model: LoadAtlasActionModel, *args, **kwargs):
        self.model = model
        super().__init__(*args, **kwargs)
        self.setText(self.model.text)
        self.triggered.connect(self.model.run)
