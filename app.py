import sys

from PyQt5.QtWidgets import QApplication

from actions import LoadCellsAction, LoadAtlasAction
from main_window import MainWindow
from model import AppState
from plot_3d import PlotterWindow, PlotterModel
from region_tree import BrainRegionTree
from sidebar import Sidebar

if __name__ == '__main__':

    model = AppState()

    app = QApplication(sys.argv)

    plotter_model = PlotterModel()
    plotter_model.observe_model(model=model)

    win = MainWindow(
        main_widgets=[
            BrainRegionTree(model=model),
            PlotterWindow(model=model, vmodel=plotter_model),
            Sidebar(model=model),
        ],
        menu_actions=[
            LoadCellsAction(model=model),
            LoadAtlasAction(model=model),
        ]
    )
    win.show()
    sys.exit(app.exec_())
