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
# Version: $Id: wdg_ms.py 21 2012-10-26 01:48:25Z zh $

"""
Widget (Panel) for creating mapping scheme
"""
from PyQt4.QtGui import QWidget, QMessageBox, QDialog, QAbstractItemView
from PyQt4.QtCore import QObject, QSize, QPoint, pyqtSlot, QString

from sidd.ms import MappingScheme, MappingSchemeZone, StatisticNode 
from sidd.exception import SIDDException

from ui.exception import SIDDUIException
from ui.constants import logUICall, get_ui_string, UI_PADDING
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
                    logUICall.log('function call %s from module %s' % (f.__name__, f.__module__), logUICall.DEBUG)                    
                    return f(*args, **kw)                
                except SIDDUIException as uie:
                    logUICall.log(get_ui_string("app.error.unexpected"), logUICall.WARNING)
                    QMessageBox.warning(None, get_ui_string("app.error.unexpected"), str(uie))
                except SIDDException as se:
                    logUICall.log(get_ui_string("app.error.model"), logUICall.ERROR)
                    QMessageBox.critical(None,get_ui_string("app.error.model"), str(se))
                except Exception as e:
                    logUICall.log(get_ui_string("app.error.ui"), logUICall.ERROR)
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
        self.dlgEditMS.setModal(True)
        self.dlgSaveMS = DialogSaveMS(self.app)        
        self.dlgSaveMS.setModal(True)

        # connect slots (ui event)
        self.ui.btn_build_ms.clicked.connect(self.buildMS)
        self.ui.btn_create_ms.clicked.connect(self.createMS)
        self.ui.btn_save_ms.clicked.connect(self.saveMS)
        self.ui.btn_add_child.clicked.connect(self.addBranch)
        self.ui.btn_del_child.clicked.connect(self.removeBranch)
        self.ui.btn_edit_level.clicked.connect(self.editBranch)

        self.ui.ck_enable_ms_library.clicked.connect(self.toggleMSLibrary)
        self.ui.list_ms_library_regions.clicked.connect(self.regionSelected)
        self.ui.list_ms_library_types.clicked.connect(self.typeSelected)
        self.ui.list_ms_library_msnames.clicked.connect(self.msSelected)
        self.ui.btn_del_lib_ms.clicked.connect(self.deleteLibraryMS)

        self.ui.btn_add_branch.clicked.connect(self.appendBranch)

        self.ui.btn_secondary_mod.clicked.connect(self.setModifiers)
        self.ui.btn_build_exposure.clicked.connect(self.applyMS)
        

    # UI event handling calls
    ###############################
    @pyqtSlot(QObject)
    def resizeEvent(self, event):
        """ handle window resize """ 
        ui = self.ui
        # right align box_ms_library
        ui.box_ms_library.move(
            QPoint(self.width()-ui.box_ms_library.width()-UI_PADDING,
                   ui.box_ms_library.y()))
        ui.ck_enable_ms_library.move(
            QPoint(ui.box_ms_library.x(),ui.ck_enable_ms_library.y()))
        
        # move buttons to bottom right
        ui.btn_build_exposure.move(
            QPoint(self.width()-ui.btn_build_exposure.width()-UI_PADDING,
                   self.height()-ui.btn_build_exposure.height()-UI_PADDING))
        ui.btn_secondary_mod.move(
            QPoint(ui.btn_build_exposure.x()-ui.btn_secondary_mod.width()-UI_PADDING,
                   ui.btn_build_exposure.y()))
        # move append branch button next to the box_ms_library
        ui.btn_add_branch.move(
            QPoint(ui.box_ms_library.x()-ui.btn_add_branch.width()-(UI_PADDING/2),
                   ui.box_ms_library.y()+(ui.box_ms_library.height()/2)))
        # adjust widget_ms_tree
        ui.widget_ms_tree.resize(
            QSize(ui.btn_add_branch.x()-ui.widget_ms_tree.x()-(UI_PADDING/2),
                  ui.btn_build_exposure.y()-ui.widget_ms_tree.y()-UI_PADDING))        
        ui.tree_ms.resize(QSize(ui.widget_ms_tree.width(), ui.widget_ms_tree.height()-ui.tree_ms.y()))
        ui.widget_ms_buttons_r.move(
            QPoint(ui.widget_ms_tree.width()-ui.widget_ms_buttons_r.width(), ui.widget_ms_buttons_r.y()))
        # adjust size of 
        logUICall.log('resize done for %s' % self.__module__, logUICall.INFO)
    
    @uiCallChecker
    @pyqtSlot()
    def buildMS(self):
        """ build mapping scheme from survey data """
        self.app.buildMappingScheme()

    @uiCallChecker
    @pyqtSlot()
    def createMS(self):
        """ create new mapping scheme """
        self.app.createEmptyMS()
        
    @uiCallChecker
    @pyqtSlot()
    def saveMS(self):
        """ save existing mapping scheme """
        if self.ms is not None:
            # show save dialogbox for mapping scheme
            self.dlgSaveMS.setMS(self.ms)
            self.dlgSaveMS.exec_()

    @uiCallChecker
    @pyqtSlot()
    def addBranch(self):
        """ add branch to mapping scheme """
        node = self.getSelectedNode(self.ui.tree_ms)
        if type(node) == MappingSchemeZone:
            node = node.stats.get_tree()
        
        # show save dialogbox for selected node
        self.dlgEditMS.setNode(node, addNew=True)
        ans = self.dlgEditMS.exec_()

        # accepted means apply change        
        if ans == QDialog.Accepted:
            # NOTE: dlgEditMS should already have performed all the checks on 
            #       values/weights pair, we can safely assume that data is clean 
            #       to be used    
                        
            # TODO: refactor call into main controller
            node.update_children(self.dlgEditMS.current_attribute, self.dlgEditMS.values, self.dlgEditMS.weights)
            self.app.visualizeMappingScheme(self.ms)

    @uiCallChecker
    @pyqtSlot()
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
    @pyqtSlot()
    def editBranch(self):
        """ edit a branch from mapping scheme tree """
        node = self.getSelectedNode(self.ui.tree_ms)
        if type(node) != StatisticNode:
            # cannot continue if if zone or tree model root node 
            # (not statistic tree root node)
            QMessageBox.warning(self, 
                                get_ui_string("app.warning.title"),
                                get_ui_string("widget.ms.warning.node.required"))
            return        
        # not zone / not root, good to continue
        
        # show save dialogbox for selected node
        self.dlgEditMS.setNode(node)
        ans = self.dlgEditMS.exec_()

        # accepted means apply change        
        if ans == QDialog.Accepted:
            # NOTE: dlgEditMS should already have performed all the checks on 
            #       values/weights pair, we can safely assume that data is clean 
            #       to be used    

            # TODO: refactor call into main controller            
            node.parent.update_children(self.dlgEditMS.current_attribute, self.dlgEditMS.values, self.dlgEditMS.weights)
            #self.app.visualizeMappingScheme(self.ms)
            self.refreshTree()
            

    @uiCallChecker
    @pyqtSlot()
    def appendBranch(self):
        """ 
        event handler for btn_add_branch 
        - append branch to mapping scheme tree 
        """
        # get selected node from working mapping scheme tree
        node = self.getSelectedNode(self.ui.tree_ms)
        branch = self.getSelectedNode(self.ui.tree_ms_library)        
        self.app.appendMSBranch(node, branch)
        
    @uiCallChecker
    @pyqtSlot()
    def setModifiers(self):
        """
        event handler for btn_secondary_mod 
        - switch view to secondary modifier tab
        """        
        self.app.showTab(2)

    @uiCallChecker
    @pyqtSlot()
    def applyMS(self):
        """  
        event handler for btn_build_exposure 
        - apply mapping scheme and generate exposure 
        """        
        self.app.buildExposure()
    
    @logUICall
    @pyqtSlot(bool)
    def toggleMSLibrary(self, value):
        """ 
        event handler for ck_enable_ms_library
        - toggle access to mapping scheme library 
        """        
        self.setMSLibraryEnabled(value)

    @uiCallChecker
    @pyqtSlot(int)
    def regionSelected(self, modelIndex):
        """
        update mapping scheme types and available mapping schemes list
        according to selected region
        """
        # get selected region
        region = self.ui.list_ms_library_regions.currentItem ().text()
        
        # adjust UI to display results
        self.resetMSLibrary()
        for mstype in self.msdb_dao.get_types_in_region(region):
            self.ui.list_ms_library_types.addItem(QString(mstype))
        
    @uiCallChecker
    @pyqtSlot(int)
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
    @pyqtSlot(int)
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

    @uiCallChecker
    @pyqtSlot()    
    def deleteLibraryMS(self):
        # get selected region/type/ms
        region = self.ui.list_ms_library_regions.currentItem ().text()
        ms_type = self.ui.list_ms_library_types.currentItem ().text()
        ms_name = self.ui.list_ms_library_msnames.currentItem().text()        
        
        if (ms_type != get_ui_string('app.mslibrary.user.multilevel') and
            ms_type != get_ui_string('app.mslibrary.user.singlelevel')):
            QMessageBox.critical(self, 
                                 get_ui_string('app.warning.title'), 
                                 get_ui_string('widget.ms.library.delete.denied'))
            return
        # deserialize mapping scheme object from XML in DB
        self.msdb_dao.delete_ms(region, ms_type, ms_name)
        self.resetMSLibrary()        
        
    # public methods
    ###############################
    
    @logUICall
    def showMappingScheme(self, ms):
        """ display mapping scheme """
        self.ms = ms
        treeUI = self.ui.tree_ms
        self.tree_model = MSTreeModel(ms)        
        treeUI.setModel(self.tree_model)
        treeUI.setSelectionMode(QAbstractItemView.SingleSelection)
        self.ui.tree_ms.setEnabled(True)

    
    def refreshTree(self):
        indices = self.tree_model.persistentIndexList()
        for index in indices:
            if self.ui.tree_ms.isExpanded(index):
                self.ui.tree_ms.setExpanded(index, False)             
                self.ui.tree_ms.setExpanded(index, True)            
        
    @logUICall
    def clearMappingScheme(self):
        self.ms = None
        self.ui.tree_ms.setModel(None)
        self.ui.tree_ms.setEnabled(False)
    
    # internal helper methods
    ###############################
    def setMSLibraryEnabled(self, enable):
        """ toggle access to mapping scheme library """
        self.ui.box_ms_library.setEnabled(enable)
        self.ui.btn_add_branch.setEnabled(enable)
        if not enable:
            self.resetMSLibrary()
    
    def getSelectedNode(self, tree):
        """ retrieve currently selected node from given tree """
        selectedIndexes = tree.selectedIndexes()
        if (len(selectedIndexes) <= 0):
            raise SIDDUIException(get_ui_string("widget.ms.warning.node.required"))
            return None
        if not selectedIndexes[0].isValid():
            raise SIDDUIException(get_ui_string("widget.ms.warning.node.invalid"))
            return None
        return selectedIndexes[0].internalPointer()

    def resetMSLibrary(self, clearTypes=True, clearNames=True):
        """ reset mapping scheme library UI elements """
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
        ui.box_ms_library.setTitle(get_ui_string("widget.ms.library.title"))
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
