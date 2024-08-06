from pyqtribbon import RibbonCategoryStyle, RibbonButtonStyle
from qtpy.QtGui import QIcon
from qtpy.QtCore import Qt
from icons.constants import *
from actions.file_actions import *
from icons.icon_utilities import *
from screen.screen_identifier import ScreenIdentifier
from gui.image_tools import *
from actions.process_actions import *

process_menu = lambda :  {
            "Process": {
                "style": RibbonCategoryStyle.Normal,
                "panels": {
                    "Threshold": {
                        "showPanelOptionButton": True,
                        "widgets": {
                            "LeftMax": {
                                "type": "LineEdit",
                                "arguments": {
                                    "tooltip": "Open a worm file",
                                    "slot": lambda widget: linedit_slot(widget,"LeftMax"),
                                    "rowSpan": RibbonButtonStyle.Medium,
                                    "alignment": Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignBottom,
                                },
                            },
                            "LeftMin": {
                                "type": "LineEdit",
                                "arguments": {
                                    "tooltip": "Open a worm file",
                                    "slot": lambda widget: linedit_slot(widget,"LeftMin"),
                                    "rowSpan": RibbonButtonStyle.Medium,
                                    "alignment": Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignBottom,
                                },
                            },
                             "LeftMaxLabel": {
                                "type": "Label",
                                "args": "Left Max",
                                "arguments": {
                                    "tooltip": "Open a worm file",
                                    "rowSpan": RibbonButtonStyle.Medium,
                                    "alignment": Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignBottom,
                                },
                            },
                            "LeftMinLabel": {
                                "type": "Label",
                                "args": "Left Min",
                                "arguments": {
                                    "tooltip": "Open a worm file",
                                    "rowSpan": RibbonButtonStyle.Medium,
                                    "alignment": Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignBottom,
                                },
                            },
                            "MarginLeft": {
                                "type": "Label",
                                "args": "     ",
                                "arguments": {
                                    "rowSpan": RibbonButtonStyle.Large
                                },
                            },
                            "RightMax": {
                                "type": "LineEdit",
                                "arguments": {
                                    "tooltip": "Open a worm file",
                                    "slot": lambda widget: linedit_slot(widget,"RightMax"),
                                    "rowSpan": RibbonButtonStyle.Medium,
                                    "alignment": Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignBottom,
                                },
                            },
                            "RightMin": {
                                "type": "LineEdit",
                                "arguments": {
                                    "tooltip": "Open a worm file",
                                    "slot": lambda widget: linedit_slot(widget,"RightMin"),
                                    "rowSpan": RibbonButtonStyle.Medium,
                                    "alignment": Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignBottom,
                                },
                            },
                             "RightMaxLabel": {
                                "type": "Label",
                                "args": "Right Max",
                                "arguments": {
                                    "tooltip": "Open a worm file",
                                    "rowSpan": RibbonButtonStyle.Medium,
                                    "alignment": Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignBottom,
                                },
                            },
                            "RightMinLabel": {
                                "type": "Label",
                                "args": "Right Min",
                                "arguments": {
                                    "tooltip": "Open a worm file",
                                    "rowSpan": RibbonButtonStyle.Medium,
                                    "alignment": Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignBottom,
                                },
                            },
                        },
                    },
                    "Process Filters": {
                        "showPanelOptionButton": True,
                        "widgets": {
                            "Max": {
                                "type": "LineEdit",
                                "arguments": {
                                    "tooltip": "Open a worm file",
                                    "slot": lambda widget: linedit_slot(widget,"Max"),
                                    "rowSpan": RibbonButtonStyle.Small,
                                    "alignment": Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignBottom,
                                },
                            },
                            "Min": {
                                "type": "LineEdit",
                                "arguments": {
                                    "tooltip": "Open a worm file",
                                    "slot": lambda widget: linedit_slot(widget,"Min"),
                                    "rowSpan": RibbonButtonStyle.Small,
                                    "alignment": Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignBottom,
                                },
                            },
                            "Background": {
                                "type": "LineEdit",
                                "arguments": {
                                    "tooltip": "Open a worm file",
                                    "slot": lambda widget: linedit_slot(widget,"Background"),
                                    "rowSpan": RibbonButtonStyle.Small,
                                    "alignment": Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignBottom,
                                },
                            },
                            "MaxLabel": {
                                "type": "Label",
                                "args": "Max",
                                "arguments": {
                                    "tooltip": "Open a worm file",
                                    "rowSpan": RibbonButtonStyle.Small,
                                    "alignment": Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignBottom,
                                },
                            },
                            "MinLabel": {
                                "type": "Label",
                                "args": "Min",
                                "arguments": {
                                    "tooltip": "Open a worm file",
                                    "rowSpan": RibbonButtonStyle.Small,
                                    "alignment": Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignBottom,
                                },
                            },
                            "BackgroundLabel": {
                                "type": "Label",
                                "args": "Background",
                                "arguments": {
                                    "tooltip": "Open a worm file",
                                    "rowSpan": RibbonButtonStyle.Small,
                                    "alignment": Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignBottom,
                                },
                            },
                             "Second": {
                                "type": "Button",
                                 "arguments": {
                                    "icon":  QIcon(second_icon),
                                    "slot": lambda status: toolbutton_slot(status, ImageToolsEnum.Second),
                                    "text": "Second",
                                    "checkable": True,
                                    "tooltip": "Open a worm file",
                                    "rowSpan": RibbonButtonStyle.Large,
                                    "alignment": Qt.AlignmentFlag.AlignLeft
                                },
                            },
                        },
                    },
                    "Display Choices": {
                        "showPanelOptionButton": True,
                        "widgets": {
                            "LeftRawImage": {
                                "type": "CheckBox",
                                "args": "Left Raw",
                                "arguments": {
                                    "slot": lambda widget: checkbox_slot(widget, ScreenIdentifier.LEFTRAW), 
                                    "checkable": True,
                                    "tooltip": "Open a worm file",
                                    "rowSpan": RibbonButtonStyle.Small,
                                    "alignment": Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignBottom,
                                },
                            },
                            "LeftImage": {
                                "type": "CheckBox",
                                "args": "Left",
                                "arguments": {
                                    "slot": lambda widget: checkbox_slot(widget,ScreenIdentifier.LEFT), 
                                    "checkable": True,
                                    "tooltip": "Open a worm file",
                                    "rowSpan": RibbonButtonStyle.Small,
                                    "alignment": Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignBottom,
                                },
                            },
                            "RightRawImage": {
                                "type": "CheckBox",
                                "args": "Right Raw",
                                "arguments": {
                                    "slot": lambda widget: checkbox_slot(widget, ScreenIdentifier.RIGHTRAW), 
                                    "checkable": True,
                                    "tooltip": "Open a worm file",
                                    "rowSpan": RibbonButtonStyle.Small,
                                    "alignment": Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignBottom,
                                },
                            },
                            "RightImage": {
                                "type": "CheckBox",
                                "args": "Right",
                                "arguments": {
                                    "slot": lambda widget: checkbox_slot(widget, ScreenIdentifier.RIGHT), 
                                    "checkable": True,
                                    "tooltip": "Open a worm file",
                                    "rowSpan": RibbonButtonStyle.Small,
                                    "alignment": Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignBottom,
                                },
                            },
                            "BinaryImage": {
                                "type": "CheckBox",
                                "args": "Binary",
                                "arguments": {
                                    "slot": lambda widget: checkbox_slot(widget, ScreenIdentifier.BINARY), 
                                    "checkable": True,
                                    "tooltip": "Open a worm file",
                                    "rowSpan": RibbonButtonStyle.Small,
                                    "alignment": Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignBottom,
                                },
                            },
                        },
                    },
                    "Image Tools": {
                        "showPanelOptionButton": True,
                        "widgets": {
                            "Select": {
                                "type": "Button",
                                "arguments": {
                                    "icon":  QIcon(cursor_selection_icon),
                                    "slot": lambda: image_tools(ImageToolsEnum.Select),
                                    "text": "Select",
                                    "checkable": True,
                                    "tooltip": "Open a worm file",
                                    "rowSpan": RibbonButtonStyle.Small,
                                    "alignment": Qt.AlignmentFlag.AlignLeft
                                },
                            },
                            "ZoomIn": {
                                "type": "Button",
                                "arguments": {
                                    "icon":  QIcon(zoom_in_icon),
                                    "slot": lambda: image_tools(ImageToolsEnum.Select),
                                    "text": "Zoom In",
                                    "checkable": True,
                                    "tooltip": "Open a worm file",
                                    "rowSpan": RibbonButtonStyle.Small,
                                    "alignment": Qt.AlignmentFlag.AlignLeft
                                },
                            },
                            "ZoomOut": {
                                "type": "Button",
                                "arguments": {
                                    "icon":  QIcon(zoom_out_icon),
                                    "slot": lambda: image_tools(ImageToolsEnum.Select),
                                    "text": "Zoom Out",
                                    "checkable": True,
                                    "tooltip": "Open a worm file",
                                    "rowSpan": RibbonButtonStyle.Small,
                                    "alignment": Qt.AlignmentFlag.AlignLeft
                                },
                            },                      
                        },
                    },
                    "Processing": {
                        "showPanelOptionButton": True,
                        "widgets": {
                            "Start": {
                                "type": "LineEdit",
                                "arguments": {
                                    "tooltip": "Open a worm file",
                                    "slot": lambda widget: linedit_slot(widget,"Start"),
                                    "rowSpan": RibbonButtonStyle.Medium,
                                    "alignment": Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignBottom,
                                },
                            },
                            "End": {
                                "type": "LineEdit",
                                "arguments": {
                                    "tooltip": "Open a worm file",
                                    "slot": lambda widget: linedit_slot(widget,"End"),
                                    "rowSpan": RibbonButtonStyle.Medium,
                                    "alignment": Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignBottom,
                                },
                            },
                            "StartLabel": {
                                "type": "Label",
                                "args": "Start",
                                "arguments": {
                                    "tooltip": "Open a worm file",
                                    "rowSpan": RibbonButtonStyle.Medium,
                                    "alignment": Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignBottom,
                                },
                            },
                            "EndLabel": {
                                "type": "Label",
                                "args": "End",
                                "arguments": {
                                    "tooltip": "Open a worm file",
                                    "rowSpan": RibbonButtonStyle.Medium,
                                    "alignment": Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignBottom,
                                },
                            },
                            "MarginLeft": {
                                "type": "Label",
                                "args": "     ",
                                "arguments": {
                                    "rowSpan": RibbonButtonStyle.Large
                                },
                            },
                            "EndProcess": {
                                "type": "Button",
                                "arguments": {
                                    "icon":   QIcon(end_icon),
                                    "tooltip": "Open a worm file",
                                    "rowSpan": RibbonButtonStyle.Small,
                                    "alignment": Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignBottom,
                                    "slot": lambda: process_handle(ProcessMovement.Stop,"EndProcess")
                                },
                            },
                            "Skip": {
                                "type": "Button",
                                "arguments": {
                                    "icon":   QIcon(skip_icon),
                                    "tooltip": "Open a worm file",
                                    "rowSpan": RibbonButtonStyle.Small,
                                    "alignment": Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignBottom,
                                    "slot": lambda: process_handle(ProcessMovement.Skip,"Skip")
                                },
                            },
                            "Next": {
                                "type": "Button",
                                "arguments": {
                                    "icon":   QIcon(next_icon),
                                    "tooltip": "Open a worm file",
                                    "rowSpan": RibbonButtonStyle.Small,
                                    "alignment": Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignBottom,
                                    "slot": lambda: process_handle(ProcessMovement.Next,"Next")
                                },
                            },
                            "StartProcess": {
                                "type": "Button",
                                "arguments": {
                                    "icon":   QIcon(start_icon),
                                    "tooltip": "Open a worm file",
                                    "rowSpan": RibbonButtonStyle.Large,
                                    "alignment": Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignBottom,
                                    "slot": lambda: process_handle(ProcessMovement.Start,"StartProcess")
                                },
                            },
                        },
                    },
                }
            },
        }
        