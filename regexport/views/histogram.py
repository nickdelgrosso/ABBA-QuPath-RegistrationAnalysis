from dataclasses import dataclass
from typing import List, Optional

import numpy as np
import vedo
from traitlets import HasTraits, Instance, Bool
from vedo import Plotter, pyplot
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from regexport.model import AppState
from regexport.views.utils import HasWidget


@dataclass
class HistogramData:
    zero_count: int
    bin_edges: np.ndarray
    bar_heights: np.ndarray
    x_labels: List[str]
    title: str = ""
    zero_color: str = 'red'
    bar_color: str = 'olivedrab'

    def __post_init__(self):
        assert self.bar_heights.ndim == 1
        assert len(self.bar_heights) == len(self.bin_edges) - 1
        assert len(self.bar_heights) == len(self.x_labels)


class HistogramModel(HasTraits):
    histogram = Instance(HistogramData, allow_none=True)
    cumulative = Bool(default_value=False)

    def register(self, model: AppState):
        self.model = model
        model.observe(self.update, ['selected_cells', 'column_to_plot'])

    def update(self, change):
        model = self.model
        if model.selected_cells is None:
            self.histogram = None
            return
        
        data_column = model.selected_cells[model.column_to_plot]
        if data_column.dtype.name == 'category':
            self.histogram = None
        else:
            data = data_column.values
            zero_count = int(np.sum(data == 0))

            heights, bin_edges = np.histogram(data[data > 0], bins='auto', density=False)
            if self.cumulative:
                zero_count /= heights.sum() + zero_count
                bar_heights = heights.cumsum() / heights.sum() + zero_count
            else:
                bar_heights = heights
            self.histogram = HistogramData(
                zero_count=zero_count,
                bin_edges=bin_edges,
                bar_heights=bar_heights,
                x_labels=bin_edges[:-1].astype(int).astype(str).tolist(),
            )


class HistogramView(HasWidget):

    def __init__(self, model: HistogramModel):
        widget = QVTKRenderWindowInteractor()
        HasWidget.__init__(self, widget=widget)
        self.plotter = Plotter(qtWidget=widget)
        self.model = model
        self.model.observe(self.render)

    @staticmethod
    def render_histogram_data(data: HistogramData) -> vedo.pyplot.Plot:
        return vedo.pyplot.plot(
            [
                np.concatenate([[data.zero_count], data.bar_heights]),
                np.concatenate([['0'], data.x_labels]),
                [data.zero_color] + [data.bar_color] * len(data.bar_heights),
                np.concatenate([[0], data.bin_edges]),
            ],
            mode='bars'
        )

    def render(self, change=None):
        self.plotter.clear()
        hist: Optional[HistogramData] = self.model.histogram
        if hist is not None:
            hist_actor = self.render_histogram_data(data=hist)
            self.plotter.show(hist_actor, mode=12)
