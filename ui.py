import sys
from abc import ABC
from typing import List, Union

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from qtpy.QtCore import Qt
from qtpy.QtWidgets import QMainWindow, QWidget, QSplitter, QApplication, QTreeView
from qtpy.QtGui import QStandardItemModel, QStandardItem
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vedo import Points, Mesh, Plotter
from bg_atlasapi import BrainGlobeAtlas



class HasWidget(ABC):

    def __init__(self, widget: QWidget):
        self.__widget = widget

    @property
    def widget(self) -> QWidget:
        return self.__widget


class MainWindow(QMainWindow):

    def __init__(self, main_widgets: List[Union[QWidget, HasWidget]]):
        super().__init__()
        self._widgets = main_widgets  # keep reference to these widgets, so they aren't garbage collected.

        self._splitter = QSplitter(Qt.Horizontal)
        self.setCentralWidget(self._splitter)
        for widget in self._widgets:
            self._splitter.addWidget(widget.widget if hasattr(widget, 'widget') else widget)


class PlotterWindow(HasWidget):

    def __init__(self, cells: pd.DataFrame, atlas: BrainGlobeAtlas):
        widget = QVTKRenderWindowInteractor()
        HasWidget.__init__(self, widget=widget)
        Plotter(qtWidget=widget).show(
            Points(
                cells[['X', 'Y', 'Z']].values * 1000,
                r=3,
                c=plt.cm.tab20c((name_ids := cells.name.cat.codes) / np.max(name_ids))[:, :3]
            ),
            Mesh(
                str(atlas.structures[997]['mesh_filename']),
                alpha=0.1,
                computeNormals=True,
                c=(1., 1., 1.)
            ),
            at=0,
        )


class BrainRegionTree(HasWidget):

    def __init__(self):
        treeview = QTreeView()
        HasWidget.__init__(self, widget=treeview)
        treeview.setExpandsOnDoubleClick(False)
        treeview.setHeaderHidden(True)
        # treeView.setStyleSheet(update_css(tree_css, self.palette))
        treeview.setWordWrap(False)

        treeModel = QStandardItemModel()
        rootNode = treeModel.invisibleRootItem()
        item = QStandardItem()
        item.setText("Item")
        rootNode.appendRow(item)
