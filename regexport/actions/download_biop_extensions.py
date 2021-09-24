from pathlib import Path
from zipfile import ZipFile

from PyQt5.QtCore import QThreadPool
from PyQt5.QtWidgets import QAction, QFileDialog

from regexport.utils.parallel import Task


class SaveBiopExtensionsActionModel:
    text = "-1. Download BIOP Extensions"

    def download_extensions(self, directory: Path):
        import requests
        if not directory.exists():
            raise FileNotFoundError(f"directory {directory} does not exist.")

        urls = [
            ('extensions', "https://github.com/BIOP/qupath-biop-extensions/releases/download/v2.0.8/biop-tools-2.0.8.jar"),
            ('extensions', "https://github.com/BIOP/qupath-biop-extensions/releases/download/v2.0.8/WSI-Dependencies.zip"),
            ('.', "https://github.com/SuperElastix/elastix/releases/download/5.0.1/elastix-5.0.1-win64.zip"),
            ('.', "https://gist.githubusercontent.com/NicoKiaru/b91f9f3f0069b765a49b5d4629a8b1c7/raw/571954a443d1e1f0597022f6c19f042aefbc0f5a/TestRegister.groovy"),
        ]
        for subdir, url in urls:
            response = requests.get(url, allow_redirects=True)

            fname = directory / subdir / Path(url).name
            fname.parent.mkdir(parents=True, exist_ok=True)
            with open(fname, 'wb') as f:
                f.write(response.content)

            if fname.suffix == '.zip':
                with ZipFile(fname, 'r') as zip_ref:
                    zip_ref.extractall(fname.parent)
                fname.unlink(missing_ok=True)


class SaveBiopExtensionsAction(QAction):

    def __init__(self, model: SaveBiopExtensionsActionModel, *args, **kwargs):
        self.model = model
        super().__init__(*args, **kwargs)
        self.setText(model.text)
        self.triggered.connect(self.click)

    def click(self):
        directory = QFileDialog.getExistingDirectory(
            caption="Make a QuPath Common Files folder for your BIOP Extensions",
        )
        if not directory:
            return

        worker = Task(self.model.download_extensions, Path(directory))
        pool = QThreadPool.globalInstance()
        pool.start(worker)
