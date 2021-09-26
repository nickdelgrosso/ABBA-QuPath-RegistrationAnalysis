from typing import Tuple

from bg_atlasapi import BrainGlobeAtlas
from pandas import Series


def is_parent(id: Series, selected_ids: Tuple[int, ...], atlas: BrainGlobeAtlas) -> bool:
    assert len(id.unique()) == 1
    id = int(id.values[0])
    if id != 0:
        if id in selected_ids:
            return True
        else:
            is_ancestor = atlas.hierarchy.is_ancestor
            return any(is_ancestor(selected_id, id) for selected_id in selected_ids)
    else:
        return False
