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
# Version: $Id: wdg_mod.py 21 2012-10-26 01:48:25Z zh $

"""
Widget (Panel) for managing secondary modifier 
"""
from PyQt4.QtGui import QWidget, QDialog, QMessageBox, QAbstractItemView
from PyQt4.QtCore import pyqtSlot, Qt, QSize, QPoint 

from sidd.ms.node import StatisticModifier

from ui.constants import logUICall, get_ui_string, UI_PADDING
from ui.qt.wdg_mod_ui import Ui_widgetSecondaryModifier
from ui.helper.ms_table import MSTableModel
from ui.dlg_mod_input import DialogModInput

class WidgetSecondaryModifier(Ui_widgetSecondaryModifier, QWidget):    
    """
    Widget (Panel) for managing secondary modifier 
    """
    # constructor / destructor
    ###############################        
    def __init__(self, app):
        """ constructor """
        super(WidgetSecondaryModifier, self).__init__()
        self.ui = Ui_widgetSecondaryModifier()
        self.ui.setupUi(self)
        self.retranslateUi(self.ui)

        self.ui.table_mod.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ui.table_mod.setSelectionMode(QAbstractItemView.SingleSelection)

        self.dlgEditMod = DialogModInput(app)
        self.dlgEditMod.setModal(True)
        self.app = app
        
        # connect slots (ui event)
        self.ui.btn_add_mod.clicked.connect(self.addModifier)
        self.ui.btn_del_mod.clicked.connect(self.deleteModifier)
        self.ui.btn_edit_mod.clicked.connect(self.editModifier)
        self.ui.btn_build_exposure.clicked.connect(self.applyMS)
        
    # ui event handler
    ###############################
    def resizeEvent(self, event):
        """ handle window resize """
        self.ui.btn_build_exposure.move(self.width()-self.ui.btn_build_exposure.width()-UI_PADDING,
                                        self.height()-self.ui.btn_build_exposure.height()-UI_PADDING)
        self.ui.widget_buttons.move(self.width()-self.ui.widget_buttons.width()-UI_PADDING,
                                    self.ui.widget_buttons.y())
        self.ui.table_mod.resize(self.width()-2*UI_PADDING,
                                 self.height()-self.ui.table_mod.y()-self.ui.btn_build_exposure.height()-2*UI_PADDING)
        # adjust columns size
        self.ui.table_mod.horizontalHeader().resizeSection(0, self.ui.table_mod.width() * 0.1)
        self.ui.table_mod.horizontalHeader().resizeSection(1, self.ui.table_mod.width() * 0.6)
        self.ui.table_mod.horizontalHeader().resizeSection(2, self.ui.table_mod.width() * 0.1)
        self.ui.table_mod.horizontalHeader().resizeSection(3, self.ui.table_mod.width() * 0.1)
        
    @logUICall
    @pyqtSlot()
    def addModifier(self):
        """ add a modifier to mapping scheme. update table view """
        
        # show edit dialog box for new modifier
        self.dlgEditMod.setNode(self.ms, None, addNew=True)
        ans = self.dlgEditMod.exec_()
        
        # accepted means apply change
        if ans == QDialog.Accepted:
            # NOTE: dlgEditMod already should have performed all the checks on 
            #       values/weights pair, we can safely assume that data is clean 
            #       to be used 
            if self.dlgEditMod.node is not None:
                modifier = StatisticModifier(self.dlgEditMod.modifier_name)
                for value, weight in map(None, self.dlgEditMod.values, self.dlgEditMod.weights):
                    modifier.values[value] = weight
                self.dlgEditMod.node.set_modifier(self.dlgEditMod.modidx, modifier)
            self.app.visualizeMappingScheme(self.ms)

    @logUICall
    @pyqtSlot()
    def deleteModifier(self):
        """ delete selected modifier from mapping scheme. update table view """
        mod = self.getSelectedModifier()
        # make sure there is mod selected
        if mod is None:
            QMessageBox.warning(self, 
                                get_ui_string("app.warning.title"),
                                get_ui_string("widget.ms.warning.node.required"))
            return
        # confirm delete 
        answer = QMessageBox.warning(self,
                                     get_ui_string("app.popup.delete.confirm"),
                                     get_ui_string("widget.mod.warning.delete"),
                                     QMessageBox.Yes | QMessageBox.No)
        if answer == QMessageBox.Yes:
            # see MSTableModel about data in mod variable
            modidx, src_node = mod[4], mod[6]
            if src_node is not None:
                # remove modifier
                src_node.remove_modifier(modidx)
            self.app.visualizeMappingScheme(self.ms)
        
    @logUICall
    @pyqtSlot()
    def editModifier(self):
        """ edit selected modifier """
        mod = self.getSelectedModifier()
        # make sure there is mod selected
        if mod is None:
            QMessageBox.warning(self, 
                                get_ui_string("app.warning.title"),
                                get_ui_string("widget.ms.warning.node.required"))
            return
        
        # show edit dialog box for selected modifier
        self.dlgEditMod.setNode(self.ms, mod)
        ans = self.dlgEditMod.exec_()
        
        # accepted means apply change
        if ans == QDialog.Accepted:
            # NOTE: dlgEditMod already should have performed all the checks on 
            #       values/weights pair, we can safely assume that data is clean 
            #       to be used
            #[zone_name, bldg_type, startIdx, endIdx, modidx, modifier, node] = mod
            if self.dlgEditMod.node is not None:
                modifier = StatisticModifier(self.dlgEditMod.modifier_name)
                for value, weight in map(None, self.dlgEditMod.values, self.dlgEditMod.weights):
                    modifier.values[value] = weight
                self.dlgEditMod.node.set_modifier(self.dlgEditMod.modidx, modifier)
            self.app.visualizeMappingScheme(self.ms)
        
    @logUICall
    @pyqtSlot()
    def applyMS(self):
        """ apply mapping scheme and modifiers """
        self.app.buildExposure()

    # public methods
    ###############################
    def showMappingScheme(self, ms):
        self.ms = ms
        self.ui.table_mod.setModel(MSTableModel(ms))        
        self.ui.table_mod.resizeRowsToContents()        
        # adjust columns size
        self.ui.table_mod.horizontalHeader().resizeSection(0, self.ui.table_mod.width() * 0.1)
        self.ui.table_mod.horizontalHeader().resizeSection(1, self.ui.table_mod.width() * 0.6)
        self.ui.table_mod.horizontalHeader().resizeSection(2, self.ui.table_mod.width() * 0.1)
        self.ui.table_mod.horizontalHeader().resizeSection(3, self.ui.table_mod.width() * 0.1)        

        self.ui.btn_add_mod.setEnabled(True)
        self.ui.btn_del_mod.setEnabled(True)
        self.ui.btn_edit_mod.setEnabled(True)
        self.ui.btn_build_exposure.setEnabled(True)

    
    def closeMappingScheme(self):
        """ clear current view """
        self.ui.table_mod.setModel(None)
        self.ui.btn_add_mod.setEnabled(False)
        self.ui.btn_del_mod.setEnabled(False)
        self.ui.btn_edit_mod.setEnabled(False)
        self.ui.btn_build_exposure.setEnabled(False)

    # internal helper methods
    ###############################
    def getSelectedModifier(self):
        selected =self.ui.table_mod.selectedIndexes()
        if (len(selected) > 0):
            return selected[0].internalPointer()
        else:
            return None, None

    def retranslateUi(self, ui):
        ui.lb_panel_title.setText(get_ui_string("widget.mod.title"))        
        ui.btn_build_exposure.setText(get_ui_string("widget.mod.build"))
        