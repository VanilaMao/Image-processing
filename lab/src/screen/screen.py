# https://www.youtube.com/watch?v=3QRBk-FpWjE
from typing import Dict
from qtpy.QtCore import Qt
from qtpy.QtGui import QCloseEvent, QIcon, QCursor, QMouseEvent
from qtpy.QtWidgets import (
    QMdiArea,
    QMdiSubWindow,
    QMainWindow,
    QVBoxLayout,
    QDockWidget,
)
from events.screen_event import *
from di.di import DI
from gui.image_tools import *
from gui.image_viewer import ImageViewer
from screen.screen_identifier import ScreenIdentifier
from screen.dockbar_config import dockerbar_configuration
from gui.graph import Graph
from icons.constants import *

class Dockbar:
    def __init__(self, name, parent) -> None:
        self._name = name
        self._parent = parent
        self._allowed_areas = None
        self._dock = QDockWidget(name, parent)

    def set_allowed_area(self, areas: Qt.DockWidgetArea):
        self._dock.setAllowedAreas(areas)
        self._allowed_areas = areas

    def init_dock(self, area: Qt.DockWidgetArea):
        self._parent.addDockWidget(area, self._dock)

    def get_window(self):
        return self._dock
    
    def update(self, data):
        pass
    
class GrapgDockbar(Dockbar):
    def __init__(self, name, parent) -> None:
        super().__init__(name, parent)
        self._graph = Graph()
        self._dock.setWidget(self._graph)

    def update(self,data):
        self._graph.add_collections(data[0],data[1])

class Screen:
    def __init__(self, identifier: ScreenIdentifier,image_loader:callable= None) -> None:
        self._identifier = identifier
        self._mdi_subwindow = QMdiSubWindow()
        self._mdi_subwindow.setWindowTitle(f"{identifier.value}")
        self._mdi_subwindow.setWindowIcon(QIcon(worm_icon))
        self._mdi_subwindow.closeEvent = self.close_event
        # close event  to hide it only
        # self._prev_mousePressEvent, self._prev_mouseReleaseEvent,self._prev_mouseMoveEvent = \
        #     self._mdi_subwindow.mouseReleaseEvent, self._mdi_subwindow.mouseReleaseEvent, self._mdi_subwindow.mouseMoveEvent
        
        self._roi = False
        self._drag = False
        self._drag_start = None
        self._image_viwer = ImageViewer(
            self._mdi_subwindow.width(), self._mdi_subwindow.height()
        )
        if image_loader is not None:
            self._image_viwer.add_image(image_loader())
        self._mdi_subwindow.setWidget(self._image_viwer.create_image_viewer_widget())
        self._image_viwer.mousePressEvent = self.mousePressEvent
        self._image_viwer.mouseReleaseEvent = self.mouseReleaseEvent

    @property
    def id(self):
        return self._identifier
    
    def update(self, content_updater:callable):
        self._image_viwer.add_image(content_updater())

    def show(self):
        self._mdi_subwindow.show()

    def hide(self):
        self._mdi_subwindow.hide()

    def close(self):
        self._mdi_subwindow.close()

    def resize(self, width, height):
        self._mdi_subwindow.resize(width, height)

    def get_window(self):
        return self._mdi_subwindow

    def close_event(self, event: QCloseEvent):
        event.accept()
        DI.get_di_instance().get(ScreenEventSub).dispatchEvent(
            ScreenEvent(ScreenEventEnum.close, self._identifier)
        )

    # TODO not working on subwindow, but working in MDI Area
    def set_cursor(self, cursor):
        self._roi = True
        self._mdi_subwindow.setCursor(QCursor(cursor))
        print(self._mdi_subwindow.height())
        print(self._mdi_subwindow.width())

    # https://stackoverflow.com/questions/62749103/move-entire-window-with-middle-mouse-click-drag-in-qt
    def mousePressEvent(self, e: QMouseEvent):
        print(f"mouse press {self.id}")
        if not self._roi:
            e.ignore()
            return
        self._drag = True
        self._drag_start = self._image_viwer.mapToScene(e.pos()) 
        e.accept()
        print(f"mouse drag press {self.id}")

    # TODO create a class inherit form QMdiSubWindow, like ImageSubWindow, hanlde drag. mouseevnt and custom event bubble to parent
    # https://stackoverflow.com/questions/34854546/how-to-make-a-qevent-that-bubbles-up-to-parent-qobjects  findlicdren to subscribe signal
    def mouseReleaseEvent(self, e: QMouseEvent):
        print(f"release and event from {self.id}")
        if not self._roi or not self._drag:
            e.ignore()
            print("unexpected exit")
            return
        self._drag_end = self._image_viwer.mapToScene(e.pos())
        sc_start = Point(self._drag_start.x(), self._drag_start.y())
        sc_end = Point(self._drag_end.x(), self._drag_end.y())
        event = ScreenMouseEvent(
            ScreenEventEnum.select, self._identifier, sc_start, sc_end
        )
        DI.get_di_instance().get(ScreenEventSub).dispatchEvent(event)
        self._drag = False
        self.draw_selection_rect(sc_start, sc_end)
        e.accept()

    def draw_selection_rect(self, start: Point, end: Point):
        self._image_viwer.add_rectangle(start.x, start.y, end.x, end.y)

    def clear_screen_rect(self):
         self._image_viwer.clear_rectangle()

