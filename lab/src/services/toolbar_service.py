from typing import Dict, List
from gui.image_tools import ImageToolsEnum
from injector import inject, singleton
from qtpy.QtCore import Signal, QObject
from qtpy.QtWidgets import QWidget
from services.context_service import ContextService

@singleton
class ToolbarService(QObject):
    max_changed= Signal(int)
    min_changed= Signal(int)
    process_start=Signal(int)
    process_end=Signal(int)
    leftmax_changed=Signal(int)
    leftmin_changed=Signal(int)
    rightmax_changed=Signal(int)
    rightmin_changed=Signal(int)
    background_changed= Signal(int)
    config_set:Dict[str,callable]={
        "LeftMin": lambda config,value: setattr(config,"left_min", value),
        "LeftMax": lambda config,value: setattr(config,"left_max", value),
        "RightMin": lambda config,value: setattr(config,"right_min", value), 
        "RightMax": lambda config,value: setattr(config,"right_max", value), 
        "Max": lambda config,value: setattr(config,"particle_size_max", value), 
        "Min": lambda config,value: setattr(config,"particle_size_min", value), 
        "Start": lambda config,value: setattr(config,"start", value), 
        "End": lambda config,value: setattr(config,"end", value),
        "Background":lambda config,value: setattr(config,"background", value),
        "Second": lambda config,value: setattr(config,"first_second_shift", value),
        # "Max": lambda config,value: setattr(config,"first_second_shift", value),
    }
       
    starting_disable_list=["EndProcess","Skip","Next","StartProcess","Adjustment"] #they should be disbaled when process is not starting
    
    @inject
    def __init__(self, context_service:ContextService) -> None:
        super().__init__() 
        self._context_service = context_service
        self._slot_dict = {
            "Max": lambda : self.max_changed,
            "Min": lambda:  self.min_changed,
            "Start": lambda:  self.process_start,
            "End": lambda:  self.process_end,
            "LeftMin":lambda:  self.leftmin_changed,
            "LeftMax":lambda:  self.leftmax_changed,
            "RightMax":lambda:  self.rightmax_changed,
            "RightMin":lambda:  self.rightmin_changed,
            "Background":lambda:  self.background_changed,
        }
        self.config_widgets ={}

    def update_to_ui(self, value, element):
        signal= self._slot_dict[element]
        signal().emit(value)

    def update_to_ui(self, dict:Dict[str,int]):
        for element in dict:
            signal= self._slot_dict[element]
            signal().emit(dict[element])

    def add_signal_connect(self,element, widget, slot:callable):
        self.config_widgets[element] = widget
        signal= self._slot_dict[element]
        signal().connect(slot)

    def update_config(self, element, value):
        print(f"{element}|{value}")
        config = self._context_service.config
        if isinstance(value, str):
            value = int(value)
        self.config_set[element](config, int(value))
        self._context_service.update_config()
        
        # TODO define __call__ function in processconfig class instead

    def disable(self, element:str):
        widget:QWidget = self._context_service.widgets[element]
        widget.setEnabled(False)

    def disable_elements(self, elements:List[str]):
        for element in elements:
            self.disable(element)

    def enable(self, element:str):
        widget:QWidget = self._context_service.widgets[element]
        widget.setEnabled(True)

    def enable_elements(self, elements:List[str]):
        for element in elements:
            self.enable(element)

    def init(self):
        self.disable_elements(self.starting_disable_list)
        config = self._context_service.config
        self.update_to_ui({
                      "LeftMax":config.left_max,
                      "LeftMin":config.left_min,
                      "RightMin":config.right_min,
                      "RightMax": config.right_max,
                      "Min": config.particle_size_min,
                      "Max": config.particle_size_max,
                      "Background": config.background
                      })