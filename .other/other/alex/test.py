#!/usr/bin/env python

import math
import time
import timeit
import random
import sys
import serial 
import os
import pickle
import socket
import traceback
import sqlite3
from datetime import datetime, date

import L2_log as log

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from dateutil import parser
from matplotlib import style
# import paho.mqtt.client as paho
# style.use('fivethirtyeight')

from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg
# import RPi.GPIO as GPIO #import I/O interface             #
# from hx711 import HX711 #import HX711 class               #
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import QPoint, QRect, QSize, Qt, QObject, pyqtSignal, pyqtSlot, QThreadPool, QRunnable, QThread
from PyQt5.QtWidgets import (QSizePolicy,
        QWidget, QFrame, QRadioButton, QCheckBox)
from PyQt5.QtWidgets import (QApplication, QComboBox, QDialog,
        QDialogButtonBox, QFormLayout, QGridLayout, QGroupBox, QHBoxLayout, QLayout, 
        QLabel, QLineEdit, QMenu, QMenuBar, QPushButton, QSpinBox, QTextEdit,
        QVBoxLayout, QStatusBar, QTabWidget, QLCDNumber, QTableWidget, QTableWidgetItem, QTableView, QMainWindow, QMessageBox)

from vulcanControl import Motor


#Global Variables








# Main window containing all GUI components
class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.setupGlobalVars()
        self.setupUi()
        pg.setConfigOptions(antialias=True)


    def setupGlobalVars(self):
        self.modeSelected = 0                                   # 0:motion 1:pressure
        self.connectionState = 0                                # 0:No Connection 1:Connection Secure
        self.IpAdd = socket.gethostbyname(socket.gethostname())
        self.systemState = 0                                    # 0:idle 1:Starting 2:Running 3:Paused 4:Stopped 5:Processing 6:Homed
        self.systemCalibrated = 0                               # 0: no 1: calibrated
        # self.elapsedTime = time.perf_counter()

        self.desPos = 0
        self.desPress = 0
        self.curPos = 0
        self.curPress = 0

        self.runStartTime = 0

    def setupUi(self):

        # -- INITIALIZATION -- #

        #Initializes window and parameters
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
        

        #Initializes tab layout
        self.tabWidget = QTabWidget(self.frame)
        self.tabWidget.setGeometry(QtCore.QRect(0, 0, 1004, 420))
        self.tabWidget.setObjectName("tabWidget")

        #CSS
        self.tabWidget.setStyleSheet('QTabBar { min-height: 20px; min-width: 500px; }')
        # self.setStyleSheet('QPushButton { }')

        # TAB 1 #

        #Inits box area on left
        self.widget = QWidget()
        self.widget.setObjectName("widget")
        self.groupBox_2 = QGroupBox(self.widget)
        self.groupBox_2.setGeometry(QtCore.QRect(20, 20, 300, 360)) # positioning and sizing
        self.groupBox_2.setObjectName("groupBox_2")
        # self.groupBox_2.setStyleSheet("color: #F9F6F0;")
        self.groupBox_2.setStyleSheet("""QGroupBox { font-weight: bold; font-size: 15px; color: #F9F6F0; border-radius: 8px;}""")


        # self.groupBox_2.setStyleSheet("font-size: 15px;")
        # self.groupBox_2.setStyleSheet("border-radius: 8px;")
        # self.groupBox_2.setStyleSheet("font-weight: bold;")

        #Inits Mode select dropdown component
        self.comboBox = QComboBox(self.groupBox_2)
        self.comboBox.setGeometry(QtCore.QRect(20, 40, 200, 30)) # positioning and sizing
        self.comboBox.setAutoFillBackground(False)
        self.comboBox.setEditable(False)
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setContentsMargins(100,100,100,100)

        #Inits Logo
        self.pixmap = QPixmap('VulcanLabsLogo.png')
        self.pixmap2 = self.pixmap.scaled(260, 200, QtCore.Qt.KeepAspectRatio) # Logo
        self.labelLogo = QLabel(self.groupBox_2)
        self.labelLogo.setPixmap(self.pixmap2)
        self.labelLogo.setGeometry(20,80,300,300)

        #Inits window icon as logo
        self.setWindowIcon(QtGui.QIcon('3DPrinterLogo.png')) # Logo as Icon
        # self.setStyleSheet("background-color: rgb(255, 255, 255)") #Sets background color of GUI

        #Inits Parameter Group Box
        self.groupBox_3 = QGroupBox(self.widget)
        self.groupBox_3.setGeometry(QtCore.QRect(350, 20, 300, 360)) # positioning and sizing
        self.groupBox_3.setObjectName("groupBox_3")
        self.groupBox_3.setStyleSheet("""QGroupBox { font-weight: bold; font-size: 15px; color: #F9F6F0; border-radius: 8px;}""")


        #Inits initial layer height input
        self.lineEdit = QLineEdit(self.groupBox_3)
        self.lineEdit.setGeometry(QtCore.QRect(160, 40, 60, 30)) # pos and size
        self.lineEdit.setObjectName("lineEdit")
