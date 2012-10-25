# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt\win_main.ui'
#
# Created: Mon Sep 17 15:14:10 2012
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_mainWindow(object):
    def setupUi(self, mainWindow):
        mainWindow.setObjectName(_fromUtf8("mainWindow"))
        mainWindow.resize(957, 766)
        self.centralwidget = QtGui.QWidget(mainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.mainTabs = QtGui.QTabWidget(self.centralwidget)
        self.mainTabs.setEnabled(True)
        self.mainTabs.setGeometry(QtCore.QRect(0, 0, 951, 721))
        self.mainTabs.setTabsClosable(False)
        self.mainTabs.setObjectName(_fromUtf8("mainTabs"))
        mainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(mainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 957, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        self.menuView = QtGui.QMenu(self.menubar)
        self.menuView.setObjectName(_fromUtf8("menuView"))
        mainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(mainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        mainWindow.setStatusBar(self.statusbar)
        self.actionOpen_New = QtGui.QAction(mainWindow)
        self.actionOpen_New.setObjectName(_fromUtf8("actionOpen_New"))
        self.actionOpen_Existing = QtGui.QAction(mainWindow)
        self.actionOpen_Existing.setObjectName(_fromUtf8("actionOpen_Existing"))
        self.actionExit = QtGui.QAction(mainWindow)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.actionData_Input = QtGui.QAction(mainWindow)
        self.actionData_Input.setObjectName(_fromUtf8("actionData_Input"))
        self.actionMapping_Schemes = QtGui.QAction(mainWindow)
        self.actionMapping_Schemes.setObjectName(_fromUtf8("actionMapping_Schemes"))
        self.actionResult = QtGui.QAction(mainWindow)
        self.actionResult.setObjectName(_fromUtf8("actionResult"))
        self.actionAbout = QtGui.QAction(mainWindow)
        self.actionAbout.setObjectName(_fromUtf8("actionAbout"))
        self.actionSave = QtGui.QAction(mainWindow)
        self.actionSave.setObjectName(_fromUtf8("actionSave"))
        self.menuFile.addAction(self.actionOpen_New)
        self.menuFile.addAction(self.actionOpen_Existing)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuHelp.addAction(self.actionAbout)
        self.menuView.addAction(self.actionData_Input)
        self.menuView.addAction(self.actionMapping_Schemes)
        self.menuView.addAction(self.actionResult)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(mainWindow)
        self.mainTabs.setCurrentIndex(-1)
        QtCore.QObject.connect(self.actionExit, QtCore.SIGNAL(_fromUtf8("triggered()")), mainWindow.close)
        QtCore.QObject.connect(self.actionOpen_New, QtCore.SIGNAL(_fromUtf8("triggered()")), mainWindow.createProj)
        QtCore.QObject.connect(self.actionOpen_Existing, QtCore.SIGNAL(_fromUtf8("triggered()")), mainWindow.loadProj)
        QtCore.QObject.connect(self.actionAbout, QtCore.SIGNAL(_fromUtf8("triggered()")), mainWindow.showAbout)
        QtCore.QObject.connect(self.actionMapping_Schemes, QtCore.SIGNAL(_fromUtf8("triggered()")), mainWindow.changeTab)
        QtCore.QObject.connect(self.actionData_Input, QtCore.SIGNAL(_fromUtf8("triggered()")), mainWindow.changeTab)
        QtCore.QObject.connect(self.actionResult, QtCore.SIGNAL(_fromUtf8("triggered()")), mainWindow.changeTab)
        QtCore.QObject.connect(self.actionSave, QtCore.SIGNAL(_fromUtf8("triggered()")), mainWindow.saveProj)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        mainWindow.setWindowTitle(QtGui.QApplication.translate("mainWindow", "MainWindow", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("mainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelp.setTitle(QtGui.QApplication.translate("mainWindow", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.menuView.setTitle(QtGui.QApplication.translate("mainWindow", "View", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen_New.setText(QtGui.QApplication.translate("mainWindow", "Create New", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen_Existing.setText(QtGui.QApplication.translate("mainWindow", "Open Existing", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setText(QtGui.QApplication.translate("mainWindow", "Exit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionData_Input.setText(QtGui.QApplication.translate("mainWindow", "Data Input", None, QtGui.QApplication.UnicodeUTF8))
        self.actionMapping_Schemes.setText(QtGui.QApplication.translate("mainWindow", "Mapping Schemes", None, QtGui.QApplication.UnicodeUTF8))
        self.actionResult.setText(QtGui.QApplication.translate("mainWindow", "Result", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout.setText(QtGui.QApplication.translate("mainWindow", "About", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave.setText(QtGui.QApplication.translate("mainWindow", "Save", None, QtGui.QApplication.UnicodeUTF8))

