from enum import Enum, auto

import pandas as pd
from bg_atlasapi import BrainGlobeAtlas
from traitlets import HasTraits, Instance, observe, Tuple, Int, List


def read_detection_file(filename: str, atlas: BrainGlobeAtlas) -> pd.DataFrame:
    return (
        pd.read_csv(filename, sep='\t')
        .rename(columns={'Allen CCFv3 X mm': 'X', 'Allen CCFv3 Y mm': 'Y', 'Allen CCFv3 Z mm': 'Z'})
        .astype({'X': float, 'Y': float, 'Z': float})
        .pipe(lambda df: df.assign(
            BGIdx=atlas.annotation[
                (df.X / (atlas.resolution[0] / 1000)).values.astype(int),
                (df.Y / (atlas.resolution[1] / 1000)).values.astype(int),
                (df.Z / (atlas.resolution[2] / 1000)).values.astype(int),
            ]
        ))
        .merge(atlas.lookup_df, right_on="id", left_on="BGIdx", how="left")
        .astype({'acronym': 'category', 'name': 'category'})
        .drop(columns=['id'])
    )#.sample(10000)


class Colormap(Enum):
    tab20c = auto()
    viridis = auto()


class AppState(HasTraits):
    atlas = Instance(BrainGlobeAtlas, allow_none=True)
    cells = Instance(pd.DataFrame, allow_none=True)
    selected_region_ids = Tuple(default_value=())  # should be tuple of ints
    colormap_options = List(Instance(Colormap), default_value=list(Colormap))
    selected_colormap = Instance(Colormap, default_value=Colormap.tab20c)


    @observe('selected_region_ids')
    def _on_change_selected_region_ids(self, change):
        print(f"Selected: {change['new']}")

    @observe('selected_colormap')
    def _on_colormap_change(self, change):
        print('changed colormap to', self.selected_colormap)