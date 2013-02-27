# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt\dlg_mod_input.ui'
#
# Created: Tue Feb 19 17:03:10 2013
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_modifierInputDialog(object):
    def setupUi(self, modifierInputDialog):
        modifierInputDialog.setObjectName(_fromUtf8("modifierInputDialog"))
        modifierInputDialog.resize(444, 378)
        self.lb_ms_tree = QtGui.QLabel(modifierInputDialog)
        self.lb_ms_tree.setGeometry(QtCore.QRect(10, 50, 181, 16))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.lb_ms_tree.setFont(font)
        self.lb_ms_tree.setObjectName(_fromUtf8("lb_ms_tree"))
        self.lb_mod_values = QtGui.QLabel(modifierInputDialog)
        self.lb_mod_values.setGeometry(QtCore.QRect(200, 100, 111, 16))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.lb_mod_values.setFont(font)
        self.lb_mod_values.setObjectName(_fromUtf8("lb_mod_values"))
        self.table_mod_values = QtGui.QTableView(modifierInputDialog)
        self.table_mod_values.setGeometry(QtCore.QRect(200, 130, 231, 171))
        self.table_mod_values.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.table_mod_values.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.table_mod_values.setObjectName(_fromUtf8("table_mod_values"))
        self.btn_apply = QtGui.QPushButton(modifierInputDialog)
        self.btn_apply.setGeometry(QtCore.QRect(280, 340, 75, 23))
        self.btn_apply.setObjectName(_fromUtf8("btn_apply"))
        self.btn_cancel = QtGui.QPushButton(modifierInputDialog)
        self.btn_cancel.setGeometry(QtCore.QRect(360, 340, 75, 23))
        self.btn_cancel.setObjectName(_fromUtf8("btn_cancel"))
        self.lb_title = QtGui.QLabel(modifierInputDialog)
        self.lb_title.setGeometry(QtCore.QRect(10, 10, 541, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setWeight(75)
        font.setBold(True)
        self.lb_title.setFont(font)
        self.lb_title.setObjectName(_fromUtf8("lb_title"))
        self.txt_total_weights = QtGui.QLineEdit(modifierInputDialog)
        self.txt_total_weights.setGeometry(QtCore.QRect(360, 310, 51, 20))
        self.txt_total_weights.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.txt_total_weights.setReadOnly(True)
        self.txt_total_weights.setObjectName(_fromUtf8("txt_total_weights"))
        self.lb_percent = QtGui.QLabel(modifierInputDialog)
        self.lb_percent.setGeometry(QtCore.QRect(410, 310, 16, 20))
        self.lb_percent.setObjectName(_fromUtf8("lb_percent"))
        self.lb_total_weights = QtGui.QLabel(modifierInputDialog)
        self.lb_total_weights.setGeometry(QtCore.QRect(200, 310, 141, 20))
        self.lb_total_weights.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lb_total_weights.setObjectName(_fromUtf8("lb_total_weights"))
        self.tree_ms = QtGui.QTreeView(modifierInputDialog)
        self.tree_ms.setGeometry(QtCore.QRect(10, 70, 181, 261))
        self.tree_ms.setObjectName(_fromUtf8("tree_ms"))
        self.widget_mod_values_menu_r = QtGui.QWidget(modifierInputDialog)
        self.widget_mod_values_menu_r.setGeometry(QtCore.QRect(310, 100, 121, 31))
        self.widget_mod_values_menu_r.setObjectName(_fromUtf8("widget_mod_values_menu_r"))
        self.btn_add = QtGui.QPushButton(self.widget_mod_values_menu_r)
        self.btn_add.setGeometry(QtCore.QRect(60, 0, 31, 23))
        self.btn_add.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/imgs/icons/add.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_add.setIcon(icon)
        self.btn_add.setObjectName(_fromUtf8("btn_add"))
        self.btn_delete = QtGui.QPushButton(self.widget_mod_values_menu_r)
        self.btn_delete.setGeometry(QtCore.QRect(90, 0, 31, 23))
        self.btn_delete.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/imgs/icons/minus.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_delete.setIcon(icon1)
        self.btn_delete.setObjectName(_fromUtf8("btn_delete"))
        self.cb_attributes = QtGui.QComboBox(modifierInputDialog)
        self.cb_attributes.setGeometry(QtCore.QRect(200, 70, 231, 22))
        self.cb_attributes.setObjectName(_fromUtf8("cb_attributes"))
        self.lb_attribute = QtGui.QLabel(modifierInputDialog)
        self.lb_attribute.setGeometry(QtCore.QRect(200, 50, 111, 16))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.lb_attribute.setFont(font)
        self.lb_attribute.setObjectName(_fromUtf8("lb_attribute"))

        self.retranslateUi(modifierInputDialog)
        QtCore.QMetaObject.connectSlotsByName(modifierInputDialog)

    def retranslateUi(self, modifierInputDialog):
        modifierInputDialog.setWindowTitle(QtGui.QApplication.translate("modifierInputDialog", "Secondary Modifier Input", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_ms_tree.setText(QtGui.QApplication.translate("modifierInputDialog", "Zone", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_mod_values.setText(QtGui.QApplication.translate("modifierInputDialog", "Values", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_apply.setText(QtGui.QApplication.translate("modifierInputDialog", "OK", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_cancel.setText(QtGui.QApplication.translate("modifierInputDialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_title.setText(QtGui.QApplication.translate("modifierInputDialog", "Edit Modifier", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_percent.setText(QtGui.QApplication.translate("modifierInputDialog", "%", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_total_weights.setText(QtGui.QApplication.translate("modifierInputDialog", "Some of Weights", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_attribute.setText(QtGui.QApplication.translate("modifierInputDialog", "Attrbitue", None, QtGui.QApplication.UnicodeUTF8))

import SIDDResource_rc
