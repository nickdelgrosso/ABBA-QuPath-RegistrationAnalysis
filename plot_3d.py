import numpy as np
import pandas as pd
from bg_atlasapi import BrainGlobeAtlas
from matplotlib import pyplot as plt
from vedo import Plotter, Points, Mesh
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor

from model import AppState
from utils import HasWidget


class PlotterWindow(HasWidget):

    def __init__(self, model: AppState):
        widget = QVTKRenderWindowInteractor()
        HasWidget.__init__(self, widget=widget)
        Plotter(qtWidget=widget).show(
            Points(
                model.cells[['X', 'Y', 'Z']].values * 1000,
                r=3,
                c=plt.cm.tab20c((name_ids := model.cells.name.cat.codes) / np.max(name_ids))[:, :3]
            ),
            Mesh(
                str(model.atlas.structures[997]['mesh_filename']),
                alpha=0.1,
                computeNormals=True,
                c=(1., 1., 1.)
            ),
            at=0,
        )
