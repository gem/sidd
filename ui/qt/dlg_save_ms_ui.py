# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt\dlg_save_ms.ui'
#
# Created: Wed Feb 27 10:16:42 2013
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_saveMSDialog(object):
    def setupUi(self, saveMSDialog):
        saveMSDialog.setObjectName(_fromUtf8("saveMSDialog"))
        saveMSDialog.resize(614, 500)
        self.tree_ms_view = QtGui.QTreeView(saveMSDialog)
        self.tree_ms_view.setGeometry(QtCore.QRect(310, 50, 291, 401))
        self.tree_ms_view.setObjectName(_fromUtf8("tree_ms_view"))
        self.btn_save = QtGui.QPushButton(saveMSDialog)
        self.btn_save.setGeometry(QtCore.QRect(450, 460, 75, 23))
        self.btn_save.setObjectName(_fromUtf8("btn_save"))
        self.btn_close = QtGui.QPushButton(saveMSDialog)
        self.btn_close.setGeometry(QtCore.QRect(530, 460, 75, 23))
        self.btn_close.setObjectName(_fromUtf8("btn_close"))
        self.lb_ms_source = QtGui.QLabel(saveMSDialog)
        self.lb_ms_source.setGeometry(QtCore.QRect(10, 180, 80, 25))
        self.lb_ms_source.setObjectName(_fromUtf8("lb_ms_source"))
        self.lb_ms_quality = QtGui.QLabel(saveMSDialog)
        self.lb_ms_quality.setGeometry(QtCore.QRect(10, 220, 80, 25))
        self.lb_ms_quality.setObjectName(_fromUtf8("lb_ms_quality"))
        self.txt_ms_notes = QtGui.QTextEdit(saveMSDialog)
        self.txt_ms_notes.setGeometry(QtCore.QRect(120, 260, 180, 191))
        self.txt_ms_notes.setObjectName(_fromUtf8("txt_ms_notes"))
        self.lb_ms_notes = QtGui.QLabel(saveMSDialog)
        self.lb_ms_notes.setGeometry(QtCore.QRect(10, 260, 80, 25))
        self.lb_ms_notes.setObjectName(_fromUtf8("lb_ms_notes"))
        self.lb_ms_name = QtGui.QLabel(saveMSDialog)
        self.lb_ms_name.setGeometry(QtCore.QRect(10, 110, 80, 25))
        self.lb_ms_name.setObjectName(_fromUtf8("lb_ms_name"))
        self.lb_ms_type = QtGui.QLabel(saveMSDialog)
        self.lb_ms_type.setGeometry(QtCore.QRect(10, 80, 80, 25))
        self.lb_ms_type.setObjectName(_fromUtf8("lb_ms_type"))
        self.cb_ms_region = QtGui.QComboBox(saveMSDialog)
        self.cb_ms_region.setGeometry(QtCore.QRect(120, 46, 180, 25))
        self.cb_ms_region.setObjectName(_fromUtf8("cb_ms_region"))
        self.lb_ms_region = QtGui.QLabel(saveMSDialog)
        self.lb_ms_region.setGeometry(QtCore.QRect(10, 40, 80, 31))
        self.lb_ms_region.setObjectName(_fromUtf8("lb_ms_region"))
        self.lb_title = QtGui.QLabel(saveMSDialog)
        self.lb_title.setGeometry(QtCore.QRect(10, 10, 731, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setWeight(75)
        font.setBold(True)
        self.lb_title.setFont(font)
        self.lb_title.setObjectName(_fromUtf8("lb_title"))
        self.lb_ms_create_date = QtGui.QLabel(saveMSDialog)
        self.lb_ms_create_date.setGeometry(QtCore.QRect(10, 150, 80, 25))
        self.lb_ms_create_date.setObjectName(_fromUtf8("lb_ms_create_date"))
        self.txt_ms_type = QtGui.QLineEdit(saveMSDialog)
        self.txt_ms_type.setGeometry(QtCore.QRect(120, 80, 181, 20))
        self.txt_ms_type.setObjectName(_fromUtf8("txt_ms_type"))
        self.txt_ms_name = QtGui.QLineEdit(saveMSDialog)
        self.txt_ms_name.setGeometry(QtCore.QRect(120, 110, 181, 20))
        self.txt_ms_name.setObjectName(_fromUtf8("txt_ms_name"))
        self.txt_ms_create_date = QtGui.QLineEdit(saveMSDialog)
        self.txt_ms_create_date.setGeometry(QtCore.QRect(120, 150, 181, 20))
        self.txt_ms_create_date.setObjectName(_fromUtf8("txt_ms_create_date"))
        self.txt_ms_source = QtGui.QLineEdit(saveMSDialog)
        self.txt_ms_source.setGeometry(QtCore.QRect(120, 190, 181, 20))
        self.txt_ms_source.setObjectName(_fromUtf8("txt_ms_source"))
        self.txt_ms_quality = QtGui.QLineEdit(saveMSDialog)
        self.txt_ms_quality.setGeometry(QtCore.QRect(120, 220, 181, 20))
        self.txt_ms_quality.setObjectName(_fromUtf8("txt_ms_quality"))

        self.retranslateUi(saveMSDialog)
        QtCore.QMetaObject.connectSlotsByName(saveMSDialog)

    def retranslateUi(self, saveMSDialog):
        pass
