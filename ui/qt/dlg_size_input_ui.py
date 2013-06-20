# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt\dlg_size_input.ui'
#
# Created: Mon Jun 17 13:49:30 2013
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_sizeInputDialog(object):
    def setupUi(self, sizeInputDialog):
        sizeInputDialog.setObjectName(_fromUtf8("sizeInputDialog"))
        sizeInputDialog.resize(427, 341)
        self.lb_ms_tree = QtGui.QLabel(sizeInputDialog)
        self.lb_ms_tree.setGeometry(QtCore.QRect(10, 50, 181, 16))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.lb_ms_tree.setFont(font)
        self.lb_ms_tree.setObjectName(_fromUtf8("lb_ms_tree"))
        self.lb_size = QtGui.QLabel(sizeInputDialog)
        self.lb_size.setGeometry(QtCore.QRect(200, 110, 111, 16))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.lb_size.setFont(font)
        self.lb_size.setObjectName(_fromUtf8("lb_size"))
        self.btn_apply = QtGui.QPushButton(sizeInputDialog)
        self.btn_apply.setGeometry(QtCore.QRect(260, 310, 75, 23))
        self.btn_apply.setObjectName(_fromUtf8("btn_apply"))
        self.btn_cancel = QtGui.QPushButton(sizeInputDialog)
        self.btn_cancel.setGeometry(QtCore.QRect(340, 310, 75, 23))
        self.btn_cancel.setObjectName(_fromUtf8("btn_cancel"))
        self.lb_title = QtGui.QLabel(sizeInputDialog)
        self.lb_title.setGeometry(QtCore.QRect(10, 10, 541, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setWeight(75)
        font.setBold(True)
        self.lb_title.setFont(font)
        self.lb_title.setObjectName(_fromUtf8("lb_title"))
        self.txt_size = QtGui.QLineEdit(sizeInputDialog)
        self.txt_size.setGeometry(QtCore.QRect(200, 130, 211, 20))
        self.txt_size.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.txt_size.setReadOnly(False)
        self.txt_size.setObjectName(_fromUtf8("txt_size"))
        self.tree_ms = QtGui.QTreeView(sizeInputDialog)
        self.tree_ms.setGeometry(QtCore.QRect(10, 70, 181, 261))
        self.tree_ms.setObjectName(_fromUtf8("tree_ms"))
        self.lb_bldg_type = QtGui.QLabel(sizeInputDialog)
        self.lb_bldg_type.setGeometry(QtCore.QRect(200, 50, 111, 16))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.lb_bldg_type.setFont(font)
        self.lb_bldg_type.setObjectName(_fromUtf8("lb_bldg_type"))
        self.txt_bldg_type = QtGui.QLineEdit(sizeInputDialog)
        self.txt_bldg_type.setGeometry(QtCore.QRect(200, 80, 211, 20))
        self.txt_bldg_type.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.txt_bldg_type.setReadOnly(True)
        self.txt_bldg_type.setObjectName(_fromUtf8("txt_bldg_type"))
        self.lb_rep_cost = QtGui.QLabel(sizeInputDialog)
        self.lb_rep_cost.setGeometry(QtCore.QRect(200, 160, 211, 16))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.lb_rep_cost.setFont(font)
        self.lb_rep_cost.setObjectName(_fromUtf8("lb_rep_cost"))
        self.txt_rep_cost = QtGui.QLineEdit(sizeInputDialog)
        self.txt_rep_cost.setGeometry(QtCore.QRect(200, 180, 211, 20))
        self.txt_rep_cost.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.txt_rep_cost.setReadOnly(False)
        self.txt_rep_cost.setObjectName(_fromUtf8("txt_rep_cost"))

        self.retranslateUi(sizeInputDialog)
        QtCore.QMetaObject.connectSlotsByName(sizeInputDialog)

    def retranslateUi(self, sizeInputDialog):
        sizeInputDialog.setWindowTitle(QtGui.QApplication.translate("sizeInputDialog", "Edit Average Building Size", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_ms_tree.setText(QtGui.QApplication.translate("sizeInputDialog", "Mapping Scheme", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_size.setText(QtGui.QApplication.translate("sizeInputDialog", "Average Size (m2)", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_apply.setText(QtGui.QApplication.translate("sizeInputDialog", "OK", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_cancel.setText(QtGui.QApplication.translate("sizeInputDialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_title.setText(QtGui.QApplication.translate("sizeInputDialog", "Edit Average Building Size", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_bldg_type.setText(QtGui.QApplication.translate("sizeInputDialog", "Building Type", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_rep_cost.setText(QtGui.QApplication.translate("sizeInputDialog", "Replacement Cost Per Area Unit", None, QtGui.QApplication.UnicodeUTF8))

import SIDDResource_rc
