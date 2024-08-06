from dataclasses import dataclass
from typing import List

from models.location import *

@dataclass
class Margin:
    right:int =0  #positive move right
    bottom: int =0 #postitive move down

@dataclass
class Cell:
    rect:Rect= None
    second:bool= False
    mean_density:tuple = None
    centroid:Point= None


class Worm:
    def __init__(self,track:Point) -> None:
        self._cells:List[Cell] = []      #(x.y.width,height)
        self._track:Point= track #x,y in the microscope
        self._motion_x = 300
        self._motion_y = 600

    @property
    def cells(self):
        return self._cells
    
    # dTempX[iTempIndex] = dTempX[iTempIndex] - (thisCentroid.x - iTempImageX/2);	   //
	# dTempY[iTempIndex] = dTempY[iTempIndex] - (thisCentroid.y - iTempImageY/2);
    @property
    def track(self):
        if len(self.cells)>0:
            cell = self.cells[0]
            x= self._track.x - (cell.centroid.x-self._motion_x)
            y= self._track.y - (cell.centroid.y-self._motion_y)
            return Point(x,y)
        return self._track
    
    def set_motion_xy(self, x,y):
        self._motion_x = x/2
        self._motion_y = y/2

class Carbin:
    right_margin:Margin = None
    def __init__(self, worm:Worm,time, file, left_img:callable, right_img:callable) -> None:  # make img callable to load it when it is really need to save memory
        self._worm :Worm = worm 
        self._time = time
        self._left_img = left_img
        self._right_img = right_img
        self._left = None
        self._right = None
        self._img_file = file
        self._processed = False

    def set_flag(self,status):
        self._processed = status

    @property
    def file(self):
        return self._img_file

    @property
    def status(self):
        return self._processed 

    @property
    def time(self):
        return self._time

    @property
    def worm(self):
        return self._worm

    @property
    def left(self):
        if self._left is None:
            self._left = self._left_img(self._img_file)
            height,width = self._left.shape
            self.worm.set_motion_xy(width,height)
        return self._left
    
    @property
    def right(self):
        if self._right is None:
            self._right = self._right_img(self._img_file)
        return self._right
    
    def clear_cache(self):
        self._left = None
        self._right= None
        self._processed = False

    def update_worm():
        pass

@dataclass   
class CarbinReport:
    speed:float = 0.0
    time:float = 0.0
    ratio:float = 0.0
    trajectory:Point =None


