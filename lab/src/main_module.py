from injector import Module, provider, singleton
from qtpy.QtWidgets import QMainWindow
from icons.constants import *
from qtpy.QtGui import QIcon

import icons_rc

class MainModule(Module):
    @singleton
    @provider
    def provide_main_window(self)->QMainWindow:
        # Central widget
        window = QMainWindow()
        window.setWindowIcon(QIcon(app_icon))
        window.setWindowTitle("Image Processing")
        return window