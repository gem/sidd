# Copyright (c) 2011-2013, ImageCat Inc.
#
# SIDD is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
#
"""
dialog for editing mapping scheme branches
"""
from PyQt4.QtCore import Qt, QVariant
from PyQt4.QtGui import QItemDelegate, QComboBox, QMessageBox

from ui.constants import get_ui_string

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
        code = self.valid_codes[str(editor.currentText())]
        try:
            existing_values.index(code)
            if index.data().toString() != code:
                QMessageBox.warning(None,
                                    get_ui_string("app.warning.title"), 
                                    get_ui_string("dlg.msbranch.error.attribute.exists", (code)))
        except:
            # code not in existing values list
            model.setData(index, QVariant(code), Qt.EditRole)
        
    def getCurrentModelValue(self, model, index):
        return model.data(index, Qt.DisplayRole)
    
        