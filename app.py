import sys

from PyQt5.QtWidgets import QApplication

from bg_atlasapi import BrainGlobeAtlas

from model import model, read_detection_file
from plot_3d import PlotterWindow
from main_window import MainWindow
from region_tree import BrainRegionTree
from sidebar import Sidebar

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow(
        main_widgets=[
            BrainRegionTree(model=model),
            PlotterWindow(model=model),
            Sidebar(model=model),
        ]
    )
    win.show()
    sys.exit(app.exec_())
