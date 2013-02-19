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
from PyQt4.QtGui import QDialog, QTableWidgetItem, QMessageBox
from PyQt4.QtCore import pyqtSlot, Qt, QAbstractTableModel, QString, QVariant, QObject

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
        return self.__values[0]
    
    @property
    def max_values(self):
        return self.__values[1]
        
    @pyqtSlot()
    def add_range(self):
        self.ui.table_ranges.insertRow(self.ui.table_ranges.rowCount())
        self.__values[0].append(None)
        self.__values[1].append(None)
    
    @pyqtSlot()
    def remove_range(self):        
        self.ui.table_ranges.removeRow(self.ui.table_ranges.rowCount()-1)
        self.__values[0].pop()
        self.__values[1].pop()
    
    @pyqtSlot(QObject)
    def verifyData(self, item):
        item_val = item.data(Qt.DisplayRole)
        if item_val == QVariant('None'):
            return         
        int_val = item_val.toInt()
        row, col = item.row(), item.column()
        # TODO: check again min/max value
        if int_val[1]:
            # is integer
            # set value
            self.__values[col][row] = int_val[0]
        else:
            # not integer
            # restore
            QMessageBox.warning(self, "Error", get_ui_string('dlg.attr.value.error'))
            self.ui.table_ranges.setItem(row, col, QTableWidgetItem('%s'%self.__values[col][row]))
    
    def set_values(self, attribute, min_values, max_values):
        self.ui.lb_attribute.setText(attribute)
        self.__values = [min_values, max_values]        
        table = self.ui.table_ranges 
        table.clearContents()
        table.setRowCount(0)             
        for i, min_val, max_val in map(None, range(len(min_values)), min_values, max_values):
            table.insertRow(i)
            table.setItem(i, 0, QTableWidgetItem('%s'%min_val))
            table.setItem(i, 1, QTableWidgetItem('%s'%max_val))        
    
    def retranslateUi(self, ui):
        self.setWindowTitle(get_ui_string('dlg.attr.range.window.title'))
        ui.lb_title.setText(get_ui_string('dlg.attr.title'))
        ui.table_ranges.setHorizontalHeaderLabels([get_ui_string('dlg.attr.min_value'), get_ui_string('dlg.attr.max_value')])

