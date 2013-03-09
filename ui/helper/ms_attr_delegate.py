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
# Version: $Id: ms_level_table.py 18 2012-10-24 20:21:41Z zh $

"""
dialog for editing mapping scheme branches
"""
from PyQt4.QtCore import Qt, QVariant
from PyQt4.QtGui import QItemDelegate, QComboBox

class MSAttributeItemDelegate(QItemDelegate):
    def __init__(self, parent, valid_codes, min_editables):
        super(MSAttributeItemDelegate, self).__init__(parent)
        self.valid_codes = valid_codes
        self.valid_code_names = []    
        for description, code in valid_codes.iteritems():
            self.valid_code_names.append(description)
        self.valid_code_names.sort()
        self.min_editables = min_editables
    
    # returns the widget used to change data from the model and can be re-implemented to customize editing behavior.
    def createEditor(self, parent, option, index):
        if index.row() >= self.min_editables:
            editor = QComboBox(parent)
            return editor
        else:
            return None
    
    # provides the widget with data to manipulate
    def setEditorData(self, editor, index):
        current_val = str(index.data(Qt.DisplayRole).toString())
        editor.clear()
        for idx, name in enumerate(self.valid_code_names):
            editor.addItem(name)            
            # set current value as selected from the drop-down
            if self.valid_codes[name] == current_val:
                editor.setCurrentIndex(idx)
 
    # ensures that the editor is displayed correctly with respect to the item view.
    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect);
        pass
     
    # returns updated data to the model.
    def setModelData(self, editor, model, index):
        existing_values = index.model().values
        code = self.valid_codes[editor.currentText()]
        try:
            existing_values.index(code)
        except:
            # code not in existing values list
            model.setData(index, QVariant(code), Qt.EditRole)
        
    def getCurrentModelValue(self, model, index):
        return model.data(index, Qt.DisplayRole)
    
        