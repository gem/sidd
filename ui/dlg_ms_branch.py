# Copyright (c) 2011-2013, ImageCat Inc.
#
# SIDD is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
#
"""
dialog for editing mapping scheme branches
"""
from PyQt4.QtGui import QDialog, QMessageBox, QAbstractItemView
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
        
        self.dlgAttrRange = DialogAttrRanges()
        
        # connect slots (ui events)
        self.ui.btn_apply.clicked.connect(self.updateWeights)
        self.ui.btn_add.clicked.connect(self.addValue)
        self.ui.btn_delete.clicked.connect(self.deleteValue)        
        self.ui.cb_attributes.currentIndexChanged[str].connect(self.attributeUpdated)        
        self.ui.btn_save.clicked.connect(self.saveMSBranch)
        self.ui.btn_close.clicked.connect(self.reject)
        
        self.initialized = True
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
    def attributeUpdated(self, new_attribute):        
        """ 
        event handler for cb_attributes
        - update list of possible values according to attribute selected
        """
        if not self.initialized:
            return
        attribute_name = new_attribute
        
        attribute = None
        for attr in self.taxonomy.attributes:
            if attr.name == attribute_name:
                attribute = attr
                break
        
        self.valid_codes = {}
        if attribute.type == 20000:
            if self._ranges.has_key(str(attribute_name)):
                ranges = self._ranges[attribute_name]
                self.dlgAttrRange.set_values(attribute_name, ranges['min_values'], ranges['max_values'])
            else:
                self.dlgAttrRange.set_values(attribute_name, [], [])
            if self.dlgAttrRange.exec_() == QDialog.Accepted:
                self._ranges[attribute_name] = {'min_values':self.dlgAttrRange.min_values,
                                                'max_values':self.dlgAttrRange.max_values}
                for min, max in map(None, self.dlgAttrRange.min_values, self.dlgAttrRange.max_values):                
                    print min, max
            else:
                return
        else:
            for code_name, code in self.taxonomy.codes.iteritems():                
                if code.attribute.name == attribute_name and code.level == 1:
                    self.valid_codes[code.description]=code_name                                    
        attr_editor = MSAttributeItemDelegate(self.ui.table_ms_level, self.valid_codes, len(self.node.children))
        self.ui.table_ms_level.setItemDelegateForColumn(0, attr_editor)

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
            for attr in self.taxonomy.attributes:
                if attr.name != attribute_name:
                    continue
                use_combobox = (attr.type == 1)
                break
            self.valid_codes = {}
            for code_name, code in self.taxonomy.codes.iteritems():                
                if code.attribute.name == attribute_name and code.level == 1:
                    self.valid_codes[code.description]=code_name
            if use_combobox and len(self.valid_codes) > 0:
                attr_editor = MSAttributeItemDelegate(self.ui.table_ms_level, self.valid_codes, 0)
                self.ui.table_ms_level.setItemDelegateForColumn(0, attr_editor)
            else:
                self.ui.table_ms_level.setItemDelegateForColumn(0, self.ui.table_ms_level.itemDelegateForColumn(1))
        else:
            existing_attributes = node.ancestor_names
            existing_attributes.append(node.name)
            for attr in self.taxonomy.attributes:
                try:
                    existing_attributes.index(attr.name)
                except:
                    self.ui.cb_attributes.addItem(attr.name)
            
        for _child in self.node.children:
            values.append(_child.value)
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
            QMessageBox.warning(self, 'Node Not Selected', 'Please select node first.')
            return None       
        if not selectedIndexes[0].isValid():
            QMessageBox.warning(self, 'Invalid Node', 'Select node does not support this function.')
            return None
        return selectedIndexes[0]    
