from bg_atlasapi import BrainGlobeAtlas
from traitlets import HasTraits, Instance, observe, Tuple, Int


class AppState(HasTraits):
    atlas = Instance(BrainGlobeAtlas)
    selected_region_ids = Tuple(default_value=())  # should be tuple of ints

    @observe('selected_region_ids')
    def _on_change_selected_region_ids(self, change):
        print(f"Selected: {change['new']}")


model = AppState(
    atlas=BrainGlobeAtlas("allen_mouse_25um")
)
