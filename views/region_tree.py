from typing import Optional

from PyQt5.QtWidgets import QTreeWidget, QAbstractItemView, QTreeWidgetItem
from bg_atlasapi import BrainGlobeAtlas
from traitlets import HasTraits, Instance, Tuple, directional_link
from treelib import Tree, Node

from model import AppState
from .utils import HasWidget


class BrainRegionTreeViewModel(HasTraits):
    tree = Instance(Tree, allow_none=False, default_value=Tree())
    selected_region_ids = Tuple(default_value=())  # Tuple of ints

    def register(self, model: AppState):
        directional_link((self, 'selected_region_ids'), (model, 'selected_region_ids'))
        directional_link((model, 'atlas'), (self, 'tree'), self.update_tree)

    @staticmethod
    def update_tree(atlas: Optional[BrainGlobeAtlas]) -> Tree:
        if atlas is None:
            return Tree()

        new_tree = Tree()
        for id in (tree := atlas.hierarchy).expand_tree(mode=Tree.DEPTH):
            region_name = atlas._get_from_structure(id, "name")
            node = Node(identifier=id, data=region_name)
            new_tree.add_node(node, parent=tree.parent(id))
        return new_tree


class BrainRegionTree(HasWidget):

    def __init__(self, model: BrainRegionTreeViewModel):
        self.model = model

        treeview = QTreeWidget()
        treeview.setHeaderHidden(True)
        treeview.setWordWrap(False)
        treeview.setSelectionMode(QAbstractItemView.ExtendedSelection)
        treeview.setSelectionBehavior(QAbstractItemView.SelectRows)
        treeview.itemSelectionChanged.connect(self.onSelectionChanged)
        HasWidget.__init__(self, widget=treeview)

        self.treeview = treeview

        self.model.observe(self.on_change_tree, names=['tree'])

    def on_change_tree(self, change):

        if (tree := change['new']) is None:
            return
        ids = tree.expand_tree(mode=Tree.DEPTH)
        next(ids)  # skip displaying root

        for id in ids:
            node = tree.get_node(id)
            node.item = QTreeWidgetItem()
            node.item.setText(0, node.data)
            node.item.setText(1, str(node.identifier))

            if (parent := tree.parent(node.identifier)).is_root():
                self.treeview.addTopLevelItem(node.item)
            else:
                parent.item.addChild(node.item)

        # Finish up
        self.treeview.expandToDepth(2)

    def onSelectionChanged(self):
        self.model.selected_region_ids = tuple(int(item.text(1)) for item in self.treeview.selectedItems())

