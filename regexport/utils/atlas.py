from typing import Optional

from bg_atlasapi import BrainGlobeAtlas
from treelib import Tree, Node


def create_brain_region_tree(atlas: Optional[BrainGlobeAtlas]) -> Tree:
    if atlas is None:
        return Tree()

    new_tree = Tree()
    for id in (tree := atlas.hierarchy).expand_tree(mode=Tree.DEPTH):
        region_name = atlas._get_from_structure(id, "name")
        node = Node(identifier=id, data=region_name)
        new_tree.add_node(node, parent=tree.parent(id))
    return new_tree