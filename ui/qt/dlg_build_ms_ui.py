# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt\dlg_build_ms.ui'
#
# Created: Tue Jul 23 15:45:15 2013
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_msOptionsDialog(object):
    def setupUi(self, msOptionsDialog):
        msOptionsDialog.setObjectName(_fromUtf8("msOptionsDialog"))
        msOptionsDialog.resize(477, 479)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(msOptionsDialog.sizePolicy().hasHeightForWidth())
        msOptionsDialog.setSizePolicy(sizePolicy)
        self.buttons = QtGui.QDialogButtonBox(msOptionsDialog)
        self.buttons.setGeometry(QtCore.QRect(290, 430, 171, 32))
        self.buttons.setOrientation(QtCore.Qt.Horizontal)
        self.buttons.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttons.setObjectName(_fromUtf8("buttons"))
        self.radioEmptyMS = QtGui.QRadioButton(msOptionsDialog)
        self.radioEmptyMS.setGeometry(QtCore.QRect(10, 50, 281, 17))
        self.radioEmptyMS.setObjectName(_fromUtf8("radioEmptyMS"))
        self.radioBuildMS = QtGui.QRadioButton(msOptionsDialog)
        self.radioBuildMS.setGeometry(QtCore.QRect(10, 70, 281, 17))
        self.radioBuildMS.setObjectName(_fromUtf8("radioBuildMS"))
        self.lb_title = QtGui.QLabel(msOptionsDialog)
        self.lb_title.setGeometry(QtCore.QRect(10, 10, 341, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setWeight(75)
        font.setBold(True)
        self.lb_title.setFont(font)
        self.lb_title.setObjectName(_fromUtf8("lb_title"))
        self.ck_use_sampling = QtGui.QCheckBox(msOptionsDialog)
        self.ck_use_sampling.setGeometry(QtCore.QRect(300, 70, 211, 17))
        self.ck_use_sampling.setObjectName(_fromUtf8("ck_use_sampling"))

        self.retranslateUi(msOptionsDialog)
        QtCore.QMetaObject.connectSlotsByName(msOptionsDialog)

    def retranslateUi(self, msOptionsDialog):
        msOptionsDialog.setWindowTitle(QtGui.QApplication.translate("msOptionsDialog", "Create Mapping Scheme", None, QtGui.QApplication.UnicodeUTF8))
        self.radioEmptyMS.setText(QtGui.QApplication.translate("msOptionsDialog", "Create Empty Mapping Scheme", None, QtGui.QApplication.UnicodeUTF8))
        self.radioBuildMS.setText(QtGui.QApplication.translate("msOptionsDialog", "Build from Survey Data", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_title.setText(QtGui.QApplication.translate("msOptionsDialog", "Create Mapping Scheme", None, QtGui.QApplication.UnicodeUTF8))
        self.ck_use_sampling.setText(QtGui.QApplication.translate("msOptionsDialog", "Use Stratified Sampling Method", None, QtGui.QApplication.UnicodeUTF8))

import SIDDResource_rc
