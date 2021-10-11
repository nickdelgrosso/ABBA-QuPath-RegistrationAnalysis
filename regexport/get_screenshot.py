import sys
from pathlib import Path

from PySide2.QtWidgets import QApplication

from regexport.app import App
from regexport.utils.screenshots import save_screenshot


def main():
    print('starting app...')
    qapp = QApplication(sys.argv)
    app = App()
    win = app.create_gui()
    win.show()
    app.load_atlas_button.click()
    app.load_cells_button.submit([
        Path("example_data/tsvs_exported_from_qupath/section1.tsv"),
        Path("example_data/tsvs_exported_from_qupath/section2.tsv"),
    ])
    app.colordata_selector_dropdown.select("Esr1 (Opal 480): Num Spots")

    qapp.processEvents()
    save_screenshot(win, 'imgs/screenshot.jpg')

if __name__ == '__main__':
    main()
