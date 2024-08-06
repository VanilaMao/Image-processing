try:
    os.chdir(sys._MEIPASS)  #pyinstaller
    print(sys._MEIPASS)
except:
    pass
import sys
import os
from qtpy.QtGui import QFont, QIcon
from qtpy.QtWidgets import (
    QApplication,
    QMainWindow,
    QToolButton,
)
from ribbon import LabRibbon
from pyqtribbon import RibbonBar
from icons.constants import *
from menus.file_menu import *
from menus.process_menu import *
from services.toolbar_service import ToolbarService
from di.di import DI


import icons_rc

if __name__ == "__main__":

    # config DI
    di = DI.get_di_instance()

    # Monkey patch ribbon bugs
    LabRibbon.patch_panel_addWidgetsBy()

    app = QApplication(sys.argv)
    app.setFont(QFont("Times New Roman", 8))

    window = di.get(QMainWindow)

    # Ribbon bar
    ribbonbar = RibbonBar()

    app_button = ribbonbar.applicationOptionButton()
    app_button.setToolTip("Settings")
    app_button.setIcon(QIcon(worm_icon))
    app_button.setVisible(False)
    window.setMenuBar(ribbonbar)

    # Right toolbar
    rbutton = QToolButton()
    rbutton.setText("Contact")
    ribbonbar.addRightToolButton(rbutton)

    file_category = ribbonbar.addCategoriesBy(file_menu())

    process_category = ribbonbar.addCategoriesBy(process_menu())

    # init central screen
    tb = di.get(ToolbarService)
    tb.init()

    # Show the window
    window.resize(1000, 800)  # type: ignore
    window.statusBar().showMessage("Ready")
    window.show()
    sys.exit(app.exec_())
