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
# Version: $Id: ms_tree.py 18 2012-10-24 20:21:41Z zh $

"""
tree model for visualizing mapping scheme
"""

from PyQt4.QtCore import Qt, QVariant,\
                         QAbstractItemModel, QModelIndex

from sidd.ms import MappingSchemeZone, StatisticNode

from ui.constants import logUICall, get_ui_string
from ui.helper.common import build_attribute_tooltip

class MSTreeModel(QAbstractItemModel):  
    """
    tree model for visualizing mapping scheme
    """
    def __init__(self, ms, flag=None):
        """ constructor """
        super(MSTreeModel, self).__init__(None)
        self.setMS(ms)  
        if flag is None:
            self.flag = Qt.ItemIsEnabled | Qt.ItemIsSelectable 
        else:
            self.flag = flag        
    
    def setMS(self, ms):
        self.ms = ms
        self.valid_codes = ms.taxonomy.codes
        self.rootNode = object()        
        self.zones = ms.get_zones()
        for zone in self.zones:
            #print zone, type(zone.stats.root), zone.stats.root.value
            zone.stats.get_tree().value = zone.name

    def nodeFromIndex(self, index):
        """ (override function) retrieve internal stored node from given index """
        logUICall.log("nodeFromIndx %s" %index, logUICall.DEBUG_L2)
        if index.isValid():  
            return index.internalPointer()  
        else:
            return self.rootItem
    
    def columnCount(self, parent):
        """ (override function) Mapping Scheme tree only has 1 column """
        return 1

    def rowCount(self, parent):
        """ (override function) retrieve number of children from a given parent node """
        logUICall.log("rowCount %s" % (parent), logUICall.DEBUG_L2)
        #if parent.column() > 0: # there is only one column
        #    return 0
        if not parent.isValid(): # invalid case treated same as root node
            return len(self.zones)
        
        # find children
        parentItem = parent.internalPointer()        
        if parentItem == self.rootNode:
            # root node, return number of zones
            logUICall.log("\tparent is root", logUICall.DEBUG_L2)
            return len(self.zones)
        elif isinstance(parentItem, MappingSchemeZone):
            # zone node (first level under root node)
            # get top level from statistic tree
            logUICall.log("\tparent is zone: %s" % (parentItem.name), logUICall.DEBUG_L2)
            stats = self.ms.get_assignment(parentItem)
            return len(stats.get_tree().children)
        else:
            # statistic node
            # get appropriate number of children for given node
            logUICall.log("\tparent is node: %s" % (parentItem.value), logUICall.DEBUG_L2)
            return len(parentItem.children)
    
    def data(self, index, role):
        """
        (override function) retrieve appropriate data to show in UI given a index
        currently only DisplayRole is implemented
        """
        logUICall.log("data %s" % (index), logUICall.DEBUG_L2)
        
        if not index.isValid():  # invalid case, nothing to display
            return None
        
        if role == Qt.DisplayRole:
            # construct data to show in tree UI
            item = index.internalPointer()
            if item == self.rootNode:
                # root node
                logUICall.log("\tindex is root", logUICall.DEBUG_L2)
                return 'ROOT'
            elif isinstance(item, MappingSchemeZone):
                # zone node(first level under root node)
                # statistic in each zone should be 100%
                logUICall.log("\tindex is zone %s" % (item.name), logUICall.DEBUG_L2)
                return '%s - %2.1f%%' % (item.name, 100.0)
            else:
                # statistic node 
                # show weight for node
                logUICall.log("\tindex is node %s %s" % (item.value, item.weight), logUICall.DEBUG_L2)
                return '%s - %2.1f%%' % (item.value, item.weight)
        elif role == Qt.ToolTipRole: 
            # lookup data to show in tool tip
            item = index.internalPointer()
            if isinstance(item, MappingSchemeZone):
                return "Mapping Scheme Zone - %s" % item.name
            elif isinstance(item, StatisticNode):
                return build_attribute_tooltip(self.valid_codes, item.value)
            else:
                return ""                
        else:
            return None
        
    
    def index(self, row, column, parent):
        """
        (override function) find appropriate children using row from given parent node
        this function is tightly associated with rowCount
        """
        logUICall.log("index %s %s %s" % (row, column, parent), logUICall.DEBUG_L2)
        if not parent.isValid():    # parent invalid, assume root node
            parentItem = self.rootNode
        else:                       # get parent node
            parentItem = parent.internalPointer()
        
        # find child for given parent and row
        childItem = False 
        if parentItem == self.rootNode:
            # root node
            # get zone
            logUICall.log("\tparent is root, child is zone", logUICall.DEBUG_L2)
            childItem = self.zones[row] 
        elif isinstance(parentItem, MappingSchemeZone):
            # zone node
            # get top level from zone's statistical tree            
            logUICall.log("\tparent is zone %s, child is node"%(parentItem.name), logUICall.DEBUG_L2)
            stats = self.ms.get_assignment(parentItem) 
            if row>=0 and row<len(stats.get_tree().children):           
                childItem = stats.get_tree().children[row]
        else:
            # statistic node
            # get appropriate children            
            logUICall.log("\tparent is node %s, child is node"%(parentItem.value), logUICall.DEBUG_L2)
            if row>=0 and row<len(parentItem.children):            
                childItem = parentItem.children[row]            
                
        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QModelIndex()
    
    def parent(self, index):
        """ (override function) find parent for given node """        
        logUICall.log("parent %s" % (index), logUICall.DEBUG_L2)
        if not index.isValid(): # invalid node, no parent
            return QModelIndex()
        
        # find parent of given node
        childItem = index.internalPointer()                
              
        if childItem == self.rootNode:
            # root node, no parent
            logUICall.log("\tchild is root. invalid", logUICall.DEBUG_L2)
            return QModelIndex()
        elif isinstance(childItem, MappingSchemeZone):
            # zone node, parent is root
            logUICall.log("\tchild is zone. parent is root", logUICall.DEBUG_L2)
            return self.createIndex(0, 0, self.rootNode)
            
        elif isinstance(childItem, StatisticNode):
            # statistic node
            # get node's parent from node's internal pointer
            # if parent node is top node is statistic tree 
            # then replace that zone associated with the statistic
            # (see MappingScheme definition for relationship of zone and statistic)
            parentItem = childItem.parent
            if (parentItem.level == 0):                
                # top level, get zone
                logUICall.log("\tchild is node level 1. parent is zone", logUICall.DEBUG_L2)
                for _idx, _zone in enumerate(self.zones):
                    if _zone.name == parentItem.value:
                        return self.createIndex(_idx, 0, _zone)
                return QModelIndex()
            else:
                # not top level, get node's parent
                logUICall.log("\tchild is node below level 1. parent is node", logUICall.DEBUG_L2)
                _row_idx = parentItem.parent.children.index(parentItem) 
                return self.createIndex(_row_idx, 0, parentItem)
        else:
            return QModelIndex()
    
    def flags(self, index):
        """ (override function) visualization option flags """
        if not index.isValid():  
            return Qt.NoItemFlags    
        return self.flag
    
    def headerData(self, section, orientation, role):
        """ (override function) retrieve only column heading for display """
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:  
            return QVariant(get_ui_string("widget.ms.tree.title"))
        return None

    def match(self, index, role, value, hits=1, flags=Qt.MatchStartsWith | Qt.MatchWrap):
        found = []
        if index.isValid():
            item = index.internalPointer()
            if item == self.rootNode:
                # root node
                node_value = 'ROOT'
            elif isinstance(item, MappingSchemeZone):
                # zone node(first level under root node)
                # statistic in each zone should be 100%
                node_value = item.name
            else:
                # statistic node 
                # show weight for node                
                node_value = item.value           
        else:
            node_value = 'ROOT'                
        if node_value == value:
            found.append(index)
            hits -= 1
        if hits>0:
            for i in range(self.rowCount(index)):
                child = self.index(i, 1, index)
                indices = self.match(child, role, value, hits, flags)
                if len(indices) == 0:
                    continue
                while hits > 0:
                    found.append(indices.pop())
                    hits-= 1
                if hits == 0:
                    break
        return found
            
        
        