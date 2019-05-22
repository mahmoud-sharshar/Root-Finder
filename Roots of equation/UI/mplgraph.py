from PyQt5 import QtWidgets, QtGui
from matplotlib.backends.backend_qt5agg import (FigureCanvasQTAgg as FigureCanvas,
                                                NavigationToolbar2QT as NavigationToolbar)
from matplotlib.figure import Figure


class MplCanvas(FigureCanvas):
    def __init__(self):
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        FigureCanvas.__init__(self, self.fig)
        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)


class MplGraph(QtWidgets.QWidget):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.canvas = MplCanvas()
        self.canvas2 = MplCanvas()
        self.vbl = QtWidgets.QVBoxLayout()
        self.n = NavigationToolbar(self.canvas, self)
        self.n2 = NavigationToolbar(self.canvas2, self)
        self.vbl.addWidget(self.n)
        self.vbl.addWidget(self.canvas)
        self.vbl.addWidget(self.n2)
        self.vbl.addWidget(self.canvas2)
        self.n2.setVisible(False)
        self.canvas2.setVisible(False)
        self.setLayout(self.vbl)

    def update_canvas(self, method):
        method.plot(self.canvas)
