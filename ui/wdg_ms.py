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
# Version: $Id: wdg_ms.py 20 2012-10-25 16:17:10Z zh $

"""
Widget (Panel) for creating mapping scheme
"""
from PyQt4.QtGui import *
from PyQt4.QtCore import *

from utils import *

from sidd.ms import *
from sidd.exception import SIDDException

from ui.exception import SIDDUIException
from ui.constants import logUICall, get_ui_string
from ui.dlg_ms_branch import DialogEditMS
from ui.dlg_save_ms import DialogSaveMS 
from ui.helper.ms_tree import MSTreeModel
from ui.qt.wdg_ms_ui import Ui_widgetMappingSchemes

class WidgetMappingSchemes(Ui_widgetMappingSchemes, QWidget):
    """
    Widget (Panel) for creating mapping scheme
    """
    # internal decorator to perform common checks required
    # for many calls
    #############################
    class UICallChecker(object):        
        def __init__(self):
            pass

        def __call__(self, f):
            import functools
            import traceback
            @functools.wraps(f)
            def wrapper(*args, **kw):
                # try requested operation
                try:
                    return f(*args, **kw)                
                except SIDDUIException as uie:
                    QMessageBox.warning(None, get_ui_string("app.error.unexpected"), str(uie))
                except SIDDException as se:
                    QMessageBox.critical(None,get_ui_string("app.error.model"), str(se))
                except Exception as e:
                    traceback.print_exc()
                    QMessageBox.critical(None,get_ui_string("app.error.ui"), str(e))
            return wrapper
        
    uiCallChecker = UICallChecker()

    # constructor / destructor
    ###############################    
    def __init__(self, app):
        QWidget.__init__(self)        
        self.ui = Ui_widgetMappingSchemes()
        self.ui.setupUi(self)
        self.retranslateUi(self.ui)

        self.app = app
        self.ms = None
        self.ui.tree_ms.animated=True
        
        self.msdb_dao =  app.msdb_dao
        for region in self.msdb_dao.get_regions(with_ms=True):
            self.ui.list_ms_library_regions.addItem(QString(region))
        
        self.clearMappingScheme()
        self.setMSLibraryEnabled(False)
        
        self.dlgEditMS = DialogEditMS(self.app)
        self.dlgSaveMS = DialogSaveMS(self.app)        

    # public methods
    ###############################
    
    @logUICall
    def showMappingScheme(self, ms):
        """ display mapping scheme """
        self.ms = ms
        treeUI = self.ui.tree_ms
        treeUI.setModel(MSTreeModel(ms))
        treeUI.setSelectionMode(QAbstractItemView.SingleSelection)
        self.ui.tree_ms.setEnabled(True)
    
    @logUICall
    def clearMappingScheme(self):
        self.ms = None
        self.ui.tree_ms.setModel(None)
        self.ui.tree_ms.setEnabled(False)
    
    # UI event handling calls
    ###############################
    
    @uiCallChecker
    @logUICall
    def buildMS(self):
        """ build mapping scheme from survey data """
        self.clearMappingScheme()
        self.app.buildMappingScheme()

    @uiCallChecker
    @logUICall
    def createMS(self):
        """ create new mapping scheme """
        self.clearMappingScheme()
        self.app.createEmptyMS()
        
    @uiCallChecker
    @logUICall
    def saveMS(self):
        """ save existing mapping scheme """
        if self.ms is not None:
            self.dlgSaveMS.setMS(self.ms)
            self.dlgSaveMS.setModal(True)
            self.dlgSaveMS.exec_()

    @uiCallChecker
    @logUICall
    def addBranch(self):
        """ add branch to mapping scheme """
        node = self.getSelectedNode(self.ui.tree_ms)
        if type(node) == MappingSchemeZone:
            node = node.stats.get_tree()
        
        self.dlgEditMS.setNode(node, addNew=True)
        self.dlgEditMS.setModal(True)
        self.dlgEditMS.exec_()
        ans = self.dlgEditMS.exec_()
        if ans == QDialog.Accepted:            
            node.update_children(self.dlgEditMS.values, self.dlgEditMS.weights)
            self.app.visualizeMappingScheme(self.ms)
        

    @uiCallChecker
    @logUICall
    def removeBranch(self):
        """ remove branch from mapping scheme tree """
        node = self.getSelectedNode(self.ui.tree_ms)
        answer = QMessageBox.warning(self,
                                     get_ui_string("app.popup.delete.confirm"),
                                     get_ui_string("widget.ms.warning.deletebranch"),
                                     QMessageBox.Yes | QMessageBox.No)
        if answer == QMessageBox.Yes:
            self.app.deleteMSBranch(node)
        
    @uiCallChecker
    @logUICall
    def editBranch(self):
        """ edit a branch from mapping scheme tree """
        node = self.getSelectedNode(self.ui.tree_ms)
        if type(node) != StatisticNode:
            QMessageBox.warning(self, 
                                get_ui_string("app.warning.title"),
                                get_ui_string("widget.ms.warning.node.required"))
            return        
        # not zone / not root, good to continue
        
        self.dlgEditMS.setNode(node)
        self.dlgEditMS.setModal(True)
        ans = self.dlgEditMS.exec_()
        if ans == QDialog.Accepted:            
            node.parent.update_children(self.dlgEditMS.values, self.dlgEditMS.weights)
            self.app.visualizeMappingScheme(self.ms)

    @uiCallChecker
    @logUICall
    def appendBranch(self):
        """ append branch to mapping scheme tree """
        # get selected node from working mapping scheme tree
        node = self.getSelectedNode(self.ui.tree_ms)
        branch = self.getSelectedNode(self.ui.tree_repo_ms)
        self.app.appendMSBranch(node, branch)
        
    @uiCallChecker
    @logUICall
    def setModifiers(self):
        """  """
        pass

    @uiCallChecker
    @logUICall
    def applyMS(self):
        """  apply mapping scheme and generate exposure """
        self.app.buildExposure()
    
    @logUICall
    def toggleMSLibrary(self, value):
        self.setMSLibraryEnabled(value)

    @uiCallChecker
    @logUICall
    def regionSelected(self, modelIndex):
        """
        update mapping scheme types and available mapping schemes list
        according to selected region
        """
        # get selected region
        region = self.ui.list_ms_library_regions.currentItem ().text()
        
        # adjust UI to display results
        #self.ui.list_ms_library_types.clear()
        #self.ui.list_ms_library_msnames.clear()
        self.resetMSLibrary()
        for mstype in self.msdb_dao.get_types_in_region(region):
            self.ui.list_ms_library_types.addItem(QString(mstype))
        
    @uiCallChecker
    @logUICall
    def typeSelected(self, modelIndex):
        """
        update available mapping schemes list according to selected type
        """

        # get selected region/type
        region = self.ui.list_ms_library_regions.currentItem ().text()
        mstype = self.ui.list_ms_library_types.currentItem ().text()
        
        # adjust UI to display results
        #self.ui.list_ms_library_msnames.clear()
        self.resetMSLibrary(clearTypes=False)               
        for ms_name in self.msdb_dao.get_ms_in_region_type(region, mstype):
            self.ui.list_ms_library_msnames.addItem(QString(ms_name))        

    @uiCallChecker
    @logUICall
    def msSelected(self, modelIndex):
        """ visualize selected mapping scheme from available list """

        # get selected region/type/ms
        region = self.ui.list_ms_library_regions.currentItem ().text()
        ms_type = self.ui.list_ms_library_types.currentItem ().text()
        ms_name = self.ui.list_ms_library_msnames.currentItem().text()        
        
        # deserialize mapping scheme object from XML in DB
        [date_created, data_source, quality, use_notes, ms_xml] = self.msdb_dao.get_ms(region, ms_type, ms_name)
        
        self.ui.txt_ms_library_date.setText(date_created)
        self.ui.txt_ms_library_datasource.setText(data_source)
        self.ui.txt_ms_library_quality.setText(quality)
        self.ui.txt_ms_library_notes.setText(use_notes) 
        lib_ms = MappingScheme(None)
        lib_ms.from_text(ms_xml)
        
        # adjust UI to display results
        self.ui.tree_ms_library.setModel(MSTreeModel(lib_ms))
        self.ui.tree_ms_library.setSelectionMode(QAbstractItemView.SingleSelection)
        
        if (ms_type == get_ui_string('app.mslibrary.user.multilevel') or
            ms_type == get_ui_string('app.mslibrary.user.singlelevel')):
            self.ui.btn_del_lib_ms.setEnabled(True)
    
    def deleteLibraryMS(self):
        # get selected region/type/ms
        region = self.ui.list_ms_library_regions.currentItem ().text()
        ms_type = self.ui.list_ms_library_types.currentItem ().text()
        ms_name = self.ui.list_ms_library_msnames.currentItem().text()        
        
        if (ms_type != get_ui_string('app.mslibrary.user.multilevel') and
            ms_type != get_ui_string('app.mslibrary.user.singlelevel') ):
            QMessageBox.critical(self, 
                                 get_ui_string('app.warning.title'), 
                                 get_ui_string('widget.ms.library.delete.denied'))
            return
        # deserialize mapping scheme object from XML in DB
        self.msdb_dao.delete_ms(region, ms_type, ms_name)
        self.resetMSLibrary()        
    
    # internal helper methods
    ###############################
    def setMSLibraryEnabled(self, enable):
        self.ui.box_library.setEnabled(enable)
        self.ui.btn_add_branch.setEnabled(enable)
        if not enable:
            self.resetMSLibrary()           
    
    def getSelectedNode(self, tree):
        selectedIndexes = tree.selectedIndexes()
        if (len(selectedIndexes) <= 0):
            raise SIDDUIException(get_ui_string("widget.ms.warning.node.required"))
        if not selectedIndexes[0].isValid():
            raise SIDDUIException(get_ui_string("widget.ms.warning.node.invalid"))
        return selectedIndexes[0].internalPointer()

    def resetMSLibrary(self, clearTypes=True, clearNames=True):
        """ reset library UI """
        if clearTypes:
            self.ui.list_ms_library_types.clear()
        if clearNames:
            self.ui.list_ms_library_msnames.clear()
        self.ui.tree_ms_library.setModel(None)
        self.ui.txt_ms_library_date.setText("")
        self.ui.txt_ms_library_datasource.setText("")
        self.ui.txt_ms_library_quality.setText("")
        self.ui.txt_ms_library_notes.setText("")   
        self.ui.btn_del_lib_ms.setEnabled(False)      

    def retranslateUi(self, ui):
        ui.lb_panel_title.setText(get_ui_string("widget.ms.title"))
        ui.box_library.setTitle(get_ui_string("widget.ms.library.title"))
        ui.lb_ms_library_regions.setText(get_ui_string("widget.ms.library.regions"))
        ui.lb_ms_library_types.setText(get_ui_string("widget.ms.library.types"))
        ui.lb_ms_library_msnames.setText(get_ui_string("widget.ms.library.names"))
        ui.btn_secondary_mod.setText(get_ui_string("widget.ms.modifier"))
        ui.btn_build_exposure.setText(get_ui_string("widget.ms.build"))
        ui.ck_enable_ms_library.setText(get_ui_string("widget.ms.library.enable"))
        
        self.ui.lb_ms_library_date.setText(get_ui_string("widget.ms.library.date"))
        self.ui.lb_ms_library_datasource.setText(get_ui_string("widget.ms.library.datasource"))
        self.ui.lb_ms_library_quality.setText(get_ui_string("widget.ms.library.quality"))
        self.ui.lb_ms_library_notes.setText(get_ui_string("widget.ms.library.notes"))
