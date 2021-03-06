# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5.QtCore import pyqtSlot, QDate, QTimer, QTime, Qt, QObject, QThread, pyqtSignal, QThreadPool, QRunnable, QTranslator
from PyQt5.QtWidgets import QLabel, QPushButton, QAction, QApplication, QLineEdit, QMainWindow, QMenu, QWidgetAction, QMessageBox
from PyQt5.QtGui import QImage, QPixmap
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 720)
        MainWindow.setMinimumSize(QtCore.QSize(1280, 720))
        MainWindow.setStyleSheet("\n"
"/* VERTICAL SCROLLBAR */\n"
" QScrollBar:vertical {\n"
"    background-color: transparent;\n"
"    border: none;\n"
"    width: 20px;\n"
"    margin: 10px 10px 10px 0px;\n"
" }\n"
"\n"
"/*  HANDLE BAR VERTICAL */\n"
"QScrollBar::handle:vertical {    \n"
"    background-color: rgb(188, 188, 188);\n"
"    min-height: 50px;\n"
"    border-radius: 5px;\n"
"}\n"
"QScrollBar::handle:vertical:hover{    \n"
"}\n"
"QScrollBar::handle:vertical:pressed {    \n"
"}\n"
"\n"
"/* BTN TOP - SCROLLBAR */\n"
"QScrollBar::sub-line:vertical {\n"
"    border: none;\n"
"    background-color: transparent;\n"
"    height: 10px;\n"
"}\n"
"\n"
"/* BTN BOTTOM - SCROLLBAR */\n"
"QScrollBar::add-line:vertical {\n"
"    border: none;\n"
"    background-color: transparent;\n"
"    height: 10px;\n"
"}\n"
"\n"
"/* RESET ARROW */\n"
"QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
"    background: none;\n"
"}\n"
"QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
"    background: none;\n"
"}\n"
"\n"
"QWidget{\n"
"    background-color: rgb(69, 90, 100);\n"
"}\n"
"")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("")
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(20, 20, 20, 20)
        self.gridLayout.setSpacing(20)
        self.gridLayout.setObjectName("gridLayout")
        self.stacked_widget = QtWidgets.QStackedWidget(self.centralwidget)
        self.stacked_widget.setObjectName("stacked_widget")
        self.page_1 = QtWidgets.QWidget()
        self.page_1.setObjectName("page_1")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.page_1)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.layout_report_area = QtWidgets.QFormLayout()
        self.layout_report_area.setHorizontalSpacing(0)
        self.layout_report_area.setVerticalSpacing(20)
        self.layout_report_area.setObjectName("layout_report_area")
        self.label_identified_list = QtWidgets.QLabel(self.page_1)
        self.label_identified_list.setStyleSheet("font: 10pt;\n"
"font-weight: bold;\n"
"color: rgb(255, 255, 255);")
        self.label_identified_list.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_identified_list.setObjectName("label_identified_list")
        self.layout_report_area.setWidget(2, QtWidgets.QFormLayout.SpanningRole, self.label_identified_list)
        self.scroll_report_area = QtWidgets.QScrollArea(self.page_1)
        self.scroll_report_area.setStyleSheet("background-color: rgb(238, 238, 238);\n"
"border-radius: 5px;")
        self.scroll_report_area.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scroll_report_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scroll_report_area.setWidgetResizable(True)
        self.scroll_report_area.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.scroll_report_area.setObjectName("scroll_report_area")
        self.report_container = QtWidgets.QWidget()
        self.report_container.setGeometry(QtCore.QRect(0, 0, 578, 238))
        self.report_container.setObjectName("report_container")
        self.report_container_layout = QtWidgets.QVBoxLayout(self.report_container)
        self.report_container_layout.setContentsMargins(10, 10, 10, 10)
        self.report_container_layout.setSpacing(10)
        self.report_container_layout.setObjectName("report_container_layout")
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.report_container_layout.addItem(spacerItem)
        self.scroll_report_area.setWidget(self.report_container)
        self.layout_report_area.setWidget(3, QtWidgets.QFormLayout.SpanningRole, self.scroll_report_area)
        self.layout_current_status = QtWidgets.QWidget(self.page_1)
        self.layout_current_status.setStyleSheet("background-color: rgb(238, 238, 238);\n"
"border-radius: 5px;")
        self.layout_current_status.setObjectName("layout_current_status")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.layout_current_status)
        self.verticalLayout_3.setContentsMargins(10, 10, 10, 10)
        self.verticalLayout_3.setSpacing(10)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_status_1 = QtWidgets.QLabel(self.layout_current_status)
        self.label_status_1.setMinimumSize(QtCore.QSize(0, 0))
        self.label_status_1.setStyleSheet("font: 10pt;\n"
"font-weight: bold;")
        self.label_status_1.setObjectName("label_status_1")
        self.verticalLayout_3.addWidget(self.label_status_1)
        self.label_status_2 = QtWidgets.QLabel(self.layout_current_status)
        self.label_status_2.setStyleSheet("font: 10pt;\n"
"font-weight: bold;")
        self.label_status_2.setObjectName("label_status_2")
        self.verticalLayout_3.addWidget(self.label_status_2)
        self.label_status_3 = QtWidgets.QLabel(self.layout_current_status)
        self.label_status_3.setStyleSheet("font: 10pt;\n"
"font-weight: bold;")
        self.label_status_3.setObjectName("label_status_3")
        self.verticalLayout_3.addWidget(self.label_status_3)
        self.layout_report_area.setWidget(1, QtWidgets.QFormLayout.SpanningRole, self.layout_current_status)
        self.label_current_status = QtWidgets.QLabel(self.page_1)
        self.label_current_status.setStyleSheet("font: 10pt;\n"
"font-weight: bold;\n"
"color: rgb(255, 255, 255);")
        self.label_current_status.setObjectName("label_current_status")
        self.layout_report_area.setWidget(0, QtWidgets.QFormLayout.SpanningRole, self.label_current_status)
        self.verticalLayout_2.addLayout(self.layout_report_area)
        self.stacked_widget.addWidget(self.page_1)
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setObjectName("page_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.page_2)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName("verticalLayout")
        self.layout_report_area_2 = QtWidgets.QFormLayout()
        self.layout_report_area_2.setSpacing(10)
        self.layout_report_area_2.setObjectName("layout_report_area_2")
        self.scroll_report_area_2 = QtWidgets.QScrollArea(self.page_2)
        self.scroll_report_area_2.setStyleSheet("background-color: rgb(238, 238, 238);\n"
"border-radius: 5px;")
        self.scroll_report_area_2.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.scroll_report_area_2.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scroll_report_area_2.setWidgetResizable(True)
        self.scroll_report_area_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.scroll_report_area_2.setObjectName("scroll_report_area_2")
        self.report_container_2 = QtWidgets.QWidget()
        self.report_container_2.setGeometry(QtCore.QRect(0, 0, 578, 486))
        self.report_container_2.setObjectName("report_container_2")
        self.report_container_layout_2 = QtWidgets.QVBoxLayout(self.report_container_2)
        self.report_container_layout_2.setContentsMargins(10, 10, 10, 10)
        self.report_container_layout_2.setSpacing(10)
        self.report_container_layout_2.setObjectName("report_container_layout_2")
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.report_container_layout_2.addItem(spacerItem1)
        self.scroll_report_area_2.setWidget(self.report_container_2)
        self.layout_report_area_2.setWidget(0, QtWidgets.QFormLayout.SpanningRole, self.scroll_report_area_2)
        self.verticalLayout.addLayout(self.layout_report_area_2)
        self.stacked_widget.addWidget(self.page_2)
        self.gridLayout.addWidget(self.stacked_widget, 2, 1, 1, 1)
        self.layout_button_page = QtWidgets.QWidget(self.centralwidget)
        self.layout_button_page.setStyleSheet("height: 50px;")
        self.layout_button_page.setObjectName("layout_button_page")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layout_button_page)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.button_page_feed = QtWidgets.QPushButton(self.layout_button_page)
        self.button_page_feed.setStyleSheet("background-color: rgb(238, 238, 238);\n"
"border-top-left-radius: 5px;\n"
"border-bottom-left-radius: 5px;\n"
"font: 10pt;\n"
"font-weight: bold;\n"
"")
        self.button_page_feed.setObjectName("button_page_feed")
        self.horizontalLayout_2.addWidget(self.button_page_feed)
        self.button_page_log = QtWidgets.QPushButton(self.layout_button_page)
        self.button_page_log.setStyleSheet("background-color: rgb(188, 188, 188);\n"
"border-top-right-radius: 5px;\n"
"border-bottom-right-radius: 5px;\n"
"font: 10pt;\n"
"font-weight: regular;")
        self.button_page_log.setObjectName("button_page_log")
        self.horizontalLayout_2.addWidget(self.button_page_log)
        self.gridLayout.addWidget(self.layout_button_page, 1, 1, 1, 1)
        self.layout_information = QtWidgets.QVBoxLayout()
        self.layout_information.setObjectName("layout_information")
        self.label_title = QtWidgets.QLabel(self.centralwidget)
        self.label_title.setMinimumSize(QtCore.QSize(576, 100))
        self.label_title.setStyleSheet("background-color: rgb(238, 238, 238);\n"
"border-radius: 5px;")
        self.label_title.setAlignment(QtCore.Qt.AlignCenter)
        self.label_title.setObjectName("label_title")
        self.layout_information.addWidget(self.label_title)
        self.gridLayout.addLayout(self.layout_information, 0, 1, 1, 1)
        self.label_camera_stream = QtWidgets.QLabel(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_camera_stream.sizePolicy().hasHeightForWidth())
        self.label_camera_stream.setSizePolicy(sizePolicy)
        self.label_camera_stream.setMinimumSize(QtCore.QSize(640, 480))
        self.label_camera_stream.setStyleSheet("background-color: rgb(238, 238, 238);\n"
"border-radius: 5px;")
        self.label_camera_stream.setAlignment(QtCore.Qt.AlignCenter)
        self.label_camera_stream.setObjectName("label_camera_stream")
        self.gridLayout.addWidget(self.label_camera_stream, 0, 0, 3, 1)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.stacked_widget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_identified_list.setText(_translate("MainWindow", "Indentified Person List:"))
        self.label_status_1.setText(_translate("MainWindow", "Identified Person: -"))
        self.label_status_2.setText(_translate("MainWindow", "Unknown Person: -"))
        self.label_status_3.setText(_translate("MainWindow", "Details: -"))
        self.label_current_status.setText(_translate("MainWindow", "Current Status:"))
        self.button_page_feed.setText(_translate("MainWindow", "FEEDS"))
        self.button_page_log.setText(_translate("MainWindow", "LOGS"))
        self.label_title.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\"><span style=\" font-size:12pt; font-weight:600;\">EYE-BEACON V1 DESKTOP DASHBOARD</span></p><p align=\"center\"><span style=\" font-size:12pt;\">Powered by teamaligness</span></p></body></html>"))
        self.label_camera_stream.setText(_translate("MainWindow", "Camera Stream"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
