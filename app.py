import sys

from PyQt5.QtWidgets import QApplication

from actions import LoadCellsAction
from main_window import MainWindow
from model import model
from plot_3d import PlotterWindow
from region_tree import BrainRegionTree
from sidebar import Sidebar

if __name__ == '__main__':
    app = QApplication(sys.argv)

    load_cells = LoadCellsAction(model=model)
    win = MainWindow(
        main_widgets=[
            BrainRegionTree(model=model),
            PlotterWindow(model=model),
            Sidebar(model=model),
        ],
        menu_actions=[
            load_cells,
        ]
    )
    win.show()
    sys.exit(app.exec_())
