from gui.dialog_widget import DialogWidget
from qtpy.QtWidgets import QWidget,QLabel, QVBoxLayout
class Message(QWidget, DialogWidget):
    def __init__(self, model) -> None:
        super().__init__()
        layout = QVBoxLayout()
        label = QLabel(model)
        label.setWordWrap(True)
        layout.addWidget(label)
        self.setLayout(layout)

