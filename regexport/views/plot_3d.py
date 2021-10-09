from pathlib import Path
from typing import Optional

import numpy as np
from traitlets import HasTraits, Instance, directional_link
from vedo import Plotter, Mesh, Points
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from regexport.model import AppState
from regexport.utils.point_cloud import PointCloud
from regexport.utils.profiling import warn_if_slow
from regexport.views.utils import HasWidget


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
            'selected_cells', 'selected_colormap', 'column_to_plot',
        ])

    def link_cells_to_points(self, change):
        model = self.model
        if model.selected_cells is None:
            self.points = PointCloud()
            return
        color_col = model.selected_cells[model.column_to_plot]
        points = PointCloud.from_cmap(
            positions=model.selected_cells[['X', 'Y', 'Z']].values * 1000,
            color_levels=color_col.cat.codes.values if color_col.dtype.name == 'category' else color_col.values,
            cmap=self.model.selected_colormap
        )
        self.points = points


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
            # worker = Task(self.load_mesh, self.model.atlas_mesh)
            # worker.signals.finished.connect(partial(setattr, self, "atlas_mesh"))
            # 
            # pool = QThreadPool.globalInstance()
            # pool.start(worker)
            self.atlas_mesh = self.load_mesh(self.model.atlas_mesh)


    @warn_if_slow()
    def render(self, change=None):
        actors = [self._atlas_mesh]
        # box = self._atlas_mesh.box().wireframe().alpha(0.2).color((255, 0, 0))

        # actors.append(box)
        if len((points := self.model.points).coords) > 0:
            coords = points.coords
            colors = (np.hstack((points.colors, points.alphas)) * 255).astype(int)  # alphas needed for fast rendering.
            actors.append(Points(coords, r=3, c=colors))

        self.plotter.clear(at=0)
        self.plotter.show(actors, at=0)
        # self.plotter.addInset(self._atlas_mesh, pos=(.9, .9), size=0.1, c='w', draggable=True)
        # note: look at from vedo.applications import SlicerPlotter for inspiration
