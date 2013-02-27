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
    
    def __init__(self, app):
        """ constructor """
        super(DialogMSOptions, self).__init__()
        self.ui = Ui_msOptionsDialog()
        self.ui.setupUi(self)
        self.retranslateUi(self.ui)

        self.dlgAttrRange = DialogAttrRanges(app)        
        self.app = app
        
        # set attribute list
        self.resetList()        
        self.refreshAttributeList(self.attr_names)
        
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
        
        self.ui.lst_attributes.itemSelectionChanged.connect(self.selectedAttributeChanged)

        # additional settings
        self.setFixedSize(self.size())  # no resize
        self.ui.lst_attributes.setSelectionMode(QAbstractItemView.SingleSelection) # allow select only one attribute
        self.ui.radioEmptyMS.click()    # default to empty MS

    @property
    def attributes(self):
        return self.attr_names

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
        value = self.attr_names[index]
        self.attr_names.remove(value)
        self.attr_names.insert(new_index, value)
        self.refreshAttributeList(self.attr_names)
        self.ui.lst_attributes.setCurrentRow(new_index)
    
    @logUICall
    @pyqtSlot()
    def attributeMoveDown(self):
        index = self.ui.lst_attributes.currentRow()
        if index == len(self.attr_names)-1:
            return
        new_index = index+1
        value = self.attr_names[index]
        self.attr_names.remove(value)
        self.attr_names.insert(new_index, value)
        self.refreshAttributeList(self.attr_names)
        self.ui.lst_attributes.setCurrentRow(new_index)
    
    @logUICall
    @pyqtSlot()
    def setAttributeRanges(self):
        index = self.ui.lst_attributes.currentRow()            
        attr_value = self.attr_names[index]
        if self.app.project.operator_options.has_key(attr_value):            
            ranges = self.app.project.operator_options[attr_value]
            self.dlgAttrRange.set_values(attr_value, ranges['min_values'], ranges['max_values'])
        else:
            self.dlgAttrRange.set_values(attr_value, [], [])
                    
        if self.dlgAttrRange.exec_() == QDialog.Accepted:
            self.app.project.operator_options[attr_value] = {'min_values':self.dlgAttrRange.min_values, 
                                                             'max_values':self.dlgAttrRange.max_values}
            
    @logUICall
    @pyqtSlot()
    def attributeMoveTop(self):
        index = self.ui.lst_attributes.currentRow()
        if index == 0:
            return
        value = self.attr_names[index]
        self.attr_names.remove(value)
        self.attr_names.insert(0, value)
        self.refreshAttributeList(self.attr_names)
        self.ui.lst_attributes.setCurrentRow(0)
    
    @logUICall
    @pyqtSlot()
    def attributeMoveBottom(self):
        index = self.ui.lst_attributes.currentRow()
        if index == len(self.attr_names)-1:
            return
        value = self.attr_names[index]
        self.attr_names.remove(value)
        self.attr_names.append(value)
        self.refreshAttributeList(self.attr_names)
        self.ui.lst_attributes.setCurrentRow(len(self.attr_names)-1)
    
    @logUICall
    @pyqtSlot()
    def selectedAttributeChanged(self):
        indices = self.ui.lst_attributes.selectedIndexes()
        if len(indices) == 1:
            self.ui.widget_attribute_buttons.setEnabled(True) 
            for att in self.app.taxonomy.attributes:
                if att.name == str(indices[0].data().toString()):
                    if att.type == 2:
                        self.ui.btn_range.setEnabled(True)
                    else:
                        self.ui.btn_range.setEnabled(False)
                    break
        else:
            self.ui.widget_attribute_buttons.setEnabled(False)
    
    def resetList(self):
        self.attr_names = []
        try:
            for att in self.app.taxonomy.attributes:
                self.attr_names.append(att.name)                                
        except:
            self.attr_names = []
    
    def refreshAttributeList(self, attributes):
        self.ui.lst_attributes.clear()
        self.ui.lst_attributes.addItems(attributes)
        self.ui.widget_attribute_buttons.setEnabled(False)
    
    def retranslateUi(self, ui):
        self.setWindowTitle(get_ui_string("dlg.buildms.title"))
        ui.lb_title.setText(get_ui_string("dlg.buildms.title"))
        ui.lb_attributes.setText(get_ui_string("dlg.buildms.attributes"))
        ui.radioEmptyMS.setText(get_ui_string("dlg.buildms.option.empty"))
        ui.radioBuildMS.setText(get_ui_string("dlg.buildms.option.survey"))
        