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
# Version: $Id: win_main.py 21 2012-10-26 01:48:25Z zh $

"""
Main application window
"""
from threading import Thread
from time import sleep

from PyQt4.QtCore import pyqtSlot, QSettings, Qt
from PyQt4.QtGui import QMainWindow, QFileDialog, QMessageBox, QCloseEvent, QDialog, QProgressDialog, QProgressBar, QBoxLayout

from sidd.exception import SIDDException
from utils.system import get_app_dir
from sidd.constants import SIDD_COMPANY, SIDD_APP_NAME, SIDD_VERSION, logAPICall, \
                           ProjectStatus, SyncModes
from sidd.project import Project
from sidd.taxonomy import get_taxonomy

from ui.constants import logUICall, get_ui_string, FILE_MS_DB
from ui.exception import SIDDUIException
from ui.qt.win_main_ui import Ui_mainWindow
from ui.wdg_data import WidgetDataInput
from ui.wdg_ms import WidgetMappingSchemes
from ui.wdg_result import WidgetResult
from ui.wdg_mod import WidgetSecondaryModifier
from ui.dlg_about import DialogAbout
from ui.dlg_apply import DialogApply
from ui.dlg_proc_options import DialogProcessingOptions

from ui.helper.msdb_dao import MSDatabaseDAO
from ui.helper.async import invoke_async

