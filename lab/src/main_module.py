import time
from injector import Module, provider, singleton, inject
from qtpy.QtWidgets import QMainWindow, QMdiSubWindow
from icons.constants import *
from qtpy.QtGui import QIcon
from qtpy.QtCore import QObject, QThread
from gui.utilities import process_ui_event

import icons_rc
from services.context_service import ContextService
from services.document_service import DocType, DocumentService

class SaveWorker(QObject):
    def __init__(self, locs):
        super().__init__()
        self._locs = locs

    def save(self):
        print(f"worker {self._locs}")
        time.sleep(20)
        print(self._locs)


class LabWindow(QMainWindow):
    def __init__(self, locations, doc_service:DocumentService):
        super().__init__()
        self._locs = locations
        self._doc_service = doc_service
    
    def closeEvent(self, event):
        print("close event")
        for children in self.findChildren(QMdiSubWindow):
            children.close()

        process_ui_event()
        self._doc_service.save(DocType.Settings, self._locs)
        super(LabWindow, self).closeEvent(event)

class MainModule(Module):
    @singleton
    @provider
    @inject
    def provide_main_window(self,context_service:ContextService, doc_service:DocumentService)->QMainWindow:
        # Central widget
        context_service.ui.locations = doc_service.load(DocType.Settings)
        window = LabWindow(context_service.ui.locations, doc_service)
        window.setWindowIcon(QIcon(app_icon))
        window.setWindowTitle("Image Processing")
        return window