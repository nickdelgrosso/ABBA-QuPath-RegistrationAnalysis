from enum import Enum, auto

import numpy as np
import pandas as pd
from bg_atlasapi import BrainGlobeAtlas
from matplotlib import pyplot as plt
from traitlets import HasTraits, Instance, observe, Tuple, List, Unicode, Dict, Int

from regexport.utils.filters import is_parent


class AnalysisType(Enum):
    RegionLabel = auto()
    SubCellCount = auto()


class AppState(HasTraits):
    atlas = Instance(BrainGlobeAtlas, allow_none=True)
    cells = Instance(pd.DataFrame, allow_none=True)
    selected_region_ids = Tuple(default_value=())  # should be tuple of ints
    selected_cell_ids = Instance(np.ndarray, default_value=np.array([], dtype=int))  # array of ints
    column_to_plot_options = List(Unicode(), default_value=["BrainRegion"])
    column_to_plot = Unicode(default_value="BrainRegion")
    colormap_options = List(Unicode(), default_value=[cmap for cmap in plt.colormaps() if not cmap.endswith('_r')])#['tab20c', 'viridis'])
    selected_colormap = Unicode(default_value='tab20c')
    selected_cells = Instance(pd.DataFrame, allow_none=True)
    max_numspots_filters = Dict(key_trait=Unicode(), value_trait=Int(), default_value={})

    @observe('cells')
    def _update_max_numspots_filter_to_max_of_each_numspots_column(self, change):
        if self.cells is None:
            self.max_numspots_filters = {}
        else:
            self.max_numspots_filters = {col: int(self.cells[col].max()) for col in self.cells.columns if 'Num Spots' in col}

    @observe('cells')
    def _update_column_to_plot_options(self, change):
        if self.cells is None:
            return
        self.cells: pd.DataFrame
        columns = [name for name in self.cells.columns if 'Num Spots' in name]
        self.column_to_plot = "BrainRegion"
        self.column_to_plot_options = ["BrainRegion"] + columns

    @observe('column_to_plot')
    def _validate_column_to_plot(self, change):
        assert self.column_to_plot in self.column_to_plot_options

    @observe('selected_region_ids', 'cells')
    def _update_selected_cell_ids(self, change):
        if self.cells is None:
            return
        elif len(self.selected_region_ids) == 0:
            self.selected_cell_ids = self.cells.index.values
            self.selected_cells = self.cells
        else:
            is_parented = self.cells.groupby('BGIdx', as_index=False).BGIdx.transform(
                lambda ids: is_parent(ids.values[0], selected_ids=self.selected_region_ids, tree=self.atlas.hierarchy) if ids.values[0] != 0 else False
            )
            only_parented = is_parented[is_parented.BGIdx].index.values
            self.selected_cell_ids = only_parented
            self.selected_cells = self.cells.iloc[only_parented]
