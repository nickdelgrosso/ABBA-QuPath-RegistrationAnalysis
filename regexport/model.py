from enum import Enum, auto

import pandas as pd
from bg_atlasapi import BrainGlobeAtlas
from matplotlib import pyplot as plt
from traitlets import HasTraits, Instance, observe, Tuple, List, UseEnum, Unicode


class AnalysisType(Enum):
    RegionLabel = auto()
    SubCellCount = auto()


class AppState(HasTraits):
    atlas = Instance(BrainGlobeAtlas, allow_none=True)
    cells = Instance(pd.DataFrame, allow_none=True)
    selected_region_ids = Tuple(default_value=())  # should be tuple of ints
    colormap_options = List(Unicode(), default_value=[cmap for cmap in plt.colormaps() if not cmap.endswith('_r')])#['tab20c', 'viridis'])
    selected_colormap = Unicode(default_value='tab20c')
    analysis_type = UseEnum(AnalysisType, default_value=AnalysisType.RegionLabel)

    @observe('selected_region_ids')
    def _on_change_selected_region_ids(self, change):
        print(f"Selected: {change['new']}")

    @observe('selected_colormap')
    def _on_colormap_change(self, change):
        print('changed colormap to', self.selected_colormap)