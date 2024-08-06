from enum import Enum
from qtpy.QtCore import Qt

class ImageToolsEnum(Enum):
    Select= 1
    ZoomIn = 2
    ZoomOut=3
    Second= 4

image_cursor_dict = {
    ImageToolsEnum.Select: Qt.CursorShape.CrossCursor
}