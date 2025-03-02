# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'form_createmodel.ui'
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
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QComboBox, QDialog,
    QHBoxLayout, QLabel, QListWidget, QListWidgetItem,
    QPushButton, QScrollArea, QSizePolicy, QSpinBox,
    QWidget)

class Ui_CreateModel(object):
    def setupUi(self, CreateModel):
        if not CreateModel.objectName():
            CreateModel.setObjectName(u"CreateModel")
        CreateModel.setWindowModality(Qt.ApplicationModal)
        CreateModel.resize(660, 605)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(CreateModel.sizePolicy().hasHeightForWidth())
        CreateModel.setSizePolicy(sizePolicy)
        CreateModel.setMinimumSize(QSize(660, 605))
        CreateModel.setMaximumSize(QSize(660, 605))
        self.setmodel_button = QPushButton(CreateModel)
        self.setmodel_button.setObjectName(u"setmodel_button")
        self.setmodel_button.setGeometry(QRect(570, 570, 80, 24))
        self.layoutWidget = QWidget(CreateModel)
        self.layoutWidget.setObjectName(u"layoutWidget")
        self.layoutWidget.setGeometry(QRect(20, 20, 111, 27))
        self.horizontalLayout = QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.layercount_label = QLabel(self.layoutWidget)
        self.layercount_label.setObjectName(u"layercount_label")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.layercount_label.sizePolicy().hasHeightForWidth())
        self.layercount_label.setSizePolicy(sizePolicy1)
        self.layercount_label.setMaximumSize(QSize(80, 16777215))

        self.horizontalLayout.addWidget(self.layercount_label)

        self.layercount_spinBox = QSpinBox(self.layoutWidget)
        self.layercount_spinBox.setObjectName(u"layercount_spinBox")
        self.layercount_spinBox.setMaximumSize(QSize(30, 16777215))
        self.layercount_spinBox.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.layercount_spinBox.setMinimum(2)
        self.layercount_spinBox.setMaximum(25)

        self.horizontalLayout.addWidget(self.layercount_spinBox)

        self.widget = QWidget(CreateModel)
        self.widget.setObjectName(u"widget")
        self.widget.setGeometry(QRect(270, 260, 380, 300))
        self.layerCustomizationArea = QScrollArea(CreateModel)
        self.layerCustomizationArea.setObjectName(u"layerCustomizationArea")
        self.layerCustomizationArea.setGeometry(QRect(10, 70, 251, 521))
        self.layerCustomizationArea.setWidgetResizable(True)
        self.layerCustomizationWidget = QWidget()
        self.layerCustomizationWidget.setObjectName(u"layerCustomizationWidget")
        self.layerCustomizationWidget.setGeometry(QRect(0, 0, 249, 519))
        self.layerCustomizationArea.setWidget(self.layerCustomizationWidget)
        self.restore_button = QPushButton(CreateModel)
        self.restore_button.setObjectName(u"restore_button")
        self.restore_button.setGeometry(QRect(142, 23, 111, 22))
        self.target_label = QLabel(CreateModel)
        self.target_label.setObjectName(u"target_label")
        self.target_label.setGeometry(QRect(280, 180, 81, 16))
        self.trainingcols_label = QLabel(CreateModel)
        self.trainingcols_label.setObjectName(u"trainingcols_label")
        self.trainingcols_label.setGeometry(QRect(280, 12, 101, 16))
        self.layoutWidget1 = QWidget(CreateModel)
        self.layoutWidget1.setObjectName(u"layoutWidget1")
        self.layoutWidget1.setGeometry(QRect(450, 140, 101, 27))
        self.horizontalLayout_2 = QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_2.setSpacing(3)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.stepfuture_label = QLabel(self.layoutWidget1)
        self.stepfuture_label.setObjectName(u"stepfuture_label")
        sizePolicy.setHeightForWidth(self.stepfuture_label.sizePolicy().hasHeightForWidth())
        self.stepfuture_label.setSizePolicy(sizePolicy)
        self.stepfuture_label.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_2.addWidget(self.stepfuture_label)

        self.stepfuture_spinbox = QSpinBox(self.layoutWidget1)
        self.stepfuture_spinbox.setObjectName(u"stepfuture_spinbox")
        self.stepfuture_spinbox.setMaximumSize(QSize(30, 16777215))
        self.stepfuture_spinbox.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.stepfuture_spinbox.setMinimum(1)
        self.stepfuture_spinbox.setMaximum(100)

        self.horizontalLayout_2.addWidget(self.stepfuture_spinbox)

        self.layoutWidget2 = QWidget(CreateModel)
        self.layoutWidget2.setObjectName(u"layoutWidget2")
        self.layoutWidget2.setGeometry(QRect(450, 100, 94, 27))
        self.horizontalLayout_3 = QHBoxLayout(self.layoutWidget2)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.steppast_label = QLabel(self.layoutWidget2)
        self.steppast_label.setObjectName(u"steppast_label")

        self.horizontalLayout_3.addWidget(self.steppast_label)

        self.steppast_spinbox = QSpinBox(self.layoutWidget2)
        self.steppast_spinbox.setObjectName(u"steppast_spinbox")
        self.steppast_spinbox.setMaximumSize(QSize(30, 16777215))
        self.steppast_spinbox.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.steppast_spinbox.setMinimum(1)
        self.steppast_spinbox.setMaximum(200)
        self.steppast_spinbox.setValue(10)

        self.horizontalLayout_3.addWidget(self.steppast_spinbox)

        self.layoutWidget3 = QWidget(CreateModel)
        self.layoutWidget3.setObjectName(u"layoutWidget3")
        self.layoutWidget3.setGeometry(QRect(450, 180, 127, 27))
        self.horizontalLayout_4 = QHBoxLayout(self.layoutWidget3)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.forecastperiod_label = QLabel(self.layoutWidget3)
        self.forecastperiod_label.setObjectName(u"forecastperiod_label")

        self.horizontalLayout_4.addWidget(self.forecastperiod_label)

        self.forecastperiod_spinbox = QSpinBox(self.layoutWidget3)
        self.forecastperiod_spinbox.setObjectName(u"forecastperiod_spinbox")
        self.forecastperiod_spinbox.setMaximumSize(QSize(30, 16777215))
        self.forecastperiod_spinbox.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.forecastperiod_spinbox.setMinimum(1)
        self.forecastperiod_spinbox.setMaximum(100)

        self.horizontalLayout_4.addWidget(self.forecastperiod_spinbox)

        self.layoutWidget4 = QWidget(CreateModel)
        self.layoutWidget4.setObjectName(u"layoutWidget4")
        self.layoutWidget4.setGeometry(QRect(450, 60, 135, 26))
        self.horizontalLayout_5 = QHBoxLayout(self.layoutWidget4)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.optimizer_label = QLabel(self.layoutWidget4)
        self.optimizer_label.setObjectName(u"optimizer_label")

        self.horizontalLayout_5.addWidget(self.optimizer_label)

        self.optimizer_combobox = QComboBox(self.layoutWidget4)
        self.optimizer_combobox.setObjectName(u"optimizer_combobox")

        self.horizontalLayout_5.addWidget(self.optimizer_combobox)

        self.layoutWidget5 = QWidget(CreateModel)
        self.layoutWidget5.setObjectName(u"layoutWidget5")
        self.layoutWidget5.setGeometry(QRect(450, 20, 184, 26))
        self.horizontalLayout_6 = QHBoxLayout(self.layoutWidget5)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.loss_label = QLabel(self.layoutWidget5)
        self.loss_label.setObjectName(u"loss_label")

        self.horizontalLayout_6.addWidget(self.loss_label)

        self.loss_combobox = QComboBox(self.layoutWidget5)
        self.loss_combobox.setObjectName(u"loss_combobox")
        self.loss_combobox.setEnabled(True)
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.loss_combobox.sizePolicy().hasHeightForWidth())
        self.loss_combobox.setSizePolicy(sizePolicy2)
        self.loss_combobox.setMinimumSize(QSize(150, 0))
        self.loss_combobox.setMaximumSize(QSize(100, 16777215))

        self.horizontalLayout_6.addWidget(self.loss_combobox)

        self.layoutWidget6 = QWidget(CreateModel)
        self.layoutWidget6.setObjectName(u"layoutWidget6")
        self.layoutWidget6.setGeometry(QRect(450, 220, 79, 27))
        self.horizontalLayout_7 = QHBoxLayout(self.layoutWidget6)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.epochs_label = QLabel(self.layoutWidget6)
        self.epochs_label.setObjectName(u"epochs_label")

        self.horizontalLayout_7.addWidget(self.epochs_label)

        self.epochs_spinbox = QSpinBox(self.layoutWidget6)
        self.epochs_spinbox.setObjectName(u"epochs_spinbox")
        self.epochs_spinbox.setMaximumSize(QSize(30, 16777215))
        self.epochs_spinbox.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.epochs_spinbox.setMinimum(1)
        self.epochs_spinbox.setMaximum(30)
        self.epochs_spinbox.setValue(5)

        self.horizontalLayout_7.addWidget(self.epochs_spinbox)

        self.trainingcols_listwidget = QListWidget(CreateModel)
        self.trainingcols_listwidget.setObjectName(u"trainingcols_listwidget")
        self.trainingcols_listwidget.setGeometry(QRect(280, 35, 141, 101))
        self.selectalltcols_button = QPushButton(CreateModel)
        self.selectalltcols_button.setObjectName(u"selectalltcols_button")
        self.selectalltcols_button.setGeometry(QRect(280, 135, 71, 20))
        self.deselectalltcols_button = QPushButton(CreateModel)
        self.deselectalltcols_button.setObjectName(u"deselectalltcols_button")
        self.deselectalltcols_button.setGeometry(QRect(350, 135, 71, 20))
        self.target_placeholder_label = QLabel(CreateModel)
        self.target_placeholder_label.setObjectName(u"target_placeholder_label")
        self.target_placeholder_label.setGeometry(QRect(280, 200, 111, 16))

        self.retranslateUi(CreateModel)

        QMetaObject.connectSlotsByName(CreateModel)
    # setupUi

    def retranslateUi(self, CreateModel):
        CreateModel.setWindowTitle(QCoreApplication.translate("CreateModel", u"Create Model", None))
        self.setmodel_button.setText(QCoreApplication.translate("CreateModel", u"Set Model", None))
        self.layercount_label.setText(QCoreApplication.translate("CreateModel", u"Layer Count: ", None))
        self.restore_button.setText(QCoreApplication.translate("CreateModel", u"Restore Defaults", None))
        self.target_label.setText(QCoreApplication.translate("CreateModel", u"Target Variable:", None))
        self.trainingcols_label.setText(QCoreApplication.translate("CreateModel", u"Training Columns:", None))
        self.stepfuture_label.setText(QCoreApplication.translate("CreateModel", u"Step Future:", None))
        self.steppast_label.setText(QCoreApplication.translate("CreateModel", u"Step Past:  ", None))
        self.forecastperiod_label.setText(QCoreApplication.translate("CreateModel", u"Forecast Period:  ", None))
        self.optimizer_label.setText(QCoreApplication.translate("CreateModel", u"Optimizer:", None))
        self.loss_label.setText(QCoreApplication.translate("CreateModel", u"Loss:", None))
        self.epochs_label.setText(QCoreApplication.translate("CreateModel", u"Epochs:  ", None))
        self.selectalltcols_button.setText(QCoreApplication.translate("CreateModel", u"Select All", None))
        self.deselectalltcols_button.setText(QCoreApplication.translate("CreateModel", u"Deselect All", None))
        self.target_placeholder_label.setText(QCoreApplication.translate("CreateModel", u"target_placeholder", None))
    # retranslateUi

