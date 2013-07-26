# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt\dlg_ms_branch.ui'
#
# Created: Fri Jun 21 10:53:02 2013
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
        editMSDialog.resize(403, 381)
        self.lb_title = QtGui.QLabel(editMSDialog)
        self.lb_title.setGeometry(QtCore.QRect(10, 10, 731, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setWeight(75)
        font.setBold(True)
        self.lb_title.setFont(font)
        self.lb_title.setObjectName(_fromUtf8("lb_title"))
        self.table_ms_level = QtGui.QTableView(editMSDialog)
        self.table_ms_level.setGeometry(QtCore.QRect(10, 99, 381, 201))
        self.table_ms_level.setObjectName(_fromUtf8("table_ms_level"))
        self.btn_add = QtGui.QPushButton(editMSDialog)
        self.btn_add.setGeometry(QtCore.QRect(270, 70, 31, 23))
        self.btn_add.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/imgs/icons/add.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_add.setIcon(icon)
        self.btn_add.setObjectName(_fromUtf8("btn_add"))
        self.btn_delete = QtGui.QPushButton(editMSDialog)
        self.btn_delete.setGeometry(QtCore.QRect(300, 70, 31, 23))
        self.btn_delete.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/imgs/icons/minus.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_delete.setIcon(icon1)
        self.btn_delete.setObjectName(_fromUtf8("btn_delete"))
        self.btn_apply = QtGui.QPushButton(editMSDialog)
        self.btn_apply.setGeometry(QtCore.QRect(240, 350, 75, 23))
        self.btn_apply.setFlat(False)
        self.btn_apply.setObjectName(_fromUtf8("btn_apply"))
        self.btn_close = QtGui.QPushButton(editMSDialog)
        self.btn_close.setGeometry(QtCore.QRect(320, 350, 75, 23))
        self.btn_close.setFlat(False)
        self.btn_close.setObjectName(_fromUtf8("btn_close"))
        self.btn_save = QtGui.QPushButton(editMSDialog)
        self.btn_save.setGeometry(QtCore.QRect(360, 70, 31, 23))
        self.btn_save.setText(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/imgs/icons/save.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_save.setIcon(icon2)
        self.btn_save.setObjectName(_fromUtf8("btn_save"))
        self.lb_attribute = QtGui.QLabel(editMSDialog)
        self.lb_attribute.setGeometry(QtCore.QRect(10, 42, 291, 21))
        self.lb_attribute.setObjectName(_fromUtf8("lb_attribute"))
        self.cb_attributes = QtGui.QComboBox(editMSDialog)
        self.cb_attributes.setGeometry(QtCore.QRect(10, 70, 241, 22))
        self.cb_attributes.setObjectName(_fromUtf8("cb_attributes"))
        self.lb_total_weights = QtGui.QLabel(editMSDialog)
        self.lb_total_weights.setGeometry(QtCore.QRect(130, 310, 171, 20))
        self.lb_total_weights.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lb_total_weights.setObjectName(_fromUtf8("lb_total_weights"))
        self.txt_total_weights = QtGui.QLineEdit(editMSDialog)
        self.txt_total_weights.setGeometry(QtCore.QRect(310, 310, 51, 20))
        self.txt_total_weights.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.txt_total_weights.setReadOnly(True)
        self.txt_total_weights.setObjectName(_fromUtf8("txt_total_weights"))
        self.lb_percent = QtGui.QLabel(editMSDialog)
        self.lb_percent.setGeometry(QtCore.QRect(370, 310, 21, 20))
        self.lb_percent.setObjectName(_fromUtf8("lb_percent"))
        self.btn_range = QtGui.QPushButton(editMSDialog)
        self.btn_range.setGeometry(QtCore.QRect(330, 70, 30, 23))
        self.btn_range.setText(_fromUtf8(""))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/imgs/icons/cog.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_range.setIcon(icon3)
        self.btn_range.setObjectName(_fromUtf8("btn_range"))

        self.retranslateUi(editMSDialog)
        QtCore.QMetaObject.connectSlotsByName(editMSDialog)

    def retranslateUi(self, editMSDialog):
        editMSDialog.setWindowTitle(QtGui.QApplication.translate("editMSDialog", "Edit Mapping Scheme Branch", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_title.setText(QtGui.QApplication.translate("editMSDialog", "Edit Mapping Scheme Branch", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_add.setToolTip(QtGui.QApplication.translate("editMSDialog", "Add Value", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_delete.setToolTip(QtGui.QApplication.translate("editMSDialog", "Delete Selected Value", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_apply.setText(QtGui.QApplication.translate("editMSDialog", "Apply", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_close.setText(QtGui.QApplication.translate("editMSDialog", "Close", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_save.setToolTip(QtGui.QApplication.translate("editMSDialog", "Save Mapping Scheme Branch", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_attribute.setText(QtGui.QApplication.translate("editMSDialog", "Attribute Name", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_total_weights.setText(QtGui.QApplication.translate("editMSDialog", "Sum of weights", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_percent.setText(QtGui.QApplication.translate("editMSDialog", "%", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_range.setToolTip(QtGui.QApplication.translate("editMSDialog", "Edit Value Grouping", None, QtGui.QApplication.UnicodeUTF8))

import SIDDResource_rc
