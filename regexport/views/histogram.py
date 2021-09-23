import numpy as np
from traitlets import HasTraits, Instance
from vedo import Plotter
from vedo.pyplot import histogram
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from regexport.model import AppState
from regexport.views.utils import HasWidget


class HistogramModel(HasTraits):
    x_data = Instance(np.ndarray, default_value=np.zeros(0))
    y_data = Instance(np.ndarray, default_value=np.zeros(0))
    z_data = Instance(np.ndarray, default_value=np.zeros(0))
    x_hist_title = "X"


    def register(self, model: AppState):
        self.model = model
        model.observe(self.update, ['cells'])

    def update(self, change):
        if (cells := self.model.cells) is None:
            self.x_data = np.zeros(0)
            self.y_data = np.zeros(0)
            self.z_data = np.zeros(0)
        else:
            self.x_data = cells.X.values
            self.y_data = cells.Y.values
            self.z_data = cells.Z.values


class HistogramView(HasWidget):

    def __init__(self, model: HistogramModel):

        widget = QVTKRenderWindowInteractor()
        HasWidget.__init__(self, widget=widget)
        self.plotter = Plotter(qtWidget=widget)

        self.model = model
        self.model.observe(self.render)

    def render(self, change):
        hist = histogram(self.model.y_data, bins=20, title=self.model.x_hist_title)
        self.plotter.show(hist, mode=12)
