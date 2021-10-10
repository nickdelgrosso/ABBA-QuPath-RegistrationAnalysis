from pathlib import Path

import pytest
from treelib import Tree

from regexport.app import App
from regexport.views.channel_filter import ChannelFilterView, ChannelFilterModel
from regexport.views.histogram import HistogramView, HistogramModel
from regexport.views.labelled_slider import LabelledSliderView, LabelledSliderModel
from regexport.views.main_window import MainWindow
from regexport.views.plot_3d import PlotterModel, PlotterView
from regexport.views.region_tree import BrainRegionTree, BrainRegionTreeModel
from regexport.views.sidebar import Sidebar
from regexport.views.text_selector import DropdownTextSelectorView, TextSelectorModel


def test_histogram_renders_without_problems(qtbot):
    histogram_view = HistogramView(model=HistogramModel())
    qtbot.add_widget(histogram_view.widget)
    histogram_view.render()


def test_plotter_renders_without_problems(qtbot):
    plotter_view = PlotterView(model=PlotterModel())
    qtbot.add_widget(plotter_view.widget)
    plotter_view.render()


def test_region_tree_renders_without_problems(qtbot):
    tree = Tree()
    tree.create_node(identifier=0, data='all regions')
    tree.create_node(identifier=20, data='Cerebrum', parent=0)
    tree.create_node(identifier=30, data='Cerebellum', parent=0)
    tree.create_node(identifier=40, data='V1', parent=20)

    tree_view = BrainRegionTree(model=BrainRegionTreeModel(tree=tree))
    qtbot.add_widget(tree_view.widget)
    tree_view.render()


def test_sidebar_renders_without_problems(qtbot):
    sidebar = Sidebar()
    qtbot.add_widget(sidebar.widget)


def test_dropdown_box_renders_without_problems(qtbot):
    dropdown = DropdownTextSelectorView(model=TextSelectorModel())
    qtbot.add_widget(dropdown.widget)
    dropdown.render()


def test_labelled_slider_view_renders_without_problems(qtbot):
    slider = LabelledSliderView(model=LabelledSliderModel())
    qtbot.add_widget(slider.widget)
    slider.render()


def test_channel_filter_view_renders_without_problems(qtbot):
    view = ChannelFilterView(model=ChannelFilterModel(
        sliders=[
            LabelledSliderModel(label='a'),
            LabelledSliderModel(label='b'),
        ]
    ))
    qtbot.add_widget(view.widget)
    view.render()

def test_main_window_renders_without_problems(qtbot):
    main_window = MainWindow()
    qtbot.add_widget(main_window)


@pytest.mark.buggyci
def test_full_app_gui_launches_without_problems(qtbot):
    app = App()
    win = app.create_gui()
    qtbot.add_widget(win)


@pytest.mark.buggyci
def test_app_does_main_actions_without_crashing(qtbot):
    app = App()
    win = app.create_gui()
    qtbot.add_widget(win)
    app.load_atlas_button.click()
    app.load_cells_button.submit([
        Path("example_data/tsvs_exported_from_qupath/section1.tsv"),
    ])
    app.colordata_selector_dropdown.select('Esr1 (Opal 480): Num Spots')
