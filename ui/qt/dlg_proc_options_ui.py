# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt\dlg_proc_options.ui'
#
# Created: Tue Feb 26 16:48:50 2013
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_procOptionsDialog(object):
    def setupUi(self, procOptionsDialog):
        procOptionsDialog.setObjectName(_fromUtf8("procOptionsDialog"))
        procOptionsDialog.resize(313, 168)
        self.box_extrapolate_options = QtGui.QGroupBox(procOptionsDialog)
        self.box_extrapolate_options.setGeometry(QtCore.QRect(10, 20, 291, 91))
        self.box_extrapolate_options.setObjectName(_fromUtf8("box_extrapolate_options"))
        self.radio_random = QtGui.QRadioButton(self.box_extrapolate_options)
        self.radio_random.setGeometry(QtCore.QRect(20, 20, 200, 17))
        self.radio_random.setChecked(True)
        self.radio_random.setObjectName(_fromUtf8("radio_random"))
        self.radio_actual = QtGui.QRadioButton(self.box_extrapolate_options)
        self.radio_actual.setGeometry(QtCore.QRect(20, 40, 200, 17))
        self.radio_actual.setObjectName(_fromUtf8("radio_actual"))
        self.radio_actual_rounded = QtGui.QRadioButton(self.box_extrapolate_options)
        self.radio_actual_rounded.setGeometry(QtCore.QRect(20, 60, 200, 17))
        self.radio_actual_rounded.setObjectName(_fromUtf8("radio_actual_rounded"))
        self.widgetButtons = QtGui.QWidget(procOptionsDialog)
        self.widgetButtons.setGeometry(QtCore.QRect(10, 130, 291, 31))
        self.widgetButtons.setObjectName(_fromUtf8("widgetButtons"))
        self.btn_ok = QtGui.QPushButton(self.widgetButtons)
        self.btn_ok.setGeometry(QtCore.QRect(130, 0, 75, 23))
        self.btn_ok.setObjectName(_fromUtf8("btn_ok"))
        self.btn_close = QtGui.QPushButton(self.widgetButtons)
        self.btn_close.setGeometry(QtCore.QRect(210, 0, 75, 23))
        self.btn_close.setObjectName(_fromUtf8("btn_close"))

        self.retranslateUi(procOptionsDialog)
        QtCore.QMetaObject.connectSlotsByName(procOptionsDialog)

    def retranslateUi(self, procOptionsDialog):
        procOptionsDialog.setWindowTitle(QtGui.QApplication.translate("procOptionsDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.box_extrapolate_options.setTitle(QtGui.QApplication.translate("procOptionsDialog", "Extrapolation Options", None, QtGui.QApplication.UnicodeUTF8))
        self.radio_random.setText(QtGui.QApplication.translate("procOptionsDialog", "Random Walk", None, QtGui.QApplication.UnicodeUTF8))
        self.radio_actual.setText(QtGui.QApplication.translate("procOptionsDialog", "Actual Ratio ", None, QtGui.QApplication.UnicodeUTF8))
        self.radio_actual_rounded.setText(QtGui.QApplication.translate("procOptionsDialog", "Actual Ratio (Rounded)", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_ok.setText(QtGui.QApplication.translate("procOptionsDialog", "OK", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_close.setText(QtGui.QApplication.translate("procOptionsDialog", "Close", None, QtGui.QApplication.UnicodeUTF8))

