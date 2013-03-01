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
# Version: $Id: dlg_ms_branch.py 21 2012-10-26 01:48:25Z zh $

"""
dialog for editing mapping scheme branches
"""
from PyQt4.QtGui import QDialog, QMessageBox, QAbstractItemView
from PyQt4.QtCore import Qt, pyqtSlot, QObject

from sidd.ms import MappingScheme, MappingSchemeZone, Statistics, StatisticNode 

from ui.constants import logUICall, get_ui_string
from ui.dlg_save_ms import DialogSaveMS
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
        self.retranslateUi(self.ui)
        
        self.app =  app
        self.taxonomy = app.taxonomy

        # save mapping scheme dialog box        
        self.dlgSave = DialogSaveMS(self.app)
        self.dlgSave.setModal(True)
        
        # connect slots (ui events)
        self.ui.btn_apply.clicked.connect(self.updateWeights)
        self.ui.btn_add.clicked.connect(self.addValue)
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
        self.valid_codes = []
        attribute_name = new_attribute
        for code in self.taxonomy.codes.itervalues():
            if code.attribute.name == attribute_name and code.level == 1:
                self.valid_codes.append(code)
                
        attr_editor = MSAttributeItemDelegate(self.ui.table_ms_level, self.valid_codes, len(self.node.children))
        self.ui.table_ms_level.setItemDelegateForColumn(0, attr_editor)

    # public methods    
    #############################            
    @logUICall
    def setNode(self, node, addNew=False):
        """ 
        shows values/weights in table_ms_level for given node
        if addNew values/weights correspond to node's children (if any)
        otherwise, values/weights are from node's sibling (if any) 
        """        
        self.ui.cb_attributes.clear()
        
        # create copy of values to be shown and modified
        values = []
        weights = []
        
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
            self.valid_codes = []
            for code in self.taxonomy.codes.itervalues():                
                if code.attribute.name == attribute_name and code.level == 1:
                    self.valid_codes.append(code)
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
            
        self.levelModel = MSLevelTableModel(values, weights, self.taxonomy, self.taxonomy.codes)
        
        # initialize table view 
        tableUI = self.ui.table_ms_level                
        tableUI.setModel(self.levelModel)
        tableUI.setSelectionMode(QAbstractItemView.SingleSelection)
        table_width = tableUI.width()
        value_col_width = round(table_width*0.6, 0)
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
    
    def retranslateUi(self, ui):
        """ set text for ui elements """
        # dialog title
        self.setWindowTitle(get_ui_string("dlg.msbranch.edit.window.title"))
        # ui elements
        ui.lb_title.setText(get_ui_string("dlg.msbranch.edit.title"))
        ui.lb_attribute.setText(get_ui_string("dlg.msbranch.edit.attribute.name"))
        ui.lb_total_weights.setText(get_ui_string("dlg.msbranch.edit.weight.total"))
        ui.lb_percent.setText("%")
        ui.btn_apply.setText(get_ui_string("app.dialog.button.apply"))
        ui.btn_close.setText(get_ui_string("app.dialog.button.close"))    
        # tooltip
        ui.btn_add.setToolTip(get_ui_string("dlg.msbranch.button.add"))
        ui.btn_delete.setToolTip(get_ui_string("dlg.msbranch.button.delete"))
        ui.btn_save.setToolTip(get_ui_string("dlg.msbranch.button.save"))

