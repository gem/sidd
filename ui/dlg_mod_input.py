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

from sidd.ms import StatisticNode

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
        self.ui.btn_add.clicked.connect(self.addValue)
        self.ui.btn_delete.clicked.connect(self.deleteValue)
        self.ui.btn_apply.clicked.connect(self.setModifier)
        self.ui.btn_cancel.clicked.connect(self.reject)
        
        self.ui.cb_attributes.currentIndexChanged[str].connect(self.setModifierName)
        
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
        # adjust attributes label and combobox
        ui.lb_attribute.move(ui.lb_mod_values.x(),
                             ui.lb_attribute.y())
        ui.cb_attributes.setGeometry(ui.lb_mod_values.x(), ui.cb_attributes.y(),
                                     w * 0.5, ui.cb_attributes.height())
                
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
            self.modModel.deleteValue(selected.row())

    @logUICall
    @pyqtSlot()
    def nodeSelected(self):
        """ 
        event handler for tree_ms
        use tree view to set currently selected node         
        """
        index = self.ui.tree_ms.selectedIndexes()[0]        
        node = index.internalPointer()
        if isinstance(node, StatisticNode):
            self.node = node
        else:
            self.node = None
    
    @logUICall
    @pyqtSlot(str)
    def setModifierName(self, selected_val):        
        self.modifier_name = selected_val
    
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
                
        # construct mapping scheme tree
        self.tree_model = MSTreeModel(ms)        
        self.ui.tree_ms.setModel(self.tree_model)
        self.ui.tree_ms.setSelectionMode(QAbstractItemView.SingleSelection)
        self.ui.tree_ms.setEnabled(True)
        
        self.ui.cb_attributes.clear()
        
        if not addNew and mod is not None:
            # see MSTableModel about data in mod variable
            modidx, modifier, src_node = mod[4:]

            # expand tree from root to node 
            indices = self.tree_model.match(self.ui.tree_ms.rootIndex(), Qt.DisplayRole, src_node.value, 1)            
            if len(indices)==1:
                index = indices[0]
                while index <> self.ui.tree_ms.rootIndex():
                    self.ui.tree_ms.setExpanded(index, True)
                    index = self.tree_model.parent(index)
            # set node as selected            
            self.ui.tree_ms.selectionModel().select(indices[0], QItemSelectionModel.ClearAndSelect | QItemSelectionModel.Rows)
            
            # create reference for use once dialog box returns
            self.node = src_node
            self.modidx = modidx
            self.modifier_name = modifier.name
            
            # store values in modifier 
            for k, v in modifier.iteritems():                
                self.values.append(k)
                self.weights.append(v)
            
            # update additional UI elements based on given modifier 
            self.ui.txt_total_weights.setText('%.1f' % (sum(self.weights)))            
            self.ui.cb_attributes.addItem(modifier.name)
        else:
            # no modfier given
            # create event handler for selected node 
            self.ui.tree_ms.selectionModel().selectionChanged.connect(self.nodeSelected)
            
            # create reference for use once dialog box returns
            self.modifier_name = 'Custom'
            self.modidx = -1
            
            # update additional UI elements based on given modifier 
            self.ui.txt_total_weights.setText('%.1f' % (0))
            for attr in self.ms.taxonomy.attributes:
                self.ui.cb_attributes.addItem(attr.name)
            
            # cannot apply until values are set and node is selected
            self.ui.btn_apply.setEnabled(False)            
        
        # initialize table of values
        self.modModel = MSLevelTableModel(self.values, self.weights)
        self.ui.table_mod_values.setModel(self.modModel)
        # update total once table value is changed
        self.modModel.dataChanged.connect(self.verifyWeights)

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