#         self.setStyleSheet(""")
# QLineEdit {
#     padding: 1px;
#     color: #F9F6F0;
#     border: 2px solid #F9F6F0;
#     border-radius: 8px;
#     font-weight: bold;
# }

        #Inits initial layer height unit select
        self.comboBox_2 = QComboBox(self.groupBox_3)
        self.comboBox_2.setGeometry(QtCore.QRect(230, 40, 60, 30)) # pos and size
        self.comboBox_2.setAutoFillBackground(False)
        self.comboBox_2.setEditable(False)
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")

        #Inits initial layer height label
        self.label_9 = QLabel(self.groupBox_3)
        self.label_9.setGeometry(QtCore.QRect(20, 40, 130, 20)) # pos and size
        self.label_9.setObjectName("label_9")
        self.label_9.setStyleSheet("""QLabel { color: #F9F6F0; font-weight: bold; font-size: 14px; }""")
        self.setStyleSheet("""QLabel { color: #F9F6F0; font-weight: bold; font-size: 14px; }""")

        #Inits final layer height unit select
        self.comboBox_3 = QComboBox(self.groupBox_3)
        self.comboBox_3.setGeometry(QtCore.QRect(230, 100, 60, 30)) # pos and size
        self.comboBox_3.setAutoFillBackground(False)
        self.comboBox_3.setEditable(False)
        self.comboBox_3.setObjectName("comboBox_3")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")

        #Inits final layer height input
        self.lineEdit_2 = QLineEdit(self.groupBox_3)
        self.lineEdit_2.setGeometry(QtCore.QRect(160, 100, 60, 30)) # pos and size
        self.lineEdit_2.setObjectName("lineEdit_2")

        #Inits final layer label
        self.label_10 = QLabel(self.groupBox_3)
        self.label_10.setGeometry(QtCore.QRect(20, 100, 130, 20)) # pos and size
        self.label_10.setObjectName("label_10")

        #Inits number of layers label
        self.label_11 = QLabel(self.groupBox_3)
        self.label_11.setGeometry(QtCore.QRect(20, 150, 150, 20)) # pos and size
        self.label_11.setObjectName("label_11")

        #Inits number of layers input
        self.lineEdit_3 = QLineEdit(self.groupBox_3)
        self.lineEdit_3.setGeometry(QtCore.QRect(160, 150, 60, 30)) # pos and size
        self.lineEdit_3.setObjectName("lineEdit_3")

        #Inits desired pressure label
        self.label_12 = QLabel(self.groupBox_3)
        self.label_12.setGeometry(QtCore.QRect(20, 200, 150, 20)) # pos and size
        self.label_12.setObjectName("label_12")

        #Inits desired pressure input
        self.lineEdit_4 = QLineEdit(self.groupBox_3)
        self.lineEdit_4.setGeometry(QtCore.QRect(160, 200, 60, 30)) # pos and size
        self.lineEdit_4.setObjectName("lineEdit_4")

        #Inits desired pressure unit select
        self.comboBox_6 = QComboBox(self.groupBox_3)
        self.comboBox_6.setGeometry(QtCore.QRect(230, 200, 60, 30)) # pos and size
        self.comboBox_6.setAutoFillBackground(False)
        self.comboBox_6.setEditable(False)
        self.comboBox_6.setObjectName("comboBox_6")
        self.comboBox_6.addItem("")
        self.comboBox_6.addItem("")

        #Inits STOP button
        self.pushButton = QPushButton(self.widget)
        self.pushButton.setGeometry(QtCore.QRect(700, 110, 260, 60)) # pos and size
        self.pushButton.setFont(QFont('Arial', 14))#, QFont.Bold)) #adjust font
        self.pushButton.setObjectName("pushButton")
        # self.pushButton.clicked.connect(motor.stopRun)
        self.pushButton.setStyleSheet("""QPushButton:disabled {font-weight: bold; font-size: 16px; color: #000; border: 2px solid #202020; border-radius: 8px; min-width: 10px; background-color: #66380d;}""")
        # self.pushButton.setStyleSheet("""QPushButton:hover { background-color: green; }""")
        self.pushButton.setStyleSheet("""QPushButton {
    font-weight: bold;
    font-size: 16px;
    color: #303030;
    border: 2px solid #202020;
    border-radius: 8px;
    min-width: 10px;
    background-color: #FF7C0A;}""")

        #Inits Home button
        self.pushButton_2 = QPushButton(self.widget)
        self.pushButton_2.setGeometry(QtCore.QRect(700, 280, 140, 30)) # pos and size
        self.pushButton_2.setObjectName("pushButton_2")
        # self.pushButton_2.clicked.connect(motor.Home)
        self.pushButton_2.setStyleSheet("""QPushButton:disabled {font-weight: bold; font-size: 16px; color: #000; border: 2px solid #202020; border-radius: 8px; min-width: 10px; background-color: #66380d;}""")
        self.pushButton_2.setStyleSheet("""QPushButton {
    font-weight: bold;
    font-size: 16px;
    color: #303030;
    border: 2px solid #202020;
    border-radius: 8px;
    min-width: 10px;
    background-color: #FF7C0A;}""")

        #Inits Down button
        self.pushButton_5 = QPushButton(self.widget)
        self.pushButton_5.setGeometry(QtCore.QRect(700, 320, 140, 30)) # pos and size
        self.pushButton_5.setObjectName("pushButton_5")
        self.pushButton_5.clicked.connect(lambda x: motor.jogDown(self.comboBox_5.currentIndex()))
        self.pushButton_5.setStyleSheet("""QPushButton:disabled {font-weight: bold; font-size: 16px; color: #000; border: 2px solid #202020; border-radius: 8px; min-width: 10px; background-color: #66380d;}""")
        self.pushButton_5.setStyleSheet("""QPushButton {
    font-weight: bold;
    font-size: 16px;
    color: #303030;
    border: 2px solid #202020;
    border-radius: 8px;
    min-width: 10px;
    background-color: #FF7C0A;}""")

        #Inits Up button
        self.pushButton_6 = QPushButton(self.widget)
        self.pushButton_6.setGeometry(QtCore.QRect(700, 240, 140, 30)) # pos and size
        self.pushButton_6.setObjectName("pushButton_6")
        # self.pushButton_6.clicked.connect(lambda x: DB.getTable(list([0])))
        self.pushButton_6.clicked.connect(lambda x: motor.jogUp(self.comboBox_5.currentIndex()))
        self.pushButton_6.setStyleSheet("""QPushButton:disabled {font-weight: bold; font-size: 16px; color: #000; border: 2px solid #202020; border-radius: 8px; min-width: 10px; background-color: #66380d;}""")
        self.pushButton_6.setStyleSheet("""QPushButton {
    font-weight: bold;
    font-size: 16px;
    color: #303030;
    border: 2px solid #202020;
    border-radius: 8px;
    min-width: 10px;
    background-color: #FF7C0A;}""")


        #Inits Jogging box area
        self.groupBox_4 = QGroupBox(self.widget)
        self.groupBox_4.setGeometry(QtCore.QRect(680, 200, 300, 180)) # pos and size
        self.groupBox_4.setObjectName("groupBox_4")
        self.groupBox_4.setStyleSheet("""QGroupBox { font-weight: bold; font-size: 15px; color: #F9F6F0; border-radius: 8px;}""")


        #Inits jog step size select
        self.comboBox_5 = QComboBox(self.groupBox_4)
        self.comboBox_5.setGeometry(QtCore.QRect(200, 120, 80, 30)) # pos and size
        self.comboBox_5.setAutoFillBackground(False)
        self.comboBox_5.setEditable(False)
        self.comboBox_5.setObjectName("comboBox_5")
        self.comboBox_5.addItem("")
        self.comboBox_5.addItem("")
        self.comboBox_5.addItem("")

        #Inits program group box area
        self.groupBox_6 = QGroupBox(self.widget)
        self.groupBox_6.setGeometry(QtCore.QRect(680, 20, 300, 180)) # pos and size
        self.groupBox_6.setObjectName("groupBox_6")
        self.groupBox_6.setStyleSheet("""QGroupBox { font-weight: bold; font-size: 15px; color: #F9F6F0; border-radius: 8px;}""")

        #Inits pause button
        self.pushButton_3 = QPushButton(self.widget)
        self.pushButton_3.setGeometry(QtCore.QRect(790, 60, 80, 40)) # pos and size
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.setStyleSheet("""QPushButton:disabled {font-weight: bold; font-size: 16px; color: #000; border: 2px solid #202020; border-radius: 8px; min-width: 10px; background-color: #66380d;}""")
        self.pushButton_3.setStyleSheet("""QPushButton {
    font-weight: bold;
    font-size: 16px;
    color: #303030;
    border: 2px solid #202020;
    border-radius: 8px;
    min-width: 10px;
    background-color: #FF7C0A;}""")

        #Inits run button
        self.pushButton_4 = QPushButton(self.widget)
        self.pushButton_4.setGeometry(QtCore.QRect(700, 60, 80, 40)) # pos and size
        self.pushButton_4.setObjectName("pushButton_4")
        self.pushButton_4.clicked.connect(self.runStartTimer)
        self.pushButton_4.setStyleSheet("""QPushButton {
    font-weight: bold;
    font-size: 16px;
    color: #303030;
    border: 2px solid #202020;
    border-radius: 8px;
    min-width: 10px;
    background-color: #FF7C0A;}""")
        # self.pushButton_4.setStyleSheet("""QPushButton:disabled {font-weight: bold; font-size: 16px; color: #000; border: 2px solid #202020; border-radius: 8px; min-width: 10px; background-color: #66380d;}""")

        #Inits resume button
        self.pushButton_7 = QPushButton(self.widget)
        self.pushButton_7.setGeometry(QtCore.QRect(880, 60, 80, 40)) # pos and size
        self.pushButton_7.setObjectName("pushButton_7")
        self.pushButton_7.setStyleSheet("""QPushButton:disabled {font-weight: bold; font-size: 16px; color: #000; border: 2px solid #202020; border-radius: 8px; min-width: 10px; background-color: #66380d;}""")
        self.pushButton_7.setStyleSheet("""QPushButton {
    font-weight: bold;
    font-size: 16px;
    color: #303030;
    border: 2px solid #202020;
    border-radius: 8px;
    min-width: 10px;
    background-color: #FF7C0A;}""")

        # raise_() brings components to front layer
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

        # TAB 2 #

        #Inits tab 2
        self.tabWidget.addTab(self.widget, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName("tab_2")
        self.lcdNumber = QLCDNumber(self.tab_2)                     #VALUE DISPLAY ON TAB 3
        self.lcdNumber.setGeometry(QtCore.QRect(350, 70, 191, 51))
        self.lcdNumber.setObjectName("lcdNumber2")
        self.lcdNumber2 = QLCDNumber(self.tab_2)                     #VALUE DISPLAY ON TAB 3
        self.lcdNumber2.setGeometry(QtCore.QRect(350, 270, 191, 51))
        self.lcdNumber2.setObjectName("lcdNumber2")
        self.lcdNumber3 = QLCDNumber(self.tab_2)                     #VALUE DISPLAY ON TAB 3
        self.lcdNumber3.setGeometry(QtCore.QRect(350, 170, 191, 51))
        self.lcdNumber3.setObjectName("lcdNumber3")
        self.label_21 = QLabel(self.tab_2)
        self.label_21.setGeometry(QtCore.QRect(20, 70, 300, 51))
        self.label_tab2_pressure = QLabel(self.tab_2)
        self.label_tab2_pressure.setGeometry(QtCore.QRect(20, 270, 300, 51))
        self.label_tab2_pressure_units = QLabel(self.tab_2)
        self.label_tab2_pressure_units.setGeometry(QtCore.QRect(550, 270, 300, 51))
        self.label_tab2_force = QLabel(self.tab_2)
        self.label_tab2_force.setGeometry(QtCore.QRect(20, 170, 300, 51))
        self.label_tab2_force.setFont(QFont('Arial', 18))
        self.label_tab2_force_units = QLabel(self.tab_2)
        self.label_tab2_force_units.setGeometry(QtCore.QRect(550, 170, 300, 51))
        self.label_tab2_force_units.setFont(QFont('Arial', 18))
        self.label_tab2_load_units = QLabel(self.tab_2)
        self.label_tab2_load_units.setGeometry(QtCore.QRect(550, 70, 300, 51))
        self.pushButton_8 = QPushButton(self.tab_2)
        self.pushButton_8.setGeometry(QtCore.QRect(700, 280, 140, 30)) # Calibration Button
        self.pushButton_8.setObjectName("pushButton_8")
        self.pushButton_8.raise_() # -- Calibration Button

        font = QtGui.QFont()
        font.setPointSize(18)

        #Inits lcd display
        self.lcdNumber = QLCDNumber(self.tab_2)
        self.lcdNumber.setGeometry(QtCore.QRect(350, 70, 191, 51)) # pos and size
        self.lcdNumber.setObjectName("lcdNumber")

        #Inits lcd display 2
        self.lcdNumber2 = QLCDNumber(self.tab_2)
        self.lcdNumber2.setGeometry(QtCore.QRect(350, 270, 191, 51)) # pos and size
        self.lcdNumber2.setObjectName("lcdNumber2")

        #Inits load cell reading label
        self.label_21 = QLabel(self.tab_2)
        self.label_21.setGeometry(QtCore.QRect(20, 70, 300, 51)) # pos and size
        self.label_21.setFont(QFont('Arial', 18))
        self.label_21.setObjectName("label_21")

        #Inits pressure reading label
        self.label_tab2_pressure = QLabel(self.tab_2)
        self.label_tab2_pressure.setGeometry(QtCore.QRect(20, 270, 300, 51)) # pos and size
        self.label_tab2_pressure.setFont(font)
        self.label_tab2_pressure.setObjectName("label_tab2_pressure")

        #Inits pressure reading units label
        self.label_tab2_pressure_units = QLabel(self.tab_2)
        self.label_tab2_pressure_units.setGeometry(QtCore.QRect(550, 270, 300, 51)) # pos and size
        self.label_tab2_pressure_units.setFont(font)
        self.label_tab2_pressure_units.setObjectName("label_tab2_pressure_units")

        #Inits load cell reading units label
        self.label_tab2_load_units = QLabel(self.tab_2)
        self.label_tab2_load_units.setGeometry(QtCore.QRect(550, 70, 300, 51)) # pos and size
        self.label_tab2_load_units.setObjectName("label_tab2_load_units")
        self.label_tab2_load_units.setFont(QFont('Arial', 18))

        #Inits calibration button
        self.pushButton_8 = QPushButton(self.tab_2)
        self.pushButton_8.setGeometry(QtCore.QRect(700, 280, 140, 30)) # pos and size
        self.pushButton_8.setObjectName("pushButton_8")
        self.pushButton_8.raise_() # brings to front

        #Inits tare button
        self.tareButton = QPushButton(self.tab_2)
        self.tareButton.setGeometry(QtCore.QRect(700, 220, 140, 30)) # tare Button
        self.tareButton.setObjectName("tareButton")
        self.tareButton.raise_() # -- tare Button

        # TAB 3 #

        #Init tab 3
        self.tabWidget.addTab(self.tab_2, "")
        self.tab_3 = QWidget()
        self.tab_3.setObjectName("tab_3")

        #Init data table area
        self.widget_2 = QWidget(self.tab_3)
        self.widget_2.setGeometry(QtCore.QRect(9, 9, 994, 350)) # pos and size
        self.widget_2.setObjectName("widget_2")

        #Inits refresh plot button
        self.refreshButton = QPushButton(self.tab_3)
        self.refreshButton.setGeometry(550, 20, 80, 30)
        self.refreshButton.setObjectName("button_refresh")
        self.refreshButton.clicked.connect(DB.getTable)

        self.plotForceRadio = QCheckBox(self.tab_3)
        self.plotForceRadio.setGeometry(550, 80, 120, 30)
        self.plotForceRadio.setText("Plot Force")
        # self.plotForceRadio.toggled.connect(lambda x: self.plotState(self.plotForceRadio))

        self.plotPressureRadio = QRadioButton(self.tab_3)
        self.plotPressureRadio.setGeometry(550, 120, 120, 30)
        self.plotPressureRadio.setText("Plot Pressure")
        self.plotPressureRadio.toggled.connect(lambda x: self.plotState(self.plotPressureRadio))

        self.plotWeightRadio = QRadioButton(self.tab_3)
        self.plotWeightRadio.setGeometry(550, 160, 120, 30)
        self.plotWeightRadio.setText("Plot Weight")
        self.plotWeightRadio.toggled.connect(lambda x: self.plotState(self.plotWeightRadio))

        self.clearButton = QPushButton(self.tab_3)
        self.clearButton.setGeometry(550, 300, 80, 30)
        self.clearButton.setObjectName("button_clear")
        self.clearButton.clicked.connect(DB.clearTable)

        # TAB 4 #

        #Init tab 4
        self.tabWidget.addTab(self.tab_3, "")
        self.tab_4 = QWidget()
        self.tab_4.setObjectName("tab_4")

        self.dataTable = QTableWidget(self.tab_4)
        self.dataTable.setGeometry(QtCore.QRect(10,10,881,791))
        self.dataTable.setRowCount(50)
        self.dataTable.setColumnCount(8)
        self.dataTable.setObjectName("dataTable")
        item = QTableWidgetItem()
        self.dataTable.setHorizontalHeaderItem(0, item)
        item = QTableWidgetItem()
        self.dataTable.setHorizontalHeaderItem(1, item)
        item = QTableWidgetItem()
        self.dataTable.setHorizontalHeaderItem(2, item)
        item = QTableWidgetItem()
        self.dataTable.setHorizontalHeaderItem(3, item)
        item = QTableWidgetItem()
        self.dataTable.setHorizontalHeaderItem(4, item)
        item = QTableWidgetItem()
        self.dataTable.setHorizontalHeaderItem(5, item)
        item = QTableWidgetItem()
        self.dataTable.setHorizontalHeaderItem(6, item)
        item = QTableWidgetItem()
        self.dataTable.setHorizontalHeaderItem(7, item)
        self.dataTable.horizontalHeader().setDefaultSectionSize(150)
        self.dataTable.horizontalHeader().setMinimumSectionSize(41)
        self.exportButton = QPushButton(self.tab_4)
        self.exportButton.setGeometry(QtCore.QRect(10, 810, 151, 20))
        self.exportButton.setObjectName("exportButton")

        self.tabWidget.addTab(self.tab_4, "")
        self.tab_5 = QWidget()
        self.tab_5.setObjectName("tab_5")

        #Init communication box area
        self.groupBox_7 = QGroupBox(self.tab_5)
        self.groupBox_7.setGeometry(QtCore.QRect(10, 30, 400, 300)) # pos and size
        self.groupBox_7.setObjectName("groupBox_7")
        self.groupBox_7.setStyleSheet("""QGroupBox { font-weight: bold; font-size: 15px; color: #F9F6F0; border-radius: 8px;}""")

        #Init connection label
        self.label_15 = QLabel(self.groupBox_7)
        self.label_15.setGeometry(QtCore.QRect(10, 30, 200, 20)) # pos and size
        self.label_15.setObjectName("label_15")

        #Init IP label
        self.label_16 = QLabel(self.groupBox_7)
        self.label_16.setGeometry(QtCore.QRect(10, 60, 200, 20)) # pos and size
        self.label_16.setObjectName("label_16")

        #Init Connection IP label
        self.label_17 = QLabel(self.groupBox_7)
        self.label_17.setGeometry(QtCore.QRect(10, 90, 200, 21)) # pos and size
        self.label_17.setObjectName("label_17")

        #Init system group box area
        self.groupBox_9 = QGroupBox(self.tab_5)
        self.groupBox_9.setGeometry(QtCore.QRect(440, 30, 401, 300)) # pos and size
        self.groupBox_9.setObjectName("groupBox_9")
        self.groupBox_9.setStyleSheet("""QGroupBox { font-weight: bold; font-size: 15px; color: #F9F6F0; border-radius: 8px;}""")

        #Init system time label
        self.label_18 = QLabel(self.groupBox_9)
        self.label_18.setGeometry(QtCore.QRect(10, 30, 200, 20)) # pos and size
        self.label_18.setObjectName("label_18")

        #Init system date label
        self.label_19 = QLabel(self.groupBox_9)
        self.label_19.setGeometry(QtCore.QRect(10, 60, 200, 20)) # pos and size
        self.label_19.setObjectName("label_19")

        #Init system runtime label
        self.label_20 = QLabel(self.groupBox_9)
        self.label_20.setGeometry(QtCore.QRect(10, 90, 200, 20)) # pos and size
        self.label_20.setObjectName("label_20")

        #                 # TAB 5 #

        # #Inits tab 5
        # self.tabWidget.addTab(self.tab_4,"")
        # self.tab_5 = QWidget()
        # self.tab_5.setObjectName("tab_5")
        self.graphFrame = QFrame(self.tab_3)
        self.graphFrame.setGeometry(9,9,500,350)
        self.graphWidget = pg.PlotWidget(self.graphFrame)
        # self.tab_5.setCentralWidget(self.graphWidget)
        # self.graphWidget = QWidget(self.tab_5)
        self.graphWidget.setGeometry(QtCore.QRect(9, 9, 500, 400)) # pos and size
        self.graphWidget.setBackground('w')

        self.targetSpeed_x = list(range(100))  # 100 time points
        self.targetSpeed_y = [random.uniform(-10, 10) for _ in range(100)]
        self.actualSpeed_x = list(range(100))  # 100 time points
        self.actualSpeed_y = [random.uniform(-10, 10) for _ in range(100)]
        print(self.targetSpeed_x)

        self.graphLegend = self.graphWidget.addLegend()
        self.graphWidget.setTitle("Plotss", size="15pt")
        self.graphWidget.showGrid(x=True, y=True)
        grayPen = pg.mkPen(color=(120, 120, 120))
        redPen = pg.mkPen(color=(255,   0,   0))
        self.graphWidget.addItem(pg.InfiniteLine(pos=0, angle=0, pen=grayPen))
        self.leftTargetSpeed = self.graphWidget.plot(self.targetSpeed_x, self.targetSpeed_y, name = 'Target Speed', pen=redPen)

        self.startTime = time.monotonic()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_plot_data)
        self.timer.start()

        # self.graphWidget.setObjectName("stuff")

        # BOTTOM TAB #

        #Init Bottom Area frame
        self.tabWidget.addTab(self.tab_5, "")
        self.frame_2 = QFrame(self.frame)
        self.frame_2.setGeometry(QtCore.QRect(0, 440, 1004, 261)) # pos and size
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.frame_2.setObjectName("frame_2")

        #Init bottom box area
        self.groupBox = QGroupBox(self.frame_2)
        self.groupBox.setGeometry(QtCore.QRect(10, 0, 1004, 300)) # pos and size
        self.groupBox.setObjectName("groupBox")
        self.groupBox.setStyleSheet("""QGroupBox { font-weight: bold; font-size: 15px; color: #F9F6F0; border-radius: 8px;}""")

        #Init table layout
        self.tableView = QTableView(self.groupBox)
        self.tableView.setGeometry(QtCore.QRect(10, 30, 980, 90)) # pos and size
        self.tableView.setObjectName("tableView")

        #Init connected label
        self.label = QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(30, 40, 150, 20)) # pos and size
        self.label.setObjectName("label")

        #Init system status label
        self.label_2 = QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(30, 70, 150, 20)) # pos and size
        self.label_2.setObjectName("label_2")

        #Init mode label
        self.label_3 = QLabel(self.groupBox)
        self.label_3.setGeometry(QtCore.QRect(200, 40, 150, 20)) # pos and size
        self.label_3.setObjectName("label_3")
        self.label_3_modeFeedback = QLabel(self.groupBox)
        self.label_3_modeFeedback.setGeometry(QtCore.QRect(250, 40, 150, 20))
        self.label_3_modeFeedback.setObjectName("label_3_modeFeedback")

        #Init error label
        self.label_4 = QLabel(self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(200, 70, 150, 20)) # pos and size
        self.label_4.setObjectName("label_4")

        #Init desired position label
        self.label_5 = QLabel(self.groupBox)
        self.label_5.setGeometry(QtCore.QRect(480, 40, 200, 20)) # pos and size
        self.label_5.setObjectName("label_5")

        #Init desired pressure label
        self.label_6 = QLabel(self.groupBox)
        self.label_6.setGeometry(QtCore.QRect(480, 70, 200, 20)) # pos and size
        self.label_6.setObjectName("label_6")

        #Init current pressure label
        self.label_7 = QLabel(self.groupBox)
        self.label_7.setGeometry(QtCore.QRect(680, 70, 220, 20)) # pos and size
        self.label_7.setObjectName("label_7")

        #Init desired position label
        self.label_8 = QLabel(self.groupBox)
        self.label_8.setGeometry(QtCore.QRect(680, 40, 200, 20)) # pos and size
        self.label_8.setObjectName("label_8")

        #center main window with status bar
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # self.pixmap = QPixmap('VulcanLabsLogo.png')
        # self.labelLogo = QLabel(self)
        # self.labelLogo.setPixmap(self.pixmap)
        # self.labelLogo.setGeometry(30,30,100,100)
        
        #run class fnc to annotate labels properly
        self.retranslateUi(MainWindow)

        #set default index of GUI to tab 0
        self.tabWidget.setCurrentIndex(0)

        #routing slots by name
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    # Annotate Labels and Components

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
        self.label_11.setText(_translate("MainWindow", "Number of Layers"))
        self.label_12.setText(_translate("MainWindow", "Target Pressure"))
        self.comboBox_6.setItemText(0, _translate("MainWindow", "kPa"))
        self.comboBox_6.setItemText(1, _translate("MainWindow", "MPa"))
        self.pushButton.setText(_translate("MainWindow", "STOP"))
        self.pushButton_2.setText(_translate("MainWindow", "Home"))
        self.pushButton_8.setText(_translate("MainWindow", "Calibrate"))
        self.tareButton.setText(_translate("MainWindow", "Tare"))
        self.pushButton_5.setText(_translate("MainWindow", "Down"))
        self.pushButton_6.setText(_translate("MainWindow", "Up"))
        self.groupBox_4.setTitle(_translate("MainWindow", "Jogging"))
        self.comboBox_5.setItemText(0, _translate("MainWindow", "1 mm"))
        self.comboBox_5.setItemText(1, _translate("MainWindow", "5 mm"))
        self.comboBox_5.setItemText(2, _translate("MainWindow", "10 mm"))
        self.groupBox_6.setTitle(_translate("MainWindow", "Program"))
        self.pushButton_3.setText(_translate("MainWindow", "Pause"))
        self.pushButton_4.setText(_translate("MainWindow", "Run"))
        self.pushButton_7.setText(_translate("MainWindow", "Resume"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.widget), _translate("MainWindow", "Control"))
        self.label_21.setText(_translate("MainWindow", "Load Cell Reading:"))
        self.label_tab2_pressure.setText(_translate("MainWindow", "Current Pressure:"))
        self.label_tab2_pressure_units.setText(_translate("MainWindow", " kPa"))
        self.label_tab2_force.setText(_translate("MainWindow", "Current Force:"))
        self.label_tab2_force_units.setText(_translate("MainWindow", " N"))
        self.label_tab2_load_units.setText(_translate("MainWindow", " kg"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "System"))
        # item = self.tableWidget.verticalHeaderItem(0)
        # item.setText(_translate("MainWindow", "Log 3"))
        # item = self.tableWidget.verticalHeaderItem(1)
        # item.setText(_translate("MainWindow", "Log 2"))
        # item = self.tableWidget.verticalHeaderItem(2)
        # item.setText(_translate("MainWindow", "New Row"))
        # item = self.tableWidget.verticalHeaderItem(3)
        # item.setText(_translate("MainWindow", "Log 4"))
        # item = self.tableWidget.verticalHeaderItem(4)
        # item.setText(_translate("MainWindow", "New Row"))
        # item = self.tableWidget.verticalHeaderItem(5)
        # item.setText(_translate("MainWindow", "New Row"))
        # item = self.tableWidget.verticalHeaderItem(6)
        # item.setText(_translate("MainWindow", "New Row"))
        # item = self.tableWidget.verticalHeaderItem(7)
        # item.setText(_translate("MainWindow", "Log 8"))
        # item = self.tableWidget.verticalHeaderItem(8)
        # item.setText(_translate("MainWindow", "Log 6"))
        # item = self.tableWidget.horizontalHeaderItem(0)
        # item.setText(_translate("MainWindow", "Col 1"))
        # item = self.tableWidget.horizontalHeaderItem(1)
        # item.setText(_translate("MainWindow", "Col 2"))
        # item = self.tableWidget.horizontalHeaderItem(2)
        # item.setText(_translate("MainWindow", "Col 3"))
        # item = self.tableWidget.horizontalHeaderItem(3)
        # item.setText(_translate("MainWindow", "Col 4"))
        # item = self.tableWidget.horizontalHeaderItem(4)
        # item.setText(_translate("MainWindow", "Col 5"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("MainWindow", "Data"))
        self.groupBox_7.setTitle(_translate("MainWindow", "Communication"))
        self.label_15.setText(_translate("MainWindow", "Connection:"))
        self.label_16.setText(_translate("MainWindow", "System IP: "+self.IpAdd))
        self.label_17.setText(_translate("MainWindow", "Connected Device IP:"))
        self.groupBox_9.setTitle(_translate("MainWindow", "General"))
        self.label_18.setText(_translate("MainWindow", "System Time:"))
        self.label_19.setText(_translate("MainWindow", "System Date:"))
        self.label_20.setText(_translate("MainWindow", "System Runtime:"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("MainWindow", "Configuration"))
        self.groupBox.setTitle(_translate("MainWindow", "System State"))
        self.label.setText(_translate("MainWindow", "State: " + str(self.systemState)))
        self.label_2.setText(_translate("MainWindow", "System Status: "+ str(self.systemState)))
        self.label_3.setText(_translate("MainWindow", "Mode: "))
        self.label_3_modeFeedback.setText(_translate("MainWindow", "Motion Limiting"))
        self.label_4.setText(_translate("MainWindow", "Error: "+str(self.systemState)))
        self.label_5.setText(_translate("MainWindow", "Desired Position: "+str(self.desPos)))
        self.label_6.setText(_translate("MainWindow", "Desired Pressure: "+str(self.desPress)))
        self.label_7.setText(_translate("MainWindow", "Current Pressure: "+str(self.curPress)))
        self.label_8.setText(_translate("MainWindow", "Current Position: "+str(self.curPos)))
        # self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), _translate("MainWindow", "Plots"))
        self.refreshButton.setText(_translate("MainWindow", "Refresh"))
        self.clearButton.setText(_translate("MainWindow", "Clear"))


        # -- ROUTING -- #

        # Calibration Button
        self.pushButton_8.clicked.connect(self.Calibration) #cellInstance.user

        # Tare Button
        self.tareButton.clicked.connect(self.tare) #### CHANGE TO TARE FUNCTION ###

        # Update Mode after selection
        self.comboBox.currentIndexChanged.connect(self.updateMode)

        # Update desired parameters
        self.lineEdit_4.textChanged.connect(self.updateDesiredParam)
        self.comboBox_6.currentIndexChanged.connect(self.updateDesiredParam)

        # System state changes
        self.pushButton_4.clicked.connect(lambda x: self.updateSystemState(2)) #running
        # self.pushButton_4.clicked.connect(lambda x: self.setWorker(self.execute_this_fn)) #running
        self.pushButton_3.clicked.connect(lambda X: self.updateSystemState(3)) #Paused
        self.pushButton_7.clicked.connect(lambda X: self.updateSystemState(2)) #running
        self.pushButton.clicked.connect(lambda x: self.updateSystemState(4))   #Stopped
        # 0:idle 1:Starting 2:Running 3:Paused 4:Stopped 5:Processing

        # self.checkCalibration()
        # self.checkHomed()

    def checkHomed(self):
        if self.systemState == 6:
            self.pushButton.setEnabled(True)
            self.pushButton_2.setEnabled(True)
            self.pushButton_3.setEnabled(True)
            self.pushButton_4.setEnabled(True)
            self.pushButton_5.setEnabled(True)
            self.pushButton_6.setEnabled(True)
            self.pushButton_7.setEnabled(True)
        elif self.systemState != 6:
            print("not homed")
            self.pushButton.setEnabled(False)
            self.pushButton_2.setEnabled(False)
            self.pushButton_3.setEnabled(False)
            self.pushButton_4.setEnabled(False)
            self.pushButton_5.setEnabled(False)
            self.pushButton_6.setEnabled(False)
            self.pushButton_7.setEnabled(False)

    def tare(self):
        cellInstance.zeroCell()

    def runStartTimer(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        self.runStartTime = current_time
        print(f'run started at time: {self.runStartTime}')

    def plotState(self,b):
        if b.text() == 'Plot Force':
            if b.isChecked() == True:
                DB.getTable('force',1)
        if b.text() == 'Plot Force':
            if b.isChecked() == False:
                DB.getTable('force',0)
        if b.text() == 'Plot Pressure':
            if b.isChecked() == True:
                DB.getTable('pressure',1)
        if b.text() == 'Plot Pressure':
            if b.isChecked() == False:
                DB.getTable('pressure',0)
        if b.text() == 'Plot Weight':
            if b.isChecked() == True:
                DB.getTable('weight',1)
        if b.text() == 'Plot Weight':
            if b.isChecked() == False:
                DB.getTable('weight',0)

    def updateMode(self):
        mode = self.comboBox.currentText()
        print(mode)
        if mode == "Motion Limiting":
            self.modeSelected = 0
            self.label_3_modeFeedback.setText("Motion Limiting")
        else:
            self.modeSelected = 1
            self.label_3_modeFeedback.setText("Pressure Limiting")


    def UpdateForceReadingValue(self):
        """Updates the LCD Force Reading Value"""
        force_reading_raw = random.random()
        # force_reading_raw = cellInstance.cell.get_weight_mean(3)    #5 recomended for accuracy 
        if force_reading_raw < 0:
            force_reading_raw = 0
        force_reading_kg = round(force_reading_raw,3)            #(grams to kg)
        # pressure = MQtt()
        # pressure.publish(force_reading_kg,"force")
        force_reading_N = round(force_reading_kg*9.81,3)
        pistonDiameter = 20 #mm
        r = pistonDiameter/2 #mm
        r_m = r/1000    # [m]
        Area = math.pi*math.pow(r_m,2)
        pressure_reading = round((force_reading_N/Area)/1000,3)  #Kpa
        
        self.lcdNumber.display(force_reading_kg)
        DB.insert_value('weight', force_reading_kg)
        self.lcdNumber2.display(pressure_reading)
        DB.insert_value('pressure', pressure_reading)
        self.lcdNumber3.display(force_reading_N)
        DB.insert_value('force', force_reading_N)
        self.label_7.setText("Current Pressure: "+str(pressure_reading)+" "+"kPa")
        self.update()

    def Calibration(self):
        self.dialog = calibrationDialogWindow()
        self.dialog.show()

    def checkCalibration(self):
        if cellInstance.calibrated == 1:
            pass
        else:
            self.calibrationWarn()

    def calibrationWarn(self):
        self.dialog2 = calibrationWarning()
        self.dialog2.raise_()
        self.dialog2.show()

    def UpdateGUI(self):
        self.UpdateForceReadingValue()

    def updateSystemState(self,index):
        self.systemState = int(index)
        indices = {
            0: "Idle",
            1: "Starting",
            2: "Running",
            3: "Paused",
            4: "Stopped",
            5: "Processing",
            6: "Homed"
        }
        self.label.setText("State: "+ str(indices[self.systemState]))
        # print(index)

    def updateDesiredParam(self):
        self.label_6.setText(f"Desired Pressure: {self.lineEdit_4.text()} {self.comboBox_6.currentText()}")

    def update_plot_data(self):
        self.targetSpeed_x.append(self.targetSpeed_x[-1] + 1)   # Add a new value 1 higher than the last.
        self.targetSpeed_y.append(random.uniform(-10, 10))

        if self.plotForceRadio.isChecked():
            self.leftTargetSpeed.setData(self.targetSpeed_x, self.targetSpeed_y)
        else:
            self.leftTargetSpeed.clear()    

        row = self.dataTable.rowCount()
        self.dataTable.insertRow(row)
        self.dataTable.setItem(row, 0, QtGui.QTableWidgetItem(str(round(time.monotonic()-self.startTime,4))))    # Needs to be replaced with time from SCUTTLE
        self.dataTable.setItem(row, 1, QtGui.QTableWidgetItem(str(round(self.targetSpeed_x[-1:][0],4))))
        # self.testDataTable.setItem(row, 2, QtGui.QTableWidgetItem(str(round(self.actualSpeed_y[-1:][0],4))))
        # self.testDataTable.setItem(row, 3, QtGui.QTableWidgetItem(str(round(self.duty_y[-1:][0],4))))
        # self.testDataTable.setItem(row, 4, QtGui.QTableWidgetItem(str(round(self.error_y[-1:][0],4))))
        # self.testDataTable.setItem(row, 5, QtGui.QTableWidgetItem(str(round(self.targetSpeed_y[-1:][0],4))))
        # self.testDataTable.setItem(row, 6, QtGui.QTableWidgetItem(str(round(self.actualSpeed_y[-1:][0],4))))
        # self.testDataTable.setItem(row, 7, QtGui.QTableWidgetItem(str(round(self.duty_y[-1:][0],4))))

class sqlDatabase:
    def __init__(self):
        super().__init__()
        self.conn = sqlite3.connect(':memory:')
        self.c = self.conn.cursor()
        self.data = []
        self.plotter = None
        self.c.execute("""CREATE TABLE testtable (
            [timestamp] timestamp,
            type TEXT,
            value INTEGER)
            """)
        self.plots = {
            'force': 0,
            'pressure': 0,
            'weight': 0,
            'default': 0
        }

    def insert_value(self,valType,val):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        with self.conn:
            self.c.execute("INSERT INTO testtable VALUES (:timestamp, :type, :value)",
                    {'timestamp': current_time, 'type': valType, 'value': float(val)})

    def clearTable(self):
        print('deleting')
        self.c.execute('DELETE FROM testtable')
        self.data = []
        self.plotter.clear()

    def getTable(self,name='default',order='0'):
        self.c.execute("SELECT * FROM testtable")
        # print(self.c.fetchall())
        self.graph_data(name,order)
        return self.c.fetchall()

    def graph_data(self,name='default',order='0'):
        self.plots[name] = order
        for key, value in self.plots.items():
            if value == 1:
                self.c.execute('SELECT timestamp, value FROM testtable WHERE type = :type', {'type': key})
                self.data.extend(self.c.fetchall())
        self.data.sort()
        print(self.plots)
        if self.data:
            times = []
            vals = []
            if 1 == 1:
                for row in self.data:
                    print(row)
                    d = float(row[0].replace(":",""))
                    times.append(d)
                    vals.append(float(row[1]))
        else:
            times = []
            vals = []

        # mainWin.graphWidget.setBackground('#fff')
        pen = pg.mkPen(color=(255,100,100), width=8)
        # self.plotter = mainWin.graphWidget.plot(times,vals,pen=pen)
        # plt.plot_date(times,vals,'-')
        # plt.show()

class WorkerThread(QThread):
    def __init__(self, parent=None):
        super(WorkerThread, self).__init__(parent)

    def run(self):
        time.sleep(3)
        self.emit(SIGNAL('threadDone()'))

class newCalibrationWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Calibration')
        self.resize(500,300)
        self.state = 0
        self.setLayout(QFormLayout())
        self.cal_buttons = QWidget()
        self.cal_buttons.setLayout(QHBoxLayout())
        self._initialized = 0
        self.WorkerThread = WorkerThread()
        self.connect(self.WorkerThread, SIGNAL("threadDone()"), self.threadDone, Qt.DirectConnection)

        self.startWindow()
        
    def startWindow(self):
        self.dialog = QLabel('Calibration requires an object of known weight to be placed on the scale')
        self.next_button = QPushButton('Next')
        self.cancel_button = QPushButton('Cancel')
        self.submit_button = QPushButton('Submit')
        self.layout().addRow(self.dialog)
        self.cal_buttons.layout().addWidget(self.cancel_button)
        self.cal_buttons.layout().addWidget(self.next_button)
        self.layout().addRow('', self.cal_buttons)

        self.next_button.clicked.connect(self.getInputWindow)
        self.next_button.clicked.connect(self.startCalibration)
        self.next_button.clicked.connect(self.collectingDataWindow)
        self.next_button.clicked.connect(self.startCalibration)
        self.cancel_button.clicked.connect(self.close)

    def startCalibration(self):
        # i = self.initialized()
        # i = 0
        self.working = 1
        #start calibration
        for i in reversed(range(self.layout().count())):        #Clears components from first window
            self.layout().itemAt(i).widget().deleteLater()
        
        self.dialogText = QLabel('Do not touch scale. Initializing')
        self.layout().addRow('',self.dialogText)
        self.show()

        self.WorkerThread.start()
        self.dialogText.setText('starting')
        
        #fn to perform calibration
        # Ui_MainWindow.setWorker(mainWin, self.calibration_fake)
        # worker.signals.result.connect(self.print_output)
        # worker.signals.finished.connect(self.thread_complete)
        # worker.signals.progress.connect(self.progress_fn)

        # if self.working == 1:
        #     print(1)
        # else:
        #     print('alksdjhfalksjdfhakljh')
                
        # self.dialog = QLabel('wordssss')
        # self.dialogText = QLabel('Place object of known weight on scale and enter weight [g]: ')
        # self.inputWeight = QLineEdit()
        # self.layout().addRow('',self.dialogText)
        # self.layout().addRow('',self.inputWeight)


        # if self.initialized == 1:
        #     self.getInputWindow()

    def threadDone(self):
        self.dialogText.setText('finished')

    def getInputWindow(self):
        self.close()
        # self.knownGrams = 0
        # for i in reversed(range(self.layout().count())):        #Clears components from first window
        #     self.layout().itemAt(i).widget().deleteLater()
        # self.dialogText = QLabel('Place object of known weight on scale and enter weight [g]: ')
        # self.dialog = QLabel('wordssss')
        # # self.cancel_button = QPushButton('Cancel')
        # # self.submit_button = QPushButton('Submit')
        # self.inputWeight = QLineEdit()
        # # buttons = QWidget()
        # # buttons.setLayout(QHBoxLayout())
        # # buttons.layout().addWidget(self.cancel_button)
        # # buttons.layout().addWidget(self.submit_button)
        # self.layout().addRow('',self.dialogText)
        # self.layout().addRow('',self.inputWeight)
        # self.layout().addRow('',buttons)
        # self.layout().resize(300,200)
        self.show()


        # self.inputWeight.textChanged.connect(self.setKnownGrams)
        # self.submit_button.clicked.connect(self.sendKnownInput)
        # self.cancel_button.clicked.connect(self.close)

    def setKnownGrams(self,lineEdit):
        self.knownGrams = self.inputWeight.text()

    def getUserInput(self):
        print('user input started')

    def calibration_fake(self, *args, **kwargs):
        print('Initializing...')
        time.sleep(3)
        self.working = 0
        print(self.working)
        time.sleep(1)
        result = 'complete'
        return self.working
        


class calibrationWarning(QWidget):
    def __init__(self):
        super().__init__()
        self.ok_button = QPushButton('Ok')
        self.cal_button = QPushButton('Calibrate')
        self.dialog = QLabel("Load cell is not calibrated. Please calibrate.")
        self.setWindowTitle('Warning')

        self.setLayout(QFormLayout())
        self.layout().addRow(self.dialog)
        buttons = QWidget()
        buttons.setLayout(QHBoxLayout())
        buttons.layout().addWidget(self.ok_button)
        # buttons.layout().addWidget(self.cal_button)
        self.layout().addRow('', buttons)

        #Routes front end to back end
        self.ok_button.clicked.connect(self.close)
        # self.ok_button.clicked.connect(self.close)
        self.cal_button.clicked.connect(Ui_MainWindow.Calibration)

#Class handling calibration pop up boxes
class calibrationDialogWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(300,200)
        self.cancel_button = QPushButton('Cancel')
        self.next_button = QPushButton('Next')
        self.submit_button = QPushButton('Submit')
        self.finish_button = QPushButton('Finish')
        self.dialogText = QLabel('\n\n Calibration requires an object of known weight to be placed on the scale')
        self.warningText = QLabel('\n\nWarning: Continuing will pause the program')
        self.setWindowTitle('Calibration')

        #Initializes layout
        self.setLayout(QFormLayout())
        self.layout().addRow(self.dialogText)
        buttons = QWidget()
        buttons.setLayout(QHBoxLayout())
        buttons.layout().addWidget(self.cancel_button)
        buttons.layout().addWidget(self.next_button)
        self.layout().addRow('', buttons)
        self.layout().addRow('',self.warningText)

        #Routes front end to back end

        self.next_button.clicked.connect(self.getInputWindow)
        self.next_button.clicked.connect(self.startCalibration)
        # self.next_button.clicked.connect(self.collectingDataWindow)
        self.cancel_button.clicked.connect(self.close)

    def collectingDataWindow(self):
        self.close()
        self.setWindowTitle('Calibration 3')
        for i in reversed(range(self.layout().count())):        #Clears components from first window
            self.layout().itemAt(i).widget().deleteLater()
        self.dialogText = QLabel('Initializing...')
        self.layout().addRow('',self.dialogText)
        self.show()
        while cellInstance.initializing == 1:
            self.dialogText = QLabel('Initializing.')
            time.sleep(1)
            self.dialogText = QLabel('Initializing..')
            time.sleep(1)
            self.dialogText = QLabel('Initializing...')
        self.close()



    #Second window in calibration branch
    def getInputWindow(self):
        self.close()
        self.setWindowTitle('Calibration 2')
        self.knownGrams = 0
        for i in reversed(range(self.layout().count())):        #Clears components from first window
            self.layout().itemAt(i).widget().deleteLater()
        self.dialogText = QLabel('Place object of known weight on scale and enter weight [g]: ')
        self.inputWeight = QLineEdit()
        buttons = QWidget()
        buttons.setLayout(QHBoxLayout())
        buttons.layout().addWidget(self.cancel_button)
        buttons.layout().addWidget(self.submit_button)
        self.layout().addRow('',self.dialogText)
        self.layout().addRow('',self.inputWeight)
        self.layout().addRow('',buttons)
        # self.layout().resize(300,200)
        self.show()


        self.inputWeight.textChanged.connect(self.setKnownGrams)
        self.submit_button.clicked.connect(self.sendKnownInput)
        self.cancel_button.clicked.connect(self.close)

    def setKnownGrams(self,lineEdit):
        self.knownGrams = self.inputWeight.text()

    def startCalibration(self):
        cellInstance.userCalibrationPart1()

    #Sends known weight from user to Load cell calibration
    def sendKnownInput(self):
        self.close()
        self.setWindowTitle('Calibration 3')
        for i in reversed(range(self.layout().count())):
            self.layout().itemAt(i).widget().deleteLater()
        print(f'user inputted value: {self.knownGrams}')
        # while LoadCell.calibrated == 0:
        #     self.dialogText = QLabel('Calibrating...')
        self.dialogText = QLabel('Calibrating')
        buttons = QWidget()
        buttons.setLayout(QHBoxLayout())
        buttons.layout().addWidget(self.finish_button)
        self.layout().addRow('',self.dialogText)
        self.layout().addRow('',buttons)
        self.show()

        cellInstance.userCalibrationPart2(self.knownGrams)

        while cellInstance.initializing == 1:
            self.dialogText = QLabel('Calibrating.')
            time.sleep(1)
            self.dialogText = QLabel('Calibrating..')
            time.sleep(1)
            self.dialogText = QLabel('Calibrating...')

        self.finish_button.clicked.connect(self.close)

class FakeLoadCell():
    def __init__(self):
        self.recorded_configFile_name = 'calibration.vlabs'
        
        if os.path.isfile(self.recorded_configFile_name):
            with open(self.recorded_configFile_name,'rb') as File:
                # self.cell = pickle.load(File)
                self.calibrated = 1
        else:
            self.calibrated = 0
        self.reading = 0
        self.initializing = 0

    def userCalibrationPart1(self):

        self.initializing = 1

        print('getting initial data...')
        # self.reading = self.cell.get_raw_data_mean()
        time.sleep(3)

        self.initializing = 0

    def userCalibrationPart2(self,knownGrams):
        self.initializing = 1

        if knownGrams:
            known_weight_grams = knownGrams
            try:
                value = float(known_weight_grams)
                print(value, 'grams')
            except ValueError:
                print('Expected integer or float and I have got:',
                      known_weight_grams)

        print('calibrating...')
        time.sleep(3)

        self.calibrated = 1
        
        self.initializing = 0

        print("done calibrating")

class LoadCell():
    def __init__(self):
        GPIO.setmode(GPIO.BCM)  #set GPIO pind mode to BCM
        self.pd_sckPin=20
        self.dout_pin=21
        self.recorded_configFile_name = 'calibration.vlabs'
        self.cell = HX711(self.dout_pin,self.pd_sckPin)
        if os.path.isfile(self.recorded_configFile_name):
            with open(self.recorded_configFile_name,'rb') as File:
                self.cell = pickle.load(File)   #loading calibrated HX711 object
                self.calibrated = 1
        else:
            self.calibrated = 0
        self.reading = 0
        self.initializing = 0
 
    def userCalibrationPart1(self):
        self.cell = HX711(self.dout_pin,self.pd_sckPin)
        #send the user calibration message
        err = self.cell.zero()
        if err:
            raise ValueError('Tare is unsuccessful.')
        self.initializing = 1
        self.reading = self.cell.get_raw_data_mean()
        self.initializing = 0
        print(f'raw_data_mean: {self.reading}, predicted ratio = {self.reading/198}')

    def userCalibrationPart2(self,knownGrams):
        self.initializing = 1
        self.reading = self.cell.get_data_mean()
        fileName = 'calibration.vlabs'
        print(f'get_data_mean: {self.reading}, predicted ratio = {self.reading/198}')

        if self.reading:
            known_weight_grams = knownGrams
            try:
                value = float(known_weight_grams)
                print(value, 'grams')
            except ValueError:
                print('Expected integer or float and I have got:',
                      known_weight_grams)

            ratio = self.reading / value  # calculate the ratio for channel A and gain 128
            print(ratio)
            self.cell.set_scale_ratio(ratio)  # set ratio for current channel
            print('Ratio is set.')
        else:
            raise ValueError(
                'Cannot calculate mean value. Try debug mode. Variable reading:',
                self.reading)
                    
        print('Saving the HX711 state to swap file on persistant memory')
        with open(fileName, 'wb') as File:
            pickle.dump(self.cell, File)
            File.flush()
            os.fsync(File.fileno())
            # you have to flush, fsynch and close the file all the time.
            # This will write the file to the drive. It is slow but safe.

        if os.path.isfile(self.recorded_configFile_name):
            with open(self.recorded_configFile_name,'rb') as File:
                self.cell = pickle.load(File)   #loading calibrated HX711 object
                self.calibrated = 1
        
        self.initializing = 0

    def zeroCell(self):
        self.cell.zero()
        self.tare = 1 

        print("Calibration is succesful")
"""
##import time
import paho.mqtt.client as paho

# Setup MQTT
broker="broker.hivemq.com"
port=1883

topic = "scuttle/infrastructure/data/001/scale/latest"

def on_publish(client,userdata,result):         # create function for callback
    pass

mqtt = paho.Client()                          # create client object
mqtt.on_publish = on_publish                  # assign function to callback
mqtt.connect(broker,port)                     # establish connection


if __name__ == "__main__":
    while 1:
        weight = ser.readline().decode('utf-8')
        print("Weight Station Reading: " + weight)
        # time.sleep(0.01)
        mqtt.publish(topic, str(weight))

"""
class MQtt():
    #settup MQTT
    def __init__(self):        
        self.baseTopic = "VulcanLabs/" #base topic
        self.mqtt = paho.Client()
        self.broker="broker.hivemq.com"
        self.port=1883
    def on_publish(self,client,userdata,result):
        pass
    
    def publish(self,value,topicName): # something.publish(value,"topicName")
        self.mqtt.on_publish = self.on_publish
        self.mqtt.connect(self.broker,self.port)
        self.value = value
        self.topic = topicName
        self.mqtt.publish((self.baseTopic + self.topic), str(self.value))




                
if __name__ == '__main__':
    # motor = Motor()
    # cellInstance = FakeLoadCell()
    DB = sqlDatabase()
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    mainWin = Ui_MainWindow()
    styleFile=os.path.join(os.path.split(__file__)[0],"styleVulcan.stylesheet")
    styleSheetStr = open(styleFile,"r").read()
    mainWin.setStyleSheet(styleSheetStr)
    mainWin.show()

    fps = 3
    # timer = QtCore.QTimer()
    # timer.timeout.connect(mainWin.UpdateGUI)
    # timer.setInterval(int(1000/fps))
    # timer.start()

    sys.exit(app.exec_())

