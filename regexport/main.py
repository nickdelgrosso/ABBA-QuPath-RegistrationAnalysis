import sys

from PyQt5.QtWidgets import QApplication

from regexport.actions.download_biop_extensions import SaveBiopExtensionsAction, SaveBiopExtensionsActionModel
from regexport.actions.load_cells import LoadCellsAction, LoadCellsActionModel
from regexport.actions.load_atlas import LoadAtlasActionModel, LoadAtlasAction
from regexport.actions.save_cells import SaveCellsAction, SaveCellsActionModel
from regexport.actions.save_script import SaveGroovyScriptAction, SaveGroovyScriptActionModel
from regexport.views.histogram import HistogramView, HistogramModel
from regexport.views.main_window import MainWindow
from regexport.model import AppState
from regexport.views.plot_3d import PlotterModel, PlotterView
from regexport.views.region_tree import BrainRegionTree, BrainRegionTreeViewModel
from regexport.views.sidebar import Sidebar, SidebarModel
from regexport.views.text_selector import TextSelectorModel, DropdownTextSelectorView


def main():
    global model
    model = AppState()
    app = QApplication(sys.argv)
    plotter_model = PlotterModel()
    plotter_model.register(model=model)
    brain_region_tree_model = BrainRegionTreeViewModel()
    brain_region_tree_model.register(model=model)
    load_atlas_action_model = LoadAtlasActionModel()
    load_atlas_action_model.register(model=model)
    load_cells_action_model = LoadCellsActionModel()
    load_cells_action_model.register(model=model)
    save_cells_action_model = SaveCellsActionModel()
    save_cells_action_model.register(model=model)
    colormap_selector_model = TextSelectorModel()
    colormap_selector_model.register(model=model, options_attr='colormap_options', selected_attr='selected_colormap')
    colordata_selector_model = TextSelectorModel()
    colordata_selector_model.register(model=model, options_attr='column_to_plot_options', selected_attr='column_to_plot')

    sidebar_model = SidebarModel()
    histogram_model = HistogramModel()
    histogram_model.register(model=model)
    win = MainWindow(
        main_widgets=[
            BrainRegionTree(model=brain_region_tree_model),
            PlotterView(model=plotter_model),
            Sidebar(
                model=sidebar_model,
                widgets=[
                    DropdownTextSelectorView(model=colordata_selector_model),
                    DropdownTextSelectorView(model=colormap_selector_model),
                    HistogramView(model=histogram_model),
                ]
            ),
        ],
        menu_actions=[
            SaveBiopExtensionsAction(model=SaveBiopExtensionsActionModel()),
            SaveGroovyScriptAction(model=SaveGroovyScriptActionModel()),
            LoadAtlasAction(model=load_atlas_action_model),
            LoadCellsAction(model=load_cells_action_model),
            SaveCellsAction(model=save_cells_action_model),
        ]
    )
    win.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
