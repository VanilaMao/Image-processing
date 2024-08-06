# https://stackoverflow.com/questions/34135624/how-to-properly-execute-gui-operations-in-qt-main-thread
from dataclasses import dataclass
from enum import Enum
from qtpy import QtCore
from models.location import Point
from screen.screen_identifier import ScreenIdentifier

class ScreenEventEnum(Enum):
    close = 1
    select = 2
    open = 3

@dataclass
class ScreenEvent:
    event_type:ScreenEventEnum = None
    screen_id:ScreenIdentifier= None

@dataclass
class ScreenMouseEvent(ScreenEvent):
    start_pos: Point = None
    end_pos:Point = None

# @functools.lru_cache()
class ScreenEventSub(QtCore.QObject):
    def __init__(self):
        super().__init__()
        self._events = {}

    def addEventListener(self, event_type: ScreenEventEnum, func):
        if event_type not in self._events:
            self._events[event_type] = [func]
        else:
            self._events[event_type].append(func)

    def dispatchEvent(self, event: ScreenEvent):
        functions = self._events.get(event.event_type, [])
        for func in functions:
            QtCore.QTimer.singleShot(0, lambda: func(event))
