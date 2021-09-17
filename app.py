import sys

from PyQt5.QtWidgets import QApplication

from actions.load_cells import LoadCellsAction, LoadCellsModel
from actions.load_atlas import LoadAtlasActionModel, LoadAtlasAction
from views.main_window import MainWindow
from model import AppState
from views.plot_3d import PlotterView, PlotterModel
from views.region_tree import BrainRegionTree
from views.sidebar import Sidebar

if __name__ == '__main__':

    model = AppState()

    app = QApplication(sys.argv)

    plotter_model = PlotterModel()
    plotter_model.register(model=model)

    load_atlas_action_model = LoadAtlasActionModel()
    load_atlas_action_model.register(model=model)

    load_cells_action_model = LoadCellsModel()
    load_cells_action_model.register(model=model)


    win = MainWindow(
        main_widgets=[
            BrainRegionTree(model=model),
            PlotterView(model=plotter_model),
            Sidebar(model=model),
        ],
        menu_actions=[
            LoadCellsAction(model=load_cells_action_model),
            LoadAtlasAction(model=load_atlas_action_model),
        ]
    )
    win.show()
    sys.exit(app.exec_())
