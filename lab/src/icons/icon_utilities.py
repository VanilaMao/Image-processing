from qtpy.QtGui import  QColor, QPixmap, QImage, QPainter
from qtpy import QtSvg
def transfer_svg_to_icon(file:str, color:QColor)->QPixmap:
    svg = QtSvg.QSvgRenderer(file)
    if not svg.isValid:
        return None
    image = QImage(256,256,QImage.Format.Format_ARGB32)
    painter = QPainter(image)
    svg.render(painter)
    painter.setCompositionMode(
        painter.CompositionMode.CompositionMode_SourceIn)
    painter.fillRect(image.rect(),color)
    painter.end()
    return QPixmap.fromImage(image)