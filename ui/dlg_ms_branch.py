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
dialog for editing mapping scheme branches
"""
from PyQt4.QtGui import QDialog, QAbstractItemView
from PyQt4.QtCore import Qt, pyqtSlot, QObject

from sidd.ms import MappingScheme, MappingSchemeZone, Statistics, StatisticNode 

from ui.constants import logUICall
from ui.dlg_save_ms import DialogSaveMS
from ui.dlg_attr_range import DialogAttrRanges

from ui.qt.dlg_ms_branch_ui import Ui_editMSDialog
from ui.helper.ms_level_table import MSLevelTableModel
from ui.helper.ms_attr_delegate import MSAttributeItemDelegate

class DialogEditMS(Ui_editMSDialog, QDialog):
    """
    dialog for editing mapping scheme branches
    """
    # constructor
    ###############################
    
    def __init__(self, app):
        super(DialogEditMS, self).__init__()
        self.ui = Ui_editMSDialog()
        self.ui.setupUi(self)

        self.setFixedSize(self.size())  # no resize
        
        self.app =  app
        self.taxonomy = app.taxonomy

        # save mapping scheme dialog box        
        self.dlgSave = DialogSaveMS(self.app)
        self.dlgSave.setModal(True)
        
        # connect slots (ui events)
        self.ui.btn_apply.clicked.connect(self.updateWeights)
        self.ui.btn_add.clicked.connect(self.addValue)
        self.ui.btn_range.clicked.connect(self.editRanges)
        self.ui.btn_delete.clicked.connect(self.deleteValue)
        self.ui.cb_attributes.currentIndexChanged[str].connect(self.attributeUpdated)
        self.ui.btn_save.clicked.connect(self.saveMSBranch)
        self.ui.btn_close.clicked.connect(self.reject)

    # public properties
    ###############################

    @property
    def current_attribute(self):
        return self.ui.cb_attributes.currentText()

    # ui event handler
    ###############################
    @pyqtSlot(QObject)
    def resizeEvent(self, event):
        return
    
    @logUICall
    @pyqtSlot()
    def updateWeights(self):
        """ 
        event handler for btn_apply
        - return new set of values/weights to be applied  
        """
        self.values = self.levelModel.values
        self.weights = self.levelModel.weights
        # TODO: performs checks before returning
        # 1. no empty values
        # 2. weights add up to 100
        self.accept()
    
    @logUICall
    @pyqtSlot()
    def addValue(self):
        """ 
        event handler for btn_add
        - add another pair of value/weights  
        """
        self.levelModel.addValues()
    
    @logUICall 
    @pyqtSlot() 
    def deleteValue(self):
        """ 
        event handler for btn_delete
        - delete currently selected row of value/weights from table table_ms_level  
        """    
        selected = self.getSelectedCell()
        if selected is not None:
            self.levelModel.deleteValue(selected.row())

    @logUICall 
    @pyqtSlot()     
    def editRanges(self):
        attribute_name = str(self.ui.cb_attributes.currentText())
        
        if self.app.setRange(self._ranges, attribute_name):
            self.attributeUpdated(self.ui.cb_attributes.currentText())

    @logUICall
    @pyqtSlot()
    def saveMSBranch(self):
        """ 
        event handler for btn_save
        - open "Save mapping scheme" dialog box to save current set of values/weights
          as a single level mapping scheme
        """
        ms = MappingScheme(self.taxonomy)
        stats = Statistics(self.taxonomy)
        root = stats.get_tree()
        for v, w in map(None, self.levelModel.values, self.levelModel.weights):
            node = StatisticNode(root, '', v)
            node.weight = w
            root.children.append(node)
        stats.finalized = True
        ms.assign(MappingSchemeZone('ALL'), stats)
        
        self.dlgSave.setMS(ms, True)
        self.dlgSave.exec_()

    @logUICall
    @pyqtSlot(str)
    def attributeUpdated(self, attribute_name):        
        """ 
        event handler for cb_attributes
        - update list of possible values according to attribute selected
        """
        if attribute_name=='':
            return
        attribute = self.taxonomy.get_attribute_by_name(attribute_name)
        if attribute is None:
            return
        
        self.valid_codes = {}
        if attribute.type == 2: # numeric type that can have ranges
            
            # retrieve range if exists
            if self._ranges.has_key(str(attribute_name)):
                ranges = self._ranges[str(attribute_name)]                

                # add all ranges to list of codes for drop-down
                for min_val, max_val in map(None, ranges['min_values'], ranges['max_values']):
                    value = attribute.make_string([min_val, max_val])
                    self.valid_codes[value] = value
    
                # test for range [0,0], which is the unknown case
                if ranges['min_values'] >0 and ranges['max_values']>0:
                    value = attribute.make_string([None, None])
                    self.valid_codes[value] = value                    
            #else:
                # allow user use default edit feature
                            
            # enable button for editing ranges 
            self.ui.btn_range.setEnabled(True)
        else:               # code only types that cannot have ranges 
            try:
                node = self.node
                taxonomy = self.taxonomy
                filter_code = taxonomy.get_code_by_name(str(node.value))
                while filter_code.attribute.order > 1 and not taxonomy.has_rule(filter_code.attribute.name):
                    node = node.parent
                    filter_code = taxonomy.get_code_by_name(str(node.value))                                        
                attribute = taxonomy.get_attribute_by_name(attribute_name)                
                if filter_code.attribute.group.name != attribute.group.name:
                    filter_code = None
            except:
                filter_code = None
            for code in self.taxonomy.get_code_by_attribute(attribute_name, filter_code):
                self.valid_codes[code.description]=code.code
            # disable button for editing ranges            
            self.ui.btn_range.setEnabled(False)
        
        # set list of values to table editor
        # do not allow add if there is no codes available
        allow_add = False 
        if len(self.valid_codes) > 1:
            attr_editor = MSAttributeItemDelegate(self.ui.table_ms_level, self.valid_codes, 0)
            self.ui.table_ms_level.setItemDelegateForColumn(0, attr_editor)
            allow_add = True            
        
        # adjust ui
        self.ui.btn_add.setEnabled(allow_add)
        self.ui.btn_apply.setEnabled(allow_add)
        self.ui.btn_delete.setEnabled(allow_add)
        self.ui.btn_range.setEnabled(allow_add)
        self.ui.btn_save.setEnabled(allow_add)            

    # public methods    
    #############################            
    @logUICall
    def setNode(self, node, ranges, addNew=False):
        """ 
        shows values/weights in table_ms_level for given node
        if addNew values/weights correspond to node's children (if any)
        otherwise, values/weights are from node's sibling (if any) 
        """        
        self.ui.cb_attributes.clear()
        
        # create copy of values to be shown and modified
        values = []
        weights = []
        
        self._ranges = ranges
        if not addNew:
            self.node = node.parent
            attribute_name = node.name
            has_know_attribute = True
        else:
            self.node = node        
            if len(self.node.children) > 0:
                attribute_name = self.node.children[0].name
                has_know_attribute = True
            else:
                attribute_name = ""
                has_know_attribute = False
        
        if has_know_attribute:
            self.ui.cb_attributes.addItem(attribute_name)
        else:
            existing_attributes = node.ancestor_names
            existing_attributes.append(node.name)            
            
            node_attr = self.taxonomy.get_attribute_by_name(node.name)
            if node_attr is None:
                node_group, node_order = '', 1
            else:
                node_group, node_order = node_attr.group.name, node_attr.order 
                        
            for attr in self.taxonomy.attributes:
                try:
                    # make sure it does not already exist
                    existing_attributes.index(attr.name)
                except:
                    # this step reached if attribute not found in existing_attributes list 
                    add_attribute = False
                    # add 1st attribute of group or in current group  
                    if (node_group != attr.group.name and attr.order == 1 ):    
                        add_attribute = True
                    
                    # add next attribute of current group
                    if (node_group == attr.group.name and attr.order == node_order+1):
                        add_attribute = True
                        
                    if (add_attribute):
                        self.ui.cb_attributes.addItem(attr.name)
        
        for _child in self.node.children:
            values.append(str(_child.value))
            weights.append(_child.weight)
        
        self.levelModel = MSLevelTableModel(values, weights, self.taxonomy, self.taxonomy.codes,
                                            is_editable=[True, True])
        # initialize table view 
        tableUI = self.ui.table_ms_level                
        tableUI.setModel(self.levelModel)
        tableUI.setSelectionMode(QAbstractItemView.SingleSelection)
        table_width = tableUI.width()
        value_col_width = round(table_width*0.7, 0)
        tableUI.setColumnWidth(0, value_col_width)
        tableUI.setColumnWidth(1, table_width-value_col_width)
        tableUI.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # handle dataChanged event
        self.levelModel.dataChanged.connect(self.verifyWeights)
        
        # check total weights
        self.verifyWeights(None, None)

    def verifyWeights(self, startIndex, endIndex):
        sum_weights = sum(self.levelModel.weights)
        self.ui.txt_total_weights.setText('%.1f' % sum_weights)
        if (sum_weights == 100):
            self.ui.txt_total_weights.setStyleSheet('color:black')
            self.ui.btn_apply.setEnabled(True)
        else:
            self.ui.txt_total_weights.setStyleSheet('color:red')
            self.ui.btn_apply.setEnabled(False)

    # internal helper methods
    ###############################
    def getSelectedCell(self):
        """ return selected cell in table_ms_level """
        selectedIndexes = self.ui.table_ms_level.selectedIndexes()
        if (len(selectedIndexes) <= 0):
            logUICall.log('Please select node first.', logUICall.WARNING)            
            return None       
        if not selectedIndexes[0].isValid():
            logUICall.log('Select node does not support this function.', logUICall.WARNING)
            return None
        return selectedIndexes[0]    
