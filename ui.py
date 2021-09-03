import sys
from abc import ABC
from typing import List, Union

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from PyQt5.QtCore import QItemSelectionModel
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem, QAbstractItemView
from qtpy.QtCore import Qt
from qtpy.QtWidgets import QMainWindow, QWidget, QSplitter, QApplication, QTreeView
from qtpy.QtGui import QStandardItemModel, QStandardItem
from qtpy import QtGui
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vedo import Points, Mesh, Plotter
from bg_atlasapi import BrainGlobeAtlas
from treelib import Node, Tree


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

    def __init__(self, atlas: BrainGlobeAtlas):
        treeview = QTreeWidget()
        treeview.setHeaderHidden(True)
        treeview.setWordWrap(False)
        treeview.setSelectionMode(QAbstractItemView.ExtendedSelection)
        treeview.setSelectionBehavior(QAbstractItemView.SelectRows)
        HasWidget.__init__(self, widget=treeview)

        # Add element's hierarchy
        tree = Tree((t := atlas.hierarchy).subtree(t.root), deep=True)
        for id in tree.expand_tree(mode=Tree.DEPTH):
            node = tree.get_node(id)

            node.item = QTreeWidgetItem()
            node.item.setText(0, atlas._get_from_structure(node.identifier, "name"))

            if not node.is_root():
                if (parent := tree.parent(node.identifier)).is_root():
                    treeview.addTopLevelItem(node.item)
                else:
                    parent.item.addChild(node.item)

        # Finish up
        treeview.expandToDepth(2)
