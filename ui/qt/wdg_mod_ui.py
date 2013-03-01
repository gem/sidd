# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt\wdg_mod.ui'
#
# Created: Mon Feb 04 11:16:55 2013
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_widgetSecondaryModifier(object):
    def setupUi(self, widgetSecondaryModifier):
        widgetSecondaryModifier.setObjectName(_fromUtf8("widgetSecondaryModifier"))
        widgetSecondaryModifier.resize(922, 655)
        self.btn_build_exposure = QtGui.QPushButton(widgetSecondaryModifier)
        self.btn_build_exposure.setGeometry(QtCore.QRect(780, 610, 131, 31))
        self.btn_build_exposure.setObjectName(_fromUtf8("btn_build_exposure"))
        self.table_mod = QtGui.QTableView(widgetSecondaryModifier)
        self.table_mod.setGeometry(QtCore.QRect(10, 40, 901, 561))
        self.table_mod.setObjectName(_fromUtf8("table_mod"))
        self.table_mod.verticalHeader().setVisible(False)
        self.table_mod.verticalHeader().setDefaultSectionSize(0)
        self.lb_panel_title = QtGui.QLabel(widgetSecondaryModifier)
        self.lb_panel_title.setGeometry(QtCore.QRect(10, 0, 701, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setWeight(75)
        font.setBold(True)
        self.lb_panel_title.setFont(font)
        self.lb_panel_title.setObjectName(_fromUtf8("lb_panel_title"))
        self.widget_buttons = QtGui.QWidget(widgetSecondaryModifier)
        self.widget_buttons.setGeometry(QtCore.QRect(730, 10, 181, 31))
        self.widget_buttons.setObjectName(_fromUtf8("widget_buttons"))
        self.btn_del_mod = QtGui.QPushButton(self.widget_buttons)
        self.btn_del_mod.setGeometry(QtCore.QRect(120, 0, 31, 23))
        self.btn_del_mod.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/imgs/icons/minus.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_del_mod.setIcon(icon)
        self.btn_del_mod.setObjectName(_fromUtf8("btn_del_mod"))
        self.btn_edit_mod = QtGui.QPushButton(self.widget_buttons)
        self.btn_edit_mod.setGeometry(QtCore.QRect(150, 0, 31, 23))
        self.btn_edit_mod.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/imgs/icons/edit.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_edit_mod.setIcon(icon1)
        self.btn_edit_mod.setObjectName(_fromUtf8("btn_edit_mod"))
        self.btn_add_mod = QtGui.QPushButton(self.widget_buttons)
        self.btn_add_mod.setGeometry(QtCore.QRect(90, 0, 31, 23))
        self.btn_add_mod.setText(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/imgs/icons/add.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btn_add_mod.setIcon(icon2)
        self.btn_add_mod.setObjectName(_fromUtf8("btn_add_mod"))

        self.retranslateUi(widgetSecondaryModifier)
        QtCore.QMetaObject.connectSlotsByName(widgetSecondaryModifier)

    def retranslateUi(self, widgetSecondaryModifier):
        pass

import SIDDResource_rc
