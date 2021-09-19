import sys

from PyQt5.QtWidgets import QApplication

from actions.load_cells import LoadCellsAction, LoadCellsModel
from actions.load_atlas import LoadAtlasActionModel, LoadAtlasAction
from views.analysis_selector import AnalysisSelectorModel, AnalysisSelectorView
from views.main_window import MainWindow
from model import AppState
from views.plot_3d import PlotterModel
from views.plot_3d.view import PlotterView
from views.region_tree import BrainRegionTree, BrainRegionTreeViewModel
from views.sidebar import Sidebar, SidebarModel
from views.text_selector import TextSelectorModel, DropdownTextSelectorView

if __name__ == '__main__':

    model = AppState()

    app = QApplication(sys.argv)

    plotter_model = PlotterModel()
    plotter_model.register(model=model)

    brain_region_tree_model = BrainRegionTreeViewModel()
    brain_region_tree_model.register(model=model)

    load_atlas_action_model = LoadAtlasActionModel()
    load_atlas_action_model.register(model=model)

    load_cells_action_model = LoadCellsModel()
    load_cells_action_model.register(model=model)

    colormap_selector_model = TextSelectorModel()
    colormap_selector_model.register(
        model=model,
        options_attr='colormap_options',
        selected_attr='selected_colormap',
    )

    analysis_selector_model = AnalysisSelectorModel()
    analysis_selector_model.register(model=model)

    sidebar_model = SidebarModel()

    win = MainWindow(
        main_widgets=[
            BrainRegionTree(model=brain_region_tree_model),
            PlotterView(model=plotter_model),
            Sidebar(
                model=sidebar_model,
                widgets=[
                    AnalysisSelectorView(model=analysis_selector_model),
                    DropdownTextSelectorView(model=colormap_selector_model),
                ]
            ),
        ],
        menu_actions=[
            LoadCellsAction(model=load_cells_action_model),
            LoadAtlasAction(model=load_atlas_action_model),
        ]
    )
    win.show()
    sys.exit(app.exec_())
