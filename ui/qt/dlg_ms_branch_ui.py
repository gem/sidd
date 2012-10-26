# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt\dlg_ms_branch.ui'
#
# Created: Thu Oct 25 15:50:34 2012
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_editMSDialog(object):
    def setupUi(self, editMSDialog):
        editMSDialog.setObjectName(_fromUtf8("editMSDialog"))
        editMSDialog.resize(335, 379)
        self.lb_title = QtGui.QLabel(editMSDialog)
        self.lb_title.setGeometry(QtCore.QRect(10, 10, 731, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setWeight(75)
        font.setBold(True)
        self.lb_title.setFont(font)
        self.lb_title.setObjectName(_fromUtf8("lb_title"))
        self.table_ms_level = QtGui.QTableView(editMSDialog)
        self.table_ms_level.setGeometry(QtCore.QRect(10, 69, 300, 241))
        self.table_ms_level.setObjectName(_fromUtf8("table_ms_level"))
        self.btn_add = QtGui.QPushButton(editMSDialog)
        self.btn_add.setGeometry(QtCore.QRect(210, 40, 31, 23))
        self.btn_add.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/imgs/icons/add.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_add.setIcon(icon)
        self.btn_add.setObjectName(_fromUtf8("btn_add"))
        self.btn_delete = QtGui.QPushButton(editMSDialog)
        self.btn_delete.setGeometry(QtCore.QRect(240, 40, 31, 23))
        self.btn_delete.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/imgs/icons/minus.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_delete.setIcon(icon1)
        self.btn_delete.setObjectName(_fromUtf8("btn_delete"))
        self.btn_apply = QtGui.QPushButton(editMSDialog)
        self.btn_apply.setGeometry(QtCore.QRect(160, 320, 75, 23))
        self.btn_apply.setFlat(False)
        self.btn_apply.setObjectName(_fromUtf8("btn_apply"))
        self.btn_close = QtGui.QPushButton(editMSDialog)
        self.btn_close.setGeometry(QtCore.QRect(240, 320, 75, 23))
        self.btn_close.setFlat(False)
        self.btn_close.setObjectName(_fromUtf8("btn_close"))
        self.btn_save = QtGui.QPushButton(editMSDialog)
        self.btn_save.setGeometry(QtCore.QRect(280, 40, 31, 23))
        self.btn_save.setText(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/imgs/icons/save.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_save.setIcon(icon2)
        self.btn_save.setObjectName(_fromUtf8("btn_save"))

        self.retranslateUi(editMSDialog)
        QtCore.QObject.connect(self.btn_apply, QtCore.SIGNAL(_fromUtf8("clicked()")), editMSDialog.updateWeights)
        QtCore.QObject.connect(self.btn_close, QtCore.SIGNAL(_fromUtf8("clicked()")), editMSDialog.reject)
        QtCore.QObject.connect(self.btn_add, QtCore.SIGNAL(_fromUtf8("clicked()")), editMSDialog.addValue)
        QtCore.QObject.connect(self.btn_delete, QtCore.SIGNAL(_fromUtf8("clicked()")), editMSDialog.deleteValue)
        QtCore.QObject.connect(self.btn_save, QtCore.SIGNAL(_fromUtf8("clicked()")), editMSDialog.saveMSBranch)
        QtCore.QMetaObject.connectSlotsByName(editMSDialog)

    def retranslateUi(self, editMSDialog):
        editMSDialog.setWindowTitle(QtGui.QApplication.translate("editMSDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_title.setText(QtGui.QApplication.translate("editMSDialog", "Edit Mapping Scheme Branch", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_apply.setText(QtGui.QApplication.translate("editMSDialog", "Apply", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_close.setText(QtGui.QApplication.translate("editMSDialog", "Close", None, QtGui.QApplication.UnicodeUTF8))

import SIDDResource_rc
