# Copyright (c) 2011-2013, ImageCat Inc.
#
# This program is free software: you can redistribute it and/or modify 
# it under the terms of the GNU Affero General Public License as published by 
# the Free Software Foundation, either version 3 of the License, or 
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, 
# but WITHOUT ANY WARRANTY; without even the implied warranty of 
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License 
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
"""
Main application window
"""
import functools
import os
from time import sleep

from PyQt4.QtCore import pyqtSlot, QSettings
from PyQt4.QtGui import QMainWindow, QFileDialog, QMessageBox, QCloseEvent, QDialog, QLabel

from sidd.exception import SIDDException, SIDDProjectException
from utils.system import get_app_dir, get_temp_dir, delete_folders_in_dir
from sidd.constants import SIDD_COMPANY, SIDD_APP_NAME, SIDD_VERSION, logAPICall, \
                           ProjectStatus, SyncModes, ProjectErrors
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
from ui.wdg_data_wizard import WidgetDataWizard

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
            @functools.wraps(f)
            def wrapper(*args, **kw):
                self.main_window.setEnabled(False)
                try:
                    logUICall.log('function call %s from module %s' % (f.__name__, f.__module__), logUICall.DEBUG)                                        
                    return f(*args, **kw)
                except SIDDUIException as uie:
                    logUICall.log(uie, logUICall.WARNING)
                    self.main_window.ui.statusbar.showMessage(get_ui_string('app.error.ui'))
                except SIDDException as se:
                    logUICall.log(se, logUICall.WARNING)
                    self.main_window.ui.statusbar.showMessage(get_ui_string('app.error.model'))
                except Exception as e:
                    logUICall.log(e, logUICall.ERROR)
                    self.main_window.ui.statusbar.showMessage(get_ui_string('app.error.unexpected'))
                finally:
                    self.main_window.setEnabled(True)
            return wrapper
        
    apiCallChecker = CallChecker()

    # CONSTANTS
    #############################    
    UI_WINDOW_GEOM = 'app_main/geometry'
    UI_WINDOW_STATE = 'app_main/windowState'

    TAB_DATA, TAB_MS, TAB_MOD, TAB_RESULT = range(4)

    # constructor / destructor
    #############################    
    def __init__(self, qtapp, app_config):
        """
        constructor
        - initialize UI elements
        - connect UI elements to callback            
        """
        # create UI
        super(AppMainWindow, self).__init__()
        AppMainWindow.apiCallChecker.setWindow(self)
        
        self.qtapp = qtapp
        self.app_config = app_config
        self.taxonomy = get_taxonomy(app_config.get('options', 'taxonomy', 'gem'))
        self.ui = Ui_mainWindow()
        self.ui.setupUi(self)
        
        self.settings = QSettings(SIDD_COMPANY, '%s %s' %(SIDD_APP_NAME, SIDD_VERSION));
        self.restoreGeometry(self.settings.value(self.UI_WINDOW_GEOM).toByteArray());
        self.restoreState(self.settings.value(self.UI_WINDOW_STATE).toByteArray());
        
        self.lb_map_location = QLabel(self)
        self.lb_map_location.resize(self.ui.statusbar.width()/3, self.ui.statusbar.height())
        self.ui.statusbar.addPermanentWidget(self.lb_map_location)
        
        self.msdb_dao = MSDatabaseDAO(FILE_MS_DB)
        
        self.tab_datainput = WidgetDataInput(self)
        self.ui.mainTabs.addTab(self.tab_datainput, get_ui_string("app.window.tab.input"))

        self.tab_ms = WidgetMappingSchemes(self)
        self.ui.mainTabs.addTab(self.tab_ms, get_ui_string("app.window.tab.ms"))

        self.tab_mod = WidgetSecondaryModifier(self)
        self.ui.mainTabs.addTab(self.tab_mod, get_ui_string("app.window.tab.mod"))

        self.tab_result = WidgetResult(self)
        self.ui.mainTabs.addTab(self.tab_result, get_ui_string("app.window.tab.result"))
        self.previewInput = True
        
        self.about = DialogAbout(self)
        self.about.setModal(True)        
        
        self.progress = DialogApply(self)
        self.progress.setModal(True)
        
        self.proc_options = DialogProcessingOptions(self)
        self.proc_options.setModal(True)
        
        # connect menu action to slots (ui events)        
        self.ui.mainTabs.currentChanged.connect(self.tabChanged)
        
        self.ui.actionProject_Blank.triggered.connect(self.createBlank)
        self.ui.actionUsing_Data_Wizard.triggered.connect(self.createWizard)
        self.ui.actionOpen_Existing.triggered.connect(self.loadProj)
        self.ui.actionSave.triggered.connect(self.saveProj)
        self.ui.actionSave_as.triggered.connect(self.saveProjAs)
        self.ui.actionExit.triggered.connect(self.close)
        
        self.ui.actionData_Input.triggered.connect(self.changeTab)
        self.ui.actionMapping_Schemes.triggered.connect(self.changeTab)
        self.ui.actionResult.triggered.connect(self.changeTab)
        
        self.ui.actionProcessing_Options.triggered.connect(self.setProcessingOptions)
        
        self.ui.actionAbout.triggered.connect(self.showAbout)
        
        # set project to None and adjust ui as needed
        self.closeProject()        
        self.ui.statusbar.showMessage(get_ui_string("app.status.ready"))

        # perform clean up from previous runs
        try:
            delete_folders_in_dir(get_temp_dir(), "tmp*")
        except:
            # cleanup is not-critical. no action taken even if fails
            pass

        # hide features 
        if not app_config.get('options', 'parse_modifier', True, bool):
            self.tab_mod.setVisible(False)
            self.ui.mainTabs.removeTab(self.TAB_MOD) 
            self.TAB_MOD = self.TAB_MS
            self.TAB_RESULT -= 1             
            
        # hide view menu
        self.ui.menuView.menuAction().setVisible(False)
        # hide data wizard
        self.ui.actionUsing_Data_Wizard.setVisible(False)

    # event handlers
    #############################
    @pyqtSlot(QCloseEvent)
    def resizeEvent(self, event):
        """ handle window resize """
        self.ui.mainTabs.resize(self.width(), self.height()-40)
    
    @pyqtSlot(QCloseEvent)    
    def closeEvent(self, event):
        self.closeProject()
        self.settings.setValue(self.UI_WINDOW_GEOM, self.saveGeometry());
        self.settings.setValue(self.UI_WINDOW_STATE, self.saveState());
        self.msdb_dao.close()       
        super(AppMainWindow, self).closeEvent(event)
    
    @logUICall 
    @pyqtSlot()   
    def createBlank(self):
        """ create a new project """
        # create new project file
        project = Project(self.app_config, self.taxonomy)
        # open project and sync UI
        self.setProject(project, skipVerify=True)
        self.ui.statusbar.showMessage(get_ui_string("app.status.project.created"))
    
    @logUICall 
    @pyqtSlot()     
    def createWizard(self):
        try:
            # should not update preview while using wizard
            self.setVisible(False)
            self.previewInput = False   
                        
            wizard = WidgetDataWizard(self, Project(self.app_config, self.taxonomy))            
            if wizard.exec_() == QDialog.Accepted:
                # setProject makes call to GIS component that requires visibility 
                self.setVisible(True)
                self.previewInput = True                
                self.setProject(wizard.project)
                self.ui.statusbar.showMessage(get_ui_string("app.status.project.created"))
            # else
            # do nothing?
        except:
            pass            
        finally:
            # return to normal window
            # these calls are reached 
            # 1. in case any exception occurs,
            # 2. wizard finished or cancelled  
            self.setVisible(True)
            self.previewInput = True
    
    @logUICall 
    @pyqtSlot()   
    def loadProj(self):
        """ open file dialog to load an existing application """
        self.getOpenFileName(self, 
                             get_ui_string("app.window.msg.project.open"),
                             get_ui_string("app.extension.db"), 
                             self.openProjectFile)
        self.ui.statusbar.showMessage(get_ui_string("app.status.project.loaded"))
    
    @logUICall
    @pyqtSlot()    
    def saveProj(self):
        """ save active project """
        if self.project is None:
            return
        try: 
            self.project.sync(SyncModes.Write)
            self.ui.statusbar.showMessage(get_ui_string("app.status.project.saved"))
        except SIDDProjectException as se:
            if se.error == ProjectErrors.FileNotSet:
                self.saveProjAs()

    @logUICall
    @pyqtSlot()   
    def saveProjAs(self):
        if self.project is None:
            return
        filename = QFileDialog.getSaveFileName(self,
                                               get_ui_string("app.window.msg.project.create"),
                                               get_app_dir(),
                                               get_ui_string("app.extension.db"))
        # no need to check for file overwrite, because QFileDialog return always confirmed overwrite       
        if not filename.isNull():
            filename = str(filename)
            self.project.set_project_path(filename)                
            self.project.sync(SyncModes.Write)
            self.saveLastOpenDir(filename[0:filename.rfind("/")])            
            self.ui.statusbar.showMessage(get_ui_string("app.status.project.saved"))                

    @logUICall
    @pyqtSlot()    
    def setProcessingOptions(self):
        if self.project is None:                
            return

        # set options to be those defined in project
        self.proc_options.resetOptions()
        for attribute in dir(self.proc_options):
            try:
                proc_attribute = self.project.operator_options['proc.%s'%attribute]
                setattr(self.proc_options, attribute, proc_attribute)
            except:
                # for empty project, this is the first time proc.options is set
                # just use default from proc_option dialogbox
                pass
            
        if self.proc_options.exec_() == QDialog.Accepted:
            for attribute in dir(self.proc_options):                
                self.project.operator_options['proc.%s'%attribute] = getattr(self.proc_options, attribute)
            # alert user
            answer = QMessageBox.question(self,
                                         get_ui_string("app.confirm.title"),
                                         get_ui_string("app.confirm.build.exposure"),
                                         buttons = QMessageBox.No | QMessageBox.Yes,
                                         defaultButton=QMessageBox.No)
            if answer == QMessageBox.No:
                return
            self.buildExposure()
            
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
            self.showTab(self.TAB_DATA)
        elif sender == self.ui.actionMapping_Schemes:
            self.showTab(self.TAB_MS)            
        elif sender == self.ui.actionResult:
            self.showTab(self.TAB_RESULT)
        else:
            logUICall.log('\tdo nothing. should not even be here', logUICall.WARNING)

    @logUICall 
    @pyqtSlot(int)   
    def tabChanged(self, index):
        if index == self.TAB_RESULT:
            self.lb_map_location.setVisible(True)
        else:
            self.lb_map_location.setVisible(False)

    # public methods    
    #############################
    @apiCallChecker
    def openProjectFile(self, path_to_file):
        """ 
        load project from given path
        shows error if path does not exist 
        """
        # NOTE: set_project_path will create new project if path_to_file
        #       does not exist, os.path.exists check is not optional
        if os.path.exists(path_to_file):
            # read file to create project
            project = Project(self.app_config, self.taxonomy)
            project.set_project_path(path_to_file)
            project.sync(SyncModes.Read)
            # open project and sync UI        
            self.setProject(project)
    
    @apiCallChecker
    def setProject(self, project, skipVerify=False):
        """ open a project and sync UI accordingly"""        
        # close and reset UI 
        self.closeProject()
        self.project = project        
        
        # sync ui
        self.tab_datainput.setProject(project)
        
        # set processing options
        for attribute in dir(self.proc_options):
            if self.project.operator_options.has_key('proc.%s'%attribute):
                setattr(self.proc_options, attribute, self.project.operator_options['proc.%s'%attribute])
        
        if not skipVerify:
            # verify to make sure input file are still in same place
            self.verifyInputs()        

        if self.project.ms is not None:
            self.visualizeMappingScheme(self.project.ms)
            self.ui.mainTabs.setTabEnabled(self.TAB_MS, True)
            self.ui.mainTabs.setTabEnabled(self.TAB_MOD, True)                           
        self.ui.mainTabs.setTabEnabled(self.TAB_DATA, True)
        self.ui.mainTabs.setTabEnabled(self.TAB_RESULT, True)
        self.ui.actionSave.setEnabled(True)
        self.ui.actionSave_as.setEnabled(True)                
        self.tab_result.set_project(project)

    @apiCallChecker    
    def closeProject(self):
        """ close opened project and update UI elements accordingly """
        # adjust UI in application window
        self.tab_result.closeAll()  # this call must happen first. 
                                    # otherwise, it locks temporary GIS files
        self.ui.mainTabs.setTabEnabled(self.TAB_DATA, False)            
        self.ui.mainTabs.setTabEnabled(self.TAB_MS, False)
        self.ui.mainTabs.setTabEnabled(self.TAB_MOD, False)               
        self.ui.mainTabs.setTabEnabled(self.TAB_RESULT, False) 
        self.showTab(self.TAB_DATA)
        # disable menu/menu items
        self.ui.actionSave.setEnabled(False)
        self.ui.actionSave_as.setEnabled(False)
        self.ui.actionMapping_Schemes.setEnabled(False)
        self.ui.actionResult.setEnabled(False)
        self.ui.actionProcessing_Options.setEnabled(False)

        if getattr(self, 'project', None) is not None:
            # save existing project is needed
            if self.project.require_save:
                ans = QMessageBox.question(self, 
                                           get_ui_string("app.window.msg.project.not_saved"),
                                           get_ui_string("app.window.msg.project.save_or_not"),
                                           buttons=QMessageBox.Yes|QMessageBox.No,
                                           defaultButton=QMessageBox.Yes)
                if ans == QMessageBox.Yes:
                    self.saveProj()
            
            # adjust UI in tabs 
            self.tab_datainput.closeProject()
            self.tab_ms.clearMappingScheme()
            self.tab_mod.closeMappingScheme()
            self.project.clean_up()           
            del self.project
            self.project = None
            
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
        self.ui.mainTabs.setTabEnabled(self.TAB_MS, True)
        self.ui.mainTabs.setTabEnabled(self.TAB_MOD, True)
        self.ui.actionMapping_Schemes.setEnabled(True)
        self.ui.actionResult.setEnabled(True)      
        self.ui.actionProcessing_Options.setEnabled(True)   
        
        self.ui.statusbar.showMessage(get_ui_string("app.status.input.verified"))       

    @apiCallChecker
    def buildMappingScheme(self):
        """ build mapping scheme with given data """
        self.ui.statusbar.showMessage(get_ui_string("app.status.ms.processing"))
        # invoke asynchronously
        try:
            invoke_async(get_ui_string("app.status.processing"), self.project.build_ms)
        except SIDDException as err:
            # different error message used in this case
            raise SIDDUIException(get_ui_string('project.error.sampling', str(err)))
        
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
        self.project.ms.append_branch(node, branch)
        self.visualizeMappingScheme(self.project.ms)
        self.ui.statusbar.showMessage(get_ui_string("app.status.ms.modified"))
    
    @apiCallChecker
    def deleteMSBranch(self, node):
        """ delete selected node and children from mapping scheme tree """
        self.ui.statusbar.showMessage(get_ui_string("app.status.ms.processing"))
        self.project.ms.delete_branch(node)
        self.visualizeMappingScheme(self.project.ms)
        self.ui.statusbar.showMessage(get_ui_string("app.status.ms.modified"))

    @apiCallChecker
    def exportMS(self, path, format):
        """ export mapping scheme leaves as CSV """
        self.ui.statusbar.showMessage(get_ui_string("app.status.ms.processing"))
        # invoke asynchronously       
        invoke_async(get_ui_string("app.status.processing"), self.project.export_ms, path, format)
        self.ui.statusbar.showMessage(get_ui_string("app.status.ms.exported"))
        
    @apiCallChecker
    def loadMS(self, path):
        self.ui.statusbar.showMessage(get_ui_string("app.status.ms.processing"))
        # invoke asynchronously       
        invoke_async(get_ui_string("app.status.processing"), self.project.load_ms, path)
        self.visualizeMappingScheme(self.project.ms)
        self.ui.statusbar.showMessage(get_ui_string("app.status.ms.created"))

    @apiCallChecker
    def exportResults(self, export_format, export_path):
        """ export mapping scheme leaves as CSV """
        self.ui.statusbar.showMessage(get_ui_string("app.status.exposure.exported"))
        # invoke asynchronously
        self.project.set_export(export_format, export_path)        
        invoke_async(get_ui_string("app.status.processing"), self.project.export_data)
        self.ui.statusbar.showMessage(get_ui_string("app.status.exposure.exported"))

    @apiCallChecker
    def buildExposure(self):        
        """ build exposure """
        self.ui.statusbar.showMessage(get_ui_string("app.status.ms.processing"))
                
        # verify current dataset to make sure can process exposure
        self.project.verify_data()
        
        # can not proceed if project is not ready for exposure
        if self.project.status != ProjectStatus.ReadyForExposure:
            logUICall.log(get_ui_string("project.error.NotEnoughData"), logUICall.WARNING)

            # show result 
            self.tab_datainput.showVerificationResults()
            self.ui.mainTabs.setCurrentIndex(0)
            return
        
        # close current results
        self.tab_result.closeResult()
        self.ui.mainTabs.setTabEnabled(self.TAB_RESULT, True)

        # reset progress dialog
        self.progress.setVisible(True)
        self.progress.ui.pb_progress.setRange(0, self.project.build_exposure_total_steps())        
        self.progress.ui.txt_progress.clear()
        self.progress.ui.txt_progress.appendPlainText(get_ui_string("app.status.processing"))        
        self.qtapp.processEvents()
        
        cancelled = False
        error_occured = False
        error_message = ""
        curStep = 0
        for step in self.project.build_exposure_steps():
            if cancelled or error_occured:
                break
            
            # use introspection to get operator class                           
            class_name = str(step.__class__)
            # result of above call has format 
            # <class '...'> where ... is the class name of interest
            class_name = class_name[class_name.find("'")+1:class_name.rfind("'")]
            
            # update UI
            logAPICall.log('\t %s' % step.name, logAPICall.DEBUG)
            self.progress.ui.txt_progress.appendPlainText(get_ui_string('message.%s'% class_name))
            self.progress.ui.pb_progress.setValue(curStep)                        
            self.qtapp.processEvents()
            sleep(0.5)
            
            # perform operation
            try:
                step.do_operation()
                if not self.progress.isVisible():
                    cancelled = True
            except Exception as err:
                error_message = err.message
                error_occured = True
                self.progress.setVisible(False)
            
            # operation successful
            curStep+=1
            
        if error_occured:
            # processing cancelled
            logUICall.log(error_message, logUICall.WARNING)
            self.ui.statusbar.showMessage(get_ui_string("app.status.cancelled"))
        elif cancelled:
            # processing cancelled
            logUICall.log(get_ui_string("app.status.cancelled"), logUICall.WARNING)
            self.ui.statusbar.showMessage(get_ui_string("app.status.cancelled"))
        else:
            # processing completed            
            self.project.verify_result()
            self.progress.setVisible(False)
        
            # show result
            self.tab_result.refreshResult()
            self.ui.mainTabs.setTabEnabled(self.TAB_RESULT, True)
            self.ui.mainTabs.setCurrentIndex(self.TAB_RESULT)
            self.ui.statusbar.showMessage(get_ui_string("app.status.exposure.created"))       
    
    def showTab(self, index):
        """ switch view to tab with given index. do nothing if index is not valid """
        if index >=self.TAB_DATA and index <=self.TAB_RESULT:
            self.ui.mainTabs.setCurrentIndex(index)
    
    def refreshPreview(self):
        """ refresh all layers shown in Preview tab """
        if self.previewInput:
            self.tab_result.refreshView()

    def visualizeMappingScheme(self, ms):
        """ display the given mapping scheme in Mapping scheme and Modifier tabs"""
        self.tab_ms.showMappingScheme(ms)
        self.tab_mod.showMappingScheme(ms)
    
    def updateMapLocation(self, x, y):
        self.lb_map_location.setText("Longitude %.4f latitude %4f" % (x, y))
    
    # utility methods    
    # no error checking is performed in these functions
    # caller must catch possible exception
    ###############################
    def getOpenFileName(self, parent, title, extension, callback):
        """ show open file dialog box to get a filename """
        filename = QFileDialog.getOpenFileName(parent, title, self.getLastOpenDir(), extension)
        if not filename.isNull():
            filename = str(filename)
            if os.path.exists(filename):                
                # store directory to file, so next Open will be in same dir
                self.saveLastOpenDir(filename[0:filename.rfind("/")])
                callback(filename)  # no error catching to make sure callback is actually a function

    def saveLastOpenDir(self, dir_path):
        """ store path so it can be retrieved by other parts of the application """
        self.settings.setValue('LAST_OPEN_DIR', dir_path)

    def getLastOpenDir(self):
        """ retrieve remembered path """
        last_dir = self.settings.value('LAST_OPEN_DIR').toString()
        if last_dir is None:
            return get_app_dir()
        else:
            return str(last_dir)
    