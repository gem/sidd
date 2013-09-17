# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'qt\win_main.ui'
#
# Created: Fri Jun 21 14:01:30 2013
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
        mainWindow.resize(930, 750)
        mainWindow.setMinimumSize(QtCore.QSize(930, 750))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/imgs/icon.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        mainWindow.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(mainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.mainTabs = QtGui.QTabWidget(self.centralwidget)
        self.mainTabs.setEnabled(True)
        self.mainTabs.setGeometry(QtCore.QRect(0, 0, 951, 721))
        self.mainTabs.setTabsClosable(False)
        self.mainTabs.setObjectName(_fromUtf8("mainTabs"))
        mainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(mainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 930, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuHelp = QtGui.QMenu(self.menubar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        self.menuView = QtGui.QMenu(self.menubar)
        self.menuView.setObjectName(_fromUtf8("menuView"))
        self.menuProcessing = QtGui.QMenu(self.menubar)
        self.menuProcessing.setObjectName(_fromUtf8("menuProcessing"))
        mainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(mainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        mainWindow.setStatusBar(self.statusbar)
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
        self.actionUsing_Data_Wizard = QtGui.QAction(mainWindow)
        self.actionUsing_Data_Wizard.setObjectName(_fromUtf8("actionUsing_Data_Wizard"))
        self.actionProject_Blank = QtGui.QAction(mainWindow)
        self.actionProject_Blank.setObjectName(_fromUtf8("actionProject_Blank"))
        self.actionSave_as = QtGui.QAction(mainWindow)
        self.actionSave_as.setObjectName(_fromUtf8("actionSave_as"))
        self.menuFile.addAction(self.actionProject_Blank)
        self.menuFile.addAction(self.actionUsing_Data_Wizard)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionOpen_Existing)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_as)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuHelp.addAction(self.actionAbout)
        self.menuView.addAction(self.actionData_Input)
        self.menuView.addAction(self.actionMapping_Schemes)
        self.menuView.addAction(self.actionResult)
        self.menuProcessing.addAction(self.actionProcessing_Options)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuProcessing.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(mainWindow)
        self.mainTabs.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(mainWindow)

    def retranslateUi(self, mainWindow):
        mainWindow.setWindowTitle(QtGui.QApplication.translate("mainWindow", "Spatial Inventory Data Developer", None, QtGui.QApplication.UnicodeUTF8))
        self.menuFile.setTitle(QtGui.QApplication.translate("mainWindow", "File", None, QtGui.QApplication.UnicodeUTF8))
        self.menuHelp.setTitle(QtGui.QApplication.translate("mainWindow", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.menuView.setTitle(QtGui.QApplication.translate("mainWindow", "View", None, QtGui.QApplication.UnicodeUTF8))
        self.menuProcessing.setTitle(QtGui.QApplication.translate("mainWindow", "Options", None, QtGui.QApplication.UnicodeUTF8))
        self.actionOpen_Existing.setText(QtGui.QApplication.translate("mainWindow", "Open Existing", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setText(QtGui.QApplication.translate("mainWindow", "Exit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionData_Input.setText(QtGui.QApplication.translate("mainWindow", "Data Input", None, QtGui.QApplication.UnicodeUTF8))
        self.actionMapping_Schemes.setText(QtGui.QApplication.translate("mainWindow", "Mapping Schemes", None, QtGui.QApplication.UnicodeUTF8))
        self.actionResult.setText(QtGui.QApplication.translate("mainWindow", "Preview", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout.setText(QtGui.QApplication.translate("mainWindow", "About", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave.setText(QtGui.QApplication.translate("mainWindow", "Save Project", None, QtGui.QApplication.UnicodeUTF8))
        self.actionProcessing_Options.setText(QtGui.QApplication.translate("mainWindow", "Processing Options ...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionUsing_Data_Wizard.setText(QtGui.QApplication.translate("mainWindow", "Using Data Wizard ...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionProject_Blank.setText(QtGui.QApplication.translate("mainWindow", "Blank Project", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_as.setText(QtGui.QApplication.translate("mainWindow", "Save Project as ...", None, QtGui.QApplication.UnicodeUTF8))

import SIDDResource_rc
