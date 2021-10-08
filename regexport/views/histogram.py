from functools import partial

import numpy as np
from PyQt5.QtCore import QThreadPool
from traitlets import HasTraits, Instance, Unicode
from vedo import Plotter
from vedo.pyplot import histogram
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from regexport.model import AppState
from regexport.utils.parallel import Task
from regexport.views.utils import HasWidget


class HistogramModel(HasTraits):
    data = Instance(np.ndarray, default_value=np.zeros(0))
    title = Unicode(default_value="")

    def register(self, model: AppState):
        self.model = model
        model.observe(self.update, ['selected_cells', 'column_to_plot'])

    def update(self, change):
        model = self.model
        if model.selected_cells is None:
            self.data = np.zeros(0)
        elif (data_column := model.selected_cells[model.column_to_plot]).dtype.name == 'category':
            self.data = np.zeros(0)
        else:
            print(f'updating selected cell data ({len(data_column)} rows)')
            self.data = data_column.values

class HistogramView(HasWidget):

    def __init__(self, model: HistogramModel):

        widget = QVTKRenderWindowInteractor()
        HasWidget.__init__(self, widget=widget)
        self.plotter = Plotter(qtWidget=widget)

        self.model = model
        self.model.observe(self.render)

    @staticmethod
    def make_histogram(data: np.ndarray):
        bin_edges = np.histogram_bin_edges(data, bins='scott')
        hist = histogram(data, bins=len(bin_edges), gap=0.)
        return hist

    @staticmethod
    def send_hist_to_plotter(plotter, hist):
        plotter.clear()
        plotter.show(hist, mode=12)


    def render(self, change=None):
        data = self.model.data
        if len(data) == 0:
            self.plotter.clear()
            return
        task = Task(self.make_histogram, data=data)
        task.signals.finished.connect(partial(self.send_hist_to_plotter, self.plotter))
        pool = QThreadPool.globalInstance()
        pool.start(task)
