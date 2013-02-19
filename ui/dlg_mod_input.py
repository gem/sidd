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
from PyQt4.QtGui import QDialog, QMessageBox, QAbstractItemView, QItemSelectionModel
from PyQt4.QtCore import pyqtSlot, Qt, QObject, QSize

from sidd.ms import MappingSchemeZone, StatisticNode

from ui.constants import logUICall, get_ui_string, UI_PADDING 
from ui.qt.dlg_mod_input_ui import Ui_modifierInputDialog
from ui.helper.ms_level_table import MSLevelTableModel
from ui.helper.ms_tree import MSTreeModel

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
        
        self.ms = None
        
        self.ui.table_mod_values.verticalHeader().hide()
                
        # connect slots (ui events)
        self.ui.btn_mod_build.clicked.connect(self.buildFromSurvey)
        self.ui.btn_add.clicked.connect(self.addValue)
        self.ui.btn_delete.clicked.connect(self.deleteValue)
        self.ui.btn_apply.clicked.connect(self.setModifier)
        self.ui.btn_cancel.clicked.connect(self.reject)
        
        # hide mod_build button
        self.ui.btn_mod_build.setVisible(False)
        
    # ui event handler
    ###############################
    @pyqtSlot(QObject)
    def resizeEvent(self, event):
        """ handle window resize """ 
        ui = self.ui
        w= self.width()-3*UI_PADDING        

        # set up bottom right for dialog buttons
        ui.btn_cancel.move(self.width()-ui.btn_cancel.width()-UI_PADDING, 
                           self.height()-ui.btn_cancel.height()-UI_PADDING)
        ui.btn_apply.move(ui.btn_cancel.x()-ui.btn_apply.width()-UI_PADDING,
                          ui.btn_cancel.y())
        # set left panel for mapping scheme tree 
        ui.tree_ms.resize(QSize(w*0.5, ui.btn_cancel.y()-ui.tree_ms.y()-UI_PADDING))
        # adjust label / buttons on top of table
        ui.lb_mod_values.move(ui.tree_ms.x()+ui.tree_ms.width()+UI_PADDING, 
                              ui.lb_mod_values.y())        
        ui.widget_mod_values_menu_r.move(self.width()-ui.widget_mod_values_menu_r.width()-UI_PADDING,
                                         ui.widget_mod_values_menu_r.y())        
        # adjust label/txtbox at topp of the table
        ui.lb_percent.move(self.width()-ui.lb_percent.width()-UI_PADDING, 
                           ui.btn_cancel.y()-ui.lb_percent.height()-UI_PADDING)
        ui.txt_total_weights.move(ui.lb_percent.x()-ui.txt_total_weights.width(), ui.lb_percent.y())
        ui.lb_total_weights.move(ui.txt_total_weights.x()-ui.lb_total_weights.width()-UI_PADDING,
                                 ui.lb_percent.y())        
        # set right panel for mod table
        ui.table_mod_values.setGeometry(ui.lb_mod_values.x(), ui.table_mod_values.y(),
                                        w * 0.5, ui.lb_percent.y()-ui.table_mod_values.y()-UI_PADDING)           
        ui.table_mod_values.horizontalHeader().resizeSection(0, ui.table_mod_values.width() * 0.6)
        ui.table_mod_values.horizontalHeader().resizeSection(1, ui.table_mod_values.width() * 0.4)               
        
    @logUICall
    @pyqtSlot()
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
    
    @logUICall
    @pyqtSlot()
    def addValue(self):
        """
        event handler for btn_add
        - add another pair of value/weights to table_mod_values
        """
        self.modModel.addValues()
    
    @logUICall
    @pyqtSlot()
    def deleteValue(self):
        """
        event handler for btn_delete
        - delete currently selected row of value/weights from table_mod_values          
        """
        selected = self.getSelectedCell()
        if selected is not None:
            self.modModel.deleteValue(selected)
    
    @logUICall
    @pyqtSlot()
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
                
        treeUI = self.ui.tree_ms
        self.tree_model = MSTreeModel(ms)        
        treeUI.setModel(self.tree_model)
        treeUI.setSelectionMode(QAbstractItemView.SingleSelection)
        self.ui.tree_ms.setEnabled(True)
        
        if not addNew and mod is not None:
            #[zone_name, level1, level2, level3, startIdx, endIdx, modidx, modifier, src_node] = mod
            [zone_name, parent_str, startIdx, endIdx, modidx, modifier, src_node] = mod
            indices = self.tree_model.match(treeUI.rootIndex(), Qt.DisplayRole, src_node.value, 1)            
            if len(indices)==1:
                index = indices[0]
                while index <> treeUI.rootIndex():
                    treeUI.setExpanded(index, True)
                    index = self.tree_model.parent(index)            
            treeUI.selectionModel().select(indices[0], QItemSelectionModel.ClearAndSelect | QItemSelectionModel.Rows)
            self.node = src_node
            self.modidx = modidx
            for k, v in modifier.iteritems():                
                self.values.append(k)
                self.weights.append(v)
            self.ui.txt_total_weights.setText('%.1f' % (sum(self.weights)))
        else:
            self.ui.txt_total_weights.setText('%.1f' % (0))
            self.ui.btn_apply.setEnabled(False)
            treeUI.selectionModel().selectionChanged.connect(self.nodeSelected)

        self.modModel = MSLevelTableModel(self.values, self.weights)
        self.ui.table_mod_values.setModel(self.modModel)
        self.modModel.dataChanged.connect(self.verifyWeights)

    def nodeSelected(self):
        index = self.ui.tree_ms.selectedIndexes()[0]        
        node = index.internalPointer()
        if isinstance(node, StatisticNode):
            self.node = node
        else:
            self.node = None

    # internal helper methods
    #############################
    def verifyWeights(self, startIndex, endIndex):
        sum_weights = sum(self.modModel.weights)
        self.ui.txt_total_weights.setText('%.1f' % sum_weights)
        if (sum_weights == 100):
            self.ui.txt_total_weights.setStyleSheet('color:black')
            self.ui.btn_apply.setEnabled(True)
        else:
            self.ui.txt_total_weights.setStyleSheet('color:red')
            self.ui.btn_apply.setEnabled(False)

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

        ui.lb_mod_values.setText(get_ui_string("dlg.mod.mod_values"))
        ui.lb_ms_tree.setText('Mapping Scheme Tree')
        ui.lb_total_weights.setText('Values')
        
        ui.btn_apply.setText(get_ui_string("app.dialog.button.apply"))
        ui.btn_cancel.setText(get_ui_string("app.dialog.button.close"))
