# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt\dlg_search_feature.ui'
#
# Created: Fri Mar 15 10:56:34 2013
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_searchFeatureDialog(object):
    def setupUi(self, searchFeatureDialog):
        searchFeatureDialog.setObjectName(_fromUtf8("searchFeatureDialog"))
        searchFeatureDialog.resize(359, 162)
        self.lb_title = QtGui.QLabel(searchFeatureDialog)
        self.lb_title.setGeometry(QtCore.QRect(10, 10, 341, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setWeight(75)
        font.setBold(True)
        self.lb_title.setFont(font)
        self.lb_title.setObjectName(_fromUtf8("lb_title"))
        self.btn_find = QtGui.QPushButton(searchFeatureDialog)
        self.btn_find.setGeometry(QtCore.QRect(180, 120, 75, 23))
        self.btn_find.setObjectName(_fromUtf8("btn_find"))
        self.btn_close = QtGui.QPushButton(searchFeatureDialog)
        self.btn_close.setGeometry(QtCore.QRect(260, 120, 75, 23))
        self.btn_close.setObjectName(_fromUtf8("btn_close"))
        self.txt_value = QtGui.QLineEdit(searchFeatureDialog)
        self.txt_value.setGeometry(QtCore.QRect(100, 90, 231, 20))
        self.txt_value.setObjectName(_fromUtf8("txt_value"))
        self.cb_attribute = QtGui.QComboBox(searchFeatureDialog)
        self.cb_attribute.setGeometry(QtCore.QRect(100, 60, 231, 22))
        self.cb_attribute.setObjectName(_fromUtf8("cb_attribute"))
        self.lb_attribute = QtGui.QLabel(searchFeatureDialog)
        self.lb_attribute.setGeometry(QtCore.QRect(20, 60, 46, 13))
        self.lb_attribute.setObjectName(_fromUtf8("lb_attribute"))
        self.lb_value = QtGui.QLabel(searchFeatureDialog)
        self.lb_value.setGeometry(QtCore.QRect(20, 90, 46, 13))
        self.lb_value.setObjectName(_fromUtf8("lb_value"))

        self.retranslateUi(searchFeatureDialog)
        QtCore.QMetaObject.connectSlotsByName(searchFeatureDialog)

    def retranslateUi(self, searchFeatureDialog):
        pass

