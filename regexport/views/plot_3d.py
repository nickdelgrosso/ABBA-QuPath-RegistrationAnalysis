from dataclasses import dataclass, field
from functools import partial
from pathlib import Path
from typing import Optional, Tuple

import numpy as np
import pandas as pd
from PyQt5.QtCore import QThreadPool
from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap
from traitlets import HasTraits, Instance, directional_link
from vedo import Plotter, Mesh, Points
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from regexport.model import AppState
from regexport.utils.parallel import Task
from regexport.utils.plotting import convert_values_to_colors
from regexport.utils.profiling import warn_if_slow
from regexport.views.utils import HasWidget


@dataclass(frozen=True)
class PointCloud:
    coords: np.ndarray = field(default=np.empty((0, 3), dtype=float))
    colors: np.ndarray = field(default=np.empty((0, 3), dtype=float))
    alphas: np.ndarray = field(default=np.empty((0, 1), dtype=float))

    def __post_init__(self):
        assert self.coords.ndim == 2 and self.coords.shape[1] == 3
        assert self.colors.ndim == 2 and self.colors.shape[1] == 3
        assert self.alphas.ndim == 2 and self.alphas.shape[1] == 1


class PlotterModel(HasTraits):
    atlas_mesh = Instance(Path, allow_none=True)
    points = Instance(PointCloud, default_value=PointCloud())

    def register(self, model: AppState):
        self.model = model
        directional_link(
            (model, 'atlas'),
            (self, 'atlas_mesh'),
            lambda atlas: Path(str(atlas.structures[997]['mesh_filename'])) if atlas is not None else None
        )
        model.observe(self.link_cells_to_points, names=[
            'selected_cell_ids', 'cells', 'selected_colormap'
        ])

    def link_cells_to_points(self, change):
        model = self.model
        worker = Task(
            self.plot_cells,
            cells=model.cells,
            selected_cell_ids=model.selected_cell_ids,
            cmap=self.model.selected_colormap
        )
        worker.signals.finished.connect(partial(setattr, self, "points"))
        pool = QThreadPool.globalInstance()
        pool.start(worker)

    @staticmethod
    @warn_if_slow()
    def plot_cells(cells: Optional[pd.DataFrame], selected_cell_ids: Optional[Tuple[int]], cmap: str = 'tab20c') -> PointCloud:
        if cells is None:
            return PointCloud()
        print('plotting')
        df = cells.copy(deep=False)
        print(df.head(), df.columns, sep='\n')
        cell_colors = convert_values_to_colors(df.BrainRegion.cat.codes, getattr(plt.cm, cmap))
        df[['red', 'green', 'blue', 'alpha']] = pd.DataFrame(cell_colors)
        if selected_cell_ids is not None:
            df = df.iloc[selected_cell_ids]
            if len(df) == 0:
                return PointCloud()

        points = PointCloud(
            coords=df[['X', 'Y', 'Z']].values * 1000,
            colors=df[['red', 'green', 'blue']].values,
            alphas=df[['alpha']].values,
        )
        return points


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
        # box = self._atlas_mesh.box().wireframe().alpha(0.2).color((255, 0, 0))

        # actors.append(box)
        if len((points := self.model.points).coords) > 0:
            coords = points.coords
            colors = (np.hstack((points.colors, points.alphas)) * 255).astype(int)  # alphas needed for fast rendering.
            actors.append(Points(coords, r=3, c=colors))

        self.plotter.show(actors, at=0)
        self.plotter.addInset(self._atlas_mesh, pos=(.9, .9), size=0.1, c='w', draggable=True)
        # note: look at from vedo.applications import SlicerPlotter for inspiration