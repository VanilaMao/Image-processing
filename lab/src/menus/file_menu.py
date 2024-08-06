from pyqtribbon import RibbonCategoryStyle, RibbonButtonStyle
from qtpy.QtGui import QIcon
from qtpy.QtCore import Qt
from icons.constants import *
from actions.file_actions import *
from icons.icon_utilities import *
file_menu = lambda :  {
            "File": {
                "style": RibbonCategoryStyle.Normal,
                "panels": {
                    "Load": {
                        "showPanelOptionButton": True,
                        "widgets": {
                            "Open": {
                                "type": "Button",
                                "arguments": {
                                    "icon":   QIcon(open_icon),
                                    "text": "Open",
                                    "tooltip": "Open a worm file",
                                    "rowSpan": RibbonButtonStyle.Large,
                                    "colSpan": 2,
                                    "slot": lambda: open_file()
                                },
                            },
                            "ReOpen": {
                                "type": "Button",
                                "arguments": {
                                    "icon":  QIcon(reopen_icon),
                                    "text": "ReOpen",
                                    "tooltip": "Open a worm file",
                                    "rowSpan": RibbonButtonStyle.Medium,
                                    "colSpan": 1,
                                    "alignment": Qt.AlignmentFlag.AlignLeft
                                },
                            },
                            "Close": {
                                "type": "Button",
                                "arguments": {
                                    "icon":  QIcon(close_icon),
                                    "text": "Close",
                                    "tooltip": "Open a worm file",
                                    "rowSpan": RibbonButtonStyle.Medium,
                                    "colSpan": 1,
                                    "alignment": Qt.AlignmentFlag.AlignLeft
                                },
                            },
                        },
                    },
                    "Image Adjustment": {
                        "showPanelOptionButton": True,
                        "widgets": {
                            "Left": {
                                "type": "Button",
                                "arguments": {
                                    "icon":  QIcon(left_icon),
                                    "text": "Move Left ",
                                    "rowSpan": RibbonButtonStyle.Medium,
                                    "tooltip": "Open a worm file",
                                    "alignment": Qt.AlignmentFlag.AlignLeft
                                },
                            },
                            "Right": {
                                "type": "Button",
                                "arguments": {
                                    "icon":  QIcon(right_icon),
                                    "text": "Move Right",
                                    "tooltip": "Open a worm file",
                                    "rowSpan": RibbonButtonStyle.Medium,
                                    "alignment": Qt.AlignmentFlag.AlignLeft
                                },
                            },
                            "Up": {
                                "type": "Button",
                                "arguments": {
                                    "icon":  QIcon(up_icon),
                                    "text": "Move Up",
                                    "rowSpan": RibbonButtonStyle.Medium,
                                    "tooltip": "Open a worm file",
                                    "alignment": Qt.AlignmentFlag.AlignLeft
                                },
                            },
                            "Down": {
                                "type": "Button",
                                "arguments": {
                                    "icon":  QIcon(down_icon),
                                    "text": "Move Down",
                                    "tooltip": "Open a worm file",
                                    "rowSpan": RibbonButtonStyle.Medium,
                                    "alignment": Qt.AlignmentFlag.AlignLeft
                                },
                                
                            },
                            "Preview": {
                                "type": "Button",
                                "arguments": {
                                    "icon":  QIcon(preview_icon),
                                    "text": "preview",
                                    "tooltip": "Open a worm file",
                                    "rowSpan": RibbonButtonStyle.Medium,
                                    "alignment": Qt.AlignmentFlag.AlignLeft
                                },
                                
                            },
                            "Adjustment": {
                                "type": "Button",
                                "arguments": {
                                    "icon":  QIcon(adjustment_icon),
                                    "text": "Adjust",
                                    "slot": lambda: adjust_carbin(),
                                    "tooltip": "Open a worm file",
                                    "rowSpan": RibbonButtonStyle.Medium,
                                    "alignment": Qt.AlignmentFlag.AlignLeft
                                },
                                
                            },
                        },
                    },
                    "Video Play": {
                        "showPanelOptionButton": True,
                        "widgets": {
                            "play": {
                                "type": "Button",
                                "arguments": {
                                    "icon":  QIcon(play_icon),
                                    "text": "Play",
                                    "rowSpan": RibbonButtonStyle.Small,
                                    "tooltip": "Open a worm file",
                                    "alignment": Qt.AlignmentFlag.AlignLeft
                                },
                            },
                            "pause": {
                                "type": "Button",
                                "arguments": {
                                    "icon":  QIcon(pause_icon),
                                    "text": "Pause",
                                    "rowSpan": RibbonButtonStyle.Small,
                                    "tooltip": "Open a worm file",
                                    "alignment": Qt.AlignmentFlag.AlignLeft
                                },
                            },
                            "stop": {
                                "type": "Button",
                                "arguments": {
                                    "icon":  QIcon(stop_icon),
                                    "text": "Stop",
                                    "rowSpan": RibbonButtonStyle.Small,
                                    "tooltip": "Open a worm file",
                                    "alignment": Qt.AlignmentFlag.AlignLeft
                                },
                            },
                        }
                     }
                },
            }
        }