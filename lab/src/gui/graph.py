# QtCharts vs pyqtgraph https://www.pyqtgraph.org/ vs VisPy
# https://www.pythonguis.com/tutorials/pyside6-plotting-pyqtgraph/
import math
import numpy as np
import pyqtgraph as pg
from qtpy.QtUiTools import loadUiType
from qtpy.QtWidgets import QWidget
# uiclass, baseclass = loadUiType("gui/graph.ui")
from gui.graph_widget import Ui_Widget

class Graph(Ui_Widget, QWidget):
    def __init__(self, min = 0 , max= 0):
        super().__init__()
        self.setupUi(self)
        self._plotGraph: pg.PlotWidget = self.plotGraph
        self._plotGraph.setBackground('#000000')
        self._max= max
        self._min = min
        self.max.setValue(self._max)
        self.min.setValue(self._min)
        self.max.valueChanged.connect(lambda x: self.set_minmax(x,1))
        self.min.valueChanged.connect(lambda x: self.set_minmax(x, 0))
        self._plotGraph.showGrid(x=True, y=True)
        self._x_values=[]
        self._y_values = []
        self._line = self._plotGraph.plot(
            self._x_values,
            self._y_values,
            pen = pg.mkPen(color=(255, 0, 0),width=2)
        )
    
    def add_data(self, x, y):
        self._x_values.append(x)
        self._y_values.append(y)
        self._line.setData(self._x_values,self._y_values)
        self.set_yaxis_max()

    def add_collections(self, x_set,y_set):
        self._x_values = x_set
        self._y_values = y_set
        self._line.setData(x_set,y_set)
        self.set_yaxis_max()

    def set_minmax(self, value, max):
        if max:
            self._plotGraph.setYRange(self._min, value)
            self._max= value
        else:
            self._plotGraph.setYRange(value, self._max)
            self._min = value
    
    def set_yaxis_max(self):
        if math.isclose(self._max, 0.0):
            max = np.max(self._y_values)+1
            min = np.max(self._y_values)-1
            self._plotGraph.setYRange(min, max)
        else:
            self._plotGraph.setYRange(self._min, self._max)