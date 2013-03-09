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
from PyQt4.QtGui import QApplication, QDialog, QDialogButtonBox
from PyQt4.QtCore import pyqtSlot

from ui.constants import logUICall, get_ui_string, UI_PADDING 
from ui.qt.dlg_edit_attributes_ui import Ui_editAttributesDialog
from ui.wdg_sel_attributes import WidgetSelectAttribute

class DialogEditAttributes(Ui_editAttributesDialog, QDialog):
    """
    dialog specifying options for creating mapping scheme
    """
    BUILD_EMPTY, BUILD_FROM_SURVEY=range(2)
    
    def __init__(self, taxonomy, attribute, attribute_value):
        """ constructor """
        super(DialogEditAttributes, self).__init__()
        self.ui = Ui_editAttributesDialog()
        self.ui.setupUi(self)

        self.ui.btn_add.clicked.connect(self.add_code)        
        self.ui.btn_delete.clicked.connect(self.del_code)
        self.ui.buttonBox.accepted.connect(self.accept)
        self.ui.buttonBox.rejected.connect(self.reject)

        self.retranslateUi(self.ui)

        self._taxonomy = taxonomy        
        self.set_attribute(attribute, attribute_value)
    
    @property
    def attribute_value(self):
        """ return attribute value from combining the selection of all input widget """
        codes = []
        for _widget in self._code_widgets:
            codes.append(_widget.selected_code)
        return str(self._taxonomy.level_separator).join(codes)
    
    @pyqtSlot
    def add_code(self):
        """ event handler for adding new empty attribute input widget """
        self.add_blank()
        self.refreshUI()
    
    @pyqtSlot    
    def del_code(self):
        """ event handler for deleting the last attribute input widget """
        self._code_widgets.pop()
        if len(self._code_widgets) == 0:
            self.add_blank()
        self.refreshUI()

    @pyqtSlot
    def updateAttributeValue(self):
        """ event handler for attribute value combo box """
        self.ui.txt_attribute_value.setText(self.attribute_value)

    # public methods
    ###############################
    @logUICall
    def set_attribute(self, attribute, attribute_value):
        """ 
        set data to display 
        - attribute: name of the attribute
        - attribute_value: attribute value 
        """
        self._attribute = attribute
        self.ui.txt_attribute.setText(attribute)
        self.ui.txt_attribute_value.setText(attribute_value)

        self._code_widgets = []
        try:
            if attribute_value is not None and attribute_value != "":
                _str_values = attribute_value.split(self._taxonomy.level_separator)
            else:
                _str_values = ['']
            for _value in _str_values:                
                if self._taxonomy.codes.has_key(_value):
                    _code = self._taxonomy.codes[_value]
                    _valid_codes = {}
                    for _valid_code in self._taxonomy.get_codes_for_attribute(_code.attribute.name, _code.level):
                        _valid_codes[_valid_code.code]=_valid_code.description    
                    _widget = WidgetSelectAttribute(self.ui.boxAttributes, _code.attribute.name, _valid_codes, _value)
                    _widget.codeUpdated.connect(self.updateAttributeValue)                    
                    self._code_widgets.append(_widget)
                else:
                    self.add_blank()
        except Exception as err:
            print err
        self.refreshUI()
    
    # internal helper methods
    ###############################
    def add_blank(self):
        """ add a blank row with new widget """ 
        _valid_codes = {}
        _valid_codes['']=''
        for _valid_code in self._taxonomy.get_codes_for_attribute(self._attribute):
            _valid_codes[_valid_code.code]=_valid_code.description        
        _widget = WidgetSelectAttribute(self.ui.boxAttributes, self._attribute, _valid_codes, "")
        _widget.codeUpdated.connect(self.updateAttributeValue)
        self._code_widgets.append(_widget)
        
    def refreshUI(self):
        """ 
        adjust UI, based on input widgets 
        and resize window 
        """
        # adjust all widget
        _widget_y = 10;
        for _widget in self._code_widgets:
                _widget.setGeometry(10, _widget_y, _widget.width(), _widget.height())
                _widget.setVisible(True)
                _widget_y+= _widget.height()
        # adjust rest of UI
        self.ui.boxAttributes.resize(self.ui.boxAttributes.width(), _widget_y)
        self.ui.buttonBox.move(self.ui.buttonBox.x(), self.ui.boxAttributes.y()+self.ui.boxAttributes.height()+UI_PADDING)
        self.resize(self.width(), self.ui.buttonBox.y()+self.ui.buttonBox.height()+2*UI_PADDING)
    
    def retranslateUi(self, ui):
        """ set UI labels """
        self.setWindowTitle(QApplication.translate("editAttributesDialog", "Edit Attribute", None, QApplication.UnicodeUTF8))
        ui.lb_attribute.setText(QApplication.translate("editAttributesDialog", "Attribute", None, QApplication.UnicodeUTF8))
        ui.lb_title.setText(QApplication.translate("editAttributesDialog", "Create Mapping Scheme", None, QApplication.UnicodeUTF8))
        ui.boxAttributes.setTitle(QApplication.translate("editAttributesDialog", "Values", None, QApplication.UnicodeUTF8))
        ui.lb_attribute_value.setText(QApplication.translate("editAttributesDialog", "Attribute Value", None, QApplication.UnicodeUTF8))

        ui.buttonBox.button(QDialogButtonBox.Ok).setText(get_ui_string('app.dialog.button.ok'))
        ui.buttonBox.button(QDialogButtonBox.Cancel).setText(get_ui_string('app.dialog.button.cancel'))
