from pathlib import Path

import pandas as pd
from PyQt5.QtWidgets import QAction, QFileDialog

from model import AppState


class SaveCellsActionModel:
    text = "Save Cells"

    def register(self, model: AppState):
        self.model = model

    def savedata(self, filename):
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
        df: pd.DataFrame = df.drop(columns=['BGIdx'])

        print(df.info())
        print(filename)

        if filename.suffix.lower() == ".csv":
            df.to_csv(filename, index=False)
        elif filename.suffix.lower() == ".feather":
            df.to_feather(filename)
        else:
            raise TypeError(f"Error saving file {str(filename)}: {filename.suffix} extension not supported.")
        print("File saved")


class SaveCellsAction(QAction):

    def __init__(self, model: SaveCellsActionModel, *args, **kwargs):
        self.model = model
        super().__init__(*args, **kwargs)
        self.setText(model.text)
        self.triggered.connect(self.click)

    def click(self):
        filename, filetype_filter = QFileDialog.getSaveFileName(filter="Feather file (*.feather);;CSV file (*.csv)")

        if not filename:
            return

        self.model.savedata(Path(filename))