class Conductor:
    def __init__(self, parent: QMainWindow | None = ...) -> None:
        self._parent = parent
        self._mdi_area = QMdiArea(parent)
        self._mdi_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        self._mdi_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self._parent.setCentralWidget(self._mdi_area)
        self._screens: Dict[ScreenIdentifier, Screen] = {}
        self._dockbars: Dict[str, Dockbar] = {}
        for dockbar_name in dockerbar_configuration:
            self._dockbars[dockbar_name] = GrapgDockbar(dockbar_name, parent)
            self._dockbars[dockbar_name].set_allowed_area(
                Qt.DockWidgetArea.RightDockWidgetArea
            )
            # self._dockbars[dockbar_name].init_dock(Qt.DockWidgetArea.RightDockWidgetArea)
        self.tabify_dockbars(Qt.DockWidgetArea.RightDockWidgetArea)
        self._current_screen = None
        self._layout = None

    def activate_screen(self, screenIdentifier: ScreenIdentifier, image_loader:callable= None):
        if screenIdentifier not in self._screens:
            screen = Screen(screenIdentifier,image_loader)
            self._screens[screenIdentifier] = screen
            self._mdi_area.addSubWindow(screen.get_window())
            self._screens[screenIdentifier].resize(256, 512)         
        elif image_loader is not None:
            self.update_screen(screenIdentifier,image_loader)
        
        self._screens[screenIdentifier].show()
        self._current_screen = self._screens[screenIdentifier]

    def update_screen(self, screenIdentifier: ScreenIdentifier, content_updater:callable):
        if screenIdentifier not in self._screens:
            print("f{screenIdentifier: ScreenIdentifier} is not found")
            return
        self._screens[screenIdentifier].update(content_updater)

    def close_screen(self, screenIdentifier: ScreenIdentifier):
        if self._screens[screenIdentifier]:
            self._screens[screenIdentifier].close()
            del self._screens[screenIdentifier]
            self._current_screen = next(iter(self._screens), None)

    def hide_screen(self, screenIdentifier: ScreenIdentifier):
        if screenIdentifier in self._screens:
            self._screens[screenIdentifier].hide()
            self._current_screen = next(iter(self._screens), None)

    def get_layout(self):
        if self._layout is None:
            self._layout = QVBoxLayout(self._mdi_area)
        return self._layout

    def tabify_dockbars(self, area: Qt.DockWidgetArea):
        prev = None
        for dockbar in self._dockbars:
            self._parent.addDockWidget(area, self._dockbars[dockbar].get_window())
            if prev:
                self._parent.tabifyDockWidget(
                    prev, self._dockbars[dockbar].get_window()
                )
            prev = self._dockbars[dockbar].get_window()

    def image_tools(self, tool: ImageToolsEnum):
        # self._mdi_area.setCursor(QCursor(image_cursor_dict[tool]))
        for screen in self._screens:
            self._screens[screen].set_cursor(image_cursor_dict[tool])

    def draw_screen_rect(self, id, start: Point, end: Point):
        for screen in self._screens:
            if id == self._screens[screen].id:
                continue
            self._screens[screen].draw_selection_rect(start, end)
    
    def clear_screen_rect(self):
         for screen in self._screens:
            self._screens[screen].clear_screen_rect()

    def report(self,dock_name,x_set,y_set):
        dock = self._dockbars[dock_name]
        dock.update((x_set,y_set))