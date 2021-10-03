from dataclasses import dataclass, field, fields, Field

from PyQt5.QtWidgets import QMainWindow

from regexport.actions.download_biop_extensions import SaveBiopExtensionsAction, SaveBiopExtensionsActionModel
from regexport.actions.load_atlas import LoadAtlasActionModel, LoadAtlasAction
from regexport.actions.load_cells import LoadCellsActionModel, LoadCellsAction
from regexport.actions.save_cells import SaveCellsActionModel, SaveCellsAction
from regexport.actions.save_script import SaveGroovyScriptActionModel, SaveGroovyScriptAction
from regexport.model import AppState
from regexport.views.histogram import HistogramModel, HistogramView
from regexport.views.main_window import MainWindow
from regexport.views.plot_3d import PlotterModel, PlotterView
from regexport.views.region_tree import BrainRegionTreeViewModel, BrainRegionTree
from regexport.views.sidebar import Sidebar
from regexport.views.text_selector import TextSelectorModel, DropdownTextSelectorView


class App:
    def __init__(self):
        self.model = AppState()

        self.plot_window = PlotterModel()
        self.plot_window.register(model=self.model)

        self.brain_region_tree_model = BrainRegionTreeViewModel()
        self.brain_region_tree_model.register(model=self.model)

        self.load_atlas_button = LoadAtlasActionModel()
        self.load_atlas_button.register(model=self.model)

        self.load_cells_button = LoadCellsActionModel()
        self.load_cells_button.register(model=self.model)

        self.export_data_button = SaveCellsActionModel()
        self.export_data_button.register(model=self.model)

        self.colormap_selector_model = TextSelectorModel()
        self.colormap_selector_model.register(model=self.model, options_attr='colormap_options',
                                              selected_attr='selected_colormap')

        self.colordata_selector_model = TextSelectorModel()
        self.colordata_selector_model.register(model=self.model, options_attr='column_to_plot_options',
                                               selected_attr='column_to_plot')

        self.histogram_model = HistogramModel()
        self.histogram_model.register(model=self.model)

        self.save_biop_extensions_button = SaveBiopExtensionsActionModel()
        self.save_groovy_script_button = SaveGroovyScriptActionModel()

    def create_gui(self) -> QMainWindow:
        return MainWindow(
            main_widgets=[
                BrainRegionTree(model=self.brain_region_tree_model),
                PlotterView(model=self.plot_window),
                Sidebar(
                    widgets=[
                        DropdownTextSelectorView(model=self.colordata_selector_model),
                        DropdownTextSelectorView(model=self.colormap_selector_model),
                        HistogramView(model=self.histogram_model),
                    ]
                ),
            ],
            menu_actions=[
                SaveBiopExtensionsAction(model=self.save_biop_extensions_button),
                SaveGroovyScriptAction(model=self.save_groovy_script_button),
                LoadAtlasAction(model=self.load_atlas_button),
                LoadCellsAction(model=self.load_cells_button),
                SaveCellsAction(model=self.export_data_button),
            ]
        )

