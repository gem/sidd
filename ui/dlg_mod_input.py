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
# Version: $Id: dlg_mod_input.py 18 2012-10-24 20:21:41Z zh $

"""
dialog for editing secondary modifiers
"""
from PyQt4.QtGui import *
from PyQt4.QtCore import *

from sidd.exception import *
from sidd.ms import *

from ui.constants import logUICall, get_ui_string 
from ui.qt.dlg_mod_input_ui import Ui_modifierInputDialog
from ui.helper.ms_level_table import MSLevelTableModel

class DialogModInput(Ui_modifierInputDialog, QDialog):
    """
    dialog for editing mapping scheme brances
    """
    
    def __init__(self, mainWin):
        super(DialogModInput, self).__init__()
        self.ui = Ui_modifierInputDialog()
        self.ui.setupUi(self)
        self.retranslateUi(self.ui)
        
        self.ui.table_mod_values.horizontalHeader().resizeSection(0, self.ui.table_mod_values.width() * 0.6)
        self.ui.table_mod_values.horizontalHeader().resizeSection(1, self.ui.table_mod_values.width() * 0.4)
        self.ui.btn_mod_build.setVisible(False)

    @logUICall
    def setNode(self, ms, mod, addNew=False):
        """ from given node, all sibling are used in dialog """
        self.ms = ms
        self.mod = mod
        self.addNew = addNew
        self.values = []
        self.weights = []
        self.node = None
        
        if not addNew and mod is not None:
            [zone_name, level1, level2, level3, startIdx, endIdx, modidx, modifier] = mod
            # get zone
            stats = self.ms.get_assignment_by_name(zone_name)
            root_node = stats.get_tree()
            # get level1 selections
            lv1_node = self.getSelectedNode(root_node, level1)            
            if lv1_node is not None:
                self.node = lv1_node 
            # get level2 selections
            lv2_node = self.getSelectedNode(lv1_node, level2)
            if lv2_node is not None:
                self.node = lv2_node 
            # get level3 selections
            lv3_node = self.getSelectedNode(lv2_node, level3)
            if lv3_node is not None:
                self.node = lv3_node 

            self.modidx = modidx
            for k, v in modifier.iteritems():                
                self.values.append(k)
                self.weights.append(v)

            # update combo values            
            self.ui.cb_ms_zone.clear()
            self.ui.cb_ms_zone.addItem(zone_name)
            self.ui.cb_level1.clear()
            self.ui.cb_level1.addItem(level1)
            self.ui.cb_level2.clear()
            self.ui.cb_level2.addItem(level2)
            self.ui.cb_level3.clear()
            self.ui.cb_level3.addItem(level3)
            
        else:            
            # set zone combo
            for zone in self.ms.get_zones():
                self.ui.cb_ms_zone.addItem(QString(zone.name))        
            #self.ui.cb_ms_zone.setCurrentIndex(self.ui.cb_ms_zone.findText(zone_name))
            self.modidx = -1
            
        self.modModel = MSLevelTableModel(self.values, self.weights)
        self.ui.table_mod_values.setModel(self.modModel)
            
    def zoneSelected(self):
        if not self.addNew :
            return
        stats = self.ms.get_assignment_by_name(self.ui.cb_ms_zone.currentText())
        self.root_node = stats.get_tree()        
        self.lv1_node = self.popComboxBox(self.ui.cb_level1, self.root_node, '')
        
    def level1Selected(self):
        if not self.addNew :
            return
        self.lv1_node = self.getSelectedNode(self.root_node, self.ui.cb_level1.currentText())
        if self.lv1_node is not None:
            self.node = self.lv1_node
        self.lv2_node = self.popComboxBox(self.ui.cb_level2, self.lv1_node, '')
    
    def level2Selected(self):
        if not self.addNew :
            return
        self.lv2_node = self.getSelectedNode(self.lv1_node, self.ui.cb_level2.currentText())
        if self.lv2_node is not None:
            self.node = self.lv2_node
        self.lv3_node = self.popComboxBox(self.ui.cb_level3, self.lv2_node, '')
    
    def level3Selected(self):
        if not self.addNew :
            return
        self.lv3_node = self.getSelectedNode(self.lv2_node, self.ui.cb_level3.currentText())
        if self.lv3_node is not None:
            self.node = self.lv3_node                        
    
    def setModifier(self):
        self.values = self.modModel.values
        self.weights = self.modModel.weights
        self.accept()
    
    
    def addValue(self):
        self.modModel.addValues()
    
    def deleteValue(self):
        self.modModel.deleteValue(self.getSelectedCell())
    
    def buildFromSurvey(self):
        pass
    
    def popComboxBox(self, cb, node, selected_val):        
        if node is None:
            return None
        cb.clear()
        cb.addItem(QString(''))
        child_node = None
        for child in node.children:
            child_val = child.value
            cb.addItem(QString(child_val))
            if selected_val == child_val:
                child_node = child
                cb.setCurrentIndex(cb.findText(selected_val))
        return child_node                

    # internal helper methods
    #############################

    def getSelectedNode(self, node, selected_val):        
        if node is None:
            return None
        child_node = None
        for child in node.children:
            child_val = child.value
            if selected_val == child_val:
                child_node = child
        return child_node

    def getSelectedCell(self):
        selectedIndexes = self.table_mod_values.selectedIndexes()
        if (len(selectedIndexes) <= 0):
            QMessageBox.warning(self, 'Node Not Selected', 'Please select node first.')
        if not selectedIndexes[0].isValid():
            QMessageBox.warning(self, 'Invalid Node', 'Select node does not support this function.')
        return selectedIndexes[0]
        
    def retranslateUi(self, ui):
        self.setWindowTitle(get_ui_string("dlg.mod.window.title"))
        ui.lb_title.setText(get_ui_string("dlg.mod.title"))
        ui.lb_ms_zone.setText(get_ui_string("dlg.mod.zone"))
        ui.lb_mod_values.setText(get_ui_string("dlg.mod.mod_values"))
        ui.lb_level1.setText(get_ui_string("dlg.mod.level1"))
        ui.lb_level2.setText(get_ui_string("dlg.mod.level2"))
        ui.lb_level3.setText(get_ui_string("dlg.mod.level3"))
        ui.btn_mod_build.setText(get_ui_string("dlg.mod.build"))
        ui.btn_ok.setText(get_ui_string("app.dialog.button.ok"))
        ui.btn_cancel.setText(get_ui_string("app.dialog.button.close"))
