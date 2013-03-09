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
# Version: $Id: wdg_mod.py 21 2012-10-26 01:48:25Z zh $

"""
Widget (Panel) for managing secondary modifier 
"""
from PyQt4.QtGui import QWidget
from PyQt4.QtCore import pyqtSignal, pyqtSlot

from ui.constants import logUICall
from ui.qt.wdg_sel_attributes_ui import Ui_widgetSelectAttribute

class WidgetSelectAttribute(Ui_widgetSelectAttribute, QWidget):    
    """
    Widget (Panel) for managing secondary modifier 
    """

    # custom event 
    codeUpdated = pyqtSignal()

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
        return str(self.ui.cb_codes.currentText())
    
    @pyqtSlot(str)
    def updateDescription(self, code):
        try:
            description = self._valid_codes[str(code)]
        except Exception as err:
            print err
            description = ""
        self.ui.lb_description.setText(description)
        self.codeUpdated.emit()

    # public methods
    ###############################
    @logUICall
    def set_attribute(self, attribute_name, valid_codes, current):
        """ set data for display """        
        # store valid codes to be used
        self._valid_codes = valid_codes
        
        # clear existing data  
        self.ui.lb_description.setText("")      
        self.ui.cb_codes.clear()
        
        # set data for combo box 
        keys = valid_codes.keys()
        keys.sort()                
        for idx, code in enumerate(keys):
            self.ui.cb_codes.addItem(code)            
            # set current value as selected from the drop-down
            if code == current:
                self.ui.cb_codes.setCurrentIndex(idx)
        