import sys

from PyQt5.QtWidgets import QApplication
from bg_atlasapi import BrainGlobeAtlas

from actions import LoadCellsAction
from main_window import MainWindow
from model import AppState
from plot_3d import PlotterWindow
from region_tree import BrainRegionTree
from sidebar import Sidebar

if __name__ == '__main__':

    model = AppState(
        atlas=BrainGlobeAtlas("allen_mouse_25um"),
    )

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
