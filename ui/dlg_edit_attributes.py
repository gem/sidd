# Copyright (c) 2011-2013, ImageCat Inc.
#
# SIDD is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
#
"""
dialog for editing secondary modifiers
"""
from PyQt4.QtGui import QDialog, QDialogButtonBox
from PyQt4.QtCore import pyqtSlot

from ui.constants import logUICall, UI_PADDING 
from ui.qt.dlg_edit_attributes_ui import Ui_editAttributesDialog
from ui.wdg_sel_attributes import WidgetSelectAttribute

class DialogEditAttributes(Ui_editAttributesDialog, QDialog):
    """
    dialog specifying options for creating mapping scheme
    """
    BUILD_EMPTY, BUILD_FROM_SURVEY=range(2)
    
    def __init__(self, app, taxonomy, attribute, attribute_value, modifier_value, allow_blank=True):
        """ constructor """
        super(DialogEditAttributes, self).__init__()
        self.ui = Ui_editAttributesDialog()
        self.ui.setupUi(self)
        self.app = app
        self.allow_blank=allow_blank

        self.ui.btn_add.clicked.connect(self.add_code)        
        self.ui.btn_delete.clicked.connect(self.del_code)
        self.ui.buttonBox.accepted.connect(self.accept)
        self.ui.buttonBox.rejected.connect(self.reject)

        self._taxonomy = taxonomy
        self.set_modifier_value(attribute, attribute_value, modifier_value)
    
    @property
    def modifier_value(self):
        """ return attribute value from combining the selection of all input widget """
        codes = []
        for _widget in self._code_widgets:
            if _widget.selected_code == '':
                continue
            try:
                # check for existing
                codes.index(_widget.selected_code)
                # no error means found, which is actually the error case                                
                logUICall.log('value %s already exists' % _widget.selected_code, logUICall.WARNING)
                self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
                return ''
            except:
                # this means not found, no error
                pass
            codes.append(_widget.selected_code)
        self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
        return str(self._taxonomy.level_separator).join(codes)

    def add_code(self):
        """ event handler for adding new empty attribute input widget """
        has_blank=False
        for _widget in self._code_widgets:
            if _widget.selected_code == '':
                has_blank=True
                break  
        if (not self.allow_blank) and has_blank:
            logUICall.log('Please set values before adding additional modifiers', logUICall.WARNING)
            return          
        self.add_blank()
        self.refreshUI()
    
    def del_code(self):
        """ event handler for deleting the last attribute input widget """
        _widget = self._code_widgets.pop()
        _widget.setParent(None)
        _widget.destroy()
        del _widget
        if len(self._code_widgets) == 0:
            self.add_blank()
        self.refreshUI()
    
    def updateAttributeValue(self):
        """ event handler for attribute value combo box """
        self.ui.txt_modifier_value.setText(self.modifier_value)

    # public methods
    ###############################
    @logUICall
    def set_modifier_value(self, attribute, attribute_value, modifier_value):
        """ 
        set data to display 
        - attribute: name of the attribute
        - modifier_value: attribute value 
        """
        self._attribute = attribute
        self._attribute_value = attribute_value
        self._attribute_code = self._taxonomy.get_code_by_name(attribute_value)
        self.ui.txt_attribute_name.setText(attribute.name)
        self.ui.txt_attribute.setText(attribute_value)
        self.ui.txt_modifier_value.setText(modifier_value)

        self._code_widgets = []
        try:
            if modifier_value is not None and modifier_value != "":
                _str_values = modifier_value.split(self._taxonomy.level_separator)
            else:
                _str_values = ['']
            for _value in _str_values:                
                if self._taxonomy.codes.has_key(_value):
                    _valid_codes = {}
                    for _valid_code in self._attribute.get_valid_codes(parent=self._attribute_code):
                        _valid_codes[_valid_code.code]=_valid_code.description    
                    _widget = WidgetSelectAttribute(self.ui.boxAttributes, self._attribute.name, _valid_codes, _value)
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
        #for _valid_code in self._taxonomy.get_codes_for_attribute(self._attribute):
        for _valid_code in self._attribute.get_valid_codes(parent=self._attribute_code):
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
