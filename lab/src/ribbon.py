import functools
from typing import Dict
from pyqtribbon.panel import RibbonPanel
from qtpy import QtWidgets
from di.di import DI
from services.context_service import ContextService

def initializer(widget: QtWidgets, *args, **kwargs):
    if isinstance(widget, QtWidgets.QLabel) or isinstance(widget, QtWidgets.QCheckBox):
        widget.setText(*args)
    if isinstance(widget, QtWidgets.QCheckBox):
        slot = kwargs.pop("slot", None)
        if slot:
            widget.stateChanged.connect(slot(widget))
    if isinstance(widget,QtWidgets.QLineEdit):
        slot = kwargs.pop("slot", None)
        if slot:
            slot(widget)


def addWidgetsBy(self, data: Dict[str, Dict]) -> Dict[str, QtWidgets.QWidget]:
    widgets = {}  # type: Dict[str, QtWidgets.QWidget]
    for key, widget_data in data.items():
        name = widget_data.pop("type", "")  # type: str
        type = name[0].upper() + name[1:]
        if hasattr(self, "add" + type):
            method = getattr(self, "add" + type)  # type: Callable
            if method is not None:
                args = widget_data.get("args", None)
                if args is not None:
                    widgets[key] = method(
                        args,
                        **widget_data.get("arguments", {}),
                        initializer=initializer
                    )
                else:
                    widgets[key] = method(**widget_data.get("arguments", {}))
    ctx = DI.get_di_instance().get(ContextService)
    ctx.widgets.update(widgets)
    return widgets


class LabRibbon:
    def __init__(self) -> None:
        pass

    @staticmethod
    def patch_panel_addWidgetsBy():  # addWidgetsBy(self, data: Dict[str, Dict]) -> Dict[str, QtWidgets.QWidget]:
        RibbonPanel.addWidgetsBy = addWidgetsBy
        RibbonPanel.addCheckBox = functools.partialmethod(
            RibbonPanel._addAnyWidget,
            cls=QtWidgets.QCheckBox,
            initializer=QtWidgets.QCheckBox.setText,
        )
        RibbonPanel.addLineEdit = functools.partialmethod(
            RibbonPanel._addAnyWidget,
            cls=QtWidgets.QLineEdit,
            initializer = initializer
        )
