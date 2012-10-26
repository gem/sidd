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
dialog for editing mapping scheme brances
"""
from PyQt4.QtGui import *
from PyQt4.QtCore import *

from sidd.ms import *
from sidd.taxonomy import get_taxonomy

from ui.constants import logUICall, get_ui_string
from ui.dlg_save_ms import DialogSaveMS
from ui.qt.dlg_ms_branch_ui import Ui_editMSDialog
from ui.helper.ms_level_table import MSLevelTableModel

class DialogEditMS(Ui_editMSDialog, QDialog):
    """
    dialog for editing mapping scheme brances
    """
    # constructor
    ###############################
    
    def __init__(self, app):
        super(DialogEditMS, self).__init__()
        self.ui = Ui_editMSDialog()
        self.ui.setupUi(self)
        self.retranslateUi(self.ui)
        
        self.app =  app        
        self.ui.table_ms_level.setSelectionMode(QAbstractItemView.SingleSelection)

        # save mapping scheme dialog box        
        self.dlgSave = DialogSaveMS(self.app)
        self.dlgSave.setModal(True)

    # ui event handler
    ###############################

    @logUICall
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
    def addValue(self):
        """ 
        event hanlder for btn_add
        - add another pair of value/weights  
        """
        self.levelModel.addValues()
    
    @logUICall  
    def deleteValue(self):
        """ 
        event hanlder for btn_delete
        - delete currently selected row of value/weights from table table_ms_level  
        """        
        selected = self.getSelectedCell()
        if selected is not None:
            self.levelModel.deleteValue(selected)

    @logUICall
    def saveMSBranch(self):
        """ 
        event hanlder for btn_save
        - open "Save mapping scheme" dialogbox to save current set of values/weights
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

    # public methods    
    #############################
            
    @logUICall
    def setNode(self, node, addNew=False):
        """ 
        shows values/weights in table_ms_level for given node
        if addNew values/weights correspond to node's children (if any)
        otherwise, values/weights are from node's sibling (if any) 
        """        
        # create copy of values to be shown and modified
        values = []
        weights = []
        ref_node = node
        if not addNew:
            ref_node = node.parent
        for _sibling in ref_node.children:
            values.append(_sibling.value)
            weights.append(_sibling.weight)            
            
        self.levelModel = MSLevelTableModel(values, weights)
        self.ui.table_ms_level.setModel(self.levelModel)
        self.taxonomy = get_taxonomy('gem')

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
        self.setWindowTitle(get_ui_string("dlg.msbranch.edit.window.title"))
        ui.lb_title.setText(get_ui_string("dlg.msbranch.edit.title"))
        ui.btn_apply.setText(get_ui_string("app.dialog.button.apply"))
        ui.btn_close.setText(get_ui_string("app.dialog.button.close"))
    
