# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'adjust.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QHBoxLayout, QLabel, QPushButton,
    QSizePolicy, QSpacerItem, QVBoxLayout, QWidget)

class Ui_widget(object):
    def setupUi(self, widget):
        if not widget.objectName():
            widget.setObjectName(u"widget")
        widget.resize(770, 602)
        self.verticalLayout_2 = QVBoxLayout(widget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.image = QLabel(widget)
        self.image.setObjectName(u"image")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.image.sizePolicy().hasHeightForWidth())
        self.image.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.image)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.left = QPushButton(widget)
        self.left.setObjectName(u"left")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.left.sizePolicy().hasHeightForWidth())
        self.left.setSizePolicy(sizePolicy1)

        self.verticalLayout.addWidget(self.left)

        self.right = QPushButton(widget)
        self.right.setObjectName(u"right")
        sizePolicy1.setHeightForWidth(self.right.sizePolicy().hasHeightForWidth())
        self.right.setSizePolicy(sizePolicy1)

        self.verticalLayout.addWidget(self.right)

        self.up = QPushButton(widget)
        self.up.setObjectName(u"up")
        sizePolicy1.setHeightForWidth(self.up.sizePolicy().hasHeightForWidth())
        self.up.setSizePolicy(sizePolicy1)

        self.verticalLayout.addWidget(self.up)

        self.down = QPushButton(widget)
        self.down.setObjectName(u"down")
        sizePolicy1.setHeightForWidth(self.down.sizePolicy().hasHeightForWidth())
        self.down.setSizePolicy(sizePolicy1)

        self.verticalLayout.addWidget(self.down)

        self.redo = QPushButton(widget)
        self.redo.setObjectName(u"redo")
        sizePolicy1.setHeightForWidth(self.redo.sizePolicy().hasHeightForWidth())
        self.redo.setSizePolicy(sizePolicy1)

        self.verticalLayout.addWidget(self.redo)

        self.undo = QPushButton(widget)
        self.undo.setObjectName(u"undo")
        sizePolicy1.setHeightForWidth(self.undo.sizePolicy().hasHeightForWidth())
        self.undo.setSizePolicy(sizePolicy1)

        self.verticalLayout.addWidget(self.undo)

        self.reset = QPushButton(widget)
        self.reset.setObjectName(u"reset")
        sizePolicy1.setHeightForWidth(self.reset.sizePolicy().hasHeightForWidth())
        self.reset.setSizePolicy(sizePolicy1)

        self.verticalLayout.addWidget(self.reset)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.verticalLayout.addItem(self.verticalSpacer)


        self.horizontalLayout.addLayout(self.verticalLayout)


        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.label = QLabel(widget)
        self.label.setObjectName(u"label")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy2)
        self.label.setMinimumSize(QSize(200, 40))
        self.label.setMaximumSize(QSize(16777215, 60))

        self.verticalLayout_2.addWidget(self.label)


        self.retranslateUi(widget)

        QMetaObject.connectSlotsByName(widget)
    # setupUi

    def retranslateUi(self, widget):
        widget.setWindowTitle(QCoreApplication.translate("widget", u"Widget", None))
        self.image.setText("")
        self.left.setText(QCoreApplication.translate("widget", u"Left", None))
        self.right.setText(QCoreApplication.translate("widget", u"Right", None))
        self.up.setText(QCoreApplication.translate("widget", u"Up", None))
        self.down.setText(QCoreApplication.translate("widget", u"Down", None))
        self.redo.setText(QCoreApplication.translate("widget", u"Redo", None))
        self.undo.setText(QCoreApplication.translate("widget", u"Undo", None))
        self.reset.setText(QCoreApplication.translate("widget", u"Restart", None))
        self.label.setText(QCoreApplication.translate("widget", u"TextLabel", None))
    # retranslateUi

