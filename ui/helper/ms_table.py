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
table model for visualizing secondary modifiers from mapping scheme
"""

from PyQt4.QtCore import Qt, QVariant, QString, \
                         QAbstractTableModel, QModelIndex

from sidd.constants import logAPICall

from ui.constants import get_ui_string
from ui.helper.common import build_attribute_tooltip

class MSTableModel(QAbstractTableModel):
    """
    table model for visualizing secondary modifiers from mapping scheme
    """
    STR_INDEX=2
    END_INDEX=3
    MOD_INDEX=5
    #MOD_INDEX=7

    def __init__(self, ms):
        """ constructor """
        super(MSTableModel, self).__init__(None)

        self.ms = ms
        self.valid_codes = self.ms.taxonomy.codes
        self.headers = [
            get_ui_string("widget.mod.tableheader.zone"),
            get_ui_string("widget.mod.tableheader.path"),
            get_ui_string("widget.mod.tableheader.value"),
            get_ui_string("widget.mod.tableheader.weight"),]
        self.modifiers = []
        self.row_count = 0        # total row count
        
        for zone, stat in self.ms.assignments():
            # get all modifier in the tree
            for node, idx, modifier in stat.get_modifiers(10):
                # each modifier has several values that will be listed in
                # different rows in the table
                # start_count / end_count are start/end row index for the table
                start_count = self.row_count
                self.row_count += len(modifier.keys())
                end_count = self.row_count
                # build the string containing path to the node 
                parent = node
                parent_str = []
                for i in range(node.level):                    
                    parent_str.append(str(parent.value))
                    # move up to next parent
                    parent = parent.parent
                # reverse to put root at the beginning
                parent_str.reverse()
                self.modifiers.append((zone.name, "/".join(parent_str),
                                       start_count, end_count,
                                       idx, modifier, node))

    def columnCount(self, parent):
        """ number of columns for the table """
        return 4    

    def rowCount(self, parent):
        """ number of rows for the table """
        return self.row_count

    def index(self, row, column, parent):
        """ provide index to data given a cell """
        logAPICall.log('index row %s col %s parent %s' % (row, column, parent), logAPICall.DEBUG_L2)
        mod = self.get_modifier(row)
        if mod is not None:
            return self.createIndex(row, column, mod)
        else:
            return QModelIndex()

    def data(self, index, role):
        """ data for cells """
        col, row = index.column(), index.row()
        logAPICall.log('data col %s row %s' % (row, col), logAPICall.DEBUG_L2)
        
        if role == Qt.DisplayRole:
            # construct data for display in table
            _mod = self.get_modifier(row)
            _idx = row - _mod[self.STR_INDEX]
            if (col < self.STR_INDEX):
                # for first 4 columns, only first row in new modifier
                # need to show the headings
                if (_idx == 0):
                    return QVariant(_mod[col])
                else:
                    return QVariant()
            else:
                # for last 2 columns, show modifier value and associated percentage
                for _key in sorted(_mod[self.MOD_INDEX].keys()):
                    if (_idx == 0):
                        if (col == self.STR_INDEX):
                            return QVariant(_key)
                        else:
                            return QVariant("%.2f" %_mod[self.MOD_INDEX].value(_key))
                    else:
                        _idx -=1
        elif role == Qt.ToolTipRole:
            # construct data for display in tooltip
            _mod = self.get_modifier(row)
            _idx = row - _mod[self.STR_INDEX]
            if col==1:
                if (_idx == 0):                    
                    return build_attribute_tooltip(self.valid_codes, self.ms.taxonomy.parse(_mod[col]))
                else:
                    return QVariant()
            elif col==2:
                _key = sorted(_mod[self.MOD_INDEX].keys())[_idx]
                if _key is not None:
                    return build_attribute_tooltip(self.valid_codes, self.ms.taxonomy.parse(_key))
            else:
                return QVariant("")
        else:
            return QVariant()

    def headerData(self, section, orientation, role):
        """ data for header row """
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:                
                return QString(self.headers[section])
            else:
                return QVariant()
        else:
            return QVariant()

    # internal helper methods
    ###############################             
    def get_modifier(self, row):
        for mod in self.modifiers:                
            if (mod[self.STR_INDEX]<= row and mod[self.END_INDEX] > row):
                return mod
        return None
        