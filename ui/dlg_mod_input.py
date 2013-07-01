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
dialog for editing secondary modifiers
"""
from PyQt4.QtGui import QCloseEvent, QDialog, QAbstractItemView, QItemSelectionModel
from PyQt4.QtCore import pyqtSlot, Qt, QSettings, QObject, QSize, QVariant

from sidd.ms import StatisticNode
from sidd.constants import SIDD_COMPANY, SIDD_APP_NAME, SIDD_VERSION

from ui.constants import logUICall, UI_PADDING 
from ui.qt.dlg_mod_input_ui import Ui_modifierInputDialog
from ui.helper.ms_level_table import MSLevelTableModel
from ui.helper.ms_tree import MSTreeModel

from ui.dlg_edit_attributes import DialogEditAttributes

class DialogModInput(Ui_modifierInputDialog, QDialog):
    """
    dialog for editing mapping scheme branches
    """
    
    # CONSTANTS
    #############################    
    UI_WINDOW_GEOM = 'dlg_mod_input/geometry'
        
    # constructor
    ###############################    
    def __init__(self, app):
        super(DialogModInput, self).__init__()
        self.ui = Ui_modifierInputDialog()
        self.ui.setupUi(self)
        
        self.settings = QSettings(SIDD_COMPANY, '%s %s' %(SIDD_APP_NAME, SIDD_VERSION));
        self.restoreGeometry(self.settings.value(self.UI_WINDOW_GEOM).toByteArray());
        
        self.app = app
        self.ms = None
        
        self.ui.table_mod_values.verticalHeader().hide()
                
        # connect slots (ui events)
        self.ui.btn_add.clicked.connect(self.addValue)
        self.ui.btn_delete.clicked.connect(self.deleteValue)
        self.ui.btn_apply.clicked.connect(self.setModifier)
        self.ui.btn_cancel.clicked.connect(self.reject)        
        self.ui.cb_attributes.currentIndexChanged[str].connect(self.setModifierName)
        self.ui.table_mod_values.doubleClicked.connect(self.editModValue)
        
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

    @pyqtSlot(QCloseEvent)
    def closeEvent(self, event):
        self.settings.setValue(self.UI_WINDOW_GEOM, self.saveGeometry());
        super(DialogModInput, self).closeEvent(event)
        
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
            if self.addNew:
                self.ui.cb_attributes.clear()
                taxonomy = self.ms.taxonomy
                names = node.descendant_names + [node.name] + node.ancestor_names
                group_names = [g.name for g in taxonomy.attributeGroups]
                for attribute in taxonomy.attributes:
                    try:
                        idx = names.index(attribute.name)
                        group_names.remove(attribute.group.name)
                    except:
                        # not found or already removed. not an error
                        pass                   
                
                if len(group_names) > 0:
                    self.ui.cb_attributes.addItems(group_names)
                    _allow_modifier=True 
                else:
                    _allow_modifier=False
                self.ui.btn_add.setEnabled(_allow_modifier)
                self.ui.btn_delete.setEnabled(_allow_modifier)
                self.ui.cb_attributes.setEnabled(_allow_modifier)
        else:
            self.node = None
    
    @logUICall
    @pyqtSlot(str)
    def setModifierName(self, selected_val):        
        self.modifier_name = selected_val
    
    @logUICall
    @pyqtSlot(QObject)
    def editModValue(self, index):
        if index.column() == 0:
            taxonomy = self.ms.taxonomy
            attribute = taxonomy.get_attribute_by_name(str(self.ui.cb_attributes.currentText()))
            """
            for _attribute in taxonomy.attributes:
                if _attribute.name == str(self.ui.cb_attributes.currentText()):
                    attribute = _attribute
                    break
            """
            if attribute is not None:
                index.model().set_cell_editable(index.column(), index.row(), False)
                edit_dlg = DialogEditAttributes(self.app,
                                                taxonomy, attribute,
                                                self.node.value, str(index.data().toString()))
                if edit_dlg.exec_() == QDialog.Accepted:                
                    index.model().setData(index, QVariant(edit_dlg.modifier_value), Qt.EditRole)
            else:
                index.model().set_cell_editable(index.column(), index.row())            

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
        self.ui.tree_ms.setEnabled(True)
        
        self.ui.cb_attributes.clear()
        
        if not addNew and mod is not None:
            # see MSTableModel about data in mod variable
            modidx, modifier, src_node = mod[4:]

            # expand tree from root to node 
            indices = self.tree_model.match(self.ui.tree_ms.rootIndex(), Qt.UserRole, src_node, 1)
            if len(indices)==1:
                index = indices[0]
                while index <> self.ui.tree_ms.rootIndex():
                    self.ui.tree_ms.setExpanded(index, True)
                    index = self.tree_model.parent(index)
            # set node as selected            
            self.ui.tree_ms.selectionModel().select(indices[0], QItemSelectionModel.ClearAndSelect | QItemSelectionModel.Rows)
            self.ui.tree_ms.setSelectionMode(QAbstractItemView.NoSelection)
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
            self.ui.tree_ms.setSelectionMode(QAbstractItemView.SingleSelection)
            # no modfier given
            # create event handler for selected node 
            self.ui.tree_ms.selectionModel().selectionChanged.connect(self.nodeSelected)            
            
            # create reference for use once dialog box returns
            self.modifier_name = 'Custom'
            self.modidx = -1
            
            # update additional UI elements based on given modifier 
            self.ui.txt_total_weights.setText('%.1f' % (0))
            #for attr in self.ms.taxonomy.attributes:
            #    self.ui.cb_attributes.addItem(attr.name)
            
            # cannot apply until values are set and node is selected
            self.ui.btn_apply.setEnabled(False)
        
        # initialize table of values
        self.modModel = MSLevelTableModel(self.values, self.weights, self.ms.taxonomy, self.ms.taxonomy.codes, 
                                          is_editable=[False, True])
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
            logUICall.log('Please select node first.', logUICall.WARNING)
            return None
        if not selectedIndexes[0].isValid():
            logUICall.log('Select node does not support this function.', logUICall.WARNING)
            return None
        return selectedIndexes[0]
       
