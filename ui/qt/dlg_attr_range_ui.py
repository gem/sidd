# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt\dlg_attr_range.ui'
#
# Created: Fri Mar 08 16:01:19 2013
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_attrRangesDialog(object):
    def setupUi(self, attrRangesDialog):
        attrRangesDialog.setObjectName(_fromUtf8("attrRangesDialog"))
        attrRangesDialog.resize(286, 344)
        self.buttons = QtGui.QDialogButtonBox(attrRangesDialog)
        self.buttons.setGeometry(QtCore.QRect(140, 310, 131, 21))
        self.buttons.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttons.setObjectName(_fromUtf8("buttons"))
        self.lb_title = QtGui.QLabel(attrRangesDialog)
        self.lb_title.setGeometry(QtCore.QRect(10, 10, 341, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setWeight(75)
        font.setBold(True)
        self.lb_title.setFont(font)
        self.lb_title.setObjectName(_fromUtf8("lb_title"))
        self.lb_attribute = QtGui.QLabel(attrRangesDialog)
        self.lb_attribute.setGeometry(QtCore.QRect(20, 50, 291, 21))
        self.lb_attribute.setObjectName(_fromUtf8("lb_attribute"))
        self.btn_add = QtGui.QPushButton(attrRangesDialog)
        self.btn_add.setGeometry(QtCore.QRect(210, 50, 31, 23))
        self.btn_add.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/imgs/icons/add.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_add.setIcon(icon)
        self.btn_add.setObjectName(_fromUtf8("btn_add"))
        self.table_ranges = QtGui.QTableWidget(attrRangesDialog)
        self.table_ranges.setGeometry(QtCore.QRect(20, 80, 251, 191))
        self.table_ranges.setObjectName(_fromUtf8("table_ranges"))
        self.table_ranges.setColumnCount(2)
        self.table_ranges.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.table_ranges.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.table_ranges.setHorizontalHeaderItem(1, item)
        self.btn_delete = QtGui.QPushButton(attrRangesDialog)
        self.btn_delete.setGeometry(QtCore.QRect(240, 50, 31, 23))
        self.btn_delete.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/imgs/icons/minus.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_delete.setIcon(icon1)
        self.btn_delete.setObjectName(_fromUtf8("btn_delete"))
        self.lb_notes = QtGui.QLabel(attrRangesDialog)
        self.lb_notes.setGeometry(QtCore.QRect(20, 280, 251, 20))
        self.lb_notes.setObjectName(_fromUtf8("lb_notes"))

        self.retranslateUi(attrRangesDialog)
        QtCore.QMetaObject.connectSlotsByName(attrRangesDialog)

    def retranslateUi(self, attrRangesDialog):
        attrRangesDialog.setWindowTitle(QtGui.QApplication.translate("attrRangesDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_title.setText(QtGui.QApplication.translate("attrRangesDialog", "Attribute Range", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_attribute.setText(QtGui.QApplication.translate("attrRangesDialog", "Attribute", None, QtGui.QApplication.UnicodeUTF8))
        self.table_ranges.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("attrRangesDialog", "Minimum Value", None, QtGui.QApplication.UnicodeUTF8))
        self.table_ranges.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("attrRangesDialog", "Maximum Value", None, QtGui.QApplication.UnicodeUTF8))

import SIDDResource_rc
