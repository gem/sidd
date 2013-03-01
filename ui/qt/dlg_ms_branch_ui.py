# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt\dlg_ms_branch.ui'
#
# Created: Mon Feb 04 16:34:11 2013
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
        editMSDialog.resize(329, 386)
        self.lb_title = QtGui.QLabel(editMSDialog)
        self.lb_title.setGeometry(QtCore.QRect(10, 10, 731, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setWeight(75)
        font.setBold(True)
        self.lb_title.setFont(font)
        self.lb_title.setObjectName(_fromUtf8("lb_title"))
        self.table_ms_level = QtGui.QTableView(editMSDialog)
        self.table_ms_level.setGeometry(QtCore.QRect(10, 99, 300, 201))
        self.table_ms_level.setObjectName(_fromUtf8("table_ms_level"))
        self.btn_add = QtGui.QPushButton(editMSDialog)
        self.btn_add.setGeometry(QtCore.QRect(200, 70, 31, 23))
        self.btn_add.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/imgs/icons/add.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_add.setIcon(icon)
        self.btn_add.setObjectName(_fromUtf8("btn_add"))
        self.btn_delete = QtGui.QPushButton(editMSDialog)
        self.btn_delete.setGeometry(QtCore.QRect(230, 70, 31, 23))
        self.btn_delete.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/imgs/icons/minus.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_delete.setIcon(icon1)
        self.btn_delete.setObjectName(_fromUtf8("btn_delete"))
        self.btn_apply = QtGui.QPushButton(editMSDialog)
        self.btn_apply.setGeometry(QtCore.QRect(160, 350, 75, 23))
        self.btn_apply.setFlat(False)
        self.btn_apply.setObjectName(_fromUtf8("btn_apply"))
        self.btn_close = QtGui.QPushButton(editMSDialog)
        self.btn_close.setGeometry(QtCore.QRect(240, 350, 75, 23))
        self.btn_close.setFlat(False)
        self.btn_close.setObjectName(_fromUtf8("btn_close"))
        self.btn_save = QtGui.QPushButton(editMSDialog)
        self.btn_save.setGeometry(QtCore.QRect(280, 70, 31, 23))
        self.btn_save.setText(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/imgs/icons/save.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_save.setIcon(icon2)
        self.btn_save.setObjectName(_fromUtf8("btn_save"))
        self.lb_attribute = QtGui.QLabel(editMSDialog)
        self.lb_attribute.setGeometry(QtCore.QRect(10, 42, 291, 21))
        self.lb_attribute.setObjectName(_fromUtf8("lb_attribute"))
        self.cb_attributes = QtGui.QComboBox(editMSDialog)
        self.cb_attributes.setGeometry(QtCore.QRect(10, 70, 181, 22))
        self.cb_attributes.setObjectName(_fromUtf8("cb_attributes"))
        self.lb_total_weights = QtGui.QLabel(editMSDialog)
        self.lb_total_weights.setGeometry(QtCore.QRect(15, 310, 171, 20))
        self.lb_total_weights.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lb_total_weights.setObjectName(_fromUtf8("lb_total_weights"))
        self.txt_total_weights = QtGui.QLineEdit(editMSDialog)
        self.txt_total_weights.setGeometry(QtCore.QRect(200, 310, 81, 20))
        self.txt_total_weights.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.txt_total_weights.setReadOnly(True)
        self.txt_total_weights.setObjectName(_fromUtf8("txt_total_weights"))
        self.lb_percent = QtGui.QLabel(editMSDialog)
        self.lb_percent.setGeometry(QtCore.QRect(290, 310, 21, 20))
        self.lb_percent.setObjectName(_fromUtf8("lb_percent"))

        self.retranslateUi(editMSDialog)
        QtCore.QMetaObject.connectSlotsByName(editMSDialog)

    def retranslateUi(self, editMSDialog):
        pass

import SIDDResource_rc
