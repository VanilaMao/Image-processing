from qtpy.QtWidgets import QLineEdit
from icons.constants import *
from actions.file_actions import *
from icons.icon_utilities import *
from di.di import DI
from processes.process_movement import ProcessMovement
from services.toolbar_service import ToolbarService
from services.screen_service import ScreenService
from screen.screen_identifier import ScreenIdentifier
from gui.image_tools import *

def image_tools(tool:ImageToolsEnum):
    sc = DI.get_di_instance().get(ScreenService)
    sc.image_tools(tool)

def checkbox_slot(widget, id: ScreenIdentifier):
    sc = DI.get_di_instance().get(ScreenService)
    sc.set_screen_map_widget(id, widget)
    def check_status(state:int):
        if state == 0:
            sc.hide_screen(id)
        if state == 2:
            sc.open_screen(id)
    return check_status

def linedit_slot(widget:QLineEdit,element:str):
    tb = DI.get_di_instance().get(ToolbarService)
    tb.add_signal_connect(element, widget, lambda value: widget.setText(str(value)))
    widget.returnPressed.connect(lambda :tb.update_config(element, widget.text()))

def toolbutton_slot(check_status,tool:ImageToolsEnum):
    tb = DI.get_di_instance().get(ToolbarService)
    if tool == ImageToolsEnum.Second:
        tb.update_config( "Second", check_status)
    elif tool == ImageToolsEnum.Auto:
        if check_status:
            print("auto_ui set to true from clicking")
            tb.disable_elements(["Skip","Next"])
        else:
            print("auto_ui set to false from clicking")
            tb.enable_elements(["Skip","Next"])
        tb.update_config( "Auto", check_status)       

def process_handle(movement:ProcessMovement, element:str):
    tb = DI.get_di_instance().get(ToolbarService)
    ctx = DI.get_di_instance().get(ContextService)
    sc = DI.get_di_instance().get(ScreenService)
    process:CarbinProcess = ctx.process
    if movement == ProcessMovement.Start:
        tb.disable_elements([element,"Start","End","Adjustment"])
        tb.enable_elements(["EndProcess","Auto","Skip","Next"])
        process.process(lambda:stop_ui(tb,sc),lambda status: auto_ui(tb, False))
    elif movement == ProcessMovement.Stop:
        process.stop()
    elif movement == ProcessMovement.Skip:
        process.skip()
    elif movement == ProcessMovement.Next:
        process.next()

def auto_ui(tb, status):
    tb.check_element("Auto",status)
    print("auto_ui")
    tb.enable_elements(["Skip","Next"])

def stop_ui(tb, sc):
    tb.disable_elements(["EndProcess","Auto","Skip","Next"])
    tb.enable_elements(["StartProcess","Start", "End","Adjustment"])
    tb.check_element("Auto",False)
    sc.show_status_message("Ready")