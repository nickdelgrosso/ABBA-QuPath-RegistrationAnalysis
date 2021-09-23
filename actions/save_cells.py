from pathlib import Path

from PyQt5.QtWidgets import QAction, QFileDialog

from model import AppState


class SaveCellsActionModel:
    text = "Save Cells"

    def register(self, model: AppState):
        self.model = model

    def savedata(self, directory):
        print('File saving...')

        types = {
            'Image': 'category',
            'BrainRegion': 'category',
            'Acronym': 'category',
            'X': 'float32',
            'Y': 'float32',
            'Z': 'float32',
        }

        types.update({col: 'uint16' for col in self.model.cells.columns if "Num Spots" in col})
        df = self.model.cells.astype(types)

        print(df.info())
        df.to_feather(Path(directory) / 'output.feather')
        print("File saved")


class SaveCellsAction(QAction):

    def __init__(self, model: SaveCellsActionModel, *args, **kwargs):
        self.model = model
        super().__init__(*args, **kwargs)
        self.setText(model.text)
        self.triggered.connect(self.click)

    def click(self):
        directory = QFileDialog.getExistingDirectory()
        self.model.savedata(directory)
