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
from PyQt4.QtCore import Qt, QVariant, QString, QAbstractTableModel
from ui.constants import logUICall, get_ui_string
from ui.helper.common import build_attribute_tooltip
from sidd.exception import SIDDException

class MSLevelTableModel(QAbstractTableModel):
    """
    table model supporting visualization of node in mapping scheme tree
    """
    def __init__(self, values, weights, parser, valid_codes, is_editable=[True, True]):
        """ constructor """
        super(MSLevelTableModel, self).__init__()

        # table header 
        self.headers = [
            get_ui_string('dlg.msbranch.edit.tableheader.value'),
            get_ui_string('dlg.msbranch.edit.tableheader.weight'),
            'Value', 'Weight (%)'
        ]        
        self.parser=parser
        self.valid_codes=valid_codes
        self.values, self.weights = self._sort(values, weights)
        self.is_editable = is_editable
        self.editable_indices = {}
    
    def columnCount(self, parent):
        """ only two columns exist. always return 2 """
        return 2

    def rowCount(self, parent):
        """ number of rows same as number of siblings """
        return len(self.weights)

    def addValues(self):
        """ add new row to table"""
        self.values.append('')
        self.weights.append(0)
        # required call to refresh view
        self.reset()
    
    def deleteValue(self, row):
        """ remove selected row """
        if row < 0 or row > len(self.values):
            return
        self.weights.remove(self.weights[row])
        self.values.remove(self.values[row])
        self.dataChanged.emit(self.index(row, 0), self.index(row,1))

    def headerData(self, section, orientation, role):
        """ return data to diaply for header row """        
        if role == Qt.DisplayRole:   
            if orientation == Qt.Horizontal:
                return QString(self.headers[section])
            else:
                # no vertical header
                return QVariant()
        elif role == Qt.ToolTipRole:            
            return QString('tool tip for %s' % self.headers[section])
        else:            
            return QVariant()
    
    def data(self, index, role):
        """ return data to be displayed in a cell """
        if role == Qt.DisplayRole:
            logUICall.log('retrieving data %s %s' % (index.column(), index.row()),
                             logUICall.DEBUG_L2)
            if (index.column() == 0):
                # first column, show value
                value = self.values[index.row()]
                if value is not None:
                    return QString(value)
                else:
                    return ""
            else:
                # second column, show weight
                return QString('%.2f'% self.weights[index.row()])
        elif role == Qt.ToolTipRole:
            # construct data for display in tooltip            
            if (index.column() == 0):
                value = self.values[index.row()]            
                if value is not None:
                    return build_attribute_tooltip(self.valid_codes, self.parser.parse(value))
            else:
                return QVariant("")            
        
        else:
            return QVariant()
    
    def setData(self, index, value, role):
        """ set data modified by cell edit """
        if role == Qt.EditRole:
            if (index.column() == 0):
                # first column, change value
                taxStr = str(value.toString())                
                # make sure there is no repeat
                try:                    
                    self.values.index(taxStr)
                    # no error means taxStr already in self.value
                    found = True                    
                except:
                    found = False
                if found:
                    raise SIDDException(get_ui_string("dlg.msbranch.error.attribute.exists") % taxStr)
                # do nothing for empty string
                if taxStr == "":
                    return False           
                # verify taxonomy
                                
                # passed all checks. set value
                self.values[index.row()] = taxStr
            else:
                # second column, change weight
                (dVal, sucess) = value.toDouble()
                # conversion to double failed
                if not sucess:
                    raise SIDDException(get_ui_string("dlg.msbranch.edit.warning.invalidweight"))
                # make sure 0 <= dVal <= 100
                if dVal < 0 or dVal > 100:
                    raise SIDDException(get_ui_string("dlg.msbranch.edit.warning.invalidweight"))
                                    
                # passed all checks. set value
                self.weights[index.row()] = round(dVal, 1)

            self.dataChanged.emit(self.createIndex(0, 0), self.createIndex(self.rowCount(0),self.columnCount(0)))
            return True
        return False
        
    def flags(self, index):
        """ cell condition flag """
        # NOTE: 
        #   ItemIsEditable also required data() and setData() function
        combined_flag = Qt.ItemIsEnabled | Qt.ItemIsSelectable  
        if index.column() < 0 and index.column() > len(self.is_editable):
            return combined_flag
        if self.is_editable[index.column()] or self.editable_indices.has_key((index.column(), index.row())):
            combined_flag = combined_flag | Qt.ItemIsEditable
        return combined_flag 

    def set_cell_editable(self, column, row, editable=True):
        key = (column, row)
        if editable:
            self.editable_indices[key] = editable
        else:
            if self.editable_indices.has_key(key):
                self.editable_indices.pop(key) 

    def sort(self, ncol, order):
        """ sort table """
        if ncol < 0 or ncol > len(self.headers):
            return
        self.layoutAboutToBeChanged.emit()
        
        if ncol == 0:
            self.values, self.weights = self.do_sort(self.values, self.weights, reverse_sort=order==Qt.DescendingOrder)
        else:
            self.weights, self.values = self.do_sort(self.weights, self.values, reverse_sort=order==Qt.DescendingOrder)            
                        
        self.layoutChanged.emit()

    # internal helper methods
    ############################### 
    def do_sort(self, col1, col2, reverse_sort=False):
        dist = []
        for v, w in map(None, col1, col2):
            dist.append({v:w})
        dist.sort(reverse=reverse_sort)
        sorted_col1, sorted_col2 = [], []
        for val in dist:            
            sorted_col1.append(val.items()[0][0])
            sorted_col2.append(val.items()[0][1])
        return sorted_col1, sorted_col2
    
