import time
from typing import Dict, List

from PyQt5.QtCore import QThread, QObject, pyqtSignal
from bg_atlasapi import BrainGlobeAtlas
from matplotlib import pyplot as plt
from traitlets import HasTraits, Instance, link, directional_link
from vedo import Plotter, Points, Mesh
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from model import AppState
from utils import HasWidget


class PointPlotterWorker(QObject):
    finished = pyqtSignal(list)

    def __init__(self, model: AppState, plotter: Plotter):
        super().__init__()
        self.model = model
        self.plotter = plotter

    def run(self):
        print('starting run')
        start_time = time.monotonic()

        actors = []

        # Pointcloud
        if self.model.cells is not None:
            max_name_ids = self.model.cells.name.cat.codes.max()
            name_ids = self.model.cells.name.cat.codes

            colors = (plt.cm.tab20c(name_ids / max_name_ids)[:, :4] * 255).astype(int)

            cells = self.model.cells
            if (selected_ids := self.model.selected_region_ids):
                is_selected = self.model.cells.BGIdx.apply(
                    lambda id: any(
                        self.model.atlas.hierarchy.is_ancestor(selected_id, id) for selected_id in selected_ids if
                        id != 0)
                )
                cells = self.model.cells[is_selected]
                colors = colors[is_selected]

            if len(cells) > 0:
                point_cloud = Points(cells[['X', 'Y', 'Z']].values * 1000, r=3, c=colors)
                actors.append(point_cloud)

        # Render
        self.finished.emit(actors)


class PlotterModel(HasTraits):
    atlas_mesh = Instance(Mesh, allow_none=True)
    cell_points = Instance(Points, allow_none=True)

    def observe_model(self, model: AppState):
        self.model = model
        directional_link(
            source=(model, 'atlas'),
            target=(self, 'atlas_mesh'),
            transform=lambda atlas: self.plot_atlas_mesh(atlas) if atlas is not None else None,
        )
        model.observe(self.plot_cells, names=['selected_region_ids', 'cells'])

    @staticmethod
    def plot_atlas_mesh(atlas: BrainGlobeAtlas) -> Mesh:
        return Mesh(
            str(atlas.structures[997]['mesh_filename']),
            alpha=0.1,
            computeNormals=True,
            c=(1., 1., 1.)
        )

    def plot_cells(self, change):
        if self.model.cells is not None:
            max_name_ids = self.model.cells.name.cat.codes.max()
            name_ids = self.model.cells.name.cat.codes

            colors = (plt.cm.tab20c(name_ids / max_name_ids)[:, :4] * 255).astype(int)

            cells = self.model.cells
            if (selected_ids := self.model.selected_region_ids):
                is_selected = self.model.cells.BGIdx.apply(
                    lambda id: any(
                        self.model.atlas.hierarchy.is_ancestor(selected_id, id) for selected_id in selected_ids if
                        id != 0)
                )
                cells = self.model.cells[is_selected]
                colors = colors[is_selected]

            if len(cells) > 0:
                self.cell_points = Points(cells[['X', 'Y', 'Z']].values * 1000, r=3, c=colors)







class PlotterWindow(HasWidget):

    def __init__(self, vmodel: PlotterModel):
        self.vmodel = vmodel
        self.item_points = {}

        widget = QVTKRenderWindowInteractor()
        HasWidget.__init__(self, widget=widget)
        self.plotter = Plotter(qtWidget=widget)

        self.vmodel.observe(self.render, names=['atlas_mesh', 'cell_points'])

    def update_plot(self, change):
        # from https://realpython.com/python-pyqt-qthread/#using-qthread-to-prevent-freezing-guis
        self.thread = QThread()
        self.worker = PointPlotterWorker(model=self.model, plotter=self.plotter)
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.render)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()

    def render(self, change):
        self.plotter.show([self.vmodel.cell_points, self.vmodel.atlas_mesh], at=0)
