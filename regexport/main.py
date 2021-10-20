import sys
import os

from PySide2.QtWidgets import QApplication
#
from regexport.app import App
#

def main(debug=False):
    qapp = QApplication(sys.argv)
    app = App(debug=debug)
    win = app.create_gui()
    win.show()
    if debug:
        app.load_atlas_button.click()
        app.load_cells_button.submit([
            "example_data/tsvs_exported_from_qupath/section1.tsv",
            "example_data/tsvs_exported_from_qupath/section2.tsv",
        ])
    sys.exit(qapp.exec_())


if __name__ == '__main__':
    debug = bool(os.environ['ABBAVIZ_DEBUG'])
    main(debug=debug)
