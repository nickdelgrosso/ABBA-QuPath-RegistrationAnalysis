from dataclasses import dataclass, field
from typing import Tuple

from bg_atlasapi import BrainGlobeAtlas


@dataclass
class AppState:
    atlas: BrainGlobeAtlas
    selected_region_ids: Tuple[int] = field(default_factory=list)


model = AppState(
    atlas=BrainGlobeAtlas("allen_mouse_25um")
)
