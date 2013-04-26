# Copyright (c) 2011-2013, ImageCat Inc.
#
# SIDD is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
#
"""
dialog for editing secondary modifiers
"""
from PyQt4.QtGui import QDialog, QTableWidgetItem, QMessageBox, QDialogButtonBox
from PyQt4.QtCore import pyqtSlot, Qt, QVariant, QObject

from ui.constants import logUICall, get_ui_string 
from ui.qt.dlg_attr_range_ui import Ui_attrRangesDialog
from ui.exception import SIDDRangeGroupException

class DialogAttrRanges(Ui_attrRangesDialog, QDialog):
    """
    dialog specifying options for creating mapping scheme
    """
    BUILD_EMPTY, BUILD_FROM_SURVEY=range(2)
    
    def __init__(self, attribute='', min_values=[], max_values=[]):
        """ constructor """
        super(DialogAttrRanges, self).__init__()
        self.ui = Ui_attrRangesDialog()
        self.ui.setupUi(self)
        self.setFixedSize(self.size())
        
        # additional table UI adjustment
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
        """ 
        callback at each table value update. two checks
        - value is integer
        - range is valid with new value
        """
        item_val = item.data(Qt.DisplayRole)
        if item_val == QVariant('None'):
            return
        int_val = item_val.toInt()
        row, col = item.row(), item.column()        
        if int_val[1]:  # is integer            
            # set value
            self._values[col][row] = int_val[0]
            
            # allow set range only if is valid 
            range_is_valid = False
            try:
                range_is_valid = self.is_range_valid()
            except SIDDRangeGroupException as err:
                # error means not valid 
                self.ui.lb_notes.setText(err.message)
            except Exception as err:
                # error means not valid
                self.ui.lb_notes.setText(err.message)
            self.ui.buttons.button(QDialogButtonBox.Ok).setEnabled(range_is_valid)
        else:
            # not integer
            # restore
            QMessageBox.warning(self, "Error", get_ui_string('dlg.attr.value.error'))
            self.ui.table_ranges.setItem(row, col, QTableWidgetItem('%s'%self._values[col][row]))

    # public method
    ###############################
    def set_values(self, attribute, min_values, max_values):
        """ set data for the table """
        self.ui.lb_attribute.setText(attribute)
        self._values = [min_values, max_values]        
        table = self.ui.table_ranges 
        table.clearContents()
        table.setRowCount(0)             
        for i, min_val, max_val in map(None, range(len(min_values)), min_values, max_values):
            table.insertRow(i)
            table.setItem(i, 0, QTableWidgetItem('%s'%min_val))
            table.setItem(i, 1, QTableWidgetItem('%s'%max_val))        

    # internal helper methods
    ###############################
    
    def is_range_valid(self):
        is_valid = True
        self.ui.lb_notes.setText("")
        for i in range(len(self._values[0])):
            # minimum must be less than maximum in same row
            max_val = self._values[1][i]
            min_val = self._values[0][i]                         
            is_valid = (min_val <= max_val)
            if not is_valid:
                # use exception to stop additional checks 
                raise SIDDRangeGroupException(get_ui_string("dlg.attr.error.max", (max_val, min_val)))
            # and minimum must be exactly 1 larger than maximum from previous row  
            if i > 0:   # first row does not have previous
                max_last = self._values[1][i-1]
                is_valid = (min_val == max_last+1)
                if not is_valid:
                    # use exception to stop additional checks
                    raise SIDDRangeGroupException(get_ui_string("dlg.attr.error.range", (max_last, min_val)))
        return is_valid                
