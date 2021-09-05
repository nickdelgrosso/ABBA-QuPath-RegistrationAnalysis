from PyQt5.QtWidgets import QTreeWidget, QAbstractItemView, QTreeWidgetItem
from treelib import Tree

from model import AppState
from utils import HasWidget


class BrainRegionTree(HasWidget):

    def __init__(self, model: AppState):
        self._model = model

        treeview = QTreeWidget()
        treeview.setHeaderHidden(True)
        treeview.setWordWrap(False)
        treeview.setSelectionMode(QAbstractItemView.ExtendedSelection)
        treeview.setSelectionBehavior(QAbstractItemView.SelectRows)
        treeview.itemSelectionChanged.connect(self.onSelectionChanged)
        HasWidget.__init__(self, widget=treeview)

        self.treeview = treeview

        self._model.observe(self.on_change_mesh, names=['atlas'])

    def on_change_mesh(self, change):
        if (atlas := change['new']) is not None:
            # Add element's hierarchy
            tree = Tree((t := atlas.hierarchy).subtree(t.root), deep=True)
            for id in tree.expand_tree(mode=Tree.DEPTH):
                node = tree.get_node(id)

                node.item = QTreeWidgetItem()
                node.item.setText(0, atlas._get_from_structure(node.identifier, "name"))
                node.item.setText(1, str(node.identifier))

                if not node.is_root():
                    if (parent := tree.parent(node.identifier)).is_root():
                        self.treeview.addTopLevelItem(node.item)
                    else:
                        parent.item.addChild(node.item)

            # Finish up
            self.treeview.expandToDepth(2)

    def onSelectionChanged(self):
        self._model.selected_region_ids = tuple(int(item.text(1)) for item in self.treeview.selectedItems())

