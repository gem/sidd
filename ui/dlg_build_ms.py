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
from PyQt4.QtGui import QDialog, QAbstractItemView
from PyQt4.QtCore import pyqtSlot

from ui.constants import logUICall, get_ui_string 
from ui.qt.dlg_build_ms_ui import Ui_msOptionsDialog
from ui.dlg_attr_range import DialogAttrRanges

class DialogMSOptions(Ui_msOptionsDialog, QDialog):
    """
    dialog specifying options for creating mapping scheme
    """
    BUILD_EMPTY, BUILD_FROM_SURVEY=range(2)
    
    def __init__(self, attributes, ranges):
        """ constructor """
        super(DialogMSOptions, self).__init__()
        self.ui = Ui_msOptionsDialog()
        self.ui.setupUi(self)
        self.retranslateUi(self.ui)

        self.dlgAttrRange = DialogAttrRanges()        
        
        # get attribute list from app.taxonomy and set to UI
        self._attr_names = []
        self._ranges ={}
        self._attribute_has_range={}
        self.attributes = attributes
        self.attribute_ranges = ranges
        
        # connect slot (ui event)
        self.ui.buttons.accepted.connect(self.accept)
        self.ui.buttons.rejected.connect(self.reject)
        
        self.ui.radioEmptyMS.toggled.connect(self.setMSOption)
        self.ui.radioBuildMS.toggled.connect(self.setMSOption)
        
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
        self.ui.radioEmptyMS.click()    # default to empty MS


    def exec_(self):
        self.refreshAttributeList(self._attr_names)
        return super(DialogMSOptions, self).exec_()
        
    # property accessor/mutators
    ###############################
    @property
    def attributes(self):
        return self._attributes
    
    @attributes.setter
    def attributes(self, attributes):
        self._attributes = attributes
        #self.attribute_order = [attr.name for attr in self.attributes]
        self._attribute_has_range = {}
        for att in attributes:
            # numeric attributes can have range
            if att.type == 2:
                self._attribute_has_range[att.name]=1

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
                self.ui.widget_attributes.setEnabled(False)   
            elif sender == self.ui.radioBuildMS:
                self.build_option = self.BUILD_FROM_SURVEY
                self.ui.widget_attributes.setEnabled(True)
            else:
                logUICall.log('\tdo nothing. should not even be here',
                              logUICall.WARNING)
        #else:
        #   ignore
        
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
        if self._ranges.has_key(attr_value):
            ranges = self._ranges[attr_value]
            self.dlgAttrRange.set_values(attr_value, ranges['min_values'], ranges['max_values'])
        else:
            self.dlgAttrRange.set_values(attr_value, [], [])
                    
        if self.dlgAttrRange.exec_() == QDialog.Accepted:
            self._ranges[attr_value] = {'min_values':self.dlgAttrRange.min_values,
                                        'max_values':self.dlgAttrRange.max_values}
            
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
            for _attr in self._attribute_has_range:
                if attribute == _attr:
                    attribute = '%s *' % attribute                    
            self._attr_names.append(attribute)
        self.refreshAttributeList(self._attr_names)
        self.refreshNotIncludedList()

    @logUICall
    @pyqtSlot()
    def attributeDelete(self):
        indices = self.ui.lst_attributes.selectedIndexes()
        if len(indices) == 1:
            attribute = str(indices[0].data().toString())
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
    
    def retranslateUi(self, ui):
        """ set text for ui elements """
        # dialog title
        self.setWindowTitle(get_ui_string("dlg.buildms.title"))
        # ui elements
        ui.lb_title.setText(get_ui_string("dlg.buildms.title"))
        ui.lb_attributes.setText(get_ui_string("dlg.buildms.attributes"))
        ui.lb_attributes_not_included.setText(get_ui_string("dlg.buildms.attributes.not_included"))
        ui.lb_notes.setText(get_ui_string("dlg.buildms.notes"))        
        ui.radioEmptyMS.setText(get_ui_string("dlg.buildms.option.empty"))
        ui.radioBuildMS.setText(get_ui_string("dlg.buildms.option.survey"))
        # tooltips
        self.ui.btn_move_up.setToolTip(get_ui_string("dlg.buildms.button.moveup"))
        self.ui.btn_move_down.setToolTip(get_ui_string("dlg.buildms.button.movedown"))
        self.ui.btn_move_top.setToolTip(get_ui_string("dlg.buildms.button.movetop"))
        self.ui.btn_move_bottom.setToolTip(get_ui_string("dlg.buildms.button.movebottom"))
        self.ui.btn_range.setToolTip(get_ui_string("dlg.buildms.button.range"))
        
        