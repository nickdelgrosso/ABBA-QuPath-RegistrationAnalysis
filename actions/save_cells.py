from pathlib import Path

from PyQt5.QtWidgets import QAction, QFileDialog

from model import AppState


class SaveCellsActionModel:
    text = "Save Cells"

    def register(self, model: AppState):
        self.model = model

    def savedata(self, directory):
        self.model.cells.to_csv(Path(directory)/'output.csv')
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
