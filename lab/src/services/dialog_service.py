from enum import Enum
from qtpy.QtCore import Qt
from gui.dialog import Dialog
from gui.dialog_widget import DialogWidget
from gui.image_adjust import ImageAdjustWidget
from gui.message import Message

class DialogType(Enum):
   AdjustImage:  int  = 1
   Message =2

class DialogService:
    def __init__(self, title,width, height, type:DialogType, model= None) -> None:
        
        self._model = model
        self._height = height
        self._width= width
        self._inner_widget = self.create_dialog_widget(type)
        self._dialog = Dialog(self._inner_widget)
        self._dialog.setWindowTitle(title)
        self._dialog.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

    def open(self):
       if self._dialog.exec(): 
          return self._inner_widget.result
       return None
    
    def create_dialog_widget(self, type:DialogType)->DialogWidget:
        if type == DialogType.AdjustImage:
            if callable(self._model):
                return ImageAdjustWidget(lambda index:self._model(index).left,lambda index:self._model(index).right, self._model(0).right_margin, self._width,self._height)   #model is carbin
        if type == DialogType.Message:
            return Message(self._model)
        return None


