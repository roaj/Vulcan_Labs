#!/usr/bin/env python


#############################################################################
##
## Copyright (C) 2013 Riverbank Computing Limited.
## Copyright (C) 2010 Nokia Corporation and/or its subsidiary(-ies).
## All rights reserved.
##
## This file is part of the examples of PyQt.
##
## $QT_BEGIN_LICENSE:BSD$
## You may use this file under the terms of the BSD license as follows:
##
## "Redistribution and use in source and binary forms, with or without
## modification, are permitted provided that the following conditions are
## met:
##   * Redistributions of source code must retain the above copyright
##     notice, this list of conditions and the following disclaimer.
##   * Redistributions in binary form must reproduce the above copyright
##     notice, this list of conditions and the following disclaimer in
##     the documentation and/or other materials provided with the
##     distribution.
##   * Neither the name of Nokia Corporation and its Subsidiary(-ies) nor
##     the names of its contributors may be used to endorse or promote
##     products derived from this software without specific prior written
##     permission.
##
## THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
## "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
## LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
## A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
## OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
## SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
## LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
## DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
## THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
## (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
## OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE."
## $QT_END_LICENSE$
##
#############################################################################
import math
import time
import random
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import QPoint, QRect, QSize, Qt
from PyQt5.QtWidgets import (QSizePolicy,
        QWidget, QFrame)
from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog,
        QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout, QLayout, 
        QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QSpinBox, QTextEdit,
        QVBoxLayout, QStatusBar, QTabWidget, QLCDNumber, QTableWidget, QTableWidgetItem, QTableView, QMainWindow)


# class Window(QWidget):
#     def __init__(self):
#         super(Window, self).__init__()

#         flowLayout = FlowLayout()
#         flowLayout.addWidget(QPushButton("Short"))
#         flowLayout.addWidget(QPushButton("Longer"))
#         flowLayout.addWidget(QPushButton("Different text"))
#         flowLayout.addWidget(QPushButton("More text"))
#         flowLayout.addWidget(QPushButton("Even longer button text"))
#         self.setLayout(flowLayout)

#         self.setWindowTitle("Flow Layout")


