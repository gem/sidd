# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt\dlg_base.ui'
#
# Created: Mon Sep 17 15:14:09 2012
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_loadBaseDataDialog(object):
    def setupUi(self, loadBaseDataDialog):
        loadBaseDataDialog.setObjectName(_fromUtf8("loadBaseDataDialog"))
        loadBaseDataDialog.resize(974, 621)
        self.widgetStudyRegion = QtGui.QWidget(loadBaseDataDialog)
        self.widgetStudyRegion.setGeometry(QtCore.QRect(20, 30, 521, 111))
        self.widgetStudyRegion.setObjectName(_fromUtf8("widgetStudyRegion"))
        self.txt_region_desc = QtGui.QTextBrowser(self.widgetStudyRegion)
        self.txt_region_desc.setGeometry(QtCore.QRect(10, 30, 471, 41))
        self.txt_region_desc.setObjectName(_fromUtf8("txt_region_desc"))
        self.btn_region_select_file = QtGui.QPushButton(self.widgetStudyRegion)
        self.btn_region_select_file.setGeometry(QtCore.QRect(320, 80, 41, 19))
        self.btn_region_select_file.setCursor(QtCore.Qt.OpenHandCursor)
        self.btn_region_select_file.setObjectName(_fromUtf8("btn_region_select_file"))
        self.txt_region_select_file = QtGui.QLineEdit(self.widgetStudyRegion)
        self.txt_region_select_file.setGeometry(QtCore.QRect(90, 80, 211, 20))
        self.txt_region_select_file.setObjectName(_fromUtf8("txt_region_select_file"))
        self.lb_region_title = QtGui.QLabel(self.widgetStudyRegion)
        self.lb_region_title.setGeometry(QtCore.QRect(10, 10, 305, 13))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.lb_region_title.setFont(font)
        self.lb_region_title.setObjectName(_fromUtf8("lb_region_title"))
        self.lb_region_select_file = QtGui.QLabel(self.widgetStudyRegion)
        self.lb_region_select_file.setGeometry(QtCore.QRect(10, 80, 71, 21))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.lb_region_select_file.setFont(font)
        self.lb_region_select_file.setObjectName(_fromUtf8("lb_region_select_file"))
        self.btn_close = QtGui.QPushButton(loadBaseDataDialog)
        self.btn_close.setGeometry(QtCore.QRect(870, 580, 75, 23))
        self.btn_close.setObjectName(_fromUtf8("btn_close"))
        self.widgetLoadBuildings = QtGui.QWidget(loadBaseDataDialog)
        self.widgetLoadBuildings.setGeometry(QtCore.QRect(550, 30, 401, 131))
        self.widgetLoadBuildings.setObjectName(_fromUtf8("widgetLoadBuildings"))
        self.lb_buildings_title = QtGui.QLabel(self.widgetLoadBuildings)
        self.lb_buildings_title.setGeometry(QtCore.QRect(10, 10, 305, 13))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.lb_buildings_title.setFont(font)
        self.lb_buildings_title.setObjectName(_fromUtf8("lb_buildings_title"))
        self.txt_buildings_desc = QtGui.QTextBrowser(self.widgetLoadBuildings)
        self.txt_buildings_desc.setGeometry(QtCore.QRect(10, 30, 351, 61))
        self.txt_buildings_desc.setObjectName(_fromUtf8("txt_buildings_desc"))
        self.btn_buildings_load = QtGui.QPushButton(self.widgetLoadBuildings)
        self.btn_buildings_load.setGeometry(QtCore.QRect(290, 100, 75, 23))
        self.btn_buildings_load.setObjectName(_fromUtf8("btn_buildings_load"))
        self.btn_buildings_options = QtGui.QPushButton(self.widgetLoadBuildings)
        self.btn_buildings_options.setGeometry(QtCore.QRect(210, 100, 75, 23))
        self.btn_buildings_options.setObjectName(_fromUtf8("btn_buildings_options"))
        self.widgetLoadZones = QtGui.QWidget(loadBaseDataDialog)
        self.widgetLoadZones.setGeometry(QtCore.QRect(550, 170, 401, 131))
        self.widgetLoadZones.setObjectName(_fromUtf8("widgetLoadZones"))
        self.lb_zones_title = QtGui.QLabel(self.widgetLoadZones)
        self.lb_zones_title.setGeometry(QtCore.QRect(10, 10, 305, 13))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.lb_zones_title.setFont(font)
        self.lb_zones_title.setObjectName(_fromUtf8("lb_zones_title"))
        self.txt_zones_desc = QtGui.QTextBrowser(self.widgetLoadZones)
        self.txt_zones_desc.setGeometry(QtCore.QRect(10, 30, 351, 61))
        self.txt_zones_desc.setObjectName(_fromUtf8("txt_zones_desc"))
        self.btn_zones_load = QtGui.QPushButton(self.widgetLoadZones)
        self.btn_zones_load.setGeometry(QtCore.QRect(290, 100, 75, 23))
        self.btn_zones_load.setObjectName(_fromUtf8("btn_zones_load"))
        self.btn_zones_options = QtGui.QPushButton(self.widgetLoadZones)
        self.btn_zones_options.setGeometry(QtCore.QRect(210, 100, 75, 23))
        self.btn_zones_options.setObjectName(_fromUtf8("btn_zones_options"))
        self.widget_map = QtGui.QWidget(loadBaseDataDialog)
        self.widget_map.setGeometry(QtCore.QRect(20, 150, 521, 451))
        self.widget_map.setObjectName(_fromUtf8("widget_map"))
        self.btn_zoom_in = QtGui.QPushButton(self.widget_map)
        self.btn_zoom_in.setGeometry(QtCore.QRect(370, 0, 31, 23))
        self.btn_zoom_in.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/imgs/icons/magnify_plus.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_zoom_in.setIcon(icon)
        self.btn_zoom_in.setObjectName(_fromUtf8("btn_zoom_in"))
        self.btn_zoom_out = QtGui.QPushButton(self.widget_map)
        self.btn_zoom_out.setGeometry(QtCore.QRect(410, 0, 31, 23))
        self.btn_zoom_out.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/imgs/icons/magnify_minus.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_zoom_out.setIcon(icon1)
        self.btn_zoom_out.setObjectName(_fromUtf8("btn_zoom_out"))
        self.btn_zoom_full = QtGui.QPushButton(self.widget_map)
        self.btn_zoom_full.setGeometry(QtCore.QRect(450, 0, 31, 23))
        self.btn_zoom_full.setText(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/imgs/icons/magnify.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_zoom_full.setIcon(icon2)
        self.btn_zoom_full.setObjectName(_fromUtf8("btn_zoom_full"))
        self.btn_info = QtGui.QPushButton(self.widget_map)
        self.btn_info.setGeometry(QtCore.QRect(490, 0, 31, 23))
        self.btn_info.setText(_fromUtf8(""))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/imgs/icons/information.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_info.setIcon(icon3)
        self.btn_info.setObjectName(_fromUtf8("btn_info"))

        self.retranslateUi(loadBaseDataDialog)
        QtCore.QMetaObject.connectSlotsByName(loadBaseDataDialog)

    def retranslateUi(self, loadBaseDataDialog):
        loadBaseDataDialog.setWindowTitle(QtGui.QApplication.translate("loadBaseDataDialog", "Load Study Region", None, QtGui.QApplication.UnicodeUTF8))
        self.txt_region_desc.setHtml(QtGui.QApplication.translate("loadBaseDataDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Tahoma\'; font-size:8pt;\">You have not provided any building footprint data. Without building footprint, SIDD cannot determine the study region boundary. Please specify study region boundary.</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_region_select_file.setText(QtGui.QApplication.translate("loadBaseDataDialog", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_region_title.setText(QtGui.QApplication.translate("loadBaseDataDialog", "Study Region Boundary", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_region_select_file.setText(QtGui.QApplication.translate("loadBaseDataDialog", "Select file:", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_close.setText(QtGui.QApplication.translate("loadBaseDataDialog", "Close", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_buildings_title.setText(QtGui.QApplication.translate("loadBaseDataDialog", "Loading default building stock from GEM", None, QtGui.QApplication.UnicodeUTF8))
        self.txt_buildings_desc.setHtml(QtGui.QApplication.translate("loadBaseDataDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Tahoma\'; font-size:8pt;\">SIDD can download default building stock data from GEM server for the study region defined. You can use it as base data to create your inventory by reassigning building characteristics</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_buildings_load.setText(QtGui.QApplication.translate("loadBaseDataDialog", "Load", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_buildings_options.setText(QtGui.QApplication.translate("loadBaseDataDialog", "Options", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_zones_title.setText(QtGui.QApplication.translate("loadBaseDataDialog", "Loading default homogeneous zone from GEM", None, QtGui.QApplication.UnicodeUTF8))
        self.txt_zones_desc.setHtml(QtGui.QApplication.translate("loadBaseDataDialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Tahoma\'; font-size:8pt;\">SIDD can download default homogeneous zone data from GEM server for this study region. </span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_zones_load.setText(QtGui.QApplication.translate("loadBaseDataDialog", "Load", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_zones_options.setText(QtGui.QApplication.translate("loadBaseDataDialog", "Options", None, QtGui.QApplication.UnicodeUTF8))

import SIDDResource_rc
