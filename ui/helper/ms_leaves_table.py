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
from PyQt4.QtCore import Qt, QVariant, QString, QAbstractTableModel, QModelIndex
from ui.helper.common import build_attribute_tooltip

class MSLeavesTableModel(QAbstractTableModel):
    """
    table model supporting visualization of node in mapping scheme tree
    """
    def __init__(self, values, headers, formats, parser, valid_codes):
        """ constructor """
        super(MSLeavesTableModel, self).__init__()

        self.headers = headers
        self.formats= formats
        self.parser=parser
        self.valid_codes=valid_codes
        self.values = values
        self.do_sort(sortIndex=0)                
    
    def columnCount(self, parent):
        """ only three columns exist. always return 3 """
        return len(self.headers)

    def rowCount(self, parent):
        """ number of rows same as number of siblings """
        return len(self.values)            

    def headerData(self, section, orientation, role):
        """ return data to diaply for header row """        
        if role == Qt.DisplayRole:   
            if orientation == Qt.Horizontal:
                return QString(self.headers[section][0])
            else:
                # no vertical header
                return QVariant()
        elif role == Qt.ToolTipRole:            
            return QString(self.headers[section][1])
        else:            
            return QVariant()
    
    def data(self, index, role):
        """ return data to be displayed in a cell """
        row, col = index.row(), index.column()                
        value = self.values[row][col]        
        if role == Qt.DisplayRole:
            if value is not None:
                return QString(self.formats[col] % value)
            else:
                return QVariant("")
        elif role == Qt.ToolTipRole:
            # construct data for display in tooltip            
            if (index.column() == 0):                            
                if value is not None:
                    return build_attribute_tooltip(self.valid_codes, self.parser.parse(value))
            else:
                return QVariant("")
        elif role == Qt.UserRole:            
            return index.internalPointer()
        else:
            return QVariant()
    
    def index(self, row, column, parent):
        """ provide index to data given a cell """
        try:
            node = self.values[row][len(self.headers)]
            return self.createIndex(row, column, node)
        except:
            return QModelIndex()        
    
    def flags(self, index):
        """ cell condition flag """
        # NOTE: 
        #   ItemIsEditable also required data() and setData() function
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def sort(self, ncol, order):
        """ sort table """
        if ncol < 0 or ncol > len(self.headers):
            return
        self.layoutAboutToBeChanged.emit()            
        self.do_sort(sortIndex=ncol, reverse_sort=order==Qt.DescendingOrder)
        self.layoutChanged.emit()

    # internal helper methods
    ############################### 
    def do_sort(self, sortIndex = 0, reverse_sort=False):
        def sort_key(row):
            return row[sortIndex]        
        self.values.sort(key=sort_key, reverse=reverse_sort)
    