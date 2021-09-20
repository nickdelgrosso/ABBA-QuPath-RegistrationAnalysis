from pathlib import Path
from typing import List

import pandas as pd
from PyQt5.QtWidgets import QAction, QFileDialog
from bg_atlasapi import BrainGlobeAtlas
from traitlets import HasTraits, Unicode, directional_link, Instance

from model import AppState
from data.load_data import read_detection_files


class LoadCellsModel(HasTraits):
    text = Unicode("&Load TSV Files")
    atlas = Instance(BrainGlobeAtlas, allow_none=True)
    cells = Instance(pd.DataFrame, allow_none=True)

    def register(self, model: AppState):
        directional_link((model, 'atlas'), (self, 'atlas'))
        directional_link((self, 'cells'), (model, 'cells'))

    def load_files(self, filenames: List[Path]):
        if not filenames:
            return
        if self.atlas is None:
            raise ValueError("No atlas detected, cannot register brain regions")
        df = read_detection_files(filenames, atlas=self.atlas)
        self.cells = df


class LoadCellsAction(QAction):

    def __init__(self, model: LoadCellsModel, *args, **kwargs):
        self.model = model
        super().__init__(*args, **kwargs)
        self.setText(self.model.text)
        self.triggered.connect(self.run)

    def run(self):
        filenames, filetype = QFileDialog.getOpenFileNames(
            caption="Load Cell Points from File",
            filter="TSV Files (*.tsv)"
        )

        filenames = [Path(f) for f in filenames]
        self.model.load_files(filenames=filenames)

