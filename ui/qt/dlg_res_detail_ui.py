# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt\dlg_res_detail.ui'
#
# Created: Mon Feb 04 16:14:37 2013
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_tablePreviewDialog(object):
    def setupUi(self, tablePreviewDialog):
        tablePreviewDialog.setObjectName(_fromUtf8("tablePreviewDialog"))
        tablePreviewDialog.resize(367, 380)
        self.table_result = QtGui.QTableView(tablePreviewDialog)
        self.table_result.setGeometry(QtCore.QRect(10, 40, 331, 271))
        self.table_result.setObjectName(_fromUtf8("table_result"))
        self.lb_title = QtGui.QLabel(tablePreviewDialog)
        self.lb_title.setGeometry(QtCore.QRect(10, 10, 305, 13))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.lb_title.setFont(font)
        self.lb_title.setObjectName(_fromUtf8("lb_title"))
        self.lb_bldgcount = QtGui.QLabel(tablePreviewDialog)
        self.lb_bldgcount.setGeometry(QtCore.QRect(10, 340, 111, 25))
        self.lb_bldgcount.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lb_bldgcount.setObjectName(_fromUtf8("lb_bldgcount"))
        self.txt_bldgcount = QtGui.QLineEdit(tablePreviewDialog)
        self.txt_bldgcount.setGeometry(QtCore.QRect(130, 340, 81, 20))
        self.txt_bldgcount.setObjectName(_fromUtf8("txt_bldgcount"))
        self.btn_ok = QtGui.QPushButton(tablePreviewDialog)
        self.btn_ok.setGeometry(QtCore.QRect(270, 340, 75, 23))
        self.btn_ok.setObjectName(_fromUtf8("btn_ok"))

        self.retranslateUi(tablePreviewDialog)
        QtCore.QMetaObject.connectSlotsByName(tablePreviewDialog)

    def retranslateUi(self, tablePreviewDialog):
        pass

