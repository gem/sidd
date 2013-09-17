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
model supporting tree UI for selecting attributes to include 
when creating mapping scheme  
"""
from PyQt4.QtCore import Qt, QVariant,\
                         QAbstractItemModel, QModelIndex
from ui.constants import logUICall 

class AttributesTreeModel(QAbstractItemModel):  
    """
    tree model for visualizing attribute groups and attributes
    """
    class AttributeItem(object):
        def __init__(self, value, level, parent=None, checked=Qt.Unchecked):
            self.value = value
            self.level = level
            self.parent = parent
            self.checked = checked
            self.children = []

        def __str__(self):
            return "%s %d %d %s" % (self.value, self.level, self.checked, 
                                         "\t\n".join([str(c) for c in self.children]))
            
    def __init__(self, taxonomy, selected):
        """ constructor """
        super(AttributesTreeModel, self).__init__(None)
        self.root_node = AttributesTreeModel.AttributeItem('root', 0)
        for grp in taxonomy.attribute_groups:
            grp_item = AttributesTreeModel.AttributeItem(grp.name, 1, self.root_node)
            for attr in grp.attributes:
                grp_item.children.append(AttributesTreeModel.AttributeItem(attr.name, 2, grp_item))
            self.root_node.children.append(grp_item)            
        self.selected = selected
    
    @property
    def selected(self):
        attrs = []
        for grp in self.root_node.children:
            for attr in grp.children:
                if attr.checked == Qt.Checked:
                    attrs.append(attr.value)
        return attrs
    
    @selected.setter
    def selected(self, selected):
        for grp in self.root_node.children:
            for attr in grp.children:
                try:
                    selected.index(attr.value)
                    # in selected list
                    attr.checked = Qt.Checked
                except:
                    # not in selected list
                    # do nothing
                    pass
            self.updateGroup(grp)

    def columnCount(self, parent):
        """ (override function) attribute tree only has 1 column """
        return 1

    def rowCount(self, parent):
        """ (override function) retrieve number of children from a given parent node """
        logUICall.log("rowCount %s" % (parent), logUICall.DEBUG_L2)
        if parent is None:
            return len(self.root_node.children)
        if not parent.isValid(): # invalid case treated same as root node
            return len(self.root_node.children)
        
        # find children
        item = parent.internalPointer()
        return len(item.children)
    
    def data(self, index, role):
        """
        (override function) retrieve appropriate data to show in UI given a index
        currently only DisplayRole is implemented
        """
        logUICall.log("data %s" % (index), logUICall.DEBUG_L2)
        if index is None:  # invalid case, nothing to display
            return self.root_node
        if not index.isValid():  # invalid case, nothing to display
            return self.root_node
        
        item = index.internalPointer()
        if role == Qt.DisplayRole:
            # construct data to show in tree UI
            return '%s' % (item.value)
        elif role == Qt.CheckStateRole:
            return item.checked
        elif role == Qt.UserRole:
            return item
        else:
            return None
        
    def setData(self, index, value, role):
        if role == Qt.CheckStateRole:
            item = index.internalPointer()
            item.checked = value
            if item.level==2:
                self.updateGroup(item.parent)
                self.dataChanged.emit(self.parent(index), index)
            else:
                for attr in item.children:
                    attr.checked = value
                self.dataChanged.emit(index, self.index(len(item.children)-1, 0, index))
            return True
            
    def index(self, row, column, parent):
        """
        (override function) find appropriate children using row from given parent node
        this function is tightly associated with rowCount
        """
        logUICall.log("index %s %s %s" % (row, column, parent), logUICall.DEBUG_L2)
        if parent is None:
            logUICall.log('%s is null' % (parent), logUICall.DEBUG_L2)
            return self.root_node_index
        if parent.isValid():    # get parent node            
            parentItem = parent.internalPointer()            
        else:                   # parent invalid, assume root node
            logUICall.log('parent is not valid ', logUICall.DEBUG_L2)
            try:
                parentItem = parent.internalPointer()
                logUICall.log('parentItem is %s' % (parentItem), logUICall.DEBUG_L2)
            except:
                pass            
            parentItem = self.root_node
        return self.createIndex(row, column, parentItem.children[row])
    
    def parent(self, index):
        """ (override function) find parent for given node """        
        logUICall.log("parent %s" % (index), logUICall.DEBUG_L2)
        if index is None: # invalid node, no parent
            return QModelIndex()        
        if not index.isValid(): # invalid node, no parent
            return QModelIndex()
        
        # find parent of given node
        childItem = index.internalPointer()
        if childItem is None or childItem.parent is None:
            # root node, no parent
            return QModelIndex()
        else:
            row_idx = childItem.parent.children.index(childItem)
            return self.createIndex(row_idx, 0, childItem.parent)
            
    def flags(self, index):
        """ (override function) visualization option flags """
        if not index.isValid():  
            return Qt.NoItemFlags
        return Qt.ItemIsEnabled | Qt.ItemIsSelectable | Qt.ItemIsUserCheckable
    
    def headerData(self, section, orientation, role):
        """ (override function) retrieve only column heading for display """
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:  
            return QVariant('')
        return None
        
    def updateGroup(self, grp):
        child_count = len(grp.children)
        checked_count = 0
        for attr in grp.children:
            if attr.checked == Qt.Checked:
                checked_count += 1
        if checked_count == 0:
            grp.checked = Qt.Unchecked
        elif checked_count == child_count:
            grp.checked = Qt.Checked
        else:
            grp.checked = Qt.PartiallyChecked
    
    def moveUp(self, index):
        item = index.internalPointer()
        if item.level != 1:    # can only change group order
            return False
        groups = self.root_node.children
        try:
            cur_idx = groups.index(item)
        except:
            cur_idx = 0
        new_idx = cur_idx - 1 
        if new_idx < 0:
            return False
        parent = self.parent(index)
        self.beginMoveRows(parent, cur_idx, cur_idx, parent, new_idx)
        groups.remove(item)
        groups.insert(new_idx, item)
        self.endMoveRows()     
        return True
    
    def moveDown(self, index):
        item = index.internalPointer()
        if item.level != 1:    # can only change group order
            return False
        groups = self.root_node.children
        try:
            cur_idx = groups.index(item)
        except:
            cur_idx = len(groups)
        new_idx = cur_idx + 1
        if new_idx >= len(groups):
            return False
        parent = self.parent(index)
        self.beginMoveRows(parent, cur_idx, cur_idx, parent, 
                           new_idx+1)   # + 1 required because it is not the intended position
                                        # but the position to which item is inserted before
                                        # see Qt.AbstractItemModel doc for beginMoveRows                                                                                 
        groups.remove(item)
        groups.insert(new_idx, item)
        self.endMoveRows()
        return True
    
    def moveTop(self, index):
        item = index.internalPointer()
        if item.level != 1:    # can only change group order
            return False
        groups = self.root_node.children
        try:
            cur_idx = groups.index(item)
            parent = self.parent(index)
            self.beginMoveRows(parent, cur_idx, cur_idx, parent, 0)
            groups.remove(item)
            groups.insert(0, item)
            self.endMoveRows()
            return True
        except:
            return False        

    def moveBottom(self, index):
        item = index.internalPointer()
        if item.level != 1:    # can only change group order
            return False
        groups = self.root_node.children
        try:
            cur_idx = groups.index(item)
            parent = self.parent(index)
            self.beginMoveRows(parent, cur_idx, cur_idx, parent, len(groups))
            groups.remove(item)
            groups.append(item)
            self.endMoveRows()
            return True    
        except:
            return False
    