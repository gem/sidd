# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt\dlg_about.ui'
#
# Created: Thu Feb 28 11:36:16 2013
#      by: PyQt4 UI code generator 4.8.3
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_DialogAbout(object):
    def setupUi(self, DialogAbout):
        DialogAbout.setObjectName(_fromUtf8("DialogAbout"))
        DialogAbout.resize(400, 461)
        self.buttonBox = QtGui.QDialogButtonBox(DialogAbout)
        self.buttonBox.setGeometry(QtCore.QRect(300, 410, 81, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.lb_logo = QtGui.QLabel(DialogAbout)
        self.lb_logo.setGeometry(QtCore.QRect(20, 20, 311, 101))
        self.lb_logo.setText(_fromUtf8(""))
        self.lb_logo.setPixmap(QtGui.QPixmap(_fromUtf8(":/imgs/logo.png")))
        self.lb_logo.setObjectName(_fromUtf8("lb_logo"))
        self.lb_description = QtGui.QLabel(DialogAbout)
        self.lb_description.setGeometry(QtCore.QRect(20, 111, 360, 151))
        self.lb_description.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.lb_description.setWordWrap(True)
        self.lb_description.setObjectName(_fromUtf8("lb_description"))
        self.lb_logo_gem = QtGui.QLabel(DialogAbout)
        self.lb_logo_gem.setGeometry(QtCore.QRect(20, 270, 150, 100))
        self.lb_logo_gem.setPixmap(QtGui.QPixmap(_fromUtf8(":/imgs/gem_logo_250X180.png")))
        self.lb_logo_gem.setScaledContents(True)
        self.lb_logo_gem.setObjectName(_fromUtf8("lb_logo_gem"))
        self.lb_logo_imagecat = QtGui.QLabel(DialogAbout)
        self.lb_logo_imagecat.setGeometry(QtCore.QRect(200, 280, 151, 51))
        self.lb_logo_imagecat.setPixmap(QtGui.QPixmap(_fromUtf8(":/imgs/imagecat_logo.gif")))
        self.lb_logo_imagecat.setScaledContents(True)
        self.lb_logo_imagecat.setObjectName(_fromUtf8("lb_logo_imagecat"))
        self.lb_copyright = QtGui.QLabel(DialogAbout)
        self.lb_copyright.setGeometry(QtCore.QRect(20, 380, 361, 31))
        self.lb_copyright.setObjectName(_fromUtf8("lb_copyright"))

        self.retranslateUi(DialogAbout)
        QtCore.QMetaObject.connectSlotsByName(DialogAbout)

    def retranslateUi(self, DialogAbout):
        pass
