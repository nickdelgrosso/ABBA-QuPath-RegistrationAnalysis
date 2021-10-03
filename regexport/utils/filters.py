from typing import Tuple, Any

from treelib import Tree


def is_parent(id: Any, selected_ids: Tuple[Any, ...], tree: Tree) -> bool:
    if id in selected_ids:
        return True
    else:
        return any(tree.is_ancestor(selected_id, id) for selected_id in selected_ids)
