from functools import partial
from typing import Optional, Tuple

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


class PlotterModel(HasTraits):
    atlas_mesh = Instance(Mesh, default_value=Mesh())
    cell_points = Instance(Points, default_value=Points())

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
        worker.finished.connect(partial(setattr, self, "cell_points"))
        worker.start.emit()


    @staticmethod
    @warn_if_slow()
    def plot_cells(cells: Optional[pd.DataFrame], selected_region_ids: Tuple[int], atlas: BrainGlobeAtlas) -> Points:
        if cells is None:
            return Points()
        t = since()
        print(1, next(t))
        df = cells.copy(deep=False)
        print(2, next(t))
        df[['red', 'green', 'blue', 'alpha']] = pd.DataFrame((plt.cm.tab20c((codes := df.name.cat.codes) / codes.max())[:, :4]))
        print(3, next(t))
        if selected_ids := selected_region_ids:
            print(4, next(t))
            is_parent = lambda id: id != 0 and any(atlas.hierarchy.is_ancestor(selected_id, id) for selected_id in selected_ids)
            print(5, next(t))
            df['isSelected'] = df.groupby('BGIdx', as_index=False).BGIdx.transform(is_parent)
            print(6, next(t))
            df = df[df['isSelected']]
            print(7, next(t))
            if len(df) == 0:
                return Points()

        print('a', next(t))
        colors = (df[['red', 'green', 'blue', 'alpha']] * 255).astype(int).values  # Points() is slow if alpha not supplied.
        print('a1', next(t))
        coords = df[['X', 'Y', 'Z']].values * 1000
        print('a2', next(t))
        print(colors)
        points = Points(coords, r=3, c=colors)
        print('b', next(t))
        return points


class PlotterView(HasWidget):

    def __init__(self, model: PlotterModel):
        self.model = model
        self.item_points = {}

        widget = QVTKRenderWindowInteractor()
        HasWidget.__init__(self, widget=widget)
        self.plotter = Plotter(qtWidget=widget)

        self.model.observe(self.render, names=['atlas_mesh', 'cell_points'])

    def render(self, change):
        self.plotter.show([self.model.cell_points, self.model.atlas_mesh], at=0)
