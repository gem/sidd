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
from PyQt4.QtGui import QDialog
from PyQt4.QtCore import pyqtSlot

from ui.constants import UI_PADDING, logUICall 
from ui.qt.dlg_build_ms_ui import Ui_msOptionsDialog
from ui.wdg_attr_list import WidgetAttributeList 

class DialogMSOptions(Ui_msOptionsDialog, QDialog):
    """
    dialog specifying options for creating mapping scheme
    """
    BUILD_EMPTY, BUILD_FROM_SURVEY=range(2)
    
    def __init__(self, app, taxonomy, ranges):
        """ constructor """
        super(DialogMSOptions, self).__init__()
        self.ui = Ui_msOptionsDialog()
        self.ui.setupUi(self)

        self.app = app

        self.attributeList = WidgetAttributeList(self, app, taxonomy, [], ranges)
        self.attributeList.move(30, 90)
        self.attributeList.setFixedSize(self.width() - 30 - 2*UI_PADDING, 
                                        self.ui.buttons.y() - 90 - 2*UI_PADDING)
        
        # connect slot (ui event)
        self.ui.buttons.accepted.connect(self.accept)
        self.ui.buttons.rejected.connect(self.reject)
        
        self.ui.radioEmptyMS.toggled.connect(self.setMSOption)
        self.ui.radioBuildMS.toggled.connect(self.setMSOption)
        
        # additional settings
        self.setFixedSize(self.size())  # no resize
        self.ui.radioEmptyMS.click()    # default to empty MS


    def exec_(self):
        #self.attributeList.refreshAttributeList(self.attributeList.attribute_order)
        return super(DialogMSOptions, self).exec_()
        
    # property accessor/mutators
    ###############################
    @property
    def attributes(self):
        return self.attributeList.attributes
    
    @attributes.setter
    def attributes(self, attributes):
        self.attributeList.attributes = attributes
        
    @property
    def attribute_order(self):
        return self.attributeList.attribute_order

    @attribute_order.setter
    def attribute_order(self, order):
        self.attributeList.attribute_order = order
        if len(order) > 0:
            self.ui.radioBuildMS.setChecked(True)
        
    @property
    def attribute_ranges(self):
        return self.attributeList.attribute_ranges

    @attribute_ranges.setter
    def attribute_ranges(self, ranges):
        self.attributeList.attribute_ranges = ranges
    
    @property
    def use_sampling(self):
        return self.ui.ck_use_sampling.isChecked()
    
    @use_sampling.setter
    def use_sampling(self, value):
        self.ui.ck_use_sampling.setChecked(value)
    
    # ui event handler
    ###############################
    @logUICall
    @pyqtSlot()
    def setMSOption(self):
        """ adjust options when option radio button is selected """
        sender = self.sender()
        if sender.isChecked():
            if sender == self.ui.radioEmptyMS:
                self.build_option = self.BUILD_EMPTY
                self.attributeList.setEnabled(False)                
            elif sender == self.ui.radioBuildMS:
                self.build_option = self.BUILD_FROM_SURVEY
                self.attributeList.setEnabled(True)                
            else:
                logUICall.log('\tdo nothing. should not even be here',
                              logUICall.WARNING)
        #else:
        #   ignore
        
