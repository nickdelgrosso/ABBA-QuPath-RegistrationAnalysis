import numpy as np
from matplotlib import pyplot as plt
from vedo import Plotter, Points, Mesh
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from model import AppState
from utils import HasWidget


class PlotterWindow(HasWidget):

    def __init__(self, model: AppState):
        self.model = model
        widget = QVTKRenderWindowInteractor()
        HasWidget.__init__(self, widget=widget)
        self.plotter = Plotter(qtWidget=widget)
        self.mesh = Mesh(str(model.atlas.structures[997]['mesh_filename']), alpha=0.1, computeNormals=True, c=(1., 1., 1.))
        self.plotter.show(self.mesh, at=0)

        self.model.observe(self.on_change_selected_regions, names=['selected_region_ids'])
        self.model.observe(self.plot_cell_pointcloud, names=['cells'])


    def plot_cell_pointcloud(self, change):
        print('plotting points')
        if self.model.cells is not None:
            print(type(self.model.cells))
            max_name_ids = self.model.cells.name.cat.codes.max()
            name_ids = self.model.cells.name.cat.codes
            all_colors = (plt.cm.tab20c(name_ids / max_name_ids)[:, :4] * 255).astype(int)
            self.item_points = {}
            for id in self.model.atlas.hierarchy.expand_tree():
                in_region = self.model.cells.BGIdx == id
                if in_region.sum() != 0:
                    colors = all_colors[in_region, :]
                    cells = self.model.cells[in_region]
                    points = Points(cells[['X', 'Y', 'Z']].values * 1000, r=3, c=colors)
                    self.item_points[id] = points

            self.plotter.show(list(self.item_points.values()) + [self.mesh], at=0)



    def on_change_selected_regions(self, change):
        if (selected_ids := change['new']):
            for id, points in self.item_points.items():
                # points.alpha(1. if id in selected_ids else 0.05)
                if any(self.model.atlas.hierarchy.is_ancestor(selected_id, id) for selected_id in selected_ids):
                    points.alpha(1.)
                else:
                    points.alpha(0.05)

        else:
            for points in self.item_points.values():
                points.alpha(1.)


        # Fake a button press to force canvas update
        self.plotter.interactor.MiddleButtonPressEvent()
        self.plotter.interactor.MiddleButtonReleaseEvent()

