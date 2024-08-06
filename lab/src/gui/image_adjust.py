from enum import Enum
from qtpy.QtUiTools import loadUiType
from qtpy.QtWidgets import QWidget
from qtpy.QtGui import QPixmap
from qtpy.QtCore import Qt
from image_processing.image_processing import ImageProcessing
from gui.dialog_widget import DialogWidget
from gui.adjust_widget import Ui_widget
# uiclass, baseclass = loadUiType("gui/adjust.ui")

class AdjustActionType(Enum):
    Left = 0
    Rigt=1
    Up =3
    Down =4
    Redo = 5
    Undo= 6
    Reset = 7

class ImageAdjustWidget(Ui_widget, QWidget, DialogWidget):
    def __init__(self, left, right, width, height):
        super().__init__()
        self.setupUi(self)
        self._undos = []
        self._redos= []
        self.left.clicked.connect(lambda: self.btn_action(AdjustActionType.Left))
        self.right.clicked.connect(lambda: self.btn_action(AdjustActionType.Rigt))
        self.up.clicked.connect(lambda: self.btn_action(AdjustActionType.Up))
        self.down.clicked.connect(lambda: self.btn_action(AdjustActionType.Down))
        self.redo.clicked.connect(lambda: self.btn_action(AdjustActionType.Redo))
        self.undo.clicked.connect(lambda: self.btn_action(AdjustActionType.Undo))
        self.reset.clicked.connect(lambda: self.btn_action(AdjustActionType.Reset))
        self._left= ImageProcessing.convert_uint16_to_uint8(left)
        self._right = ImageProcessing.convert_uint16_to_uint8(right)
        self._move_right = 0
        self._move_down = 0
        self._height = height
        self._width = width
        self.update_image()
        self.update_movement_label()
        self._result = (self._move_right,self._move_down)

    
    def update_movement_label(self):
        self.label.setText(f"Move Right:{self._move_right},  Move Down:{self._move_down}")

    def get_move(self):
        return self._move_right, self._move_down

    def update_image(self):
        shifted_right_img = self._right
        if self._move_right!=0 or self._move_down != 0:
            shifted_right_img = ImageProcessing.shift_img(self._right,self._move_down,self._move_right)
        img = ImageProcessing.combine_img_to_bgr(self._left,shifted_right_img)
        qimage = ImageProcessing.cv_to_qimage(img,"bgr")
        display_imgae=qimage.scaled(self._width, self._height, Qt.AspectRatioMode.KeepAspectRatio)
        self.image.setPixmap(QPixmap.fromImage(display_imgae))
        
    def btn_action(self, action:AdjustActionType):
        if action ==   AdjustActionType.Left:
            self._move_right -=1
        elif action ==   AdjustActionType.Rigt:
            self._move_right +=1
        elif action ==   AdjustActionType.Up:
            self._move_down -=1
        elif action ==   AdjustActionType.Down:
            self._move_down +=1
        elif action ==   AdjustActionType.Reset:
            self._move_right = 0
            self._move_down = 0
        self.update_image()
        self.update_movement_label()
        self._result = self._move_right, self._move_down