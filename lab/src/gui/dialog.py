from qtpy.QtWidgets import QDialog, QDialogButtonBox,QVBoxLayout
class Dialog(QDialog):
    def __init__(self, widget):
        super().__init__()

        btn_style = QDialogButtonBox.StandardButton.Ok|QDialogButtonBox.StandardButton.Cancel

        self.buttonBox = QDialogButtonBox(btn_style)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.layout = QVBoxLayout()
        self.layout.addWidget(widget)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)