class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.setupUi()
       
    def setupUi(self):
        MainWindow = self
        MainWindow.setObjectName("Vulcan Labs")
        MainWindow.resize(1024, 600)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(9, 9, 1024, 600))
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.frame.setObjectName("frame")
        self.tabWidget = QTabWidget(self.frame)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 1004, 420))
        self.tabWidget.setObjectName("tabWidget")
        self.widget = QWidget()
        self.widget.setObjectName("widget")
        self.groupBox_2 = QGroupBox(self.widget)
        self.groupBox_2.setGeometry(QtCore.QRect(20, 20, 300, 360)) # Mode select group box, mode tab
        self.groupBox_2.setObjectName("groupBox_2")
        self.frame_3 = QFrame(self.groupBox_2)
        self.frame_3.setGeometry(QtCore.QRect(30, 20, 428, 460)) # Mode select dropdown, mode tab
        self.frame_3.setFrameShape(QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.comboBox = QComboBox(self.frame_3)
        self.comboBox.setGeometry(QtCore.QRect(0, 20, 200, 30)) # Mode select dropdown, mode tab
        self.comboBox.setAutoFillBackground(False)
        self.comboBox.setEditable(False)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.pixmap = QPixmap('VulcanLabsLogo.png')
        self.pixmap2 = self.pixmap.scaled(260, 200, QtCore.Qt.KeepAspectRatio) # Logo
        self.labelLogo = QLabel(self.groupBox_2)
        self.labelLogo.setPixmap(self.pixmap2)
        self.labelLogo.setGeometry(20,80,300,300)
        self.setWindowIcon(QtGui.QIcon('3DPrinterLogo.png')) # Logo as Icon
        #self.setStyleSheet("background-color: rgb(255, 255, 255)")
        self.groupBox_3 = QGroupBox(self.widget)
        self.groupBox_3.setGeometry(QtCore.QRect(350, 20, 300, 360)) # Parameter Input group box, mode tab 1
        self.groupBox_3.setObjectName("groupBox_3")
        self.lineEdit = QLineEdit(self.groupBox_3)
        self.lineEdit.setGeometry(QtCore.QRect(160, 40, 60, 30)) # Initial layer line edit, tab 1
        self.lineEdit.setObjectName("lineEdit")
        self.comboBox_2 = QComboBox(self.groupBox_3)
        self.comboBox_2.setGeometry(QtCore.QRect(230, 40, 60, 30)) # Initial layer height unit select, tab 1
        self.comboBox_2.setAutoFillBackground(False)
        self.comboBox_2.setEditable(False)
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.label_9 = QLabel(self.groupBox_3)
        self.label_9.setGeometry(QtCore.QRect(20, 40, 130, 20)) # Initial layer height label
        self.label_9.setObjectName("label_9")
        self.comboBox_3 = QComboBox(self.groupBox_3)
        self.comboBox_3.setGeometry(QtCore.QRect(230, 100, 60, 30)) # Final layer Unit selector
        self.comboBox_3.setAutoFillBackground(False)
        self.comboBox_3.setEditable(False)
        self.comboBox_3.setObjectName("comboBox_3")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.lineEdit_2 = QLineEdit(self.groupBox_3)
        self.lineEdit_2.setGeometry(QtCore.QRect(160, 100, 60, 30)) # Final layer Line Edit
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_10 = QLabel(self.groupBox_3)
        self.label_10.setGeometry(QtCore.QRect(20, 100, 150, 16)) # Final layer Label
        self.label_10.setObjectName("label_10")
        self.label_11 = QLabel(self.groupBox_3)
        self.label_11.setGeometry(QtCore.QRect(20, 150, 71, 16)) # Number of layers label
        self.label_11.setObjectName("label_11")
        self.lineEdit_3 = QLineEdit(self.groupBox_3)
        self.lineEdit_3.setGeometry(QtCore.QRect(160, 150, 60, 30)) # Number of layers line edit
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.label_12 = QLabel(self.groupBox_3)
        self.label_12.setGeometry(QtCore.QRect(20, 200, 100, 16)) # Desired Pressure label
        self.label_12.setObjectName("label_12")
        self.lineEdit_4 = QLineEdit(self.groupBox_3)
        self.lineEdit_4.setGeometry(QtCore.QRect(160, 200, 60, 30)) # Desired Pressure Line Edit
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.comboBox_6 = QComboBox(self.groupBox_3)
        self.comboBox_6.setGeometry(QtCore.QRect(230, 200, 60, 30)) # Desired Pressure unit Select
        self.comboBox_6.setAutoFillBackground(False)
        self.comboBox_6.setEditable(False)
        self.comboBox_6.setObjectName("comboBox_6")
        self.comboBox_6.addItem("")
        self.comboBox_6.addItem("")
        self.label_13 = QLabel(self.groupBox_3)
        self.label_13.setGeometry(QtCore.QRect(235, 155, 50, 20)) # Max layers label
        self.label_13.setObjectName("label_13")
        self.label_14 = QLabel(self.groupBox_3)
        self.label_14.setGeometry(QtCore.QRect(265, 155, 21, 20)) # Max layers value placeholder
        self.label_14.setObjectName("label_14")
        self.pushButton = QPushButton(self.widget)
        self.pushButton.setGeometry(QtCore.QRect(700, 110, 260, 60)) # STOP Button = 700, 50, 80, 40
        self.pushButton.setFont(QFont('Arial', 14))#, QFont.Bold)) #adjust font
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QPushButton(self.widget)
        self.pushButton_2.setGeometry(QtCore.QRect(700, 280, 140, 30)) # Home Button
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_5 = QPushButton(self.widget)
        self.pushButton_5.setGeometry(QtCore.QRect(700, 320, 100, 30)) # Down Button
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_6 = QPushButton(self.widget)
        self.pushButton_6.setGeometry(QtCore.QRect(700, 240, 100, 30)) # up Button
        self.pushButton_6.setObjectName("pushButton_6")
        self.groupBox_4 = QGroupBox(self.widget)
        self.groupBox_4.setGeometry(QtCore.QRect(680, 200, 300, 180)) # Jogging box
        self.groupBox_4.setObjectName("groupBox_4")
        # self.groupBox_5 = QGroupBox(self.groupBox_4)
        # self.groupBox_5.setGeometry(QtCore.QRect(90, 70, 90, 30)) # extra jog box
        # self.groupBox_5.setObjectName("groupBox_5")
        self.comboBox_4 = QComboBox(self.groupBox_4)
        self.comboBox_4.setGeometry(QtCore.QRect(200, 40, 80, 30)) # Jog UP step size select
        self.comboBox_4.setAutoFillBackground(False)
        self.comboBox_4.setEditable(False)
        self.comboBox_4.setObjectName("comboBox_4")
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.comboBox_5 = QComboBox(self.groupBox_4)
        self.comboBox_5.setGeometry(QtCore.QRect(200, 120, 80, 30)) # Jog DOWN step size select
        self.comboBox_5.setAutoFillBackground(False)
        self.comboBox_5.setEditable(False)
        self.comboBox_5.setObjectName("comboBox_5")
        self.comboBox_5.addItem("")
        self.comboBox_5.addItem("")
        self.comboBox_5.addItem("")
        self.groupBox_6 = QGroupBox(self.widget)
        self.groupBox_6.setGeometry(QtCore.QRect(680, 20, 300, 180)) # Program group box
        self.groupBox_6.setObjectName("groupBox_6")
        self.pushButton_3 = QPushButton(self.widget)
        self.pushButton_3.setGeometry(QtCore.QRect(790, 60, 80, 40)) # pause button
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QPushButton(self.widget)
        self.pushButton_4.setGeometry(QtCore.QRect(700, 60, 80, 40)) # run button
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_7 = QPushButton(self.widget)
        self.pushButton_7.setGeometry(QtCore.QRect(880, 60, 80, 40)) # resume button
        self.pushButton_7.setObjectName("pushButton_7")
        self.groupBox_6.raise_()
        self.groupBox_4.raise_()
        self.groupBox_2.raise_()
        self.groupBox_3.raise_()
        self.pushButton.raise_()
        self.pushButton_2.raise_()
        self.pushButton_5.raise_()
        self.pushButton_6.raise_()
        self.pushButton_3.raise_()
        self.pushButton_4.raise_()
        self.pushButton_7.raise_()
        self.tabWidget.addTab(self.widget, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName("tab_2")
        self.lcdNumber = QLCDNumber(self.tab_2)                     #VALUE DISPLAY ON TAB 3
        self.lcdNumber.setGeometry(QtCore.QRect(350, 70, 191, 51))
        self.lcdNumber.setObjectName("lcdNumber")
        self.label_21 = QLabel(self.tab_2)
        self.label_21.setGeometry(QtCore.QRect(20, 70, 300, 51))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.label_21.setFont(font)
        self.label_21.setObjectName("label_21")
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName("tab_3")
        self.widget_2 = QWidget(self.tab_3)
        self.widget_2.setGeometry(QtCore.QRect(9, 9, 994, 500)) # data table
        self.widget_2.setObjectName("widget_2")
        self.tableWidget = QTableWidget(self.widget_2)
        self.tableWidget.setGeometry(QtCore.QRect(20, 20, 944, 340)) # data table
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(9)
        item = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(1, item)
        item = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(2, item)
        item = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(3, item)
        item = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(4, item)
        item = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(5, item)
        item = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(6, item)
        item = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(7, item)
        item = QTableWidgetItem()
        self.tableWidget.setVerticalHeaderItem(8, item)
        item = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName("tab_4")
        self.groupBox_7 = QGroupBox(self.tab_4)
        self.groupBox_7.setGeometry(QtCore.QRect(10, 30, 400, 300)) # Communication group box
        self.groupBox_7.setObjectName("groupBox_7")
        self.label_15 = QLabel(self.groupBox_7)
        self.label_15.setGeometry(QtCore.QRect(10, 30, 200, 16)) # Connection label
        self.label_15.setObjectName("label_15")
        self.label_16 = QLabel(self.groupBox_7)
        self.label_16.setGeometry(QtCore.QRect(10, 60, 100, 16)) # System IP label
        self.label_16.setObjectName("label_16")
        self.label_17 = QLabel(self.groupBox_7)
        self.label_17.setGeometry(QtCore.QRect(10, 90, 200, 21)) # Connection Device IP label
        self.label_17.setObjectName("label_17")
        self.groupBox_9 = QGroupBox(self.tab_4)
        self.groupBox_9.setGeometry(QtCore.QRect(440, 30, 401, 300)) # System group box
        self.groupBox_9.setObjectName("groupBox_9")
        self.label_18 = QLabel(self.groupBox_9)
        self.label_18.setGeometry(QtCore.QRect(10, 30, 200, 16)) # System Time
        self.label_18.setObjectName("label_18")
        self.label_19 = QLabel(self.groupBox_9)
        self.label_19.setGeometry(QtCore.QRect(10, 60, 200, 16)) # System Date
        self.label_19.setObjectName("label_19")
        self.label_20 = QLabel(self.groupBox_9)
        self.label_20.setGeometry(QtCore.QRect(10, 90, 200, 16)) # System Runtime
        self.label_20.setObjectName("label_20")
        self.tabWidget.addTab(self.tab_4, "")
        self.frame_2 = QFrame(self.frame)
        self.frame_2.setGeometry(QtCore.QRect(0, 430, 1004, 261)) # Bottom Area
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.groupBox = QGroupBox(self.frame_2)
        self.groupBox.setGeometry(QtCore.QRect(0, 0, 1004, 300)) # Bottom Box
        self.groupBox.setObjectName("groupBox")
        self.tableView = QTableView(self.groupBox)
        self.tableView.setGeometry(QtCore.QRect(10, 20, 980, 180)) # Bottom Text Area
        self.tableView.setObjectName("tableView")
        self.label = QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(30, 40, 140, 20)) # Bottom Area, Connected label
        self.label.setObjectName("label")
        self.label_2 = QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(30, 70, 140, 20)) # Bottom Area, System Status label
        self.label_2.setObjectName("label_2")
        self.label_3 = QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(180, 40, 140, 20)) # Bottom Area, Mode Label
        self.label_3.setObjectName("label_3")
        self.label_4 = QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(180, 70, 140, 20)) # Bottom Area, Error Label
        self.label_4.setObjectName("label_4")
        self.label_5 = QLabel(self.groupBox)
        self.label_5.setGeometry(QtCore.QRect(330, 40, 140, 20)) # Bottom Area, Desired Position Label
        self.label_5.setObjectName("label_5")
        self.label_6 = QLabel(self.groupBox)
        self.label_6.setGeometry(QtCore.QRect(330, 70, 140, 20)) # Bottom Area, Desired Pressure Label
        self.label_6.setObjectName("label_6")
        self.label_7 = QLabel(self.groupBox)
        self.label_7.setGeometry(QtCore.QRect(480, 70, 149, 20)) # Bottom Area, Current Pressure Label
        self.label_7.setObjectName("label_7")
        self.label_8 = QLabel(self.groupBox)
        self.label_8.setGeometry(QtCore.QRect(480, 40, 140, 20)) # Bottom Area, Desired Position Label
        self.label_8.setObjectName("label_8")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        ### --- ADDITIONAL COMPONENTS GO HERE --- ###
        # self.pixmap = QPixmap('VulcanLabsLogo.png')
        # self.labelLogo = QLabel(self)
        # self.labelLogo.setPixmap(self.pixmap)
        # self.labelLogo.setGeometry(30,30,100,100)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("Vulcan Labs", "Vulcan Labs"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Mode Select"))
        self.comboBox.setItemText(0, _translate("MainWindow", "Motion Limiting"))
        self.comboBox.setItemText(1, _translate("MainWindow", "Pressure Limiting"))
        self.groupBox_3.setTitle(_translate("MainWindow", "Parameter Input"))
        self.comboBox_2.setItemText(0, _translate("MainWindow", "mm"))
        self.comboBox_2.setItemText(1, _translate("MainWindow", "μm"))
        self.label_9.setText(_translate("MainWindow", "Initial Layer Height"))
        self.comboBox_3.setItemText(0, _translate("MainWindow", "mm"))
        self.comboBox_3.setItemText(1, _translate("MainWindow", "μm"))
        self.label_10.setText(_translate("MainWindow", "Final Layer Height"))
        self.label_11.setText(_translate("MainWindow", "# of Layers"))
        self.label_12.setText(_translate("MainWindow", "Desired Pressure"))
        self.comboBox_6.setItemText(0, _translate("MainWindow", "kPa"))
        self.comboBox_6.setItemText(1, _translate("MainWindow", "MPa"))
        self.label_13.setText(_translate("MainWindow", "max:"))
        self.label_14.setText(_translate("MainWindow", "10"))
        self.pushButton.setText(_translate("MainWindow", "STOP"))
        self.pushButton_2.setText(_translate("MainWindow", "Home"))
        self.pushButton_5.setText(_translate("MainWindow", "Down"))
        self.pushButton_6.setText(_translate("MainWindow", "Up"))
        self.groupBox_4.setTitle(_translate("MainWindow", "Jogging"))
        # self.groupBox_5.setTitle(_translate("MainWindow", "Jogging"))
        self.comboBox_4.setItemText(0, _translate("MainWindow", "1 mm"))
        self.comboBox_4.setItemText(1, _translate("MainWindow", "10 mm"))
        self.comboBox_4.setItemText(2, _translate("MainWindow", "50 mm"))
        self.comboBox_5.setItemText(0, _translate("MainWindow", "1 mm"))
        self.comboBox_5.setItemText(1, _translate("MainWindow", "10 mm"))
        self.comboBox_5.setItemText(2, _translate("MainWindow", "50 mm"))
        self.groupBox_6.setTitle(_translate("MainWindow", "Program"))
        self.pushButton_3.setText(_translate("MainWindow", "Pause"))
        self.pushButton_4.setText(_translate("MainWindow", "Run"))
        self.pushButton_7.setText(_translate("MainWindow", "Resume"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.widget), _translate("MainWindow", "Modes"))
        self.label_21.setText(_translate("MainWindow", "Load Cell Reading:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "System"))
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "Log 3"))
        item = self.tableWidget.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "Log 2"))
        item = self.tableWidget.verticalHeaderItem(2)
        item.setText(_translate("MainWindow", "New Row"))
        item = self.tableWidget.verticalHeaderItem(3)
        item.setText(_translate("MainWindow", "Log 4"))
        item = self.tableWidget.verticalHeaderItem(4)
        item.setText(_translate("MainWindow", "New Row"))
        item = self.tableWidget.verticalHeaderItem(5)
        item.setText(_translate("MainWindow", "New Row"))
        item = self.tableWidget.verticalHeaderItem(6)
        item.setText(_translate("MainWindow", "New Row"))
        item = self.tableWidget.verticalHeaderItem(7)
        item.setText(_translate("MainWindow", "Log 8"))
        item = self.tableWidget.verticalHeaderItem(8)
        item.setText(_translate("MainWindow", "Log 6"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Col 1"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Col 2"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Col 3"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Col 4"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Col 5"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Data"))
        self.groupBox_7.setTitle(_translate("MainWindow", "Communication"))
        self.label_15.setText(_translate("MainWindow", "Connection:"))
        self.label_16.setText(_translate("MainWindow", "System IP:"))
        self.label_17.setText(_translate("MainWindow", "Connected Device IP:"))
        self.groupBox_9.setTitle(_translate("MainWindow", "General"))
        self.label_18.setText(_translate("MainWindow", "System Time:"))
        self.label_19.setText(_translate("MainWindow", "System Date:"))
        self.label_20.setText(_translate("MainWindow", "System Runtime:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("MainWindow", "Configuration"))
        self.groupBox.setTitle(_translate("MainWindow", "System Feedback"))
        self.label.setText(_translate("MainWindow", "Connected: No"))
        self.label_2.setText(_translate("MainWindow", "System Status: Null"))
        self.label_3.setText(_translate("MainWindow", "Mode: Not selected"))
        self.label_4.setText(_translate("MainWindow", "Error: Null"))
        self.label_5.setText(_translate("MainWindow", "Desired Position: Null"))
        self.label_6.setText(_translate("MainWindow", "Desired Pressure: Null"))
        self.label_7.setText(_translate("MainWindow", "Current Pressure: Null"))
        self.label_8.setText(_translate("MainWindow", "Current Position: Null"))

        # MIDDLEWARE
        # self.
        # .valueChanged.connect(self.UpdateForceSliderValue)

    def UpdateForceReadingValue(self):
        """Updates the LCD Force Reading Value"""
        #force_reading_raw = self.pressure_slider.value()       ---- THIS IS WHERE WE PUT THE FORCE VALUE ----- #
        force_reading_raw = random.randint(1,101)
        force_reading_kg = force_reading_raw/1000            #(grams to kg)
        force_reading_N = force_reading_kg*9.81
        r = 10 #mm
        r_m = r/1000
        Area = math.pi*math.pow(r_m,2)
        pressure_reading = force_reading_N/Area

        self.lcdNumber.display(pressure_reading)
        self.update()

    def UpdateGUI(self):
        self.UpdateForceReadingValue()

if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    mainWin = Ui_MainWindow()
    mainWin.show()

    fps = 1
    timer = QtCore.QTimer()
    timer.timeout.connect(mainWin.UpdateGUI)
    timer.setInterval(int(1000 / fps))
    timer.start()

    sys.exit(app.exec_())