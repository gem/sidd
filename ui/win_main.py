# Copyright (c) 2011-2012, ImageCat Inc.
#
# SIDD is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License version 3
# only, as published by the Free Software Foundation.
#
# SIDD is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License version 3 for more details
# (a copy is included in the LICENSE file that accompanied this code).
#
# You should have received a copy of the GNU Lesser General Public License
# version 3 along with SIDD.  If not, see
# <http://www.gnu.org/licenses/lgpl-3.0.txt> for a copy of the LGPLv3 License.
#
# Version: $Id: win_main.py 19 2012-10-25 01:06:59Z zh $

"""
Main application window
"""
from threading import Thread

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from qgis.core import *
from qgis.gui import *

from sidd.exception import *
from sidd.constants import *
from sidd.project import Project

from ui.constants import logUICall, get_ui_string, FILE_MS_DB
from ui.exception import SIDDUIException
from ui.qt.win_main_ui import Ui_mainWindow
from ui.wdg_data import WidgetDataInput
from ui.wdg_ms import WidgetMappingSchemes
from ui.wdg_result import WidgetResult
from ui.wdg_mod import WidgetSecondaryModifier
from ui.dlg_about import DialogAbout
from ui.dlg_apply import DialogApply
from ui.helper.msdb_dao import MSDatabaseDAO

