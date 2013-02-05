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
# Version: $Id: dlg_mod_input.py 21 2012-10-26 01:48:25Z zh $

"""
dialog for editing secondary modifiers
"""
from PyQt4.QtGui import QDialog, QMessageBox
from PyQt4.QtCore import QString

from ui.constants import logUICall, get_ui_string 
from ui.qt.dlg_mod_input_ui import Ui_modifierInputDialog
from ui.helper.ms_level_table import MSLevelTableModel

class DialogModInput(Ui_modifierInputDialog, QDialog):
    """
    dialog for editing mapping scheme branches
    """
    # constructor
    ###############################    
    def __init__(self, mainWin):
        super(DialogModInput, self).__init__()
        self.ui = Ui_modifierInputDialog()
        self.ui.setupUi(self)
        self.retranslateUi(self.ui)
        
        self.ui.table_mod_values.horizontalHeader().resizeSection(0, self.ui.table_mod_values.width() * 0.6)
        self.ui.table_mod_values.horizontalHeader().resizeSection(1, self.ui.table_mod_values.width() * 0.4)
        self.ui.btn_mod_build.setVisible(False)

        self.ms = None
    # ui event handler
    ###############################    
    def zoneSelected(self):
        """
        event handler for cb_ms_zone
        - update level1 combobox according to selected zone using mapping scheme tree
          and set target node as root node of selected zone
          do nothing if 
          1. not adding new modifiers or 
          2. mapping scheme not set internally (@see setNode)          
        """
        if not self.addNew or self.ms is None:
            return
        stats = self.ms.get_assignment_by_name(self.ui.cb_ms_zone.currentText())
        self.root_node = stats.get_tree()        
        self.lv1_node = self.popComboxBox(self.ui.cb_level1, self.root_node, '')
        
    def level1Selected(self):
        """
        event handler for cb_level1
        - update level2 combobox according to selected zone using mapping scheme tree
          and set target node as current level1 node
          do nothing if 
          1. not adding new modifiers or 
          2. mapping scheme not set internally (@see setNode)          
        """
        if not self.addNew or self.ms is None:
            return
        # TODO: getSelectedNode should be method in StatisticNode class
        self.lv1_node = self.getSelectedNode(self.root_node, self.ui.cb_level1.currentText())
        if self.lv1_node is not None:
            self.node = self.lv1_node
        self.lv2_node = self.popComboxBox(self.ui.cb_level2, self.lv1_node, '')
    
    def level2Selected(self):
        """
        event handler for cb_level2
        - update level3 combobox according to selected zone using mapping scheme tree
          and set target node as current level2 node
          do nothing if 
          1. not adding new modifiers or 
          2. mapping scheme not set internally (@see setNode)          
        """
        if not self.addNew or self.ms is None:
            return
        # TODO: getSelectedNode should be method in StatisticNode class
        self.lv2_node = self.getSelectedNode(self.lv1_node, self.ui.cb_level2.currentText())
        if self.lv2_node is not None:
            self.node = self.lv2_node
        self.lv3_node = self.popComboxBox(self.ui.cb_level3, self.lv2_node, '')
    
    def level3Selected(self):
        """
        event handler for cb_level2
        - set target node as current level2 node
          do nothing if 
          1. not adding new modifiers or 
          2. mapping scheme not set internally (@see setNode)          
        """
        if not self.addNew or self.ms is None:
            return
        # TODO: getSelectedNode should be method in StatisticNode class
        self.lv3_node = self.getSelectedNode(self.lv2_node, self.ui.cb_level3.currentText())
        if self.lv3_node is not None:
            self.node = self.lv3_node
    
    def setModifier(self):
        """ 
        event handler for btn_apply
        - return new set of values/weights to be applied  
        """
        self.values = self.modModel.values
        self.weights = self.modModel.weights
        # TODO: performs checks before returning
        # 1. no empty values
        # 2. weights add up to 100        
        self.accept()    
    
    def addValue(self):
        """
        event handler for btn_add
        - add another pair of value/weights to table_mod_values
        """
        self.modModel.addValues()
    
    def deleteValue(self):
        """
        event handler for btn_delete
        - delete currently selected row of value/weights from table_mod_values          
        """
        selected = self.getSelectedCell()
        if selected is not None:
            self.modModel.deleteValue(selected)
    
    def buildFromSurvey(self):
        """ event handler for btn_mod_build """
        # TODO: delete btn_mod_build and this method 
        pass
    
    
    # public method
    ###############################
    
    @logUICall
    def setNode(self, ms, mod, addNew=False):
        """ 
        shows values/weights in table_mod_values for given node
        if addNew values/weights are two empty lists 
        otherwise, values/weights are from take from given mod  
        """ 
        self.ms = ms
        self.mod = mod
        self.addNew = addNew
        self.values = []
        self.weights = []
        self.node = None
        
        if not addNew and mod is not None:
            [zone_name, level1, level2, level3, startIdx, endIdx, modidx, modifier, src_node] = mod
            self.node = src_node
            
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

    # internal helper methods
    #############################
    def popComboxBox(self, cb, node, selected_val):
        """
        populate given combobox with node's children's value
        and show selected_val as selected   
        """
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
    
    def getSelectedNode(self, node, selected_val):
        """
        retrieve node's child with same value as selected_val
        """
        # TODO: refactor into StatisticNode
        if node is None:
            return None
        child_node = None
        for child in node.children:
            child_val = child.value
            if selected_val == child_val:
                child_node = child
        return child_node

    def getSelectedCell(self):
        """ return selected cell in table_mod_values """        
        selectedIndexes = self.ui.table_mod_values.selectedIndexes()
        if (len(selectedIndexes) <= 0):
            QMessageBox.warning(self, 'Node Not Selected', 'Please select node first.')
            return None
        if not selectedIndexes[0].isValid():
            QMessageBox.warning(self, 'Invalid Node', 'Select node does not support this function.')
            return None
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
        ui.btn_apply.setText(get_ui_string("app.dialog.button.apply"))
        ui.btn_cancel.setText(get_ui_string("app.dialog.button.close"))
