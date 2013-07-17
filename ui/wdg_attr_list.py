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
Widget (Panel) for managing attributes to use when building Mapping scheme 
"""
from PyQt4.QtGui import QWidget, QAbstractItemView
from PyQt4.QtCore import pyqtSlot, pyqtSignal, QObject

from ui.constants import UI_PADDING, logUICall
from ui.qt.wdg_attr_list_ui import Ui_widgetAttributes

class WidgetAttributeList(Ui_widgetAttributes, QWidget):    
    """
    Widget (Panel) for managing secondary modifier 
    """
    # custom event 
    listUpdated = pyqtSignal(QObject)
    rangeUpdated = pyqtSignal(QObject)

    # constructor / destructor
    ###############################        
    def __init__(self, parent, app, attributes, order, ranges):
        """ constructor """
        super(WidgetAttributeList, self).__init__(parent)
        self.ui = Ui_widgetAttributes()
        self.ui.setupUi(self)
        self.setFixedSize(self.size())
        
        self.app = app
        self.attributes = attributes
        self.attribute_order = order
        self.attribute_ranges = ranges

        self.ui.btn_move_up.clicked.connect(self.attributeMoveUp)
        self.ui.btn_move_down.clicked.connect(self.attributeMoveDown)
        self.ui.btn_move_top.clicked.connect(self.attributeMoveTop)
        self.ui.btn_move_bottom.clicked.connect(self.attributeMoveBottom)
        self.ui.btn_range.clicked.connect(self.setAttributeRanges)
        
        self.ui.btn_move_left.clicked.connect(self.attributeAdd)
        self.ui.btn_move_right.clicked.connect(self.attributeDelete)
        
        self.ui.lst_attributes.itemSelectionChanged.connect(self.selectedAttributeChanged)
        self.ui.lst_attributes_not_included.itemSelectionChanged.connect(self.selectedNotIncludedAttributeChanged)

        self.ui.btn_move_left.setEnabled(False)
        self.ui.btn_move_right.setEnabled(False)
             
        # additional settings
        self.setFixedSize(self.size())  # no resize
        self.ui.lst_attributes.setSelectionMode(QAbstractItemView.SingleSelection) # allow select only one attribute        
        
    @property
    def attributes(self):
        return self._attributes
    
    @attributes.setter
    def attributes(self, attributes):
        self._attributes = attributes
        self._attribute_has_range = {}
        for att in attributes:
            # numeric attributes can have range
            if att.type == 2:
                self._attribute_has_range[att.name]=1        
        self.refreshNotIncludedList()
        
    @property
    def attribute_order(self):
        return self._attr_names

    @attribute_order.setter
    def attribute_order(self, order):
        self._attr_names = order
        self.refreshAttributeList(self._attr_names)
        self.refreshNotIncludedList()

    @property
    def attribute_ranges(self):
        return self._ranges

    @attribute_ranges.setter
    def attribute_ranges(self, ranges):
        self._ranges = ranges    

    @logUICall
    @pyqtSlot()
    def attributeMoveUp(self):
        index = self.ui.lst_attributes.currentRow()
        if index == 0:
            return
        new_index = index-1
        value = self._attr_names[index]
        self._attr_names.remove(value)
        self._attr_names.insert(new_index, value)
        self.refreshAttributeList(self._attr_names)
        self.ui.lst_attributes.setCurrentRow(new_index)
    
    @logUICall
    @pyqtSlot()
    def attributeMoveDown(self):
        index = self.ui.lst_attributes.currentRow()
        if index == len(self._attr_names)-1:
            return
        new_index = index+1
        value = self._attr_names[index]
        self._attr_names.remove(value)
        self._attr_names.insert(new_index, value)
        self.refreshAttributeList(self._attr_names)
        self.ui.lst_attributes.setCurrentRow(new_index)
    
    @logUICall
    @pyqtSlot()
    def setAttributeRanges(self):
        index = self.ui.lst_attributes.currentRow()            
        attr_value = self._attr_names[index]
        self.app.setRange(self._ranges, attr_value)
            
    @logUICall
    @pyqtSlot()
    def attributeMoveTop(self):
        index = self.ui.lst_attributes.currentRow()
        if index == 0:
            return
        value = self._attr_names[index]
        self._attr_names.remove(value)
        self._attr_names.insert(0, value)
        self.refreshAttributeList(self._attr_names)
        self.ui.lst_attributes.setCurrentRow(0)
    
    @logUICall
    @pyqtSlot()
    def attributeMoveBottom(self):
        index = self.ui.lst_attributes.currentRow()
        if index == len(self._attr_names)-1:
            return
        value = self._attr_names[index]
        self._attr_names.remove(value)
        self._attr_names.append(value)
        self.refreshAttributeList(self._attr_names)
        self.ui.lst_attributes.setCurrentRow(len(self._attr_names)-1)

    @logUICall
    @pyqtSlot()
    def attributeAdd(self):
        indices = self.ui.lst_attributes_not_included.selectedIndexes()
        if len(indices) == 1:
            attribute = str(indices[0].data().toString())
            self._attr_names.append(attribute)
        self.refreshAttributeList(self._attr_names)
        self.refreshNotIncludedList()

    @logUICall
    @pyqtSlot()
    def attributeDelete(self):
        indices = self.ui.lst_attributes.selectedIndexes()
        if len(indices) == 1:
            attribute = str(indices[0].data().toString())
            for _attr in self._attribute_has_range:
                if attribute == '%s *' % _attr:
                    attribute = _attr               
            try:
                self._attr_names.remove(attribute)
            except:
                pass
        self.refreshAttributeList(self._attr_names)
        self.refreshNotIncludedList()
        
    @logUICall
    @pyqtSlot()
    def selectedAttributeChanged(self):
        indices = self.ui.lst_attributes.selectedIndexes()
        if len(indices) == 1:
            self.ui.widget_attribute_buttons.setEnabled(True)                                    
            _can_set_range = False
            _sel_attributes = str(indices[0].data().toString())
            for _attr in self._attribute_has_range:
                if _sel_attributes == '%s *' % _attr:
                    _can_set_range = True
                    break
            self.ui.btn_range.setEnabled(_can_set_range)
            self.ui.btn_move_right.setEnabled(True)            
        else:
            self.ui.widget_attribute_buttons.setEnabled(False)
            self.ui.btn_move_right.setEnabled(False)            
    
    @logUICall
    @pyqtSlot()
    def selectedNotIncludedAttributeChanged(self):
        indices = self.ui.lst_attributes_not_included.selectedIndexes()
        self.ui.btn_move_left.setEnabled(len(indices) == 1)
    
    @logUICall
    def resetList(self):
        self._attr_names = []
        try:
            for att in self.app.taxonomy.attributes:
                self._attr_names.append(att.name)                                
        except:
            self._attr_names = []
    
    def refreshAttributeList(self, attributes):
        self.ui.lst_attributes.clear()
        for attr in attributes:
            if self._attribute_has_range.has_key(attr):
                attr = '%s *' % attr
            self.ui.lst_attributes.addItem(attr)
        self.ui.widget_attribute_buttons.setEnabled(False)
    
    def refreshNotIncludedList(self):
        # add to not_included if not already in attribute_order list
        self.ui.lst_attributes_not_included.clear()
        for _attr in self._attributes:            
            try:
                self._attr_names.index(_attr.name)
            except:
                self.ui.lst_attributes_not_included.addItem(_attr.name)              