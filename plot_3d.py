import time
from typing import List, Dict

import numpy as np
from PyQt5.QtCore import QThread, QObject, pyqtSignal
from matplotlib import pyplot as plt
from vedo import Plotter, Points, Mesh
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from model import AppState
from utils import HasWidget

class PointPlotterWorker(QObject):
    finished = pyqtSignal(dict)

    def __init__(self, model: AppState):
        super().__init__()
        self.model = model

    def run(self):
        print('starting run')
        start_time = time.monotonic()
        max_name_ids = self.model.cells.name.cat.codes.max()
        name_ids = self.model.cells.name.cat.codes
        all_colors = (plt.cm.tab20c(name_ids / max_name_ids)[:, :4] * 255).astype(int)
        item_points = {}

        for id in self.model.atlas.hierarchy.expand_tree():
            in_region = self.model.cells.BGIdx == id
            if in_region.sum() != 0:
                colors = all_colors[in_region, :]
                cells = self.model.cells[in_region]
                points = Points(cells[['X', 'Y', 'Z']].values * 1000, r=3, c=colors)
                item_points[id] = points

        print(f"Total Time: {time.monotonic() - start_time} for {len(self.model.cells)}")
        self.finished.emit(item_points)  # Dict[int, Points]



class PlotterWindow(HasWidget):

    def __init__(self, model: AppState):
        self.model = model
        widget = QVTKRenderWindowInteractor()
        HasWidget.__init__(self, widget=widget)
        self.plotter = Plotter(qtWidget=widget)
        self.mesh = Mesh(str(model.atlas.structures[997]['mesh_filename']), alpha=0.1, computeNormals=True, c=(1., 1., 1.))
        self.plotter.show(self.mesh, at=0)

        self.model.observe(self.on_change_selected_regions, names=['selected_region_ids'])
        self.model.observe(self.plot_cells, names=['cells'])

    def plot_cells(self, change):
        if self.model.cells is not None:
            # from https://realpython.com/python-pyqt-qthread/#using-qthread-to-prevent-freezing-guis
            self.thread = QThread()
            self.worker = PointPlotterWorker(model=self.model)
            self.worker.moveToThread(self.thread)
            self.thread.started.connect(self.worker.run)
            self.worker.finished.connect(self.update_item_points)
            self.worker.finished.connect(self.worker.deleteLater)
            self.thread.finished.connect(self.thread.deleteLater)
            self.thread.start()

    def update_item_points(self, item_points: Dict[int, Points]):
        self.item_points = item_points
        self.render()

    def render(self):
        visible_points = [point for point in self.item_points.values() if point.alpha() > 0]  # vedo is slow with non-1 alphas.
        self.plotter.show(visible_points + [self.mesh], at=0)

    def on_change_selected_regions(self, change):
        if (selected_ids := change['new']):
            for id, points in self.item_points.items():
                if any(self.model.atlas.hierarchy.is_ancestor(selected_id, id) for selected_id in selected_ids):
                    points.alpha(1.)
                else:
                    points.alpha(0)
        else:
            for points in self.item_points.values():
                points.alpha(1.)

        self.render()