class AppMainWindow(Ui_mainWindow, QMainWindow):
    """
    Main application window
    """
    # internal decorator to perform common checks required
    # for many calls
    #############################
    class UICallChecker(object):        
        def __init__(self):
            pass

        def __call__(self, f):
            import functools
            @functools.wraps(f)
            def wrapper(*args, **kw):
                try:
                    return f(*args, **kw)
                except SIDDUIException as uie:
                    logUICall.log(uie, logUICall.ERROR)
                    QMessageBox.warning(None, "Cannot Process Requested Action", str(uie))                    
                except SIDDException as se:
                    logUICall.log(se, logUICall.ERROR)
                    QMessageBox.critical(None,"Error Processing", str(se))
                except Exception as e:
                    logUICall.log(e, logUICall.ERROR)
                    QMessageBox.critical(None,"Unexpected Error", str(e))
            return wrapper
        
    uiCallChecker = UICallChecker()

    # constructor / destructor
    #############################
    
    def __init__(self, qtapp):
        """ constructor """
        
        # create UI
        super(AppMainWindow, self).__init__()
        
        self.qtapp = qtapp
        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)        
        self.retranslateUi(self.ui)
        
        self.msdb_dao = MSDatabaseDAO(FILE_MS_DB)
        
        self.data_input = WidgetDataInput(self)
        self.ui.mainTabs.addTab(self.data_input, get_ui_string("app.window.tab.input"))

        self.mapping_scheme = WidgetMappingSchemes(self)
        self.ui.mainTabs.addTab(self.mapping_scheme, get_ui_string("app.window.tab.ms"))

        self.secondary_mod = WidgetSecondaryModifier(self)
        self.ui.mainTabs.addTab(self.secondary_mod, get_ui_string("app.window.tab.mod"))

        self.result = WidgetResult(self)
        self.ui.mainTabs.addTab(self.result, get_ui_string("app.window.tab.result"))
        
        self.about = DialogAbout(self)
        self.about.setModal(True)
        
        self.progress = DialogApply(self)
        self.progress.setModal(True)
        
        # disable all tabs
        self.ui.mainTabs.setTabEnabled (0, False)
        self.ui.mainTabs.setTabEnabled (1, False)
        self.ui.mainTabs.setTabEnabled (2, False)
        self.ui.mainTabs.setTabEnabled (3, False)
        
        self.ui.statusbar.showMessage(get_ui_string("app.window.status.ready"))
        
        # enable following during development
        # self._dev_short_cut()

    def _dev_short_cut(self):
        self.ui.mainTabs.setTabEnabled (1, True)
        self.ui.mainTabs.setTabEnabled (2, True)
        self.ui.mainTabs.setTabEnabled (3, True)

        from os import curdir
        self.openProject(curdir + "/test.db")

    # window event handler overrides
    #############################
    def resizeEvent(self, event):
        """ handle window resize """
        self.ui.mainTabs.resize(self.size().width(), self.size().height()-40)        
    
    def closeEvent(self, event):
        self.close_project()
        super(AppMainWindow, self).close()


    # public API call
    #############################
        
    @logAPICall
    def close_project(self):
        if getattr(self, 'project', None) is not None:
            self.result.closeResult()
            self.data_input.closeProject()
            del self.project        

    @uiCallChecker
    @logAPICall    
    def openProject(self, project_file):
        """ open a project """        
        self.close_project()
        
        project = Project(str(project_file))
        project.sync(SyncModes.Read)
        # open sucessful
        # sync ui
        self.project = project        
        self.data_input.setProject(project)
        if self.project.ms is not None:            
            self.visualizeMappingScheme(self.project.ms)
            self.ui.mainTabs.setTabEnabled(1, True)
            self.ui.mainTabs.setTabEnabled(2, True)               
        self.ui.mainTabs.setTabEnabled(0, True)

    @uiCallChecker
    @logAPICall
    def verifyInputs(self):
        # remove result
        self.result.closeResult()
        self.ui.mainTabs.setTabEnabled(3, False)        
        self.project.verify_data()
        self.ui.mainTabs.setTabEnabled(1, True)
        self.ui.mainTabs.setTabEnabled(2, True)    
        self.data_input.showVerificationResults()

    @uiCallChecker
    @logAPICall
    def buildMappingScheme(self):
        """ open a project """
        self.project.build_ms()
        self.visualizeMappingScheme(self.project.ms)

    @uiCallChecker
    @logAPICall
    def createEmptyMS(self):
        self.project.create_empty_ms()
        self.visualizeMappingScheme(self.project.ms)
    
    @uiCallChecker
    @logAPICall
    def appendMSBranch(self, node, branch):
        """ append a branch (from library) to a node in a mapping scheme tree """
        self.project.ms.append_branch(node, branch)
        self.visualizeMappingScheme(self.project.ms)
    
    @uiCallChecker
    @logAPICall
    def deleteMSBranch(self, node):
        self.project.ms.delete_branch(node)
        self.visualizeMappingScheme(self.project.ms)

    @uiCallChecker
    @logAPICall
    def visualizeMappingScheme(self, ms):
        self.mapping_scheme.showMappingScheme(ms)
        self.secondary_mod.showMappingScheme(ms)

    @uiCallChecker
    @logAPICall
    def buildExposure(self):
        self.result.closeResult()
        self.progress.setVisible(True)

        total_steps = len(self.project.workflow.operators)
        progress_bar = self.progress.ui.pb_progress
        progress_bar.setMinimum(0)
        progress_bar.setMaximum(0)
        progress_text = self.progress.ui.txt_progress
        progress_text.clear()
        
        for step in self.project.build_exposure_steps():
            logAPICall.log('\t %s' % step.name, logAPICall.DEBUG)
            progress_text.appendPlainText(step.name)
            
            # run process in separate thread
            t = Thread(None, step.do_operation, step.name)
            t.start()
            
            # wait for process to complete
            while t.isAlive():                
                for i in range(1000):
                    self.qtapp.processEvents()
        
        self.progress.setVisible(False)        
        #self.result.showResultLayer(self.project.exposure)
        self.result.showResult(self.project)
        self.ui.mainTabs.setTabEnabled(3, True)
        self.ui.mainTabs.setCurrentIndex (3)
        
    # event handlers
    #############################
    @logUICall    
    def createProj(self):
        """ create a new project """
        self.close_project()
        filename = QFileDialog.getSaveFileName(self,
                                               get_ui_string("app.window.msg.project.create"),
                                               get_app_dir(),
                                               get_ui_string("app.extension.db"))       
        if not filename.isNull():            
            project = Project(str(filename))
            
            self.project = project
            # open sucessful
            # sync ui
            self.data_input.setProject(project)
            self.ui.mainTabs.setTabEnabled (0, True)
            
    @logUICall    
    def loadProj(self):
        """ open file dialog to load an existing application """        
        filename = QFileDialog.getOpenFileName(self,
                                               get_ui_string("app.window.msg.project.open"),
                                               get_app_dir(),
                                               get_ui_string("app.extension.db"))
        if not filename.isNull():            
            self.openProject(filename)
    
    @logUICall    
    def saveProj(self):
        """ save active project """
        self.project.sync(SyncModes.Write)
        
    @logUICall    
    def showAbout(self):
        """ show about box """
        self.about.setVisible(True)

    @logUICall    
    def changeTab(self):
        """ open file dialog to load an existing application """        
        sender = self.sender()
        if sender == self.ui.actionData_Input:
            self.ui.mainTabs.setCurrentIndex (0)
        elif sender == self.ui.actionMapping_Schemes:
            self.ui.mainTabs.setCurrentIndex (1)
        elif sender == self.ui.actionResult:
            self.ui.mainTabs.setCurrentIndex (3)
        else:
            logUICall.log('\tdo nothing. should not even be here', logUICall.WARNING)

    # internal helper methods
    ###############################
    
    def retranslateUi(self, ui):
        self.setWindowTitle(get_ui_string("app.window.title"))
        ui.menuFile.setTitle(get_ui_string("app.window.menu.file"))
        ui.menuHelp.setTitle(get_ui_string("app.window.menu.help"))
        ui.menuView.setTitle(get_ui_string("app.window.menu.view"))
        ui.actionOpen_New.setText(get_ui_string("app.window.menu.file.create"))
        ui.actionSave.setText(get_ui_string("app.window.menu.file.save"))
        ui.actionOpen_Existing.setText(get_ui_string("app.window.menu.file.open"))
        ui.actionExit.setText(get_ui_string("app.window.menu.file.exit"))
        ui.actionData_Input.setText(get_ui_string("app.window.menu.view.input"))
        ui.actionMapping_Schemes.setText(get_ui_string("app.window.menu.view.ms"))
        ui.actionResult.setText(get_ui_string("app.window.menu.view.result"))
        ui.actionAbout.setText(get_ui_string("app.window.menu.help.about"))

