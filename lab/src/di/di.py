from injector import Injector
from main_module import MainModule

from di.configuration import configure_services, configure_events

class DI:
    _instance = None
    def __init__(self) -> None:
        if self._instance is not None:
            raise Exception(f"{__class__.__name__} is singletonn!")
        else:
            DI._instance = self
            self._di = Injector([configure_services, configure_events, MainModule()])
            
    @staticmethod
    def get_di_instance()->Injector:
        if DI._instance is None:
            DI()
        return DI._instance._di
        