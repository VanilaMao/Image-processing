# https://doc.qt.io/qtforpython-6/examples/example_widgets_mainwindows_mdi.html
# https://pypi.org/project/PySide6-QtAds/
from typing import List
from injector import inject, singleton
from gui.image_tools import ImageToolsEnum
from models.location import Rect
from models.worm import CarbinReport
from screen.screen import *
from screen.screen_identifier import *
from services.context_service import ContextService

@singleton
class ScreenService:
    @inject
    def __init__(self, parent: QMainWindow, ses:ScreenEventSub, context_service:ContextService) -> None:
        self._conductor: Conductor = Conductor(parent)
        self._parent = parent
        ses.addEventListener(ScreenEventEnum.close, self.close_screen)
        ses.addEventListener(ScreenEventEnum.select, self.draw_screen_rect)
        self._screen_widgets = {}
        self._context_service = context_service

    def open_screen(self, id:ScreenIdentifier, image_loader:callable= None, update_tools_bar=False, force = False):
        locations= self._context_service.ui.locations
        self._conductor.activate_screen(id,image_loader, force, locations.get(id) if locations is not None else None)
        if update_tools_bar:
            widget = self._screen_widgets[id]
            widget.setChecked(True)
    
    def hide_screen(self, id:ScreenIdentifier):
        self._conductor.hide_screen(id)

    def get_layout(self):
        return self._conductor.get_layout()
    
    def close_screen(self, event):
        widget = self._screen_widgets[event.screen_id]
        self.save_screen_location(event.screen_id,event.loc)
        widget.setChecked(False)

    def set_screen_map_widget(self, id:ScreenIdentifier, widget):
        self._screen_widgets[id] = widget
    
    def image_tools(self, tool:ImageToolsEnum):
        self._conductor.image_tools(tool)

    def draw_screen_rect(self, event:ScreenMouseEvent):
        self.draw_screen_rect(event.screen_id,event.start_pos,event.end_pos)
    
    def draw_screen_rect(self,id, start, end):
        self._conductor.draw_screen_rect(id, start, end)

    def clear_screen_rect(self):
        self._conductor.clear_screen_rect()

    def report(self,results:List[CarbinReport]):
        times = list(map(lambda x:x.time,results))
        self._conductor.report("Behavior",times, list(map(lambda x:x.speed,results)))
        self._conductor.report("Ratio",times,list(map(lambda x:x.ratio,results)))
        self._conductor.report("Trajectory",list(map(lambda x:x.trajectory.x,results)),list(map(lambda x:x.trajectory.y,results)))
        
    def show_status_message(self, message):
        status_bar = self._parent.statusBar()
        status_bar.showMessage(message)

    def save_screen_location(self,screen_id, loc):
        locations = self._context_service.ui.locations
        locations[screen_id] = loc
