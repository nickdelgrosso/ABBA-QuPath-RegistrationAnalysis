from dataclasses import dataclass, field
from functools import partial
from typing import Optional, Tuple

import numpy as np
import pandas as pd
from PyQt5.QtCore import QThread
from bg_atlasapi import BrainGlobeAtlas
from matplotlib import pyplot as plt
from traitlets import HasTraits, Instance
from vedo import Plotter, Points, Mesh
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from model import AppState
from utils import warn_if_slow, since
from .utils import HasWidget, Worker


@dataclass(frozen=True)
class PointCloud:
    coords: np.ndarray = field(default=np.empty((0, 3), dtype=float))
    colors: np.ndarray = field(default=np.empty((0, 3), dtype=float))
    alphas: np.ndarray = field(default=np.empty((0, 1), dtype=float))


class PlotterModel(HasTraits):
    atlas_mesh = Instance(Mesh, default_value=Mesh())
    cell_points = Instance(Points, default_value=Points())
    points = Instance(PointCloud, default_value=PointCloud())

    def register(self, model: AppState):
        self.model = model
        self.create_thread()

        model.observe(self.link_cells_to_points, names=['selected_region_ids', 'cells'])
        model.observe(self.link_meshes_on_thread_worker, names=['atlas'])

    def create_thread(self):
        # from https://realpython.com/python-pyqt-qthread/#using-qthread-to-prevent-freezing-guis
        self.thread = QThread()
        self.thread.start()
        self.thread.finished.connect(self.thread.deleteLater)

    @staticmethod
    def plot_atlas_mesh(atlas: BrainGlobeAtlas) -> Mesh:
        return Mesh(
            str(atlas.structures[997]['mesh_filename']),
            alpha=0.1,
            computeNormals=True,
            c=(1., 1., 1.)
        )

    def link_meshes_on_thread_worker(self, change):
        if self.model.atlas is None:
            self.atlas_mesh = Mesh()
        else:
            worker = Worker(self.plot_atlas_mesh, self.model.atlas)
            worker.moveToThread(self.thread)
            worker.finished.connect(partial(setattr, self, "atlas_mesh"))
            worker.start.emit()

    def link_cells_to_points(self, change):
        model = self.model
        worker = Worker(
            self.plot_cells,
            cells=model.cells,
            selected_region_ids=model.selected_region_ids,
            atlas=model.atlas,
        )
        worker.moveToThread(self.thread)
        worker.finished.connect(partial(setattr, self, "points"))
        worker.start.emit()


    @staticmethod
    @warn_if_slow()
    def plot_cells(cells: Optional[pd.DataFrame], selected_region_ids: Tuple[int], atlas: BrainGlobeAtlas) -> PointCloud:
        if cells is None:
            return PointCloud()
        df = cells.copy(deep=False)
        df[['red', 'green', 'blue', 'alpha']] = pd.DataFrame((plt.cm.tab20c((codes := df.name.cat.codes) / codes.max())[:, :4]))
        if selected_ids := selected_region_ids:
            is_parent = lambda id: id != 0 and any(atlas.hierarchy.is_ancestor(selected_id, id) for selected_id in selected_ids)
            df['isSelected'] = df.groupby('BGIdx', as_index=False).BGIdx.transform(is_parent)
            df = df[df['isSelected']]
            if len(df) == 0:
                return PointCloud()

        points = PointCloud(
            coords=df[['X', 'Y', 'Z']].values * 1000,
            colors=df[['red', 'green', 'blue']],
            alphas=df[['alpha']],
        )
        return points



class PlotterView(HasWidget):

    def __init__(self, model: PlotterModel):
        self.model = model
        self.item_points = {}

        widget = QVTKRenderWindowInteractor()
        HasWidget.__init__(self, widget=widget)
        self.plotter = Plotter(qtWidget=widget)

        self.model.observe(self.render, names=['atlas_mesh', 'points'])

    def render(self, change):
        actors = [self.model.atlas_mesh]
        if len((points := self.model.points).coords) > 0:
            coords = points.coords
            colors = (np.hstack((points.colors, points.alphas)) * 255).astype(int)  # alphas needed for fast rendering.
            actors.append(Points(coords, r=3, c=colors))

        self.plotter.show(actors, at=0)
