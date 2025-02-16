# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form_indicator.ui'
##
## Created by: Qt User Interface Compiler version 6.8.1
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
from PySide6.QtWidgets import (QApplication, QDialog, QLabel, QPushButton,
    QScrollArea, QSizePolicy, QWidget)

class Ui_Indicator(object):
    def setupUi(self, Indicator):
        if not Indicator.objectName():
            Indicator.setObjectName(u"Indicator")
        Indicator.resize(479, 413)
        self.available_indicators_area = QScrollArea(Indicator)
        self.available_indicators_area.setObjectName(u"available_indicators_area")
        self.available_indicators_area.setGeometry(QRect(10, 30, 211, 211))
        self.available_indicators_area.setWidgetResizable(True)
        self.layerCustomizationWidget = QWidget()
        self.layerCustomizationWidget.setObjectName(u"layerCustomizationWidget")
        self.layerCustomizationWidget.setGeometry(QRect(0, 0, 209, 209))
        self.available_indicators_area.setWidget(self.layerCustomizationWidget)
        self.available_label = QLabel(Indicator)
        self.available_label.setObjectName(u"available_label")
        self.available_label.setGeometry(QRect(12, 10, 51, 16))
        self.current_indicators_area = QScrollArea(Indicator)
        self.current_indicators_area.setObjectName(u"current_indicators_area")
        self.current_indicators_area.setGeometry(QRect(10, 270, 211, 131))
        self.current_indicators_area.setWidgetResizable(True)
        self.layerCustomizationWidget_2 = QWidget()
        self.layerCustomizationWidget_2.setObjectName(u"layerCustomizationWidget_2")
        self.layerCustomizationWidget_2.setGeometry(QRect(0, 0, 209, 129))
        self.current_indicators_area.setWidget(self.layerCustomizationWidget_2)
        self.current_label = QLabel(Indicator)
        self.current_label.setObjectName(u"current_label")
        self.current_label.setGeometry(QRect(12, 250, 49, 16))
        self.apply_button = QPushButton(Indicator)
        self.apply_button.setObjectName(u"apply_button")
        self.apply_button.setGeometry(QRect(410, 380, 61, 24))

        self.retranslateUi(Indicator)

        QMetaObject.connectSlotsByName(Indicator)
    # setupUi

    def retranslateUi(self, Indicator):
        Indicator.setWindowTitle(QCoreApplication.translate("Indicator", u"Indicators", None))
        self.available_label.setText(QCoreApplication.translate("Indicator", u"Available", None))
        self.current_label.setText(QCoreApplication.translate("Indicator", u"Current", None))
        self.apply_button.setText(QCoreApplication.translate("Indicator", u"Apply", None))
    # retranslateUi

