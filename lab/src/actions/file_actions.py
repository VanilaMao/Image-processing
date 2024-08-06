from pathlib import Path
from qtpy.QtWidgets  import QFileDialog
from di.di import DI
from processes.carbin_process import *
from services.dialog_service import *
from services.context_service import ContextService
from services.toolbar_service import ToolbarService
def open_file():
    context_service = DI.get_di_instance().get(ContextService)
    fileName = QFileDialog.getOpenFileName(None, "Open Carbin Files", "/home/lab", "Carbin files (*.ftd)")
    context_service.fileName = fileName[0]
    print(context_service.fileName)
    if not context_service.fileName:
        return
    
    total, carbin_infos = ImageProcessing.read_carbin_file(context_service.fileName)
    config:ProcessConfig = context_service.config
    config.start =0  #need to be updated bsed on real file
    config.end =total -1

    dir = Path(context_service.fileName).parents[0]
    file = Path(context_service.fileName).stem
    context_service.process = CarbinProcess(total-1, dir, file, context_service.config)
    context_service.process.build_carbins(carbin_infos)
    Carbin.right_margin = None # adjustment is reset for new file

    tb = DI.get_di_instance().get(ToolbarService)
    tb.update_to_ui({"Start":config.start,"End":config.end})
    context_service.process.init_open()
    tb.enable_elements(["StartProcess","Adjustment"])

def adjust_carbin():
    context_service = DI.get_di_instance().get(ContextService)
    process:CarbinProcess = context_service.process
    carbin = process.first_carbin
    dg = DialogService("Image Adjust", 600, 600, DialogType.AdjustImage, carbin)
    result = dg.open()
    if result is not None:
        right, down = result
        Carbin.right_margin = Margin(right, down)