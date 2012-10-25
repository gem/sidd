# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt\dlg_res_detail.ui'
#
# Created: Mon Sep 17 15:14:10 2012
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
        tablePreviewDialog.resize(342, 425)
        self.btnOK = QtGui.QDialogButtonBox(tablePreviewDialog)
        self.btnOK.setGeometry(QtCore.QRect(-20, 370, 341, 32))
        self.btnOK.setOrientation(QtCore.Qt.Horizontal)
        self.btnOK.setStandardButtons(QtGui.QDialogButtonBox.Ok)
        self.btnOK.setObjectName(_fromUtf8("btnOK"))
        self.table_result = QtGui.QTableView(tablePreviewDialog)
        self.table_result.setGeometry(QtCore.QRect(10, 40, 311, 271))
        self.table_result.setObjectName(_fromUtf8("table_result"))
        self.lb_title = QtGui.QLabel(tablePreviewDialog)
        self.lb_title.setGeometry(QtCore.QRect(10, 20, 305, 13))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.lb_title.setFont(font)
        self.lb_title.setObjectName(_fromUtf8("lb_title"))
        self.lb_bldgcount = QtGui.QLabel(tablePreviewDialog)
        self.lb_bldgcount.setGeometry(QtCore.QRect(10, 330, 191, 16))
        self.lb_bldgcount.setObjectName(_fromUtf8("lb_bldgcount"))
        self.txt_bldgcount = QtGui.QLineEdit(tablePreviewDialog)
        self.txt_bldgcount.setGeometry(QtCore.QRect(210, 330, 111, 20))
        self.txt_bldgcount.setObjectName(_fromUtf8("txt_bldgcount"))

        self.retranslateUi(tablePreviewDialog)
        QtCore.QObject.connect(self.btnOK, QtCore.SIGNAL(_fromUtf8("rejected()")), tablePreviewDialog.reject)
        QtCore.QObject.connect(self.btnOK, QtCore.SIGNAL(_fromUtf8("accepted()")), tablePreviewDialog.accept)
        QtCore.QMetaObject.connectSlotsByName(tablePreviewDialog)

    def retranslateUi(self, tablePreviewDialog):
        tablePreviewDialog.setWindowTitle(QtGui.QApplication.translate("tablePreviewDialog", "Feature Details", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_title.setText(QtGui.QApplication.translate("tablePreviewDialog", "Exposure Distribution for Selected Region", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_bldgcount.setText(QtGui.QApplication.translate("tablePreviewDialog", "Total Building Count", None, QtGui.QApplication.UnicodeUTF8))

