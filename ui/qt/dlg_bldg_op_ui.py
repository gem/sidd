# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt\dlg_bldg_op.ui'
#
# Created: Mon Sep 17 15:14:09 2012
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(426, 313)
        self.btnbox_ok_cancel = QtGui.QDialogButtonBox(Dialog)
        self.btnbox_ok_cancel.setGeometry(QtCore.QRect(250, 280, 156, 23))
        self.btnbox_ok_cancel.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.btnbox_ok_cancel.setObjectName(_fromUtf8("btnbox_ok_cancel"))
        self.mainTabs = QtGui.QTabWidget(Dialog)
        self.mainTabs.setGeometry(QtCore.QRect(20, 10, 391, 261))
        self.mainTabs.setObjectName(_fromUtf8("mainTabs"))
        self.downloadTab = QtGui.QWidget()
        self.downloadTab.setObjectName(_fromUtf8("downloadTab"))
        self.txt_download_server = QtGui.QTextEdit(self.downloadTab)
        self.txt_download_server.setGeometry(QtCore.QRect(10, 40, 241, 31))
        self.txt_download_server.setObjectName(_fromUtf8("txt_download_server"))
        self.lb_download_server = QtGui.QLabel(self.downloadTab)
        self.lb_download_server.setGeometry(QtCore.QRect(10, 20, 121, 16))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.lb_download_server.setFont(font)
        self.lb_download_server.setObjectName(_fromUtf8("lb_download_server"))
        self.lb_download_timeout = QtGui.QLabel(self.downloadTab)
        self.lb_download_timeout.setGeometry(QtCore.QRect(10, 90, 121, 16))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.lb_download_timeout.setFont(font)
        self.lb_download_timeout.setObjectName(_fromUtf8("lb_download_timeout"))
        self.txt_download_timeout = QtGui.QTextEdit(self.downloadTab)
        self.txt_download_timeout.setGeometry(QtCore.QRect(10, 110, 241, 31))
        self.txt_download_timeout.setObjectName(_fromUtf8("txt_download_timeout"))
        self.mainTabs.addTab(self.downloadTab, _fromUtf8(""))
        self.hhTab = QtGui.QWidget()
        self.hhTab.setObjectName(_fromUtf8("hhTab"))
        self.lb_hh_person_per_hh = QtGui.QLabel(self.hhTab)
        self.lb_hh_person_per_hh.setGeometry(QtCore.QRect(10, 20, 241, 16))
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.lb_hh_person_per_hh.setFont(font)
        self.lb_hh_person_per_hh.setObjectName(_fromUtf8("lb_hh_person_per_hh"))
        self.txt_hh_person_per_hh = QtGui.QTextEdit(self.hhTab)
        self.txt_hh_person_per_hh.setGeometry(QtCore.QRect(10, 40, 191, 31))
        self.txt_hh_person_per_hh.setObjectName(_fromUtf8("txt_hh_person_per_hh"))
        self.mainTabs.addTab(self.hhTab, _fromUtf8(""))
        self.lb_download_server.setBuddy(self.txt_download_server)
        self.lb_download_timeout.setBuddy(self.txt_download_timeout)

        self.retranslateUi(Dialog)
        self.mainTabs.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "GEM Default Building Stock", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_download_server.setText(QtGui.QApplication.translate("Dialog", "GEM server address", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_download_timeout.setText(QtGui.QApplication.translate("Dialog", "Connection Timeout", None, QtGui.QApplication.UnicodeUTF8))
        self.mainTabs.setTabText(self.mainTabs.indexOf(self.downloadTab), QtGui.QApplication.translate("Dialog", "Download", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_hh_person_per_hh.setText(QtGui.QApplication.translate("Dialog", "Number of person per household", None, QtGui.QApplication.UnicodeUTF8))
        self.mainTabs.setTabText(self.mainTabs.indexOf(self.hhTab), QtGui.QApplication.translate("Dialog", "Household", None, QtGui.QApplication.UnicodeUTF8))

