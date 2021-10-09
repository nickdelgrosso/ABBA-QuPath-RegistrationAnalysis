from PySide2.QtWidgets import QTreeWidget, QAbstractItemView, QTreeWidgetItem
from traitlets import HasTraits, Instance, Tuple, directional_link
from treelib import Tree

from regexport.model import AppState
from regexport.utils.atlas import create_brain_region_tree
from .utils import HasWidget


class BrainRegionTreeModel(HasTraits):
    tree = Instance(Tree, allow_none=False, default_value=Tree())
    selected_region_ids = Tuple(default_value=())  # Tuple of ints

    def register(self, model: AppState):
        directional_link((self, 'selected_region_ids'), (model, 'selected_region_ids'))
        directional_link((model, 'atlas'), (self, 'tree'), create_brain_region_tree)

    def select(self, *brain_region_ids: int):
        print(brain_region_ids)
        self.selected_region_ids = brain_region_ids


class BrainRegionTree(HasWidget):

    def __init__(self, model: BrainRegionTreeModel):
        self.model = model

        treeview = QTreeWidget()
        treeview.setHeaderHidden(True)
        treeview.setWordWrap(False)
        treeview.setSelectionMode(QAbstractItemView.ExtendedSelection)
        treeview.setSelectionBehavior(QAbstractItemView.SelectRows)
        treeview.itemSelectionChanged.connect(self.onSelectionChanged)
        HasWidget.__init__(self, widget=treeview)

        self.treeview = treeview

        self.model.observe(self.render, names=['tree'])

    def render(self, change=None):
        tree = self.model.tree

        # no need to render empty tree
        if len(tree) == 0:
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
        self.treeview.expandToDepth(1)

    def onSelectionChanged(self):
        self.model.select(*[int(item.text(1)) for item in self.treeview.selectedItems()])

