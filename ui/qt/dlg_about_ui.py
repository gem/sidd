# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt\dlg_about.ui'
#
# Created: Mon May 20 14:37:48 2013
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
        DialogAbout.setWindowTitle(QtGui.QApplication.translate("DialogAbout", "About SIDD", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_description.setText(QtGui.QApplication.translate("DialogAbout", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Version: $version<br />Last updated: $lastupdate</span></p>\n"
"<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">SIDD (Spatial Inventory Data Developer) is developed from GEM Inventory and Damage Capture Tools effort. It is part of a collection of tools that can be used for development of exposure datasets and models at the sub-national level, for exposure dataset development per-building and to capture earthquake consequences per-building </span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.lb_copyright.setText(QtGui.QApplication.translate("DialogAbout", "<p>Copyright &reg; ImageCat Inc. 2013.</p>", None, QtGui.QApplication.UnicodeUTF8))

import SIDDResource_rc
