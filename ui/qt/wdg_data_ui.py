# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt\wdg_data.ui'
#
# Created: Mon Feb 04 13:24:42 2013
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_widgetDataInput(object):
    def setupUi(self, widgetDataInput):
        widgetDataInput.setObjectName(_fromUtf8("widgetDataInput"))
        widgetDataInput.resize(845, 653)
        self.widgetSurvey = QtGui.QWidget(widgetDataInput)
        self.widgetSurvey.setGeometry(QtCore.QRect(0, 310, 401, 181))
        self.widgetSurvey.setObjectName(_fromUtf8("widgetSurvey"))
        self.lb_svy_select_file = QtGui.QLabel(self.widgetSurvey)
        self.lb_svy_select_file.setGeometry(QtCore.QRect(13, 141, 71, 21))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.lb_svy_select_file.setFont(font)
        self.lb_svy_select_file.setObjectName(_fromUtf8("lb_svy_select_file"))
        self.img_lb_svy_desc_help = QtGui.QLabel(self.widgetSurvey)
        self.img_lb_svy_desc_help.setGeometry(QtCore.QRect(280, 40, 16, 21))
        self.img_lb_svy_desc_help.setText(_fromUtf8(""))
        self.img_lb_svy_desc_help.setPixmap(QtGui.QPixmap(_fromUtf8(":/imgs/icons/help.png")))
        self.img_lb_svy_desc_help.setObjectName(_fromUtf8("img_lb_svy_desc_help"))
        self.lb_svy_desc = QtGui.QLabel(self.widgetSurvey)
        self.lb_svy_desc.setGeometry(QtCore.QRect(13, 43, 271, 16))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.lb_svy_desc.setFont(font)
        self.lb_svy_desc.setObjectName(_fromUtf8("lb_svy_desc"))
        self.btn_svy_select_file = QtGui.QToolButton(self.widgetSurvey)
        self.btn_svy_select_file.setEnabled(False)
        self.btn_svy_select_file.setGeometry(QtCore.QRect(360, 140, 41, 19))
        self.btn_svy_select_file.setCursor(QtCore.Qt.ArrowCursor)
        self.btn_svy_select_file.setObjectName(_fromUtf8("btn_svy_select_file"))
        self.radio_svy_op3 = QtGui.QRadioButton(self.widgetSurvey)
        self.radio_svy_op3.setGeometry(QtCore.QRect(16, 107, 381, 17))
        self.radio_svy_op3.setObjectName(_fromUtf8("radio_svy_op3"))
        self.radio_svy_op1 = QtGui.QRadioButton(self.widgetSurvey)
        self.radio_svy_op1.setGeometry(QtCore.QRect(16, 67, 381, 17))
        self.radio_svy_op1.setChecked(True)
        self.radio_svy_op1.setObjectName(_fromUtf8("radio_svy_op1"))
        self.radio_svy_op2 = QtGui.QRadioButton(self.widgetSurvey)
        self.radio_svy_op2.setGeometry(QtCore.QRect(16, 87, 381, 17))
        self.radio_svy_op2.setObjectName(_fromUtf8("radio_svy_op2"))
        self.txt_svy_select_file = QtGui.QLineEdit(self.widgetSurvey)
        self.txt_svy_select_file.setEnabled(False)
        self.txt_svy_select_file.setGeometry(QtCore.QRect(93, 141, 261, 20))
        self.txt_svy_select_file.setObjectName(_fromUtf8("txt_svy_select_file"))
        self.lb_svy_title = QtGui.QLabel(self.widgetSurvey)
        self.lb_svy_title.setGeometry(QtCore.QRect(10, 10, 331, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setWeight(75)
        font.setBold(True)
        self.lb_svy_title.setFont(font)
        self.lb_svy_title.setObjectName(_fromUtf8("lb_svy_title"))
        self.widgetResult = QtGui.QWidget(widgetDataInput)
        self.widgetResult.setGeometry(QtCore.QRect(420, 340, 411, 301))
        self.widgetResult.setObjectName(_fromUtf8("widgetResult"))
        self.lb_verify_title = QtGui.QLabel(self.widgetResult)
        self.lb_verify_title.setGeometry(QtCore.QRect(10, 10, 301, 16))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.lb_verify_title.setFont(font)
        self.lb_verify_title.setObjectName(_fromUtf8("lb_verify_title"))
        self.img_lb_verify_fp = QtGui.QLabel(self.widgetResult)
        self.img_lb_verify_fp.setGeometry(QtCore.QRect(10, 38, 21, 21))
        self.img_lb_verify_fp.setText(_fromUtf8(""))
        self.img_lb_verify_fp.setObjectName(_fromUtf8("img_lb_verify_fp"))
        self.img_lb_verify_zones = QtGui.QLabel(self.widgetResult)
        self.img_lb_verify_zones.setGeometry(QtCore.QRect(10, 59, 21, 21))
        self.img_lb_verify_zones.setText(_fromUtf8(""))
        self.img_lb_verify_zones.setObjectName(_fromUtf8("img_lb_verify_zones"))
        self.lb_verify_fp = QtGui.QLabel(self.widgetResult)
        self.lb_verify_fp.setGeometry(QtCore.QRect(40, 38, 111, 20))
        self.lb_verify_fp.setObjectName(_fromUtf8("lb_verify_fp"))
        self.lb_verify_svy = QtGui.QLabel(self.widgetResult)
        self.lb_verify_svy.setGeometry(QtCore.QRect(40, 80, 111, 20))
        self.lb_verify_svy.setObjectName(_fromUtf8("lb_verify_svy"))
        self.lb_verify_zones = QtGui.QLabel(self.widgetResult)
        self.lb_verify_zones.setGeometry(QtCore.QRect(40, 59, 111, 20))
        self.lb_verify_zones.setObjectName(_fromUtf8("lb_verify_zones"))
        self.img_lb_verify_svy = QtGui.QLabel(self.widgetResult)
        self.img_lb_verify_svy.setGeometry(QtCore.QRect(10, 80, 21, 21))
        self.img_lb_verify_svy.setText(_fromUtf8(""))
        self.img_lb_verify_svy.setObjectName(_fromUtf8("img_lb_verify_svy"))
        self.lb_verify_aggregation = QtGui.QLabel(self.widgetResult)
        self.lb_verify_aggregation.setGeometry(QtCore.QRect(10, 113, 171, 16))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.lb_verify_aggregation.setFont(font)
        self.lb_verify_aggregation.setObjectName(_fromUtf8("lb_verify_aggregation"))
        self.img_lb_verify_agg_grid = QtGui.QLabel(self.widgetResult)
        self.img_lb_verify_agg_grid.setGeometry(QtCore.QRect(10, 150, 21, 21))
        self.img_lb_verify_agg_grid.setText(_fromUtf8(""))
        self.img_lb_verify_agg_grid.setObjectName(_fromUtf8("img_lb_verify_agg_grid"))
        self.img_lb_verify_agg_zone = QtGui.QLabel(self.widgetResult)
        self.img_lb_verify_agg_zone.setGeometry(QtCore.QRect(10, 130, 21, 21))
        self.img_lb_verify_agg_zone.setText(_fromUtf8(""))
        self.img_lb_verify_agg_zone.setObjectName(_fromUtf8("img_lb_verify_agg_zone"))
        self.lb_verify_agg_zone = QtGui.QLabel(self.widgetResult)
        self.lb_verify_agg_zone.setGeometry(QtCore.QRect(40, 130, 131, 20))
        self.lb_verify_agg_zone.setObjectName(_fromUtf8("lb_verify_agg_zone"))
        self.lb_verify_agg_grid = QtGui.QLabel(self.widgetResult)
        self.lb_verify_agg_grid.setGeometry(QtCore.QRect(40, 150, 131, 20))
        self.lb_verify_agg_grid.setObjectName(_fromUtf8("lb_verify_agg_grid"))
        self.txt_verify_text = QtGui.QTextBrowser(self.widgetResult)
        self.txt_verify_text.setEnabled(False)
        self.txt_verify_text.setGeometry(QtCore.QRect(170, 40, 221, 201))
        self.txt_verify_text.setObjectName(_fromUtf8("txt_verify_text"))
        self.btn_verify = QtGui.QPushButton(self.widgetResult)
        self.btn_verify.setEnabled(True)
        self.btn_verify.setGeometry(QtCore.QRect(260, 270, 141, 23))
        self.btn_verify.setCursor(QtCore.Qt.ArrowCursor)
        self.btn_verify.setObjectName(_fromUtf8("btn_verify"))
        self.widgetAggr = QtGui.QWidget(widgetDataInput)
        self.widgetAggr.setGeometry(QtCore.QRect(0, 490, 401, 151))
        self.widgetAggr.setObjectName(_fromUtf8("widgetAggr"))
        self.radio_aggr_op2 = QtGui.QRadioButton(self.widgetAggr)
        self.radio_aggr_op2.setGeometry(QtCore.QRect(14, 92, 381, 17))
        self.radio_aggr_op2.setObjectName(_fromUtf8("radio_aggr_op2"))
        self.lb_aggr_desc = QtGui.QLabel(self.widgetAggr)
        self.lb_aggr_desc.setGeometry(QtCore.QRect(10, 43, 281, 16))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.lb_aggr_desc.setFont(font)
        self.lb_aggr_desc.setObjectName(_fromUtf8("lb_aggr_desc"))
        self.lb_aggr_title = QtGui.QLabel(self.widgetAggr)
        self.lb_aggr_title.setGeometry(QtCore.QRect(10, 10, 331, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setWeight(75)
        font.setBold(True)
        self.lb_aggr_title.setFont(font)
        self.lb_aggr_title.setObjectName(_fromUtf8("lb_aggr_title"))
        self.radio_aggr_op1 = QtGui.QRadioButton(self.widgetAggr)
        self.radio_aggr_op1.setGeometry(QtCore.QRect(14, 71, 381, 17))
        self.radio_aggr_op1.setObjectName(_fromUtf8("radio_aggr_op1"))
        self.img_lb_aggr_desc_help = QtGui.QLabel(self.widgetAggr)
        self.img_lb_aggr_desc_help.setGeometry(QtCore.QRect(291, 41, 16, 21))
        self.img_lb_aggr_desc_help.setText(_fromUtf8(""))
        self.img_lb_aggr_desc_help.setPixmap(QtGui.QPixmap(_fromUtf8(":/imgs/icons/help.png")))
        self.img_lb_aggr_desc_help.setObjectName(_fromUtf8("img_lb_aggr_desc_help"))
        self.btn_aggr_grid_select_file = QtGui.QToolButton(self.widgetAggr)
        self.btn_aggr_grid_select_file.setEnabled(False)
        self.btn_aggr_grid_select_file.setGeometry(QtCore.QRect(360, 120, 41, 19))
        self.btn_aggr_grid_select_file.setCursor(QtCore.Qt.ArrowCursor)
        self.btn_aggr_grid_select_file.setObjectName(_fromUtf8("btn_aggr_grid_select_file"))
        self.txt_aggr_grid_select_file = QtGui.QLineEdit(self.widgetAggr)
        self.txt_aggr_grid_select_file.setEnabled(False)
        self.txt_aggr_grid_select_file.setGeometry(QtCore.QRect(80, 120, 271, 20))
        self.txt_aggr_grid_select_file.setObjectName(_fromUtf8("txt_aggr_grid_select_file"))
        self.lb_aggr_grid_select_file = QtGui.QLabel(self.widgetAggr)
        self.lb_aggr_grid_select_file.setGeometry(QtCore.QRect(10, 120, 71, 21))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.lb_aggr_grid_select_file.setFont(font)
        self.lb_aggr_grid_select_file.setObjectName(_fromUtf8("lb_aggr_grid_select_file"))
        self.widgetFootprint = QtGui.QWidget(widgetDataInput)
        self.widgetFootprint.setGeometry(QtCore.QRect(0, 90, 401, 221))
        self.widgetFootprint.setObjectName(_fromUtf8("widgetFootprint"))
        self.cb_fp_story_field = QtGui.QComboBox(self.widgetFootprint)
        self.cb_fp_story_field.setEnabled(False)
        self.cb_fp_story_field.setGeometry(QtCore.QRect(280, 152, 121, 22))
        self.cb_fp_story_field.setObjectName(_fromUtf8("cb_fp_story_field"))
        self.radio_fp_op2 = QtGui.QRadioButton(self.widgetFootprint)
        self.radio_fp_op2.setGeometry(QtCore.QRect(13, 80, 381, 17))
        self.radio_fp_op2.setObjectName(_fromUtf8("radio_fp_op2"))
        self.txt_fp_select_file = QtGui.QLineEdit(self.widgetFootprint)
        self.txt_fp_select_file.setEnabled(False)
        self.txt_fp_select_file.setGeometry(QtCore.QRect(80, 122, 271, 20))
        self.txt_fp_select_file.setObjectName(_fromUtf8("txt_fp_select_file"))
        self.lb_fp_select_file = QtGui.QLabel(self.widgetFootprint)
        self.lb_fp_select_file.setGeometry(QtCore.QRect(10, 122, 71, 21))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.lb_fp_select_file.setFont(font)
        self.lb_fp_select_file.setObjectName(_fromUtf8("lb_fp_select_file"))
        self.radio_fp_op3 = QtGui.QRadioButton(self.widgetFootprint)
        self.radio_fp_op3.setGeometry(QtCore.QRect(13, 100, 381, 17))
        self.radio_fp_op3.setObjectName(_fromUtf8("radio_fp_op3"))
        self.lb_fp_title = QtGui.QLabel(self.widgetFootprint)
        self.lb_fp_title.setGeometry(QtCore.QRect(3, 3, 341, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setWeight(75)
        font.setBold(True)
        self.lb_fp_title.setFont(font)
        self.lb_fp_title.setObjectName(_fromUtf8("lb_fp_title"))
        self.lb_fp_desc = QtGui.QLabel(self.widgetFootprint)
        self.lb_fp_desc.setGeometry(QtCore.QRect(4, 38, 305, 13))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.lb_fp_desc.setFont(font)
        self.lb_fp_desc.setObjectName(_fromUtf8("lb_fp_desc"))
        self.cb_fp_proj = QtGui.QComboBox(self.widgetFootprint)
        self.cb_fp_proj.setEnabled(False)
        self.cb_fp_proj.setGeometry(QtCore.QRect(280, 180, 121, 22))
        self.cb_fp_proj.setObjectName(_fromUtf8("cb_fp_proj"))
        self.lb_fp_proj = QtGui.QLabel(self.widgetFootprint)
        self.lb_fp_proj.setGeometry(QtCore.QRect(10, 182, 151, 21))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.lb_fp_proj.setFont(font)
        self.lb_fp_proj.setObjectName(_fromUtf8("lb_fp_proj"))
        self.btn_fp_select_file = QtGui.QToolButton(self.widgetFootprint)
        self.btn_fp_select_file.setEnabled(False)
        self.btn_fp_select_file.setGeometry(QtCore.QRect(360, 120, 41, 19))
        self.btn_fp_select_file.setCursor(QtCore.Qt.ArrowCursor)
        self.btn_fp_select_file.setObjectName(_fromUtf8("btn_fp_select_file"))
        self.radio_fp_op1 = QtGui.QRadioButton(self.widgetFootprint)
        self.radio_fp_op1.setGeometry(QtCore.QRect(13, 60, 381, 17))
        self.radio_fp_op1.setChecked(True)
        self.radio_fp_op1.setObjectName(_fromUtf8("radio_fp_op1"))
        self.lb_fp_story_field = QtGui.QLabel(self.widgetFootprint)
        self.lb_fp_story_field.setGeometry(QtCore.QRect(10, 152, 241, 21))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.lb_fp_story_field.setFont(font)
        self.lb_fp_story_field.setObjectName(_fromUtf8("lb_fp_story_field"))
        self.img_lb_fp_desc_help = QtGui.QLabel(self.widgetFootprint)
        self.img_lb_fp_desc_help.setGeometry(QtCore.QRect(321, 34, 16, 21))
        self.img_lb_fp_desc_help.setText(_fromUtf8(""))
        self.img_lb_fp_desc_help.setPixmap(QtGui.QPixmap(_fromUtf8(":/imgs/icons/help.png")))
        self.img_lb_fp_desc_help.setObjectName(_fromUtf8("img_lb_fp_desc_help"))
        self.widgetTitle = QtGui.QWidget(widgetDataInput)
        self.widgetTitle.setGeometry(QtCore.QRect(0, 0, 831, 91))
        self.widgetTitle.setObjectName(_fromUtf8("widgetTitle"))
        self.lb_panel_title = QtGui.QLabel(self.widgetTitle)
        self.lb_panel_title.setGeometry(QtCore.QRect(10, 0, 761, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setWeight(75)
        font.setBold(True)
        self.lb_panel_title.setFont(font)
        self.lb_panel_title.setObjectName(_fromUtf8("lb_panel_title"))
        self.txt_panel_description = QtGui.QTextEdit(self.widgetTitle)
        self.txt_panel_description.setGeometry(QtCore.QRect(10, 30, 761, 51))
        self.txt_panel_description.setObjectName(_fromUtf8("txt_panel_description"))
        self.widgetZones = QtGui.QWidget(widgetDataInput)
        self.widgetZones.setGeometry(QtCore.QRect(420, 90, 411, 241))
        self.widgetZones.setObjectName(_fromUtf8("widgetZones"))
        self.radio_zones_op3 = QtGui.QRadioButton(self.widgetZones)
        self.radio_zones_op3.setGeometry(QtCore.QRect(14, 94, 391, 17))
        self.radio_zones_op3.setObjectName(_fromUtf8("radio_zones_op3"))
        self.radio_zones_op2 = QtGui.QRadioButton(self.widgetZones)
        self.radio_zones_op2.setGeometry(QtCore.QRect(14, 74, 391, 17))
        self.radio_zones_op2.setObjectName(_fromUtf8("radio_zones_op2"))
        self.lb_zones_proj = QtGui.QLabel(self.widgetZones)
        self.lb_zones_proj.setGeometry(QtCore.QRect(10, 210, 151, 21))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.lb_zones_proj.setFont(font)
        self.lb_zones_proj.setObjectName(_fromUtf8("lb_zones_proj"))
        self.lb_zones_select_file = QtGui.QLabel(self.widgetZones)
        self.lb_zones_select_file.setGeometry(QtCore.QRect(10, 121, 71, 21))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.lb_zones_select_file.setFont(font)
        self.lb_zones_select_file.setObjectName(_fromUtf8("lb_zones_select_file"))
        self.radio_zones_op1 = QtGui.QRadioButton(self.widgetZones)
        self.radio_zones_op1.setGeometry(QtCore.QRect(14, 54, 391, 17))
        self.radio_zones_op1.setChecked(True)
        self.radio_zones_op1.setObjectName(_fromUtf8("radio_zones_op1"))
        self.cb_zones_class_field = QtGui.QComboBox(self.widgetZones)
        self.cb_zones_class_field.setEnabled(False)
        self.cb_zones_class_field.setGeometry(QtCore.QRect(280, 150, 121, 22))
        self.cb_zones_class_field.setObjectName(_fromUtf8("cb_zones_class_field"))
        self.lb_zones_class_field = QtGui.QLabel(self.widgetZones)
        self.lb_zones_class_field.setGeometry(QtCore.QRect(10, 151, 281, 21))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.lb_zones_class_field.setFont(font)
        self.lb_zones_class_field.setObjectName(_fromUtf8("lb_zones_class_field"))
        self.lb_zones_title = QtGui.QLabel(self.widgetZones)
        self.lb_zones_title.setGeometry(QtCore.QRect(4, 4, 371, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setWeight(75)
        font.setBold(True)
        self.lb_zones_title.setFont(font)
        self.lb_zones_title.setObjectName(_fromUtf8("lb_zones_title"))
        self.btn_zones_select_file = QtGui.QToolButton(self.widgetZones)
        self.btn_zones_select_file.setEnabled(False)
        self.btn_zones_select_file.setGeometry(QtCore.QRect(360, 120, 41, 19))
        self.btn_zones_select_file.setCursor(QtCore.Qt.ArrowCursor)
        self.btn_zones_select_file.setObjectName(_fromUtf8("btn_zones_select_file"))
        self.cb_zones_proj = QtGui.QComboBox(self.widgetZones)
        self.cb_zones_proj.setEnabled(False)
        self.cb_zones_proj.setGeometry(QtCore.QRect(280, 210, 121, 22))
        self.cb_zones_proj.setObjectName(_fromUtf8("cb_zones_proj"))
        self.txt_zones_select_file = QtGui.QLineEdit(self.widgetZones)
        self.txt_zones_select_file.setEnabled(False)
        self.txt_zones_select_file.setGeometry(QtCore.QRect(80, 121, 271, 20))
        self.txt_zones_select_file.setObjectName(_fromUtf8("txt_zones_select_file"))
        self.lb_zones_desc = QtGui.QLabel(self.widgetZones)
        self.lb_zones_desc.setGeometry(QtCore.QRect(5, 35, 251, 16))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.lb_zones_desc.setFont(font)
        self.lb_zones_desc.setObjectName(_fromUtf8("lb_zones_desc"))
        self.img_lb_zones_desc_help = QtGui.QLabel(self.widgetZones)
        self.img_lb_zones_desc_help.setGeometry(QtCore.QRect(246, 32, 16, 21))
        self.img_lb_zones_desc_help.setText(_fromUtf8(""))
        self.img_lb_zones_desc_help.setPixmap(QtGui.QPixmap(_fromUtf8(":/imgs/icons/help.png")))
        self.img_lb_zones_desc_help.setObjectName(_fromUtf8("img_lb_zones_desc_help"))
        self.lb_zones_count_field = QtGui.QLabel(self.widgetZones)
        self.lb_zones_count_field.setGeometry(QtCore.QRect(10, 180, 271, 21))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.lb_zones_count_field.setFont(font)
        self.lb_zones_count_field.setObjectName(_fromUtf8("lb_zones_count_field"))
        self.cb_zones_count_field = QtGui.QComboBox(self.widgetZones)
        self.cb_zones_count_field.setEnabled(False)
        self.cb_zones_count_field.setGeometry(QtCore.QRect(280, 180, 121, 22))
        self.cb_zones_count_field.setObjectName(_fromUtf8("cb_zones_count_field"))

        self.retranslateUi(widgetDataInput)
        QtCore.QMetaObject.connectSlotsByName(widgetDataInput)
        widgetDataInput.setTabOrder(self.radio_fp_op1, self.radio_fp_op2)
        widgetDataInput.setTabOrder(self.radio_fp_op2, self.radio_fp_op3)
        widgetDataInput.setTabOrder(self.radio_fp_op3, self.txt_fp_select_file)
        widgetDataInput.setTabOrder(self.txt_fp_select_file, self.btn_fp_select_file)
        widgetDataInput.setTabOrder(self.btn_fp_select_file, self.cb_fp_story_field)
        widgetDataInput.setTabOrder(self.cb_fp_story_field, self.cb_fp_proj)
        widgetDataInput.setTabOrder(self.cb_fp_proj, self.radio_svy_op1)
        widgetDataInput.setTabOrder(self.radio_svy_op1, self.radio_svy_op2)
        widgetDataInput.setTabOrder(self.radio_svy_op2, self.radio_svy_op3)
        widgetDataInput.setTabOrder(self.radio_svy_op3, self.txt_svy_select_file)
        widgetDataInput.setTabOrder(self.txt_svy_select_file, self.btn_svy_select_file)
        widgetDataInput.setTabOrder(self.btn_svy_select_file, self.radio_aggr_op1)
        widgetDataInput.setTabOrder(self.radio_aggr_op1, self.radio_aggr_op2)
        widgetDataInput.setTabOrder(self.radio_aggr_op2, self.radio_zones_op1)
        widgetDataInput.setTabOrder(self.radio_zones_op1, self.radio_zones_op2)
        widgetDataInput.setTabOrder(self.radio_zones_op2, self.radio_zones_op3)
        widgetDataInput.setTabOrder(self.radio_zones_op3, self.txt_zones_select_file)
        widgetDataInput.setTabOrder(self.txt_zones_select_file, self.btn_zones_select_file)
        widgetDataInput.setTabOrder(self.btn_zones_select_file, self.cb_zones_class_field)
        widgetDataInput.setTabOrder(self.cb_zones_class_field, self.cb_zones_proj)
        widgetDataInput.setTabOrder(self.cb_zones_proj, self.btn_verify)
        widgetDataInput.setTabOrder(self.btn_verify, self.txt_panel_description)
        widgetDataInput.setTabOrder(self.txt_panel_description, self.txt_verify_text)

    def retranslateUi(self, widgetDataInput):
        widgetDataInput.setWindowTitle(QtGui.QApplication.translate("widgetDataInput", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_svy_select_file.setText(QtGui.QApplication.translate("widgetDataInput", "Select file:", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_svy_desc.setText(QtGui.QApplication.translate("widgetDataInput", "What type of survey / field data do you have?", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_svy_select_file.setText(QtGui.QApplication.translate("widgetDataInput", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.radio_svy_op3.setText(QtGui.QApplication.translate("widgetDataInput", "Sampled buildings from survey area", None, QtGui.QApplication.UnicodeUTF8))
        self.radio_svy_op1.setText(QtGui.QApplication.translate("widgetDataInput", "No Data", None, QtGui.QApplication.UnicodeUTF8))
        self.radio_svy_op2.setText(QtGui.QApplication.translate("widgetDataInput", "Complete building stock/survey area", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_svy_title.setText(QtGui.QApplication.translate("widgetDataInput", "Survey & field data", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_verify_title.setText(QtGui.QApplication.translate("widgetDataInput", "You have supplied the following types of data:", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_verify_fp.setText(QtGui.QApplication.translate("widgetDataInput", "Footprint", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_verify_svy.setText(QtGui.QApplication.translate("widgetDataInput", "Survey", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_verify_zones.setText(QtGui.QApplication.translate("widgetDataInput", "Zones", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_verify_aggregation.setText(QtGui.QApplication.translate("widgetDataInput", "With aggregation", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_verify_agg_zone.setText(QtGui.QApplication.translate("widgetDataInput", "Zone", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_verify_agg_grid.setText(QtGui.QApplication.translate("widgetDataInput", "GED Compatible Grid", None, QtGui.QApplication.UnicodeUTF8))
        self.txt_verify_text.setHtml(QtGui.QApplication.translate("widgetDataInput", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-size:8pt;\"></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_verify.setText(QtGui.QApplication.translate("widgetDataInput", "Verify Input Data", None, QtGui.QApplication.UnicodeUTF8))
        self.radio_aggr_op2.setText(QtGui.QApplication.translate("widgetDataInput", "GED Compatible 30 arc-second grid", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_aggr_desc.setText(QtGui.QApplication.translate("widgetDataInput", "How do you wish to aggregate your output data?", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_aggr_title.setText(QtGui.QApplication.translate("widgetDataInput", "Aggregation", None, QtGui.QApplication.UnicodeUTF8))
        self.radio_aggr_op1.setText(QtGui.QApplication.translate("widgetDataInput", "Output into defined zones ", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_aggr_grid_select_file.setText(QtGui.QApplication.translate("widgetDataInput", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_aggr_grid_select_file.setText(QtGui.QApplication.translate("widgetDataInput", "Select file:", None, QtGui.QApplication.UnicodeUTF8))
        self.radio_fp_op2.setText(QtGui.QApplication.translate("widgetDataInput", "Building footprints with height", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_fp_select_file.setText(QtGui.QApplication.translate("widgetDataInput", "Select file:", None, QtGui.QApplication.UnicodeUTF8))
        self.radio_fp_op3.setText(QtGui.QApplication.translate("widgetDataInput", "Building footprints without height", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_fp_title.setText(QtGui.QApplication.translate("widgetDataInput", "Building footprint data", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_fp_desc.setText(QtGui.QApplication.translate("widgetDataInput", "What type of data do you have for building footprints?", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_fp_proj.setText(QtGui.QApplication.translate("widgetDataInput", "Select/verify projection:", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_fp_select_file.setText(QtGui.QApplication.translate("widgetDataInput", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.radio_fp_op1.setText(QtGui.QApplication.translate("widgetDataInput", "No Data", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_fp_story_field.setText(QtGui.QApplication.translate("widgetDataInput", "Select field containing number of stories:", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_panel_title.setText(QtGui.QApplication.translate("widgetDataInput", "Define study region", None, QtGui.QApplication.UnicodeUTF8))
        self.txt_panel_description.setHtml(QtGui.QApplication.translate("widgetDataInput", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'Tahoma\'; font-size:8pt;\">Study region automatically aggregated from input building footprint</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.radio_zones_op3.setText(QtGui.QApplication.translate("widgetDataInput", "Land use zones with building count", None, QtGui.QApplication.UnicodeUTF8))
        self.radio_zones_op2.setText(QtGui.QApplication.translate("widgetDataInput", "Land use zones", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_zones_proj.setText(QtGui.QApplication.translate("widgetDataInput", "Select/verify projection:", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_zones_select_file.setText(QtGui.QApplication.translate("widgetDataInput", "Select file:", None, QtGui.QApplication.UnicodeUTF8))
        self.radio_zones_op1.setText(QtGui.QApplication.translate("widgetDataInput", "No Data", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_zones_class_field.setText(QtGui.QApplication.translate("widgetDataInput", "Select field containing land use/class attributes:", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_zones_title.setText(QtGui.QApplication.translate("widgetDataInput", "Zonal data", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_zones_select_file.setText(QtGui.QApplication.translate("widgetDataInput", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_zones_desc.setText(QtGui.QApplication.translate("widgetDataInput", "What type of data do you have for zones?", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_zones_count_field.setText(QtGui.QApplication.translate("widgetDataInput", "Select field containing building count", None, QtGui.QApplication.UnicodeUTF8))

import SIDDResource_rc
