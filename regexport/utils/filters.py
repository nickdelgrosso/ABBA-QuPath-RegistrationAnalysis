from typing import Tuple

from pandas import Series
from treelib import Tree


def is_parent(id: Series, selected_ids: Tuple[int, ...], tree: Tree) -> bool:
    assert len(id.unique()) == 1
    id = int(id.values[0])
    if id != 0:
        if id in selected_ids:
            return True
        else:
            return any(tree.is_ancestor(selected_id, id) for selected_id in selected_ids)
    else:
        return False
