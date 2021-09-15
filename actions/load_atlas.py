from PyQt5.QtWidgets import QAction
from bg_atlasapi import BrainGlobeAtlas
from traitlets import HasTraits, Unicode, Instance, directional_link

from model import AppState


class LoadAtlasActionModel(HasTraits):
    text = Unicode("&Load Brainglobe Atlas")
    atlas = Instance(BrainGlobeAtlas, allow_none=True)

    def register_model(self, model: AppState):
        directional_link((self, "atlas"), target=(model, "atlas"))

    def run(self):
        self.atlas = BrainGlobeAtlas("allen_mouse_25um")


class LoadAtlasAction(QAction):

    def __init__(self, model: LoadAtlasActionModel, *args, **kwargs):
        self.model = model
        super().__init__(*args, **kwargs)
        self.setText(self.model.text)
        self.triggered.connect(self.model.run)