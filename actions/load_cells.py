from pathlib import Path

from PyQt5.QtWidgets import QAction, QFileDialog

from model import AppState, read_detection_file


class LoadCellsAction(QAction):

    def __init__(self, model: AppState, *args, **kwargs):
        self.model = model
        super().__init__(*args, **kwargs)
        self.setText("&Load TSV Files")
        self.triggered.connect(self.run)

    def run(self):
        filenames, filetype = QFileDialog.getOpenFileNames(
            caption="Load Cell Points from File",
            filter="TSV Files (*.tsv)"
        )

        filenames = [Path(f) for f in filenames]
        if not filenames:
            return
        filename, *other_filenames = filenames
        if other_filenames:
            raise NotImplementedError("Multiple Filenames not yet implemented")

        df = read_detection_file(filename=filename, atlas=self.model.atlas)
        self.model.cells = df
