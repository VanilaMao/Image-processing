# https://www.pythonguis.com/tutorials/pyqt6-qgraphics-vector-graphics/
# https://github.com/elifcansuyildiz/ImageProcessingQtApplication
from qtpy.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsRectItem,QWidget,QVBoxLayout
from qtpy.QtGui import QPixmap,QPainter, QPen, QImage
from qtpy.QtCore import Qt, QRect

class ImageViewer(QGraphicsView):
    def __init__(self, width: int, height:int) -> None:
        super().__init__()
        self._scene = QGraphicsScene()  #QRect(0,0,width,height)
        self.setScene(self._scene)
        self._image_item = None
        self._rect_item = None
        self.setRenderHints(QPainter.RenderHint.Antialiasing)


    def add_image(self,image:QImage):
        if self._image_item is not None:
            self._scene.removeItem(self._image_item)
        image_item = self._scene.addPixmap(QPixmap.fromImage(image))
        image_item.setPos(0,0)
        self._image_item = image_item

    def add_rectangle(self,x1, y1, x2,y2):
        if self._rect_item is not None:
            self._scene.removeItem(self._rect_item)
        rect_item = QGraphicsRectItem(x1,y1,x2-x1,y2-y1)
        rect_item.setPen(QPen(Qt.GlobalColor.red))
        self._scene.addItem(rect_item)
        self._rect_item = rect_item

    def clear_rectangle(self):
        if self._rect_item is not None:
            self._scene.removeItem(self._rect_item)
            self._rect_item = None


    # graphview/scene support drag ans select on items, drag behvaior will be handled and stop event bubble. So have to override to bubble
    # we don't need the item drag behavior here
    def mouseReleaseEvent(self, event):
        event.ignore()

    def create_image_viewer_widget(self):
        # construct the top level widget
        widget = QWidget()
        # construct the top level layout
        layout = QVBoxLayout(widget)

        # create the widgets to add to the layout

        # add the widgets to the layout
        layout.addWidget(self)

        # set the layout on the widget
        widget.setLayout(layout)
        # we now have a single widget that contains a layout and 2 widgets
        return widget
