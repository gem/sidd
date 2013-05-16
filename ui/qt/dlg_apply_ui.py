# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt\dlg_apply.ui'
#
# Created: Thu Apr 25 17:06:38 2013
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_DialogApply(object):
    def setupUi(self, DialogApply):
        DialogApply.setObjectName(_fromUtf8("DialogApply"))
        DialogApply.resize(319, 330)
        self.lb_description = QtGui.QLabel(DialogApply)
        self.lb_description.setGeometry(QtCore.QRect(20, 10, 251, 71))
        self.lb_description.setWordWrap(True)
        self.lb_description.setObjectName(_fromUtf8("lb_description"))
        self.pb_progress = QtGui.QProgressBar(DialogApply)
        self.pb_progress.setGeometry(QtCore.QRect(20, 250, 261, 41))
        self.pb_progress.setProperty(_fromUtf8("value"), 24)
        self.pb_progress.setObjectName(_fromUtf8("pb_progress"))
        self.txt_progress = QtGui.QPlainTextEdit(DialogApply)
        self.txt_progress.setGeometry(QtCore.QRect(20, 90, 261, 151))
        self.txt_progress.setPlainText(_fromUtf8(""))
        self.txt_progress.setObjectName(_fromUtf8("txt_progress"))

        self.retranslateUi(DialogApply)
        QtCore.QMetaObject.connectSlotsByName(DialogApply)

    def retranslateUi(self, DialogApply):
        DialogApply.setWindowTitle(QtGui.QApplication.translate("DialogApply", "Building Exposure", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_description.setText(QtGui.QApplication.translate("DialogApply", "SIDD is applying mapping schemes and generating exposure.\n"
"This may takes some time. Plese check the console below to see what is being processed.", None, QtGui.QApplication.UnicodeUTF8))

