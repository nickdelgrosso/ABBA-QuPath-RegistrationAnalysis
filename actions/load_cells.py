from pathlib import Path
from typing import List

import pandas as pd
from PyQt5.QtWidgets import QAction, QFileDialog
from bg_atlasapi import BrainGlobeAtlas
from traitlets import HasTraits, Unicode, directional_link, Instance

from model import AppState, read_detection_file

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
        filename, *other_filenames = filenames
        if other_filenames:
            raise NotImplementedError("Multiple Filenames not yet implemented")

        if self.atlas is None:
            raise ValueError("No atlas detected, cannot register brain regions")
        df = read_detection_file(filename=filename, atlas=self.atlas)
        self.cells = df


class LoadCellsAction(QAction):

    def __init__(self, model: LoadCellsModel, *args, **kwargs):
        self.vmodel = model
        super().__init__(*args, **kwargs)
        self.setText(self.vmodel.text)
        self.triggered.connect(self.run)

    def run(self):
        filenames, filetype = QFileDialog.getOpenFileNames(
            caption="Load Cell Points from File",
            filter="TSV Files (*.tsv)"
        )

        filenames = [Path(f) for f in filenames]
        self.vmodel.load_files(filenames=filenames)

