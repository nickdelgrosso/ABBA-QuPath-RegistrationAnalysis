from functools import partial
from pathlib import Path
from typing import Optional

import numpy as np
from PyQt5.QtCore import QThreadPool
from vedo import Plotter, Points, Mesh
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from utils.parallel import Task
from utils.profiling import warn_if_slow
from views.plot_3d import PlotterModel
from views.utils import HasWidget


class PlotterView(HasWidget):

    def __init__(self, model: PlotterModel):
        self.model = model
        self.item_points = {}
        self._atlas_mesh = None

        widget = QVTKRenderWindowInteractor()
        HasWidget.__init__(self, widget=widget)
        self.plotter = Plotter(qtWidget=widget)

        self.model.observe(self.observe_atlas_mesh, ['atlas_mesh'])
        self.model.observe(self.render, ['points'])

    @property
    def atlas_mesh(self) -> Optional[Mesh]:
        return self._atlas_mesh

    @atlas_mesh.setter
    def atlas_mesh(self, value: Optional[Mesh]):
        self._atlas_mesh = value
        self.render(None)

    @staticmethod
    def load_mesh(filename: Path) -> Mesh:
        return Mesh(
            str(filename),
            alpha=0.1,
            computeNormals=True,
            c=(1., 1., 1.)
        )

    def observe_atlas_mesh(self, change):
        print('saw atlas change')
        if self.model.atlas_mesh is None:
            self._atlas_mesh = Mesh()
        else:
            print('loading')
            worker = Task(self.load_mesh, self.model.atlas_mesh)
            worker.signals.finished.connect(partial(setattr, self, "atlas_mesh"))

            pool = QThreadPool.globalInstance()
            pool.start(worker)


    @warn_if_slow()
    def render(self, change):
        actors = [self._atlas_mesh]
        if len((points := self.model.points).coords) > 0:
            coords = points.coords
            colors = (np.hstack((points.colors, points.alphas)) * 255).astype(int)  # alphas needed for fast rendering.
            actors.append(Points(coords, r=3, c=colors))

        self.plotter.show(actors, at=0)