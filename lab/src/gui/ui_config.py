from dataclasses import dataclass
from models.location import Rect
from screen.screen_identifier import ScreenIdentifier


@dataclass
class UiConfig:
    locations:dict[ScreenIdentifier, Rect]