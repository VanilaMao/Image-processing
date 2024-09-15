import datetime
import math
import os
from typing import List
from image_processing.image_processing import ImageProcessing
import numpy as np
from processes.process import ImageProcess
from services.document_service import DocType, DocumentService
from services.screen_service import *
from models.worm import *
from di.di import DI
from processes.process_config import ProcessConfig
from services.dialog_service import DialogService, DialogType
from gui.utilities import process_ui_event

# https://forum.qt.io/topic/134970/how-to-schedule-a-function-to-run-on-the-main-ui-thread/3 
# https://stackoverflow.com/questions/6208339/qt-correct-way-to-post-events-to-a-qthread
# https://stackoverflow.com/questions/6061352/creating-a-custom-message-event-with-qt
# https://stackoverflow.com/questions/77116363/performing-bidirectional-signals-in-qthreads
# https://forum.qt.io/topic/120262/how-can-i-queue-a-function-to-be-executed-in-the-main-thread-with-as-high-priority-as-possible/2
# https://wiki.qt.io/Threads_Events_QObjects#:~:text=We%20can%20use%20the%20thread,has%20a%20running%20event%20loop.
# https://stackoverflow.com/questions/49542608/qt-postevent-and-event-filter
# https://stackoverflow.com/questions/17658811/how-do-i-process-events-on-a-qthread
# may bring into a Qthread worker thread to handle processing

def load_carbin_img(file):
    img = ImageProcessing.load_file(file)  # "icons/0442.tif"
    left, right = ImageProcessing.split_image(img)
    return left, right


class CarbinProcess(ImageProcess):
    timestamp = None
    def __init__(self, total_frames, carbin_dir, file, config:ProcessConfig, doc_service:DocumentService= None) -> None:
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
        self._auto_process= False
        self._stop_ui_action:callable= None
        self._auto_ui_action:callable= None
        self._document_service = doc_service
        self._save_file = None

    @property
    def first_carbin(self): 
        return self._current_carbin
    
    def index_carbin(self, index):
        return self._carbins[index]

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
        sc.open_screen(ScreenIdentifier.LEFTRAW, lambda: ImageProcessing.cv_to_qimage(self._carbins[0].left),True, force=True)
        sc.open_screen(ScreenIdentifier.RIGHTRAW, lambda: ImageProcessing.cv_to_qimage(self._carbins[0].right),True, force=True)
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
        sc.open_screen(ScreenIdentifier.LEFTRAW, lambda: ImageProcessing.cv_to_qimage(left_unit8,'uint8'))
        sc.open_screen(ScreenIdentifier.RIGHTRAW, lambda: ImageProcessing.cv_to_qimage(right_unit8,'uint8'))
        sc.open_screen(ScreenIdentifier.LEFT, lambda: ImageProcessing.cv_to_qimage(left_unit8_binary,'uint8'))
        sc.open_screen(ScreenIdentifier.RIGHT, lambda: ImageProcessing.cv_to_qimage(right_unit8_binary,'uint8'))
        sc.open_screen(ScreenIdentifier.BINARY, lambda: ImageProcessing.cv_to_qimage(left_right_common_binary,'uint8'))

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

    def process(self,stop_action:callable = None,auto_action:callable = None):
        self._stop_ui_action = stop_action
        self._auto_ui_action = auto_action
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
            return False
        self.generate_reports()

        self._prev_processed_carbin_frame = self._current_carbin_frame
        self.process_next_carbin()
        return True
        
    def skip(self):
        # Save report even the carbin is skipped and not processed
        self._current_carbin.worm.cells.clear() # disgard any processing
        self.generate_reports(False)
        self._prev_processed_carbin_frame = self._current_carbin_frame

        self._total_skipped +=1
        self.process_next_carbin()

    def process_next_carbin(self):
         # alreay reach the end
        if self._current_carbin_frame>=min(self._process_config.end, self._total_expected_carbins):
            self.stop()
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
        self._auto_process = False
        self._total_skipped = 0
        self._save_file = None
        if self._stop_ui_action is not None:
            self._stop_ui_action()
        

    def update(self):
        auto_process = self._process_config.auto_process_image
        if not auto_process and self._auto_process:   # stop the auto process
            self._auto_process = False
            return
        elif auto_process and not self._auto_process:  #start the auto process
            self._auto_process = True
            self.auto_process() 
        elif auto_process and self._auto_process: #some other config setting when auto process is running
            return
        else:
            self.process_carbin()
    
    def auto_process(self):
        for _ in range(self._current_carbin_frame,int(min(self._process_config.end, self._total_expected_carbins))+1):
            if not self._auto_process: #stop auto process
                return
            if not self.next():
                self._auto_process = False
                self._auto_ui_action(False)
                return
            process_ui_event() #give an chance to response the auto process disabling


    def generate_reports(self, cal_ratio = True):
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

        if cal_ratio: 
            left_mean, right_mean,_ = carbin.worm.cells[0].mean_density
            report = CarbinReport(speed,carbin.time,right_mean/left_mean,carbin.worm.track)
            self._carbin_reports.append(report)
            DI.get_di_instance().get(ScreenService).report(self._carbin_reports)
        else:
            report = CarbinReport(speed,carbin.time,-1.0,carbin.worm.track)
        self.save_report(report,carbin)
        

    def save_report(self, report:CarbinReport, carbin:Carbin):
        @dataclass
        class ReportData:
            report:CarbinReport = None
            carbin:Carbin = None
            file:str = None
        if len(self._carbin_reports) > 0:
            if self._save_file is None:
                self._save_file = f"{self._dir}/{self._file}(Frame{int(self._process_config.start)}-{int(self._process_config.end)})-{self.timestamp}"
            self._document_service.save(DocType.Excel,ReportData(report,carbin,self._save_file))
        
