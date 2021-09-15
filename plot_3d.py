import time
from functools import partial
from typing import Dict, List, Callable, Any, Optional, Tuple

import pandas as pd
from PyQt5.QtCore import QThread, QObject, pyqtSignal, pyqtSlot
from bg_atlasapi import BrainGlobeAtlas
from matplotlib import pyplot as plt
from traitlets import HasTraits, Instance, link, directional_link
from vedo import Plotter, Points, Mesh
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from model import AppState
from utils import HasWidget


class Worker(QObject):
    start = pyqtSignal()
    started = pyqtSignal(str)
    finished = pyqtSignal(object)

    def __init__(self, fun: Callable, *args, **kwargs):
        super().__init__()
        self.fun = fun
        self.args = args
        self.kwargs = kwargs
        self.start.connect(self.run)

    # @pyqtSlot
    def run(self):
        self.finished.connect(self.deleteLater)
        print('started working...')
        self.started.emit("started run")
        result = self.fun(*self.args, **self.kwargs)
        print('finished working...')
        self.finished.emit(result)


class PlotterModel(HasTraits):
    atlas_mesh = Instance(Mesh, allow_none=True)
    cell_points = Instance(Points, allow_none=True)

    def observe_model(self, model: AppState):
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
        worker.finished.connect(partial(setattr, self, "cell_points"))
        worker.start.emit()

    @staticmethod
    def plot_cells(cells: Optional[pd.DataFrame], selected_region_ids: Tuple[int], atlas: BrainGlobeAtlas) -> Optional[Points]:
        if cells is not None:
            max_name_ids = cells.name.cat.codes.max()
            name_ids = cells.name.cat.codes

            colors = (plt.cm.tab20c(name_ids / max_name_ids)[:, :4] * 255).astype(int)

            if selected_ids := selected_region_ids:
                is_selected = cells.BGIdx.apply(
                    lambda id: any(
                        atlas.hierarchy.is_ancestor(selected_id, id) for selected_id in selected_ids if
                        id != 0)
                )
                cells = cells[is_selected]
                colors = colors[is_selected]

            if len(cells) > 0:
                return Points(cells[['X', 'Y', 'Z']].values * 1000, r=3, c=colors)
            else:
                return None





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
