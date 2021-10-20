import matplotlib
import numpy as np
from PySide2.QtWidgets import QVBoxLayout, QWidget
from traitlets import HasTraits, Instance

from regexport.model import AppState
from regexport.views.utils import HasWidget

import seaborn as sns

matplotlib.use('Qt5Agg')


from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT
from matplotlib.figure import Figure


class PlotModel(HasTraits):
    data = Instance(np.ndarray, allow_none=True)

    def register(self, model: AppState):
        self.model = model
        model.observe(self.update, ['selected_cells', 'column_to_plot'])

    def update(self, change):
        model = self.model
        if model.selected_cells is None or model.selected_cells[model.column_to_plot].dtype.name == 'category':
            self.data = None
        else:
            self.data = model.selected_cells[model.column_to_plot].values


class PlotView(HasWidget):
    # Code from https://www.pythonguis.com/tutorials/plotting-matplotlib/

    def __init__(self, model: PlotModel, width=5, height=4, dpi=100):
        # Make a figure, turn it into a canvas widget
        widget = QWidget()

        layout = QVBoxLayout()
        widget.setLayout(layout)
        HasWidget.__init__(self, widget=widget)

        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        self.canvas = FigureCanvasQTAgg(figure=self.fig)
        layout.addWidget(self.canvas)

        self.toolbar = NavigationToolbar2QT(self.canvas, widget)
        layout.addWidget(self.toolbar)

        self.model = model
        self.model.observe(self.render)

    def render(self, change):
        self.axes.cla()
        if change.new is None:
            pass
        else:
            data = self.model.data
            _, edges = np.histogram(data[data > 0], bins='auto')

            print(edges)
            self.axes.hist(
                data,
                bins=np.concatenate([[0, 1], edges]),
            )
        self.canvas.draw()

#
# class MainWindow(QtWidgets.QMainWindow):
#
#     def __init__(self, *args, **kwargs):
#         super(MainWindow, self).__init__(*args, **kwargs)
#
#         self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
#         self.setCentralWidget(self.canvas)
#
#         n_data = 50
#         self.xdata = list(range(n_data))
#         self.ydata = [random.randint(0, 10) for i in range(n_data)]
#
#         # We need to store a reference to the plotted line
#         # somewhere, so we can apply the new data to it.
#         self._plot_ref = None
#         self.update_plot()
#
#         self.show()
#
#         # Setup a timer to trigger the redraw by calling update_plot.
#         self.timer = QtCore.QTimer()
#         self.timer.setInterval(16)
#         self.timer.timeout.connect(self.update_plot)
#         self.timer.start()
#
#     def update_plot(self):
#         # Drop off the first y element, append a new one.
#         self.ydata = self.ydata[1:] + [random.randint(0, 10)]
#
#         # Note: we no longer need to clear the axis.
#         if self._plot_ref is None:
#             # First time we have no plot reference, so do a normal plot.
#             # .plot returns a list of line <reference>s, as we're
#             # only getting one we can take the first element.
#             plot_refs = self.canvas.axes.plot(self.xdata, self.ydata, 'r')
#             self._plot_ref = plot_refs[0]
#         else:
#             # We have a reference, we can use it to update the data for that line.
#             self._plot_ref.set_ydata(self.ydata)
#
#         # Trigger the canvas to update and redraw.
#         self.canvas.draw()
#
#
#
# app = QtWidgets.QApplication(sys.argv)
# w = MainWindow()
# app.exec_()
