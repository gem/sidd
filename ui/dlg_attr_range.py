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
from PyQt4.QtGui import QDialog, QTableWidgetItem, QMessageBox, QDialogButtonBox
from PyQt4.QtCore import pyqtSlot, Qt, QVariant, QObject

from ui.constants import logUICall, get_ui_string 
from ui.qt.dlg_attr_range_ui import Ui_attrRangesDialog

class DialogAttrRanges(Ui_attrRangesDialog, QDialog):
    """
    dialog specifying options for creating mapping scheme
    """
    BUILD_EMPTY, BUILD_FROM_SURVEY=range(2)
    
    def __init__(self, app, attribute='', min_values=[], max_values=[]):
        """ constructor """
        super(DialogAttrRanges, self).__init__()
        self.ui = Ui_attrRangesDialog()
        self.ui.setupUi(self)
        self.retranslateUi(self.ui)
        self.setFixedSize(self.size())
        
        self.app = app
        self.ui.table_ranges.verticalHeader().hide()
        self.ui.table_ranges.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.ui.table_ranges.horizontalHeader().resizeSection(0, self.ui.table_ranges.width() * 0.5)
        self.ui.table_ranges.horizontalHeader().resizeSection(1, self.ui.table_ranges.width() * 0.5)  
        self.ui.table_ranges.itemChanged.connect(self.verifyData)
        
        self.set_values(attribute, min_values, max_values)
        
        # connect slot (ui event)
        self.ui.buttons.accepted.connect(self.accept)
        self.ui.buttons.rejected.connect(self.reject)
        
        self.ui.btn_add.clicked.connect(self.add_range)
        self.ui.btn_delete.clicked.connect(self.remove_range)
    
    @property
    def min_values(self):
        return self._values[0]
    
    @property
    def max_values(self):
        return self._values[1]
        
    @logUICall
    @pyqtSlot()
    def add_range(self):
        self.ui.table_ranges.insertRow(self.ui.table_ranges.rowCount())
        self._values[0].append(None)
        self._values[1].append(None)
    
    @logUICall
    @pyqtSlot()
    def remove_range(self):        
        self.ui.table_ranges.removeRow(self.ui.table_ranges.rowCount()-1)
        self._values[0].pop()
        self._values[1].pop()
    
    @logUICall
    @pyqtSlot(QObject)
    def verifyData(self, item):
        item_val = item.data(Qt.DisplayRole)
        if item_val == QVariant('None'):
            return         
        int_val = item_val.toInt()
        row, col = item.row(), item.column()        
        if int_val[1]:
            # is integer
            # set value
            self._values[col][row] = int_val[0]
            
            # allow set range only if is valid 
            self.ui.buttons.button(QDialogButtonBox.Ok).setEnabled(self.is_range_valid())
        else:
            # not integer
            # restore
            QMessageBox.warning(self, "Error", get_ui_string('dlg.attr.value.error'))
            self.ui.table_ranges.setItem(row, col, QTableWidgetItem('%s'%self._values[col][row]))
    
    def set_values(self, attribute, min_values, max_values):
        self.ui.lb_attribute.setText(attribute)
        self._values = [min_values, max_values]        
        table = self.ui.table_ranges 
        table.clearContents()
        table.setRowCount(0)             
        for i, min_val, max_val in map(None, range(len(min_values)), min_values, max_values):
            table.insertRow(i)
            table.setItem(i, 0, QTableWidgetItem('%s'%min_val))
            table.setItem(i, 1, QTableWidgetItem('%s'%max_val))        
    
    def is_value_valid(self, col, row, value):
        is_valid = True
        # check again min/max value to make sure range is set correctly            
        if col==0:  # input is min value
            # must be less equal than max of its own row
            is_valid = value <= self._values[1][row]                    
            # and must be exactly 1 + max of previous row (if exists)
            if (row>0):                 
                is_valid &= (value == self._values[1][row-1]+1)                
        else:       # input is min value
            # must be larger equal than min of its own row
            is_valid = value >= self._values[0][row]
            # and must be min of next row -1 (if exists)
            if (row<len(self._values[0])-1):
                is_valid &= (value == self._values[0][row+1]-1)
        return is_valid
    
    def is_range_valid(self):        
        is_valid = True
        for i in range(len(self._values[0])):
            # min must be less than max
            is_valid = self._values[0][i] <= self._values[1][i]
            # and min must be exactly 1 + previous max (if not first row)
            if (i>0):
                is_valid &= self._values[0][i] == self._values[1][i-1]+1
        return is_valid                
    
    def retranslateUi(self, ui):
        self.setWindowTitle(get_ui_string('dlg.attr.range.window.title'))
        ui.lb_title.setText(get_ui_string('dlg.attr.title'))
        ui.table_ranges.setHorizontalHeaderLabels([get_ui_string('dlg.attr.min_value'), get_ui_string('dlg.attr.max_value')])

