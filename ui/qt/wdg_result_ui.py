# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt\wdg_result.ui'
#
# Created: Tue May 07 14:56:31 2013
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_widgetResult(object):
    def setupUi(self, widgetResult):
        widgetResult.setObjectName(_fromUtf8("widgetResult"))
        widgetResult.resize(941, 655)
        self.widget_export = QtGui.QWidget(widgetResult)
        self.widget_export.setGeometry(QtCore.QRect(650, 30, 281, 181))
        self.widget_export.setObjectName(_fromUtf8("widget_export"))
        self.btn_export_select_path = QtGui.QToolButton(self.widget_export)
        self.btn_export_select_path.setGeometry(QtCore.QRect(250, 70, 21, 20))
        self.btn_export_select_path.setCursor(QtCore.Qt.OpenHandCursor)
        self.btn_export_select_path.setObjectName(_fromUtf8("btn_export_select_path"))
        self.txt_export_select_path = QtGui.QLineEdit(self.widget_export)
        self.txt_export_select_path.setGeometry(QtCore.QRect(10, 70, 231, 20))
        self.txt_export_select_path.setObjectName(_fromUtf8("txt_export_select_path"))
        self.lb_export_select_path = QtGui.QLabel(self.widget_export)
        self.lb_export_select_path.setGeometry(QtCore.QRect(10, 40, 181, 21))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.lb_export_select_path.setFont(font)
        self.lb_export_select_path.setObjectName(_fromUtf8("lb_export_select_path"))
        self.lb_export_title = QtGui.QLabel(self.widget_export)
        self.lb_export_title.setGeometry(QtCore.QRect(6, 5, 251, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setWeight(75)
        font.setBold(True)
        self.lb_export_title.setFont(font)
        self.lb_export_title.setObjectName(_fromUtf8("lb_export_title"))
        self.btn_export = QtGui.QPushButton(self.widget_export)
        self.btn_export.setGeometry(QtCore.QRect(200, 150, 75, 23))
        self.btn_export.setObjectName(_fromUtf8("btn_export"))
        self.cb_export_format = QtGui.QComboBox(self.widget_export)
        self.cb_export_format.setGeometry(QtCore.QRect(10, 120, 261, 22))
        self.cb_export_format.setObjectName(_fromUtf8("cb_export_format"))
        self.lb_export_format = QtGui.QLabel(self.widget_export)
        self.lb_export_format.setGeometry(QtCore.QRect(10, 90, 181, 21))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.lb_export_format.setFont(font)
        self.lb_export_format.setObjectName(_fromUtf8("lb_export_format"))
        self.widget_dq_test = QtGui.QWidget(widgetResult)
        self.widget_dq_test.setGeometry(QtCore.QRect(650, 220, 281, 401))
        self.widget_dq_test.setObjectName(_fromUtf8("widget_dq_test"))
        self.lbl_dq_test_title = QtGui.QLabel(self.widget_dq_test)
        self.lbl_dq_test_title.setGeometry(QtCore.QRect(10, 10, 251, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setWeight(75)
        font.setBold(True)
        self.lbl_dq_test_title.setFont(font)
        self.lbl_dq_test_title.setObjectName(_fromUtf8("lbl_dq_test_title"))
        self.txt_dq_test_details = QtGui.QTextBrowser(self.widget_dq_test)
        self.txt_dq_test_details.setGeometry(QtCore.QRect(10, 40, 251, 351))
        self.txt_dq_test_details.setObjectName(_fromUtf8("txt_dq_test_details"))
        self.widget_map = QtGui.QWidget(widgetResult)
        self.widget_map.setGeometry(QtCore.QRect(10, 40, 631, 581))
        self.widget_map.setObjectName(_fromUtf8("widget_map"))
        self.widget_map_menu_r = QtGui.QWidget(self.widget_map)
        self.widget_map_menu_r.setGeometry(QtCore.QRect(180, 0, 451, 31))
        self.widget_map_menu_r.setObjectName(_fromUtf8("widget_map_menu_r"))
        self.lb_layer_selector = QtGui.QLabel(self.widget_map_menu_r)
        self.lb_layer_selector.setGeometry(QtCore.QRect(0, 0, 171, 21))
        self.lb_layer_selector.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lb_layer_selector.setObjectName(_fromUtf8("lb_layer_selector"))
        self.cb_layer_selector = QtGui.QComboBox(self.widget_map_menu_r)
        self.cb_layer_selector.setGeometry(QtCore.QRect(180, 0, 141, 22))
        self.cb_layer_selector.setObjectName(_fromUtf8("cb_layer_selector"))
        self.btn_theme = QtGui.QPushButton(self.widget_map_menu_r)
        self.btn_theme.setGeometry(QtCore.QRect(360, 0, 31, 23))
        self.btn_theme.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/imgs/icons/pie_chart.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_theme.setIcon(icon)
        self.btn_theme.setObjectName(_fromUtf8("btn_theme"))
        self.btn_info = QtGui.QPushButton(self.widget_map_menu_r)
        self.btn_info.setGeometry(QtCore.QRect(420, 0, 31, 23))
        self.btn_info.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/imgs/icons/information.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_info.setIcon(icon1)
        self.btn_info.setObjectName(_fromUtf8("btn_info"))
        self.btn_zoom_to_feature = QtGui.QPushButton(self.widget_map_menu_r)
        self.btn_zoom_to_feature.setGeometry(QtCore.QRect(390, 0, 31, 23))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/imgs/icons/help.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_zoom_to_feature.setIcon(icon2)
        self.btn_zoom_to_feature.setObjectName(_fromUtf8("btn_zoom_to_feature"))
        self.btn_zoom_layer = QtGui.QPushButton(self.widget_map_menu_r)
        self.btn_zoom_layer.setGeometry(QtCore.QRect(330, 0, 31, 23))
        self.btn_zoom_layer.setText(_fromUtf8(""))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/imgs/icons/magnify.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_zoom_layer.setIcon(icon3)
        self.btn_zoom_layer.setObjectName(_fromUtf8("btn_zoom_layer"))
        self.widget_map_menu_l = QtGui.QWidget(self.widget_map)
        self.widget_map_menu_l.setGeometry(QtCore.QRect(0, 0, 161, 31))
        self.widget_map_menu_l.setObjectName(_fromUtf8("widget_map_menu_l"))
        self.btn_zoom_in = QtGui.QPushButton(self.widget_map_menu_l)
        self.btn_zoom_in.setGeometry(QtCore.QRect(0, 0, 31, 23))
        self.btn_zoom_in.setText(_fromUtf8(""))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/imgs/icons/magnify_plus.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_zoom_in.setIcon(icon4)
        self.btn_zoom_in.setObjectName(_fromUtf8("btn_zoom_in"))
        self.btn_pan = QtGui.QPushButton(self.widget_map_menu_l)
        self.btn_pan.setGeometry(QtCore.QRect(60, 0, 31, 23))
        self.btn_pan.setText(_fromUtf8(""))
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(_fromUtf8(":/imgs/icons/arrows_4_way.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_pan.setIcon(icon5)
        self.btn_pan.setObjectName(_fromUtf8("btn_pan"))
        self.btn_zoom_out = QtGui.QPushButton(self.widget_map_menu_l)
        self.btn_zoom_out.setGeometry(QtCore.QRect(30, 0, 31, 23))
        self.btn_zoom_out.setText(_fromUtf8(""))
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(_fromUtf8(":/imgs/icons/magnify_minus.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_zoom_out.setIcon(icon6)
        self.btn_zoom_out.setObjectName(_fromUtf8("btn_zoom_out"))
        self.btn_zoom_full = QtGui.QPushButton(self.widget_map_menu_l)
        self.btn_zoom_full.setGeometry(QtCore.QRect(90, 0, 31, 23))
        self.btn_zoom_full.setText(_fromUtf8(""))
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(_fromUtf8(":/imgs/icons/world.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_zoom_full.setIcon(icon7)
        self.btn_zoom_full.setObjectName(_fromUtf8("btn_zoom_full"))
        self.lb_panel_title = QtGui.QLabel(widgetResult)
        self.lb_panel_title.setGeometry(QtCore.QRect(10, 0, 591, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setWeight(75)
        font.setBold(True)
        self.lb_panel_title.setFont(font)
        self.lb_panel_title.setObjectName(_fromUtf8("lb_panel_title"))

        self.retranslateUi(widgetResult)
        QtCore.QMetaObject.connectSlotsByName(widgetResult)

    def retranslateUi(self, widgetResult):
        widgetResult.setWindowTitle(QtGui.QApplication.translate("widgetResult", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_export_select_path.setText(QtGui.QApplication.translate("widgetResult", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_export_select_path.setText(QtGui.QApplication.translate("widgetResult", "Select location to save output:", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_export_title.setText(QtGui.QApplication.translate("widgetResult", "Export Exposure", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_export.setText(QtGui.QApplication.translate("widgetResult", "Export", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_export_format.setText(QtGui.QApplication.translate("widgetResult", "Select Export Data Format", None, QtGui.QApplication.UnicodeUTF8))
        self.lbl_dq_test_title.setText(QtGui.QApplication.translate("widgetResult", "Data Quality Tests", None, QtGui.QApplication.UnicodeUTF8))
        self.txt_dq_test_details.setHtml(QtGui.QApplication.translate("widgetResult", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_layer_selector.setText(QtGui.QApplication.translate("widgetResult", "Selected Layer", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_theme.setToolTip(QtGui.QApplication.translate("widgetResult", "Layer Rendering Options ...", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_info.setToolTip(QtGui.QApplication.translate("widgetResult", "Query Feature in Layer", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_zoom_to_feature.setToolTip(QtGui.QApplication.translate("widgetResult", "Zoom to Feature ...", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_zoom_layer.setToolTip(QtGui.QApplication.translate("widgetResult", "Zoom to Selected Layer", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_zoom_in.setToolTip(QtGui.QApplication.translate("widgetResult", "Zoom In", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_pan.setToolTip(QtGui.QApplication.translate("widgetResult", "Pan", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_zoom_out.setToolTip(QtGui.QApplication.translate("widgetResult", "Zoom Out", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_zoom_full.setToolTip(QtGui.QApplication.translate("widgetResult", "Zoom to Full Extent", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_panel_title.setText(QtGui.QApplication.translate("widgetResult", "Preview", None, QtGui.QApplication.UnicodeUTF8))

import SIDDResource_rc