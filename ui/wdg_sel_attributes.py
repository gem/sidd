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
Widget (Panel) for managing secondary modifier 
"""
from PyQt4.QtGui import QWidget
from PyQt4.QtCore import pyqtSignal, pyqtSlot, QObject

from ui.constants import UI_PADDING 
from ui.qt.wdg_sel_attributes_ui import Ui_widgetSelectAttribute

class WidgetSelectAttribute(Ui_widgetSelectAttribute, QWidget):    
    """
    Widget (Panel) for managing secondary modifier 
    """
    # custom event 
    codeUpdated = pyqtSignal(QObject)

    # constructor / destructor
    ###############################        
    def __init__(self, parent, attribute_name="", valid_codes={}, current=""):
        """ constructor """
        super(WidgetSelectAttribute, self).__init__(parent)
        self.ui = Ui_widgetSelectAttribute()
        self.ui.setupUi(self)
        self.setFixedSize(self.size())
        self.ui.cb_codes.currentIndexChanged[str].connect(self.updateDescription)
        self.set_attribute(attribute_name, valid_codes, current)        

    @property
    def selected_code(self):
        code = str(self.ui.cb_codes.currentText())
        if self._valid_codes.has_key(code):
            return self._valid_codes[code]
        else:
            return "" 
    
    @selected_code.setter
    def selected_code(self, code):
        for desc, valid_code in self._valid_codes.iteritems():
            if valid_code == code:
                self.ui.cb_codes.setCurrentIndex(self.ui.cb_codes.findText(desc))
    
    def set_scope(self, scope, current):
        self.set_attribute(self.attribute_name, self._valid_codes, scope, current)
    
    @pyqtSlot(str)
    def updateDescription(self, desc):
        try:
            code = self._valid_codes[str(desc)]
            description = str(code.code)
        except:
            description = ""
        self.ui.lb_description.setText(description)
        self.codeUpdated.emit(self)

    # public methods
    ###############################
    def set_attribute(self, attribute_name, valid_codes, current):
        """ set data for display """        
        # store valid codes to be used
        self.attribute_name = attribute_name
        self._valid_codes = valid_codes
        
        # clear existing data  
        self.ui.lb_attribute.setText(attribute_name)
        self.ui.lb_description.setText("")
        self.ui.cb_codes.clear()
        
        # set data for combo box 
        keys = valid_codes.keys()
        keys.sort()
        for idx, key in enumerate(keys):
            code = valid_codes[key]
            self.ui.cb_codes.addItem(key)      
 
            # set current value as selected from the drop-down
            if code == current:
                self.ui.cb_codes.setCurrentIndex(idx)

    @pyqtSlot(QObject)
    def resizeEvent(self, event):
        width = self.width()        
        height = self.ui.lb_attribute.height()
        self.resizeUI(width, height)
        
    def resizeUI(self, width, height):
        self.ui.lb_attribute.resize(width * 0.35, height)
        self.ui.cb_codes.setGeometry(self.ui.lb_attribute.x()+self.ui.lb_attribute.width()+UI_PADDING, 
                                     height*0.1, width * 0.4, height*0.8)
        self.ui.lb_description.setGeometry(self.ui.cb_codes.x()+self.ui.cb_codes.width()+2*UI_PADDING,
                                           0, width * 0.2, height)
        
    