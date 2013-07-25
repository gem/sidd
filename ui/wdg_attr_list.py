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
from PyQt4.QtCore import pyqtSlot, pyqtSignal, Qt, QObject

from ui.constants import UI_PADDING
from ui.qt.wdg_attr_list_ui import Ui_widgetAttributes
from ui.helper.attr_tree import AttributesTreeModel

class WidgetAttributeList(Ui_widgetAttributes, QWidget):    
    """
    Widget (Panel) for managing secondary modifier 
    """
    # custom event 
    listUpdated = pyqtSignal(QObject)
    rangeUpdated = pyqtSignal(QObject)

    # constructor / destructor
    ###############################        
    def __init__(self, parent, app, taxonomy, order, ranges):
        """ constructor """
        super(WidgetAttributeList, self).__init__(parent)
        self.ui = Ui_widgetAttributes()
        self.ui.setupUi(self)
        self.setFixedSize(self.size())
        
        self.app = app
        self.attribute_selected = order
        self.attribute_ranges = ranges

        self.ui.btn_move_up.clicked.connect(self.attributeMoveUp)
        self.ui.btn_move_down.clicked.connect(self.attributeMoveDown)
        self.ui.btn_move_top.clicked.connect(self.attributeMoveTop)
        self.ui.btn_move_bottom.clicked.connect(self.attributeMoveBottom)
        self.ui.btn_range.clicked.connect(self.setAttributeRanges)
        
        self.taxonomy = taxonomy
        self.selected = order
        self.attr_model = AttributesTreeModel(taxonomy, self.selected)
        self.ui.tree_attributes.setModel(self.attr_model)
        
        # additional settings
        self.setFixedSize(self.size())  # no resize
        self.ui.tree_attributes.setSelectionMode(QAbstractItemView.SingleSelection) # allow select only one attribute        
        self.ui.tree_attributes.clicked.connect(self.attributeChanged) 
    
    @pyqtSlot(QObject)
    def resizeEvent(self, event):
        self.ui.widget_attribute_buttons.move(self.width()-self.ui.widget_attribute_buttons.width()- UI_PADDING,
                                              self.ui.widget_attribute_buttons.y())
        self.ui.tree_attributes.resize(self.ui.widget_attribute_buttons.x() - UI_PADDING, 
                                       self.height() - self.ui.tree_attributes.y() - UI_PADDING)
        print "resized", self.width(), self.height()
        
    @property
    def attributes(self):
        return self.taxonomy.attribute_groups 
    
    @property
    def attribute_order(self):
        return self.attr_model.selected

    @attribute_order.setter
    def attribute_order(self, order):
        self.attr_model.selected = order        

    @pyqtSlot()
    def attributeMoveUp(self):
        self.updateAttributeOrder(self.attr_model.moveUp)
    
    @pyqtSlot()
    def attributeMoveDown(self):
        self.updateAttributeOrder(self.attr_model.moveDown)
    
    @pyqtSlot()
    def setAttributeRanges(self):
        index = self.ui.tree_attributes.selectedIndexes()[0]
        data = self.attr_model.data(index, Qt.DisplayRole)
        self.app.setRange(self.attribute_ranges, data)
            
    @pyqtSlot()
    def attributeMoveTop(self):
        self.updateAttributeOrder(self.attr_model.moveTop)
    
    @pyqtSlot()
    def attributeMoveBottom(self):
        self.updateAttributeOrder(self.attr_model.moveBottom)
    
    @pyqtSlot()
    def attributeChanged(self):
        data = self.attr_model.data(self.ui.tree_attributes.selectedIndexes()[0], Qt.UserRole)
        allow_set_range = False
        allow_change_order = False
        if data.level == 1:
            attr_grp = self.taxonomy.get_attribute_group_by_name(data.value)
            if attr_grp is not None:
                allow_set_range = (attr_grp.type == 2)
                allow_change_order = True
        self.ui.btn_range.setEnabled(allow_set_range)
        self.ui.btn_move_bottom.setEnabled(allow_change_order)
        self.ui.btn_move_down.setEnabled(allow_change_order)
        self.ui.btn_move_up.setEnabled(allow_change_order)
        self.ui.btn_move_top.setEnabled(allow_change_order)
    
    def updateAttributeOrder(self, func):
        func(self.ui.tree_attributes.selectedIndexes()[0])        
