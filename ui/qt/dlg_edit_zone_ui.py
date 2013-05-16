# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt\dlg_edit_zone.ui'
#
# Created: Fri Apr 26 13:13:34 2013
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_editZoneNameDialog(object):
    def setupUi(self, editZoneNameDialog):
        editZoneNameDialog.setObjectName(_fromUtf8("editZoneNameDialog"))
        editZoneNameDialog.resize(333, 117)
        self.buttonBox = QtGui.QDialogButtonBox(editZoneNameDialog)
        self.buttonBox.setGeometry(QtCore.QRect(160, 80, 156, 23))
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.lb_zone = QtGui.QLabel(editZoneNameDialog)
        self.lb_zone.setGeometry(QtCore.QRect(10, 20, 301, 20))
        self.lb_zone.setObjectName(_fromUtf8("lb_zone"))
        self.txt_zone = QtGui.QLineEdit(editZoneNameDialog)
        self.txt_zone.setGeometry(QtCore.QRect(10, 50, 311, 20))
        self.txt_zone.setObjectName(_fromUtf8("txt_zone"))

        self.retranslateUi(editZoneNameDialog)
        QtCore.QMetaObject.connectSlotsByName(editZoneNameDialog)

    def retranslateUi(self, editZoneNameDialog):
        editZoneNameDialog.setWindowTitle(QtGui.QApplication.translate("editZoneNameDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_zone.setText(QtGui.QApplication.translate("editZoneNameDialog", "Enter desired zone name", None, QtGui.QApplication.UnicodeUTF8))

