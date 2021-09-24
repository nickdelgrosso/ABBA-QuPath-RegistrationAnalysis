from importlib.resources import read_text
from pathlib import Path

from PyQt5.QtWidgets import QAction, QFileDialog

from regexport import qupath_scripts


class SaveGroovyScriptActionModel:
    text = "0. Get QuPath Exporter"

    def savedata(self, filename):
        groovy_script = read_text(qupath_scripts, 'export_registered_cells_to_tsv.groovy')
        with open(filename, 'w') as f:
            f.write(groovy_script)


class SaveGroovyScriptAction(QAction):

    def __init__(self, model: SaveGroovyScriptActionModel, *args, **kwargs):
        self.model = model
        super().__init__(*args, **kwargs)
        self.setText(model.text)
        self.triggered.connect(self.click)

    def click(self):
        filename, filetype_filter = QFileDialog.getSaveFileName(
            caption="Save QuPath Script",
            directory='export_registered_cells_to_tsv.groovy',
            filter="Groovy script (*.groovy)"
        )

        if not filename:
            return

        self.model.savedata(Path(filename))
