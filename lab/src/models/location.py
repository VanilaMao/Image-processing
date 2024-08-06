from dataclasses import dataclass


@dataclass
class Point:
    x:int = 0
    y:int = 0

@dataclass
class Rect:
    x:int =0
    y:int =0
    width:int =0
    height:int =0