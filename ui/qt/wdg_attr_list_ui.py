# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt\wdg_attr_list.ui'
#
# Created: Tue Jul 23 15:45:00 2013
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_widgetAttributes(object):
    def setupUi(self, widgetAttributes):
        widgetAttributes.setObjectName(_fromUtf8("widgetAttributes"))
        widgetAttributes.resize(462, 345)
        self.tree_attributes = QtGui.QTreeView(widgetAttributes)
        self.tree_attributes.setGeometry(QtCore.QRect(0, 30, 411, 311))
        self.tree_attributes.setObjectName(_fromUtf8("tree_attributes"))
        self.lb_attributes = QtGui.QLabel(widgetAttributes)
        self.lb_attributes.setGeometry(QtCore.QRect(6, 0, 141, 31))
        self.lb_attributes.setObjectName(_fromUtf8("lb_attributes"))
        self.widget_attribute_buttons = QtGui.QWidget(widgetAttributes)
        self.widget_attribute_buttons.setGeometry(QtCore.QRect(420, 30, 31, 171))
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

        self.retranslateUi(widgetAttributes)
        QtCore.QMetaObject.connectSlotsByName(widgetAttributes)

    def retranslateUi(self, widgetAttributes):
        widgetAttributes.setWindowTitle(QtGui.QApplication.translate("widgetAttributes", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_attributes.setText(QtGui.QApplication.translate("widgetAttributes", "Attributes to include", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_range.setToolTip(QtGui.QApplication.translate("widgetAttributes", "Edit Grouping", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_move_up.setToolTip(QtGui.QApplication.translate("widgetAttributes", "Move up", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_move_bottom.setToolTip(QtGui.QApplication.translate("widgetAttributes", "Move to Bottom", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_move_down.setToolTip(QtGui.QApplication.translate("widgetAttributes", "Move Down", None, QtGui.QApplication.UnicodeUTF8))
        self.btn_move_top.setToolTip(QtGui.QApplication.translate("widgetAttributes", "Move to Top", None, QtGui.QApplication.UnicodeUTF8))

import SIDDResource_rc
