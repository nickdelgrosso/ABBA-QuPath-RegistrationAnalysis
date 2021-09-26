import numpy as np
from traitlets import HasTraits, Instance, Unicode
from vedo import Plotter
from vedo.pyplot import histogram
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from regexport.model import AppState
from regexport.views.utils import HasWidget


class HistogramModel(HasTraits):
    data = Instance(np.ndarray, default_value=np.zeros(0))
    title = Unicode(default_value="")

    def register(self, model: AppState):
        self.model = model
        model.observe(self.update, ['cells', 'column_to_plot'])

    def update(self, change):
        model = self.model
        if model.cells is None:
            self.data = np.zeros(0)
        elif (data_column := model.cells[model.column_to_plot]).dtype.name == 'category':
            self.data = np.zeros(0)
        else:
            self.data = data_column.values

class HistogramView(HasWidget):

    def __init__(self, model: HistogramModel):

        widget = QVTKRenderWindowInteractor()
        HasWidget.__init__(self, widget=widget)
        self.plotter = Plotter(qtWidget=widget)

        self.model = model
        self.model.observe(self.render)

    def render(self, change):
        bin_edges = np.histogram_bin_edges(self.model.data, bins='fd')
        print('bin edges:', bin_edges)
        hist = histogram(self.model.data, bins=len(bin_edges), gap=0., title=self.model.title, )
        self.plotter.clear()
        self.plotter.show(hist, mode=12)
