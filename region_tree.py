from PyQt5.QtWidgets import QTreeWidget, QAbstractItemView, QTreeWidgetItem
from bg_atlasapi import BrainGlobeAtlas
from treelib import Tree

from utils import HasWidget


class BrainRegionTree(HasWidget):

    def __init__(self, atlas: BrainGlobeAtlas):
        treeview = QTreeWidget()
        treeview.setHeaderHidden(True)
        treeview.setWordWrap(False)
        treeview.setSelectionMode(QAbstractItemView.ExtendedSelection)
        treeview.setSelectionBehavior(QAbstractItemView.SelectRows)
        treeview.itemClicked.connect(self.onItemClicked)
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


    def onItemClicked(self, item: QTreeWidgetItem, column: int):
        if item.isSelected():
            print('selected')
        else:
            print('unselected')
