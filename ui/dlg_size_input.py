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
from PyQt4.QtGui import QCloseEvent, QDialog, QAbstractItemView, QItemSelectionModel, QDoubleValidator 
from PyQt4.QtCore import pyqtSlot, QSettings, Qt, QObject, QSize

from sidd.ms import StatisticNode, MappingSchemeZone
from sidd.constants import SIDD_COMPANY, SIDD_APP_NAME, SIDD_VERSION

from ui.constants import logUICall, UI_PADDING 
from ui.qt.dlg_size_input_ui import Ui_sizeInputDialog
from ui.helper.ms_tree import MSTreeModel

class DialogSizeInput(Ui_sizeInputDialog, QDialog):
    """
    dialog for editing mapping scheme branches
    """

    # CONSTANTS
    #############################    
    UI_WINDOW_GEOM = 'dlg_size_input/geometry'
        
    # constructor
    ###############################    
    def __init__(self, app):
        super(DialogSizeInput, self).__init__()
        self.ui = Ui_sizeInputDialog()
        self.ui.setupUi(self)
        
        self.settings = QSettings(SIDD_COMPANY, '%s %s' %(SIDD_APP_NAME, SIDD_VERSION));
        self.restoreGeometry(self.settings.value(self.UI_WINDOW_GEOM).toByteArray());
                
        self.app = app
        self.ms = None
        
        max_size = self.app.app_config.get('options', 'max_size', 1e+15, float)
        max_rep_cost = self.app.app_config.get('options', 'max_rep_cost', 1e+15, float)
        
        # connect slots (ui events)
        self.ui.btn_apply.clicked.connect(self.setAvgSize)
        self.ui.btn_cancel.clicked.connect(self.reject)
        self.ui.txt_rep_cost.setValidator(QDoubleValidator(0, max_size,  2, self))
        self.ui.txt_size.setValidator(QDoubleValidator(0, max_rep_cost, 2, self))
    
    @property
    def unit_cost(self):
        try:
            return float(self.ui.txt_rep_cost.text())
        except:
            return 0
    
    @property
    def avg_size(self):
        try:
            return float(self.ui.txt_size.text())
        except:
            return 0        
    
    # ui event handler
    ###############################
    @pyqtSlot(QObject)
    def resizeEvent(self, event):
        """ handle window resize """ 
        ui = self.ui
        if self.width() < 500 or self.height() < 400:
            self.resize(500, 400)
        w= self.width()-3*UI_PADDING        
        # set left panel for mapping scheme tree 
        ui.tree_ms.resize(QSize(w*0.5, self.height()-ui.tree_ms.y()-UI_PADDING))        

        r = ui.tree_ms.x()+ui.tree_ms.width()+UI_PADDING
        
        ui.lb_bldg_type.move(r, ui.lb_bldg_type.y())
        ui.txt_bldg_type.setGeometry(r, ui.txt_bldg_type.y(), w*0.5, ui.txt_bldg_type.height())
        ui.lb_size.move(r, ui.lb_size.y())
        ui.txt_size.setGeometry(r, ui.txt_size.y(), w*0.5, ui.txt_size.height())
        ui.lb_rep_cost.move(r, ui.lb_rep_cost.y())
        ui.txt_rep_cost.setGeometry(r, ui.txt_rep_cost.y(), w*0.5, ui.txt_rep_cost.height())
        
        # set up bottom right for dialog buttons
        ui.btn_cancel.move(self.width()-ui.btn_cancel.width()-UI_PADDING, 
                           self.height()-ui.btn_cancel.height()-UI_PADDING)
        ui.btn_apply.move(ui.btn_cancel.x()-ui.btn_apply.width()-UI_PADDING,
                          ui.btn_cancel.y())

    @pyqtSlot(QCloseEvent)
    def closeEvent(self, event):
        self.settings.setValue(self.UI_WINDOW_GEOM, self.saveGeometry());
        super(DialogSizeInput, self).closeEvent(event)
        
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
            parent = node
            parent_str = []
            for i in range(node.level):
                parent_str.append(parent.value)
                # move up to next parent
                parent = parent.parent
            # reverse to put root at the beginning
            parent_str.reverse()                
            self.ui.txt_bldg_type.setText(self.ms.taxonomy.to_string(parent_str))
        elif isinstance(node, MappingSchemeZone):
            self.node = node.stats.root
            self.ui.txt_bldg_type.setText(node.name)
        else:
            self.node = None
            self.ui.txt_bldg_type.setText("")
        
        if self.node is not None and self.node.is_leaf:
            self.ui.txt_rep_cost.setText("%.2f" % self.node.get_additional_float(StatisticNode.UnitCost))
            self.ui.txt_size.setText("%.2f" % self.node.get_additional_float(StatisticNode.AverageSize))  
        else:
            self.ui.txt_rep_cost.setText("")
            self.ui.txt_size.setText("")

    def setAvgSize(self):
        self.accept()

    # public method
    ###############################
        
    @logUICall
    def setNode(self, node, ms):
        """ 
        shows values/weights in table_mod_values for given node
        if addNew values/weights are two empty lists 
        otherwise, values/weights are from take from given mod  
        """ 
        self.ms = ms
        self.node = node
        
        # construct mapping scheme tree
        self.tree_model = MSTreeModel(self.ms)        
        self.ui.tree_ms.setModel(self.tree_model)
        self.ui.tree_ms.setEnabled(True)
                    
        indices = self.tree_model.match(self.ui.tree_ms.rootIndex(), Qt.UserRole, self.node, 1)
        if len(indices) < 1:
            return 
        
        index = indices[0]
        while index <> self.ui.tree_ms.rootIndex():
            self.ui.tree_ms.setExpanded(index, True)
            index = self.tree_model.parent(index)
            
        # set node as selected
        self.ui.tree_ms.selectionModel().select(indices[0], QItemSelectionModel.ClearAndSelect | QItemSelectionModel.Rows)
        # expand tree from root to node 
        self.ui.tree_ms.setSelectionMode(QAbstractItemView.SingleSelection)
        # no modfier given
        # create event handler for selected node
        self.ui.tree_ms.selectionModel().selectionChanged.connect(self.nodeSelected)
        
        self.nodeSelected()
