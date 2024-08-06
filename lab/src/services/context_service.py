from dataclasses import dataclass
from typing import Any, Dict
from processes.process import ImageProcess
from processes.process_config import ProcessConfig
from qtpy.QtWidgets import QWidget


@dataclass
class Context:
    fileName:str
    process:ImageProcess
    config:ProcessConfig
    widgets:Dict[str,QWidget]

class ContextService:
    def __init__(self) -> None:
        self._context = Context(None, None, ProcessConfig(0,255,50,255,500,50),{})

    def __setattr__(self, name: str, value: Any) -> None:
        if name == "fileName":
            self._context.fileName = value
        elif name == "process":
            self._context.process = value
        elif name == "config":
            self._context.config = value
        elif name == "widgets":
            self._context.widgets = value
        else:
            super(ContextService, self).__setattr__(name, value)

    def __getattr__ (self, name):
        return self._context.__getattribute__(name)
    
    def update_config(self):
        if self._context.process is not None:
            self._context.process.update()
        