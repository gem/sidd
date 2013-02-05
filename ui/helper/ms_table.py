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
# Version: $Id: ms_table.py 18 2012-10-24 20:21:41Z zh $

"""
table model for visualizing secondary modifiers from mapping scheme
"""

from PyQt4.QtCore import Qt, QVariant, QString, \
                         QAbstractTableModel, QModelIndex

from sidd.constants import logAPICall

from ui.constants import get_ui_string
from ui.helper.common import build_attribute_tooltip, build_multivalue_attribute_tooltip

class MSTableModel(QAbstractTableModel):
    """
    table model for visualizing secondary modifiers from mapping scheme
    """

    def __init__(self, ms):
        """ constructor """
        super(MSTableModel, self).__init__(None)

        self.ms = ms
        self.valid_codes = self.ms.taxonomy.codes
        self.headers = [
            get_ui_string("widget.mod.tableheader.zone"),
            get_ui_string("widget.mod.tableheader.level1"),
            get_ui_string("widget.mod.tableheader.level2"),
            get_ui_string("widget.mod.tableheader.level3"),
            get_ui_string("widget.mod.tableheader.value"),
            get_ui_string("widget.mod.tableheader.weight"),]
        
        self.modifiers = []
        self.row_count = 0
        for  _zone, _stat in self.ms.assignments():
            for _node, _idx, _modifier in _stat.get_modifiers(4):
                _start_count = self.row_count                
                self.row_count += len(_modifier.keys())
                _end_count = self.row_count
                _parents = ['', '', '']
                _parent = _node
                for i in range(_node.level):
                    _parent_idx = _node.level-1-i
                    if (_parent_idx >= 0 and _parent_idx < 3):
                        _parents[_node.level-1-i]=_parent.value
                        _parent = _parent.parent
                self.modifiers.append((_zone.name, _parents[0], _parents[1], _parents[2],
                                         _start_count, _end_count,
                                         _idx, _modifier, _node))

    def columnCount(self, parent):
        return 6

    def rowCount(self, parent):
        return self.row_count

    def index(self, row, column, parent):
        logAPICall.log('index row %s col %s parent %s' % (row, column, parent), logAPICall.DEBUG_L2)
        _mod = self._get_modifier(row)
        if _mod is not None:
            return self.createIndex(row, column, _mod)
        else:
            return QModelIndex()

    def data(self, index, role):
        col, row = index.column(), index.row()
        logAPICall.log('data col %s row %s' % (row, col), logAPICall.DEBUG_L2)
        
        if role == Qt.DisplayRole:
            # construct data for display in table
            _mod = self._get_modifier(row)
            _idx = row - _mod[4]                    
            if (col < 4):
                # for first 4 columns, only first row in new modifier
                # need to show the headings
                if (_idx == 0):
                    return QVariant(_mod[col])
                else:
                    return QVariant()
            else:
                # for last 2 columns, show modifier value and associated percentage
                for _key in sorted(_mod[7].keys()):
                    if (_idx == 0):
                        if (col == 4):
                            return QVariant(_key)
                        else:
                            return QVariant(_mod[7].value(_key))
                    else:
                        _idx -=1
        elif role == Qt.ToolTipRole:
            # construct data for display in tooltip
            _mod = self._get_modifier(row)
            _idx = row - _mod[4]
            if (col == 0):
                return ""
            elif (col < 4):
                if (_idx == 0):
                    return build_attribute_tooltip(self.valid_codes, _mod[col])
            elif (col==4):
                _key = sorted(_mod[7].keys())[_idx]
                if _key is not None:
                    return build_multivalue_attribute_tooltip(self.valid_codes, self.ms.taxonomy.parse(_key))
        else:
            return QVariant()

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:                
                return QString(self.headers[section])
            else:
                return QVariant()
        elif role == Qt.ToolTipRole:
            return QString('tool tip for %s' % self.headers[section])
        else:
            return QVariant()
            
    def _get_modifier(self, row):
        for _mod in self.modifiers:                
            if (_mod[4]<= row and _mod[5] > row):
                return _mod
        return None
        