class AppMainWindow(Ui_mainWindow, QMainWindow):
    """
    Main application window
    """
    # internal decorator to perform common checks required
    # for many calls
    #############################
    class CallChecker(object):        
        def __init__(self):
            pass
        
        def setWindow(self, main_window):
            self.main_window = main_window

        def __call__(self, f):
            import functools
            @functools.wraps(f)
            def wrapper(*args, **kw):
                self.main_window.setEnabled(False)
                try:
                    logUICall.log('function call %s from module %s' % (f.__name__, f.__module__), logUICall.DEBUG)                                        
                    return f(*args, **kw)
                except SIDDUIException as uie:
                    logUICall.log(uie, logUICall.ERROR)
                    QMessageBox.warning(None, "Cannot Process Requested Action", str(uie))                                        
                    # windows status message will be cleared out                                        
                    self.main_window.ui.statusbar.showMessage(get_ui_string('app.error.ui'))
                except SIDDException as se:
                    logUICall.log(se, logUICall.ERROR)
                    QMessageBox.critical(None,"Error Processing", str(se))
                    self.main_window.ui.statusbar.showMessage(get_ui_string('app.error.ui'))
                except Exception as e:
                    logUICall.log(e, logUICall.ERROR)
                    QMessageBox.critical(None,"Unexpected Error", str(e))
                    self.main_window.ui.statusbar.showMessage(get_ui_string('app.error.ui'))
                finally:
                    self.main_window.setEnabled(True)
            return wrapper
        
    apiCallChecker = CallChecker()

    # CONSTANTS
    #############################    
    UI_WINDOW_GEOM = 'main/geometry'
    UI_WINDOW_STATE = 'main/windowState'

    # constructor / destructor
    #############################    
    def __init__(self, qtapp, app_config):
        """ constructor """
        
        # create UI
        super(AppMainWindow, self).__init__()
        AppMainWindow.apiCallChecker.setWindow(self)
        
        self.qtapp = qtapp
        self.app_config = app_config
        self.taxonomy = get_taxonomy(app_config.get('options', 'taxonomy', 'gem'))
        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)
        self.retranslateUi(self.ui)
        
        settings = QSettings(SIDD_COMPANY, '%s %s' %(SIDD_APP_NAME, SIDD_VERSION));
        self.restoreGeometry(settings.value(self.UI_WINDOW_GEOM).toByteArray());
        self.restoreState(settings.value(self.UI_WINDOW_STATE).toByteArray());
        
        self.msdb_dao = MSDatabaseDAO(FILE_MS_DB)
        
        self.tab_datainput = WidgetDataInput(self)
        self.ui.mainTabs.addTab(self.tab_datainput, get_ui_string("app.window.tab.input"))

        self.tab_ms = WidgetMappingSchemes(self)
        self.ui.mainTabs.addTab(self.tab_ms, get_ui_string("app.window.tab.ms"))

        self.tab_mod = WidgetSecondaryModifier(self)
        self.ui.mainTabs.addTab(self.tab_mod, get_ui_string("app.window.tab.mod"))

        self.tab_result = WidgetResult(self)
        self.ui.mainTabs.addTab(self.tab_result, get_ui_string("app.window.tab.result"))
        
        self.about = DialogAbout(self)
        self.about.setModal(True)        
        
        self.progress = DialogApply(self)
        self.progress.setModal(True)
        
        self.proc_options = DialogProcessingOptions(self)
        self.proc_options.setModal(True)
        
        # disable all tabs
        self.ui.mainTabs.setTabEnabled(0, False)
        self.ui.mainTabs.setTabEnabled(1, False)
        self.ui.mainTabs.setTabEnabled(2, False)
        self.ui.mainTabs.setTabEnabled(3, False)
        
        self.showTab(0)
        
        # connect menu action to slots (ui events)
        self.ui.actionOpen_New.triggered.connect(self.createProj)
        self.ui.actionOpen_Existing.triggered.connect(self.loadProj)
        self.ui.actionSave.triggered.connect(self.saveProj)
        self.ui.actionExit.triggered.connect(self.close)
        
        self.ui.actionData_Input.triggered.connect(self.changeTab)
        self.ui.actionMapping_Schemes.triggered.connect(self.changeTab)
        self.ui.actionResult.triggered.connect(self.changeTab)
        
        self.ui.actionProcessing_Options.triggered.connect(self.setProcessingOptions)
        
        self.ui.actionAbout.triggered.connect(self.showAbout)
        
        # enable following during development
        self._dev_short_cut()
        
        self.ui.statusbar.showMessage(get_ui_string("app.status.ready"))
        
    def _dev_short_cut(self):
        self.ui.mainTabs.setTabEnabled (1, True)
        self.ui.mainTabs.setTabEnabled (2, True)
        self.ui.mainTabs.setTabEnabled (3, True)

        from os import curdir        
        project = Project(curdir + "/test.db", self.app_config, self.taxonomy)
        project.sync(SyncModes.Read)
        self.setProject(project)

    # event handlers
    #############################
    @pyqtSlot(QCloseEvent)
    def resizeEvent(self, event):
        """ handle window resize """
        self.ui.mainTabs.resize(self.width(), self.height()-40)
    
    @pyqtSlot(QCloseEvent)    
    def closeEvent(self, event):
        self.closeProject()
        settings = QSettings(SIDD_COMPANY, '%s %s' %(SIDD_APP_NAME, SIDD_VERSION));
        settings.setValue(self.UI_WINDOW_GEOM, self.saveGeometry());
        settings.setValue(self.UI_WINDOW_STATE, self.saveState());        
        super(AppMainWindow, self).closeEvent(event)
    
    @logUICall 
    @pyqtSlot()   
    def createProj(self):
        """ create a new project """
        self.closeProject()
        filename = QFileDialog.getSaveFileName(self,
                                               get_ui_string("app.window.msg.project.create"),
                                               get_app_dir(),
                                               get_ui_string("app.extension.db"))
        # no need to check for file overwrite, because QFileDialog return always confirmed overwrite       
        if not filename.isNull():
            # create new project file
            project = Project(str(filename), self.app_config, self.taxonomy)
            # open project and sync UI
            self.setProject(project)
            self.ui.statusbar.showMessage(get_ui_string("app.status.project.created"))
            
    @logUICall 
    @pyqtSlot()   
    def loadProj(self):
        """ open file dialog to load an existing application """        
        filename = QFileDialog.getOpenFileName(self,
                                               get_ui_string("app.window.msg.project.open"),
                                               get_app_dir(),
                                               get_ui_string("app.extension.db"))
        # no need to check for file exists, because QFileDialog return is always valid path or null 
        if not filename.isNull():        
            # open existing project 
            project = Project(str(filename), self.app_config, self.taxonomy)
            project.sync(SyncModes.Read)
            # open project and sync UI        
            self.setProject(project)
            self.ui.statusbar.showMessage(get_ui_string("app.status.project.loaded"))
    
    @logUICall
    @pyqtSlot()    
    def saveProj(self):
        """ save active project """
        self.project.sync(SyncModes.Write)
        self.ui.statusbar.showMessage(get_ui_string("app.status.project.saved"))

    @logUICall
    @pyqtSlot()    
    def setProcessingOptions(self):
        if self.proc_options.exec_() == QDialog.Accepted:
            #self.project.set_options()
            for attribute in dir(self.proc_options):                
                self.project.operator_options['proc.%s'%attribute] = getattr(self.proc_options, attribute)
            
            if self.project.status == ProjectStatus.ReadyForExposure:
                self._doBuildExposure()
            
    @logUICall
    @pyqtSlot()
    def showAbout(self):
        """
        event handler for menu item 
        show about box 
        """
        self.about.setVisible(True)

    @logUICall 
    @pyqtSlot()   
    def changeTab(self):
        """
        event handler for menu item in menu 
        - switch view to tab according to menu item pushed 
        """
        sender = self.sender()
        if sender == self.ui.actionData_Input:
            self.showTab(0)
        elif sender == self.ui.actionMapping_Schemes:
            self.showTab(1)            
        elif sender == self.ui.actionResult:
            self.showTab(3)
        else:
            logUICall.log('\tdo nothing. should not even be here', logUICall.WARNING)

    # public methods    
    #############################
    
    @logAPICall    
    def closeProject(self):
        """ close opened project and update UI elements accordingly """

        if getattr(self, 'project', None) is not None:
            # adjust UI in tabs 
            self.tab_datainput.closeProject()
            self.tab_ms.clearMappingScheme()
            self.tab_mod.closeMappingScheme()            
            del self.project
            self.project = None
        
        # adjust UI in application window
        self.tab_result.closeAll()
        self.ui.mainTabs.setTabEnabled(0, False)            
        self.ui.mainTabs.setTabEnabled(1, False)
        self.ui.mainTabs.setTabEnabled(2, False)               
        self.ui.mainTabs.setTabEnabled(3, False) 
        self.showTab(0)
        self.ui.actionMapping_Schemes.setEnabled(False)
        self.ui.actionResult.setEnabled(False)
        
        self.ui.statusbar.showMessage(get_ui_string("app.status.project.closed"))
        
    @apiCallChecker
    def setProject(self, project):
        """ open a project and sync UI accordingly"""        
        # close and reset UI 
        self.closeProject()

        self.project = project        
        
        # sync ui
        self.tab_datainput.setProject(project)
        if self.project.ms is not None:
            self.visualizeMappingScheme(self.project.ms)
            self.ui.mainTabs.setTabEnabled(1, True)
            self.ui.mainTabs.setTabEnabled(2, True)                           
        self.ui.mainTabs.setTabEnabled(0, True)
        self.tab_result.set_project(project)
        self.ui.mainTabs.setTabEnabled(3, True)
        
        # NOTE: project temp directory is clear everytime the project is closed.
        #       therefore, exposure from previous run cannot be preserved  
        # set processing options
        for attribute in dir(self.proc_options):
            if self.project.operator_options.has_key('proc.%s'%attribute):
                setattr(self.proc_options, attribute, self.project.operator_options['proc.%s'%attribute])

    @apiCallChecker
    def verifyInputs(self):
        """ perform checks on current dataset provided and update UI accordingly """                
        # remove result
        self.tab_result.closeResult()
        
        # verify current dataset
        self.ui.statusbar.showMessage(get_ui_string("app.status.ms.processing"))
        # invoke asynchronously 
        invoke_async(get_ui_string("app.status.processing"), self.project.verify_data)       
        self.tab_datainput.showVerificationResults()
        
        # always allow mapping scheme
        self.ui.mainTabs.setTabEnabled(1, True)
        self.ui.mainTabs.setTabEnabled(2, True)
        self.tab_result.refreshView()        

        self.ui.actionMapping_Schemes.setEnabled(True)
        self.ui.actionResult.setEnabled(True)         
        
        self.ui.statusbar.showMessage(get_ui_string("app.status.input.verified"))       

    @apiCallChecker
    def buildMappingScheme(self):
        """ build mapping scheme with given data """
        self.ui.statusbar.showMessage(get_ui_string("app.status.ms.processing"))
        # invoke asynchronously
        invoke_async(get_ui_string("app.status.processing"), self.project.build_ms)
        self.visualizeMappingScheme(self.project.ms)
        self.ui.statusbar.showMessage(get_ui_string("app.status.ms.created"))

    @apiCallChecker
    def createEmptyMS(self):
        """ build an empty mapping scheme tree for user to manipulate manually """
        self.ui.statusbar.showMessage(get_ui_string("app.status.ms.processing"))
        # invoke asynchronously 
        invoke_async(get_ui_string("app.status.processing"), self.project.create_empty_ms)
        self.visualizeMappingScheme(self.project.ms)
        self.ui.statusbar.showMessage(get_ui_string("app.status.ms.created"))
    
    @apiCallChecker
    def appendMSBranch(self, node, branch):
        """ append a branch (from library) to a node in a mapping scheme tree """
        self.ui.statusbar.showMessage(get_ui_string("app.status.ms.processing"))
        # invoke asynchronously
        invoke_async(get_ui_string("app.status.processing"), self.project.ms.append_branch, args=(node, branch))        
        self.visualizeMappingScheme(self.project.ms)
        self.ui.statusbar.showMessage(get_ui_string("app.status.ms.modified"))
    
    @apiCallChecker
    def deleteMSBranch(self, node):
        """ delete selected node and children from mapping scheme tree """
        self.ui.statusbar.showMessage(get_ui_string("app.status.ms.processing"))
        # invoke asynchronously        
        invoke_async(get_ui_string("app.status.processing"), self.project.ms.delete_branch, args=(node))
        self.visualizeMappingScheme(self.project.ms)
        self.ui.statusbar.showMessage(get_ui_string("app.status.ms.modified"))

    @apiCallChecker
    def exportMSLeaves(self, folder):
        """ export mapping scheme leaves as CSV """
        self.ui.statusbar.showMessage(get_ui_string("app.status.ms.processing"))
        # invoke asynchronously        
        invoke_async(get_ui_string("app.status.processing"), self.project.export_ms_leaves, args=(folder))
        self.ui.statusbar.showMessage(get_ui_string("app.status.ms.exported"))

    @apiCallChecker
    def buildExposure(self, verify_input=True):        
        """ build exposure """
        self.ui.statusbar.showMessage(get_ui_string("app.status.ms.processing"))
                
        # verify current dataset to make sure can process exposure
        if verify_input:
            self.project.verify_data()
        
        # can not proceed if project is not ready for exposure
        if self.project.status != ProjectStatus.ReadyForExposure:
            QMessageBox.critical(self, 
                                 get_ui_string("app.warning.title"), 
                                 get_ui_string("project.error.NotEnoughData"))
            # show result 
            self.tab_datainput.showVerificationResults()
            self.ui.mainTabs.setCurrentIndex(0)
            return
        
        self._doBuildExposure()        

    @apiCallChecker
    def showTab(self, index):
        """
        switch view to tab with given index. do nothing if index is not valid
        """
        if index >=0 and index < 3:
            self.ui.mainTabs.setCurrentIndex(index)

    @apiCallChecker
    def refreshPreview(self):
        self.tab_result.refreshView()

    @apiCallChecker
    def visualizeMappingScheme(self, ms):
        self.tab_ms.showMappingScheme(ms)
        self.tab_mod.showMappingScheme(ms)
    
    # internal helper methods
    ###############################        
    def _doBuildExposure(self):
        """ 
        perform building of exposure data
        pre-condition: project must be ready to generate exposure
        """
        # close current results
        self.tab_result.closeResult()
        self.ui.mainTabs.setTabEnabled(3, True)

        # reset progress dialog
        self.progress.setVisible(True)
        self.progress.ui.pb_progress.setRange(0, 0)
        self.progress.ui.txt_progress.clear()
        self.progress.ui.txt_progress.appendPlainText(get_ui_string("app.status.processing"))        
        self.qtapp.processEvents()
        
        cancelled = False
        for step in self.project.build_exposure_steps():
            if cancelled:
                break
            
            class_name = str(step.__class__)
            class_name = class_name[class_name.find("'")+1:class_name.rfind("'")]
            
            logAPICall.log('\t %s' % step.name, logAPICall.DEBUG)
            self.progress.ui.txt_progress.appendPlainText(get_ui_string('message.%s'% class_name))            
            
            # run process in separate thread
            t = Thread(None, step.do_operation, step.name)            
            t.start()
            
            # wait for process to complete
            while t.isAlive():
                sleep(1)
                step.do_operation()
                self.qtapp.processEvents()
                
                # once progress is closed. it is no longer visible
                # operations do cancel gracefully
                # no additional cleanup/synchronization required                
                if not self.progress.isVisible():
                    cancelled = True
            del t
        
        if cancelled:            
            # processing cancelled
            QMessageBox.information(self, 
                                    get_ui_string("app.warning.title"), 
                                    get_ui_string("app.status.cancelled"))            
            self.ui.statusbar.showMessage(get_ui_string("app.status.cancelled"))
        else:
            # processing completed            
            self.project.verify_result()
            self.progress.setVisible(False)
        
            # show result
            self.tab_result.refreshResult()
            self.ui.mainTabs.setTabEnabled(3, True)
            self.ui.mainTabs.setCurrentIndex(3)
            self.ui.statusbar.showMessage(get_ui_string("app.status.exposure.created"))    
    
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
