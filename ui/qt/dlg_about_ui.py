# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt\dlg_about.ui'
#
# Created: Mon Oct 15 17:42:18 2012
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_DialogAbout(object):
    def setupUi(self, DialogAbout):
        DialogAbout.setObjectName(_fromUtf8("DialogAbout"))
        DialogAbout.resize(400, 308)
        self.buttonBox = QtGui.QDialogButtonBox(DialogAbout)
        self.buttonBox.setGeometry(QtCore.QRect(160, 260, 81, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.label = QtGui.QLabel(DialogAbout)
        self.label.setGeometry(QtCore.QRect(40, 20, 331, 101))
        self.label.setText(_fromUtf8(""))
        self.label.setPixmap(QtGui.QPixmap(_fromUtf8(":/imgs/logo.png")))
        self.label.setObjectName(_fromUtf8("label"))
        self.textEdit = QtGui.QTextEdit(DialogAbout)
        self.textEdit.setGeometry(QtCore.QRect(90, 120, 211, 131))
        self.textEdit.setObjectName(_fromUtf8("textEdit"))

        self.retranslateUi(DialogAbout)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), DialogAbout.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), DialogAbout.reject)
        QtCore.QMetaObject.connectSlotsByName(DialogAbout)

    def retranslateUi(self, DialogAbout):
        DialogAbout.setWindowTitle(QtGui.QApplication.translate("DialogAbout", "Dialog", None, QtGui.QApplication.UnicodeUTF8))

import SIDDResource_rc
