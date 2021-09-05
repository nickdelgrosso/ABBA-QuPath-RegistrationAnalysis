import time
from typing import Dict, List

from PyQt5.QtCore import QThread, QObject, pyqtSignal
from matplotlib import pyplot as plt
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

        # Brain Mesh
        if self.model.atlas is not None:
            mesh = Mesh(
                str(self.model.atlas.structures[997]['mesh_filename']),
                alpha=0.1,
                computeNormals=True,
                c=(1., 1., 1.)
            )
            actors.append(mesh)

        # Render
        self.finished.emit(actors)



class PlotterWindow(HasWidget):

    def __init__(self, model: AppState):
        self.model = model
        self.item_points = {}

        widget = QVTKRenderWindowInteractor()
        HasWidget.__init__(self, widget=widget)
        self.plotter = Plotter(qtWidget=widget)

        self.model.observe(self.update_plot, names=['selected_region_ids', 'cells', 'mesh'])

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

    def render(self, actors: List):
        self.plotter.show(actors, at=0)
