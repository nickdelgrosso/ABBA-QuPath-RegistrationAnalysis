from regexport.views.histogram import HistogramView, HistogramModel
from regexport.views.main_window import MainWindow
from regexport.views.plot_3d import PlotterModel, PlotterView
from regexport.views.region_tree import BrainRegionTree, BrainRegionTreeModel
from regexport.views.sidebar import Sidebar
from regexport.views.text_selector import DropdownTextSelectorView, TextSelectorModel


def test_histogram_renders_without_problems(qtbot):
    histogram_view = HistogramView(model=HistogramModel())
    histogram_view.render()


def test_plotter_renders_without_problems(qtbot):
    plotter_view = PlotterView(model=PlotterModel())
    plotter_view.render()


def test_region_tree_renders_without_problems(qtbot):
    tree_view = BrainRegionTree(model=BrainRegionTreeModel())
    tree_view.render()


def test_sidebar_renders_without_problems(qtbot):
    Sidebar()


def test_dropdown_box_renders_without_problems(qtbot):
    dropdown = DropdownTextSelectorView(model=TextSelectorModel())
    dropdown.render()


def test_main_window_renders_without_problems(qtbot):
    MainWindow()

