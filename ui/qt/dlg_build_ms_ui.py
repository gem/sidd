# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt\dlg_build_ms.ui'
#
# Created: Wed Feb 13 18:54:01 2013
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
        msOptionsDialog.resize(343, 342)
        self.buttons = QtGui.QDialogButtonBox(msOptionsDialog)
        self.buttons.setGeometry(QtCore.QRect(150, 300, 171, 32))
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
        self.widget_attributes = QtGui.QWidget(msOptionsDialog)
        self.widget_attributes.setGeometry(QtCore.QRect(30, 90, 291, 201))
        self.widget_attributes.setObjectName(_fromUtf8("widget_attributes"))
        self.lst_attributes = QtGui.QListWidget(self.widget_attributes)
        self.lst_attributes.setGeometry(QtCore.QRect(0, 30, 251, 171))
        self.lst_attributes.setObjectName(_fromUtf8("lst_attributes"))
        self.lb_attributes = QtGui.QLabel(self.widget_attributes)
        self.lb_attributes.setGeometry(QtCore.QRect(0, 0, 141, 31))
        self.lb_attributes.setObjectName(_fromUtf8("lb_attributes"))
        self.widget_attribute_buttons = QtGui.QWidget(self.widget_attributes)
        self.widget_attribute_buttons.setGeometry(QtCore.QRect(260, 30, 31, 171))
        self.widget_attribute_buttons.setObjectName(_fromUtf8("widget_attribute_buttons"))
        self.btn_range = QtGui.QPushButton(self.widget_attribute_buttons)
        self.btn_range.setGeometry(QtCore.QRect(0, 70, 30, 23))
        self.btn_range.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/imgs/icons/cog.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_range.setIcon(icon)
        self.btn_range.setObjectName(_fromUtf8("btn_range"))
        self.btn_move_up = QtGui.QPushButton(self.widget_attribute_buttons)
        self.btn_move_up.setGeometry(QtCore.QRect(0, 30, 30, 23))
        self.btn_move_up.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/imgs/icons/arrow_up.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_move_up.setIcon(icon1)
        self.btn_move_up.setObjectName(_fromUtf8("btn_move_up"))
        self.btn_move_bottom = QtGui.QPushButton(self.widget_attribute_buttons)
        self.btn_move_bottom.setGeometry(QtCore.QRect(0, 140, 30, 23))
        self.btn_move_bottom.setText(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/imgs/icons/arrow_bottom.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_move_bottom.setIcon(icon2)
        self.btn_move_bottom.setObjectName(_fromUtf8("btn_move_bottom"))
        self.btn_move_down = QtGui.QPushButton(self.widget_attribute_buttons)
        self.btn_move_down.setGeometry(QtCore.QRect(0, 110, 30, 23))
        self.btn_move_down.setText(_fromUtf8(""))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/imgs/icons/arrow_down.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_move_down.setIcon(icon3)
        self.btn_move_down.setObjectName(_fromUtf8("btn_move_down"))
        self.btn_move_top = QtGui.QPushButton(self.widget_attribute_buttons)
        self.btn_move_top.setGeometry(QtCore.QRect(0, 0, 30, 23))
        self.btn_move_top.setText(_fromUtf8(""))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/imgs/icons/arrow_top.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_move_top.setIcon(icon4)
        self.btn_move_top.setObjectName(_fromUtf8("btn_move_top"))

        self.retranslateUi(msOptionsDialog)
        QtCore.QMetaObject.connectSlotsByName(msOptionsDialog)

    def retranslateUi(self, msOptionsDialog):
        msOptionsDialog.setWindowTitle(QtGui.QApplication.translate("msOptionsDialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.radioEmptyMS.setText(QtGui.QApplication.translate("msOptionsDialog", "Empty Mapping Scheme", None, QtGui.QApplication.UnicodeUTF8))
        self.radioBuildMS.setText(QtGui.QApplication.translate("msOptionsDialog", "Using Survey Data", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_title.setText(QtGui.QApplication.translate("msOptionsDialog", "Create Mapping Scheme", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_attributes.setText(QtGui.QApplication.translate("msOptionsDialog", "Attributes", None, QtGui.QApplication.UnicodeUTF8))

import SIDDResource_rc
