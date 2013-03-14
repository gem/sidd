# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt\win_main.ui'
# Created: Wed Feb 20 10:48:55 2013
#      by: PyQt4 UI code generator 4.8.3
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
        self.menuOptions = QtGui.QMenu(self.menubar)
        self.menuOptions.setObjectName(_fromUtf8("menuOptions"))
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
        self.actionProcessing_Options = QtGui.QAction(mainWindow)
        self.actionProcessing_Options.setObjectName(_fromUtf8("actionProcessing_Options"))
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
        self.menuOptions.addAction(self.actionProcessing_Options)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuOptions.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(mainWindow)
        self.mainTabs.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        pass

