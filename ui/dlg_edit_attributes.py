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
dialog for editing secondary modifiers
"""
from PyQt4.QtGui import QDialog, QDialogButtonBox
from PyQt4.QtCore import pyqtSlot, QObject

from ui.constants import logUICall, UI_PADDING 
from ui.qt.dlg_edit_attributes_ui import Ui_editAttributesDialog
from ui.wdg_sel_attributes import WidgetSelectAttribute

class DialogEditAttributes(Ui_editAttributesDialog, QDialog):
    """
    dialog specifying options for creating mapping scheme
    """
    BUILD_EMPTY, BUILD_FROM_SURVEY=range(2)
    
    def __init__(self, app, taxonomy, attribute_group, node, modifier_value, allow_blank=True):
        """ constructor """
        super(DialogEditAttributes, self).__init__()
        self.ui = Ui_editAttributesDialog()
        self.ui.setupUi(self)
        self.app = app
        self.allow_blank=allow_blank

        self.ui.buttonBox.accepted.connect(self.accept)
        self.ui.buttonBox.rejected.connect(self.reject)

        self.taxonomy = taxonomy
        self.separator = str(self.taxonomy.get_separator(self.taxonomy.Separators.Attribute))
        self.attribute_group = attribute_group
        self.node = node
        
        self.code_widgets = []
        self.code_attribute = {}
        for idx, attribute in enumerate(attribute_group.attributes):
            widget = WidgetSelectAttribute(self.ui.boxAttributes, attribute.name, {}, "")
            if idx > 0:
                widget.setEnabled(False)
            self.code_widgets.append(widget)
            self.code_attribute[attribute.name] = idx        
        self.fill_attribute_input(self.code_widgets[0],
                                  self.code_widgets[0].attribute_name,
                                  '', None)
        
        for widget in self.code_widgets:
            widget.codeUpdated.connect(self.updateAttributeValue)

        self.ui.txt_attribute_name.setText(attribute_group.name)
        self.set_modifier_value(modifier_value)

    @pyqtSlot(QObject)
    def resizeEvent(self, event):
        """ 
        adjust UI, based on input widgets 
        and resize window 
        """        
        # adjust all widget
        _width = self.width()
        _widget_y = 10;
        for _widget in self.code_widgets:
            _widget.move(10, _widget_y)                
            _widget_y+= _widget.height()
            _widget.resizeUI(_width-4*UI_PADDING, _widget.height())
            
        # adjust rest of UI
        self.ui.boxAttributes.resize(_width-2*UI_PADDING, _widget_y)
        self.ui.buttonBox.move(_width - self.ui.buttonBox.width()-UI_PADDING, 
                               self.ui.boxAttributes.y()+self.ui.boxAttributes.height()+UI_PADDING)
        self.resize(_width, self.ui.buttonBox.y()+self.ui.buttonBox.height()+2*UI_PADDING)   

    @property
    def modifier_value(self):
        """ return attribute value from combining the selection of all input widget """
        return str(self.ui.txt_modifier_value.text())

    # public methods
    ###############################
    @logUICall
    def set_modifier_value(self, modifier_value):
        """ set UI with given modifier value """
        vals = self.taxonomy.parse(modifier_value)
        for val in vals:
            cIdx = self.code_attribute[val.code.attribute.name]
            self.code_widgets[cIdx].selected_code = val.code

    # internal helper methods
    ###############################
    def fill_attribute_input(self, widget, attribute_name, current, code_filter=None):
        valid_codes = {}
        valid_codes['']=''
        for code in self.taxonomy.get_code_by_attribute(attribute_name, code_filter):
            valid_codes[code.description] = code                    
        widget.set_attribute(attribute_name, valid_codes, current)
    
    def updateAttributeValue(self, source):
        """ event handler for attribute value combo box """
        # filter available options        
        filter_code = None
        if self.taxonomy.has_rule(source.attribute_name):
            filter_code = source.selected_code
        
        attribute_idx = self.code_attribute[source.attribute_name]+1
        if attribute_idx < len(self.code_widgets) :
            widget = self.code_widgets[attribute_idx]
            self.fill_attribute_input(widget, 
                                      widget.attribute_name, 
                                      widget.selected_code, filter_code)
            widget.setEnabled(True)
        
        # build modifier_value
        codes = []        
        for widget in self.code_widgets:
            if str(widget.selected_code) == '':
                continue
            codes.append(str(widget.selected_code.code))
        if len(codes)>0:
            self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
            self.ui.txt_modifier_value.setText(self.separator.join(codes))
        else:
            self.ui.txt_modifier_value.setText('')