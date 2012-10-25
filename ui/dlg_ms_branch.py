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
# Version: $Id: dlg_ms_branch.py 18 2012-10-24 20:21:41Z zh $

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
    
    def __init__(self, app):
        super(DialogEditMS, self).__init__()
        self.ui = Ui_editMSDialog()
        self.ui.setupUi(self)
        self.retranslateUi(self.ui)
        
        self.app =  app
        self.levelUI = self.ui.table_ms_level
        self.levelUI.setSelectionMode(QAbstractItemView.SingleSelection)
        
        self.dlgSave = DialogSaveMS(self.app)
        
    @logUICall
    def setNode(self, node, addNew=False):
        """ from given node, all sibling are used in dialog """
        
        # create copy of values to be shown and modified
        values = []
        weights = []
        ref_node = node
        if not addNew:
            ref_node = node.parent
        for _sibling in ref_node.children:
            values.append(_sibling.value)
            weights.append(_sibling.weight)
            print 'weight',_sibling.weight, 'value', _sibling.value
            
        self.levelModel = MSLevelTableModel(values, weights)
        self.levelUI.setModel(self.levelModel)
        self.taxonomy = get_taxonomy('gem')

    @logUICall
    def updateWeights(self):
        """ update sibling with new set of weights. this action is irreversible """
        self.values = self.levelModel.values
        self.weights = self.levelModel.weights
        self.accept()
    
    @logUICall
    def addValue(self):
        """ add a sibling. this action is irreversible """
        self.levelModel.addValues()
    
    @logUICall  
    def deleteValue(self):
        """ delete a sibling. this action is irreversible """
        self.levelModel.deleteValue(self.getSelectedCell())

    def saveMSBranch(self):
        
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
        self.dlgSave.setModal(True)
        self.dlgSave.exec_()

    # internal helper methods
    ###############################

    def getSelectedCell(self):
        selectedIndexes = self.levelUI.selectedIndexes()
        if (len(selectedIndexes) <= 0):
            QMessageBox.warning(self, 'Node Not Selected', 'Please select node first.')
        if not selectedIndexes[0].isValid():
            QMessageBox.warning(self, 'Invalid Node', 'Select node does not support this function.')
        return selectedIndexes[0]
    
    def retranslateUi(self, ui):
        self.setWindowTitle(get_ui_string("dlg.msbranch.edit.window.title"))
        ui.lb_title.setText(get_ui_string("dlg.msbranch.edit.title"))
        ui.btn_apply.setText(get_ui_string("app.dialog.button.apply"))
        ui.btn_close.setText(get_ui_string("app.dialog.button.close"))
    
