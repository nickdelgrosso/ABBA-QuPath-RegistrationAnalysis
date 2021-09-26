from pathlib import Path

import pandas as pd
from PyQt5.QtWidgets import QAction, QFileDialog, QCheckBox, QDialog

from regexport.model import AppState


class SaveCellsActionModel:
    text = "3. Save Cells"

    def register(self, model: AppState):
        self.model = model

    def savedata(self, filename: Path, selected_regions_only: bool = False):
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
        if selected_regions_only:
            df = df.iloc[self.model.selected_cell_ids]

        print(df.info())
        print(filename)

        if filename.suffix.lower() == ".csv":
            df.to_csv(filename, index=False)
        elif filename.suffix.lower() == ".feather":
            df.reset_index(drop=True).to_feather(filename)
        else:
            raise TypeError(f"Error saving file {str(filename)}: {filename.suffix} extension not supported.")
        print("File saved")


class ChkBxFileDialog(QFileDialog):
    def __init__(self, chkBxTitle="Selected Regions Only", filter="*.txt"):
        super().__init__(filter=filter)
        self.setSupportedSchemes(["file"])
        self.setOption(QFileDialog.DontUseNativeDialog)
        self.setAcceptMode(QFileDialog.AcceptSave)
        self.setNameFilter("Feather file (*.feather);;CSV file (*.csv)")
        self.selectNameFilter("Feather file (*.feather);;CSV file (*.csv)")
        self.chkBx = QCheckBox(chkBxTitle)
        self.layout().addWidget(self.chkBx)

    @property
    def full_filename(self) -> Path:
        filename = self.selectedUrls()[0].toLocalFile()
        extension_filter = self.selectedNameFilter()
        extension = extension_filter[extension_filter.index('*.') + 1:-1]
        full_filename = Path(filename).with_suffix(extension)
        return full_filename

    @property
    def selected_regions_only(self) -> bool:
        return self.chkBx.isChecked()


class SaveCellsAction(QAction):

    def __init__(self, model: SaveCellsActionModel, *args, **kwargs):
        self.model = model
        super().__init__(*args, **kwargs)
        self.setText(model.text)
        self.triggered.connect(self.click)

    def click(self):
        # filename, filetype_filter = QFileDialog.getSaveFileName(filter="Feather file (*.feather);;CSV file (*.csv)")
        dialog = ChkBxFileDialog()
        if dialog.exec_() == QDialog.Accepted:
            self.model.savedata(
                filename=dialog.full_filename,
                selected_regions_only=dialog.selected_regions_only
            )
