import sys

from PyQt5.QtWidgets import QApplication

from actions.load_cells import LoadCellsAction
from actions.load_atlas import LoadAtlasActionModel, LoadAtlasAction
from main_window import MainWindow
from model import AppState
from plot_3d import PlotterView, PlotterModel
from region_tree import BrainRegionTree
from sidebar import Sidebar

if __name__ == '__main__':

    model = AppState()

    app = QApplication(sys.argv)

    plotter_model = PlotterModel()
    plotter_model.observe_model(model=model)

    load_atlas_action_model = LoadAtlasActionModel()
    load_atlas_action_model.register_model(model=model)

    win = MainWindow(
        main_widgets=[
            BrainRegionTree(model=model),
            PlotterView(model=plotter_model),
            Sidebar(model=model),
        ],
        menu_actions=[
            LoadCellsAction(model=model),
            LoadAtlasAction(model=load_atlas_action_model),
        ]
    )
    win.show()
    sys.exit(app.exec_())
