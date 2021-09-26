from enum import Enum, auto
from functools import cached_property, lru_cache

import numpy as np
import pandas as pd
from bg_atlasapi import BrainGlobeAtlas
from matplotlib import pyplot as plt
from traitlets import HasTraits, Instance, observe, Tuple, List, UseEnum, Unicode

from regexport.data.filters import is_parent


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
    selected_cell_ids = Instance(np.ndarray, default_value=np.array([], dtype=int))  # array of ints

    @observe('selected_region_ids')
    def _on_change_selected_region_ids(self, change):
        print(f"Selected: {change['new']}")

    @observe('selected_colormap')
    def _on_colormap_change(self, change):
        print('changed colormap to', self.selected_colormap)

    @observe('selected_region_ids', 'cells')
    def _update_selected_cell_ids(self, change):
        if self.cells is None:
            return
        elif len(self.selected_region_ids) == 0:
            self.selected_cell_ids = self.cells.index.values
        else:
            is_parented = self.cells.groupby('BGIdx', as_index=False).BGIdx.transform(is_parent, selected_ids=self.selected_region_ids, atlas=self.atlas)
            only_parented = is_parented[is_parented.BGIdx == True].index.values
            self.selected_cell_ids = only_parented



