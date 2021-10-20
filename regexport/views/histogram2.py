import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from PySide2.QtWidgets import QVBoxLayout, QWidget
from traitlets import HasTraits, Instance, Bool, directional_link

from regexport.model import AppState
from regexport.views.utils import HasWidget

matplotlib.use('Qt5Agg')


from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure


class PlotModel(HasTraits):
    selected_data = Instance(np.ndarray, allow_none=True)
    data = Instance(np.ndarray, allow_none=True)
    show = Bool(default_value=True)

    def register(self, model: AppState):
        self.model = model
        model.observe(self.update, ['cells', 'selected_cells', 'column_to_plot', 'show_plots'])
        directional_link((model, 'show_plots'), (self, 'show'))

    def update(self, change):
        model = self.model
        if model.selected_cells is None or model.selected_cells[model.column_to_plot].dtype.name == 'category':
            self.selected_data = None
        else:
            self.data = model.cells[model.column_to_plot].values
            self.selected_data = model.selected_cells[model.column_to_plot].values


class PlotView(HasWidget):
    # Code from https://www.pythonguis.com/tutorials/plotting-matplotlib/

    def __init__(self, model: PlotModel, width=5, height=4, dpi=100):
        # Make a figure, turn it into a canvas widget
        widget = QWidget()

        layout = QVBoxLayout()
        widget.setLayout(layout)
        HasWidget.__init__(self, widget=widget)

        self.fig, self.axes = plt.subplots(ncols=2, figsize=(width, height), dpi=dpi)
        self.canvas = FigureCanvasQTAgg(figure=self.fig)
        layout.addWidget(self.canvas)

        self.toolbar = NavigationToolbar2QT(self.canvas, widget)
        layout.addWidget(self.toolbar)

        self.model = model
        self.model.observe(self.render)

    def render(self, change):
        if self.model.show:
            for ax in self.axes:
                ax.cla()
            if change.new is None:
                return
            else:
                selected_data = self.model.selected_data
                if selected_data is not None:
                    data = selected_data
                    _, edges = np.histogram(data[data > 0], bins='auto')
                    all_edges = np.concatenate([[0, 1], edges])
                    self.axes[0].hist(
                        data,
                        bins=all_edges,
                        cumulative=False,
                        # density=True,
                    )

                data = self.model.data

                ax: plt.Axes = self.axes[1]
                ax.hist(
                    data,
                    bins=50,
                    cumulative=True,
                    density=True,
                )
                if selected_data is not None:
                    ax.vlines(selected_data.max(), 0, 1, colors='black', linestyles='dotted')
                # self.axes[1].set_ylim(0, 1)
            self.canvas.draw()

