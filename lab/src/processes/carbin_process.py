import datetime
import math
import os
from typing import List
from image_processing.image_processing import ImageProcessing
import numpy as np
from processes.process import ImageProcess
from services.screen_service import *
from models.worm import *
from di.di import DI
from processes.process_config import ProcessConfig
from services.dialog_service import DialogService, DialogType


def load_carbin_img(file):
    img = ImageProcessing.load_file(file)  # "icons/0442.tif"
    left, right = ImageProcessing.split_image(img)
    return left, right


class CarbinProcess(ImageProcess):
    timestamp = None
    def __init__(self, total_frames, carbin_dir, file, config:ProcessConfig) -> None:
        self._carbins:List[Carbin] = []
        self._carbin_reports:List[CarbinReport]=[]
        self._current_carbin:Carbin = None
        self._prev_processed_carbin_frame = 0
        self._current_carbin_frame = 0
        self._process_config:ProcessConfig = config
        self._total_expected_carbins = total_frames
        self._dir = carbin_dir
        self._file = file
        self._total_skipped =0
        self._process_status = False

    @property
    def first_carbin(self): 
        return self._current_carbin

    def build_carbins(self, carbin_infos):
        line = 0
        for row in carbin_infos:
            file = f"{self._dir}/{line:04}.tif"
            worm = Worm(Point(int(row[1]), int(row[2])))
            carbin = Carbin(worm,row[0]/1000.0,file,lambda f:load_carbin_img(f)[0], lambda f:load_carbin_img(f)[1])
            self._carbins.append(carbin)
            line +=1
        
    def init_open(self):
        sc = DI.get_di_instance().get(ScreenService)
        sc.open_screen(ScreenIdentifier.LEFTRAW, lambda: ImageProcessing.cv_to_qimage(self._carbins[0].left),True)
        sc.open_screen(ScreenIdentifier.RIGHTRAW, lambda: ImageProcessing.cv_to_qimage(self._carbins[0].right),True)
        self._current_carbin = self._carbins[0] # first one
        #starting processing to get rect

        self.process_carbin()

    def process_carbin(self):
        carbin:Carbin = self._current_carbin
        left = np.copy(carbin.left)
        right = np.copy(carbin.right)
        if Carbin.right_margin is not None and (Carbin.right_margin.right!=0 or Carbin.right_margin.bottom!=0):
            right=ImageProcessing.shift_img(right,Carbin.right_margin.bottom,Carbin.right_margin.right)
            
        ImageProcessing.subtract(left,self._process_config.background)
        ImageProcessing.subtract(right,self._process_config.background)
        left_unit8 = ImageProcessing.convert_uint16_to_uint8(left)
        right_unit8 = ImageProcessing.convert_uint16_to_uint8(right)
        left_unit8_binary = ImageProcessing.convert_uint8_to_binary(left_unit8,self._process_config.left_min,self._process_config.left_max)
        right_unit8_binary = ImageProcessing.convert_uint8_to_binary(right_unit8,self._process_config.right_min,self._process_config.right_max)
        left_right_common_binary = ImageProcessing.multiply(left_unit8_binary,right_unit8_binary)

        center, largest_rect = ImageProcessing.detect_blob(left_right_common_binary,
                                                           self._process_config.particle_size_max, 
                                                           self._process_config.particle_size_min,
                                                           self._process_config.first_second_shift)
        
        sc = DI.get_di_instance().get(ScreenService)
        sc.open_screen(ScreenIdentifier.LEFTRAW, lambda: ImageProcessing.cv_to_qimage(left_unit8,'uint8'),True)
        sc.open_screen(ScreenIdentifier.RIGHTRAW, lambda: ImageProcessing.cv_to_qimage(right_unit8,'uint8'),True)
        sc.open_screen(ScreenIdentifier.LEFT, lambda: ImageProcessing.cv_to_qimage(left_unit8_binary,'uint8'),True)
        sc.open_screen(ScreenIdentifier.RIGHT, lambda: ImageProcessing.cv_to_qimage(right_unit8_binary,'uint8'),True)
        sc.open_screen(ScreenIdentifier.BINARY, lambda: ImageProcessing.cv_to_qimage(left_right_common_binary,'uint8'),True)

        if largest_rect is not None:
            sc.draw_screen_rect(None,Point(largest_rect.x,largest_rect.y), Point(largest_rect.x+largest_rect.width,largest_rect.y+largest_rect.height))
            left_mean, right_mean,binary_mean= ImageProcessing.cal_ratios(left,right,left_right_common_binary,largest_rect)
            carbin.worm.cells.clear() #clear previous processed ones
            carbin.worm.cells.append(Cell(largest_rect,self._process_config.first_second_shift,(left_mean,right_mean,binary_mean),center))
            carbin.set_flag(True)
        else:
            sc.clear_screen_rect()
            carbin.set_flag(False)

        sc.show_status_message(f"Current processing Image File:{carbin.file}, Total Skipped:{self._total_skipped}")

    def process(self):
        self.timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        config = self._process_config
        self._process_status = True
        self._current_carbin = self._carbins[config.start]
        self._current_carbin_frame = config.start
        self.process_carbin()

    def next(self):
        if not self._current_carbin.status:
            message = f"the carbin image {self._current_carbin.file} is not prcoessed"
            DialogService("Error!", 400,300,DialogType.Message,message).open()
            return
        self.generate_reports()

        self._prev_processed_carbin_frame = self._current_carbin_frame
        self.process_next_carbin()
        
    def skip(self):
        self._total_skipped +=1
        self.process_next_carbin()

    def process_next_carbin(self):
         # alreay reach the end
        if self._current_carbin_frame>=min(self._process_config.end, self._total_expected_carbins):
            self.Stop()
            return    
        self._current_carbin_frame+=1
        self._current_carbin = self._carbins[self._current_carbin_frame]
        self.process_carbin()

    def stop(self):
        #won't process anything just stop
        for carbin in self._carbins:
            carbin.clear_cache()
        self._current_carbin_frame = 0
        self._current_carbin = self._carbins[self._current_carbin_frame]
        self._prev_processed_carbin_frame= 0 
        self._carbin_reports.clear()
        self._process_status = False
        self._total_skipped = 0
        sc = DI.get_di_instance().get(ScreenService)
        sc.show_status_message("Ready")
        

    def update(self):
        self.process_carbin()

    def generate_reports(self):
        config = self._process_config
        carbin = self._carbins[self._current_carbin_frame]
        speed = 0
        if self._current_carbin_frame != config.start:  #first one
            pre_carbin = self._carbins[self._prev_processed_carbin_frame]
            dx = pre_carbin.worm.track.x
            dy = pre_carbin.worm.track.y
            dx1= carbin.worm.track.x
            dy1 = carbin.worm.track.y
            dtime1 = carbin.time
            dtime = pre_carbin.time
            speed = math.sqrt((dx1-dx)*(dx1-dx)+(dy1-dy)*(dy1-dy))/(dtime1-dtime)
           
        left_mean, right_mean,binary_ratio = carbin.worm.cells[0].mean_density
        report = CarbinReport(speed,carbin.time,right_mean/left_mean,carbin.worm.track)
        self._carbin_reports.append(report)
        DI.get_di_instance().get(ScreenService).report(self._carbin_reports)
        self.save_report(report,carbin)
        

    def save_report(self, report:CarbinReport, carbin:Carbin):
        if len(self._carbin_reports) > 0:
            save_file = f"{self._dir}/{self._file}(Frame{int(self._process_config.start)}-{int(self._process_config.end)})-{self.timestamp}.txt"
            with open(save_file,"a+") as file:
                left_mean,right_mean,binary_mean = carbin.worm.cells[0].mean_density
                file.write(f"{carbin.time:<10.6f}  {binary_mean:<10.6f}   {left_mean:<14.6f}  {right_mean:<14.6f} {report.speed:<14.6f}  {carbin.worm.track.x:<14.6f} {carbin.worm.track.y:<14.6f}\n")
        

        
