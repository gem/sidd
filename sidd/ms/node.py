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
Module class for statistic node handling
"""

import random
from copy import deepcopy
from operator import attrgetter

from utils.xml import get_node_attrib
from sidd.constants import logAPICall
from sidd.taxonomy import (TaxonomyAttributeMulticodeValue,
                           TaxonomyAttributePairValue,
                           TaxonomyAttributeSinglecodeValue)

from sidd.ms.exceptions import StatisticNodeError 

class StatisticModifier(object):
    def __init__(self, name='', level=None):
        self.name = name
        self.level = level
        self.values = {}
    
    @property
    def is_default(self):
        return len(self.values) == 1 and self.values.keys()[0] is None 
    
    def iteritems(self):
        return self.values.iteritems()

    def keys(self):
        return self.values.keys()
    
    def value(self, key):
        if self.values.has_key(key):
            return self.values[key]
        else:
            return ''
    
    def calculate_weights(self, count):
        for k, v in self.values.iteritems():
            self.values[k] = v * 100.0 / count 
    
    def update(self, key):
        if not self.values.has_key(key):
            self.values[key]=1
        else:
            self.values[key]+= 1
                
    def __str__(self):
        outstr=[]
        outstr.append('(name: "%s" ' % self.name)
        for k, v in self.values.iteritems():
            outstr.append("%s: %2.1f%%  " % (k, v))
        outstr.append(')')
        # return joined string 
        return ''.join(outstr)

    @logAPICall
    def to_xml(self, pretty=False):
        """ generate XML representation of current node """
        outstr = []
        pad = ''
        line_break=''

        outstr.append('%s  <modifier name="%s" level="%s">%s' % (pad, self.name, self.level, line_break))
        for k, v in self.values.iteritems():
            outstr.append('%s    <modifiervalue value="%s" weight="%s" />%s'
                          % (pad, k, v, line_break))
        outstr.append('%s  </modifier>%s' % (pad, line_break))
        # return joined string 
        return ''.join(outstr)
    
    @logAPICall
    def from_xml(self, xmlnode):
        self.name = get_node_attrib(xmlnode, 'name')
        self.level = get_node_attrib(xmlnode, 'level')
        for mod_node in xmlnode.findall('modifiervalue'):
            if mod_node.attrib['value'] == 'None':
                val = None
            else:
                val = get_node_attrib(mod_node, 'value')            
            self.values[val]=float(get_node_attrib(mod_node, 'weight'))                 

class StatisticNode (object):
    """
    A statistic node forms part of a statistic tree.
    Each node stores structural as well as tree related information
    
    structural related information    
    -value: taxonomy value representing a structural type
    -count: count of values included
    -weight: count of current node as percentage
            of count of parent
    -modifiers: these are less important features on the strutural type
           this is used mainly to reduce the size of the statistical tree

    tree related information
    -level: level of node in a statistic tree
    -children: collection of child StatisticNode       
    """

    # static members
    ###########################
    # additional values to be attached to the node
    AverageSize, UnitCost = range(2)

    # constructor / destructor
    ###########################
    
    def __init__(self, parent, name='', value='', level=0,
                 is_default=False, is_skipped=False):
        """ constructor """
        self.parent=parent
        self.name=name
        self.value=value
        self.additional = {}
        self.label_additional = ["avg_size", "unit_cost"]
        self.is_skipped=is_skipped
        self.is_default=is_default        
        self.count=0
        self.weight=0.0
        self.modifiers=[]                
        self.level=level
        self.children=[]
    
    def __del__(self):
        """ destructor """
        del self.parent
        del self.name
        del self.value
        del self.is_default
        del self.count
        del self.modifiers
        del self.level
        for _child in self.children:
            del _child
    
    # property methods
    ###########################
    
    @property
    def is_leaf(self):
        """ is leaf if does not have children """
        return len(self.children) == 0

    @property
    def is_valid(self):
        return sum([c.weight for c in self.children]) == 100                    

    @property
    def max_level(self):
        """ get max level under current node """
        level = self.level
        for _child in self.children: 
            if _child.max_level > level:
                level = _child.level
        return level
    
    @property
    def clone(self):
        """ get a cloned copy of the node and all its children """
        return deepcopy(self)

    @property
    def ancestor_names(self):
        if self.parent is not None:
            names = self.parent.ancestor_names            
            names.append(self.parent.name)
            return names
        else:
            return []
    
    @property 
    def descendant_names(self):
        if self.is_leaf:
            return []
        else:
            names = {}            
            for child in self.children:
                names[child.name] = 1
                for name in child.descendant_names:
                    names[name] = 1
            return names.keys()
        
    # serialize / deserialize 
    ###########################

    def __str__(self):
        """
        get string representation of node.
        it works by recursively retrieving string from its children nodes
        """
        # use list to hold strings for each line and concatenate at the end of
        # the function to avoid creating throw-away strings objects
        outstr = []
        
        # add space to make it pretty
        outstr.append('  ' * self.level)
        # add current node
        outstr.append('%s:[%s=%s (%s, %s, %2.1f%% - %d)]'
                      % (self.level, self.name, self.value, self.is_default,
                         self.is_skipped, self.weight, self.count))
        # add modifiers for current node
        for mod in self.modifiers:           
            outstr.append(str(mod))
        
        # show additional data in leaf node
        if self.is_leaf:            
            outstr.append(str(self.additional))
        
        outstr.append('\n')
        # add children
        for child in self.children:
            outstr.append(str(child))
            
        # return joined string 
        return ''.join(outstr)    

    @logAPICall
    def to_xml(self, pretty=False):
        """ generate XML representation of current node """
        outstr = []
        pad = ''
        line_break=''
        if (pretty):            
            for i in range(self.level):
                pad += '  '
            line_break='\n'
        outstr.append('%s<node attribute="%s" value="%s" level="%d" is_default="%s" is_skipped="%s" weight="%f">%s'
                      % (pad, self.name, self.value, self.level, self.is_default,
                         self.is_skipped, self.weight, line_break))
        for key,value in self.additional.iteritems():
            outstr.append('%s  <additional %s="%s" />' % (pad, self.label_additional[key], value))
        outstr.append('%s  <modifiers>%s' % (pad, line_break))
        for mod in self.modifiers:
            outstr.append(mod.to_xml(pretty))
        outstr.append('%s  </modifiers>%s' % (pad, line_break))                

        if not self.is_leaf:
            outstr.append('%s  <children>%s' % (pad, line_break))
            for child in self.children:
                outstr.append(child.to_xml(pretty))
            outstr.append('%s  </children>%s' % (pad, line_break))
        outstr.append('%s  </node>%s' % (pad, line_break))
        return ''.join(outstr)
    
    @logAPICall
    def from_xml(self, xmlnode):
        """ construct node and children from XML """  
        self.name = get_node_attrib(xmlnode, 'attribute')      
        self.value = get_node_attrib(xmlnode, 'value')
        self.level = int(get_node_attrib(xmlnode, 'level'))
        self.weight = float(get_node_attrib(xmlnode, 'weight'))
        self.count = self.weight
        self.is_default = str(get_node_attrib(xmlnode, 'is_default')).upper()=='TRUE'
        self.is_skipped = str(get_node_attrib(xmlnode, 'is_skipped')).upper()=='TRUE'
        
        for add_node in xmlnode.findall('additional'):
            for idx, label in enumerate(self.label_additional):
                add_value = get_node_attrib(add_node, label)
                if add_value != '':
                    self.additional[idx]=add_value
        
        for mod_node in xmlnode.findall('modifiers/modifier'):
            mod = StatisticModifier()
            mod.from_xml(mod_node)
            self.modifiers.append(mod)
            
        for childnode in xmlnode.findall('children/node'):
            logAPICall.log('created new child with xmlnode %s' % childnode, logAPICall.DEBUG_L2)
            node = StatisticNode(self)
            node.from_xml(childnode)
            self.children.append(node)

    # readonly methods
    ###########################
    @logAPICall
    def leaves(self, taxonomy, 
               with_modifier=True, order_attributes=False,
               parent_nodes=None, parent_weight = 1.0):
        if parent_nodes is None:
            parent_nodes = []
        branch_nodes = {"":[]}
        branch_weights = {"":1.0}
        # generate modifier branch if requested
        if with_modifier:
            for mod in self.modifiers:
                # each modifier value will generate convolution with branch X modifiers.values
                _branch_nodes = {}
                _branch_weights = {}
                for _mod_val, _mod_weight in mod.iteritems():   # loop through modifiers.values
                    _mod_weight /= 100.0
                    for branch, value in branch_nodes.iteritems():  # loop through existing branches
                        branch_weight = branch_weights[branch]
                        # case that can occur are
                        # 1. modifier value is not None 
                        #    append modifier value and update weight
                        # 2. modifier value is None
                        #    No new branch is created in this case. the weight of the branch is 
                        #    updated with modifier value  
                        if ( _mod_val is not None ):    # case 1
                            if branch != "":    # case 1.1
                                _branch_key = branch + "|"+ _mod_val
                                _branch_nodes[_branch_key] = []
                                _branch_nodes[_branch_key].append(_mod_val)
                                _branch_weights[_branch_key] = branch_weight * _mod_weight                                
                            else:               # case 1.2                                                            
                                _branch_nodes[_mod_val] = []
                                _branch_nodes[_mod_val].append(_mod_val)
                                _branch_weights[_mod_val] = branch_weight * _mod_weight
                            
                        else:                           # case 2                            
                            _branch_weights[branch] = branch_weight * _mod_weight
                branch_nodes = _branch_nodes
                branch_weights = _branch_weights

        for _branch_key, _nodes in branch_nodes.iteritems():
            # root node (level=0) does not have taxonomy value attached
            # but could still have modifier attached
            added = 0
            if self.level > 0:  
                if str(self.value) != "None":  
                    parent_nodes.append(self.value)
                    added +=1
            # modifier values        
            for _node in _nodes:
                parent_nodes.append(_node)
                added +=1

            _weight = branch_weights[_branch_key]
            if (self.is_leaf):
                leaf_value = taxonomy.to_string(parent_nodes, order_attributes)
                yield leaf_value, parent_weight * self.weight / 100.0 * _weight, self
            
            for _child in self.children:
                #print '\t','child leaf', _child.value                
                for _l in _child.leaves(taxonomy, with_modifier, order_attributes,  
                                        parent_nodes, parent_weight * self.weight / 100.0 * _weight):
                    yield _l

            # remove nodes
            for i in range(added):
                parent_nodes.pop()             

    # weight related methods
    ###########################

    @logAPICall
    def set_child_weights(self, weights):
        """
        set weights for all children nodes
        throws exception
            if weights do not addup to 100
            if number of children does not equal to number of weights
        """     
        # assert valid condition
        if sum(weights) != 100:
            raise StatisticNodeError('weight must added up to 100')
        if len(weights) != len(self.children):
            raise StatisticNodeError('number of weights does not equal number of children')

        # set weight
        for child, w in map(None, self.children, weights):
            child.weight = w
    
    @logAPICall
    def calculate_weights(self):
        """
        convert count into percentage relative to sum of count for all siblings
        """
        # calculate weight for children based on count        
        if self.parent is not None:            
            if (self.parent.count != 0):
                self.weight = self.count * 100.0 / self.parent.count
            else:
                self.weight = 0
        else:
            self.weight = 100
        
        # calculate weight for attached modifiers based on count
        for mod in self.modifiers:            
            mod.calculate_weights(self.count)
        
        if self.is_leaf:
            # update additional values
            _total_size = self.count    # set to default for unitCost calculation
            if self.additional.has_key(self.AverageSize):
                # _size is total             
                _total_size = self.additional[self.AverageSize]
                self.additional[self.AverageSize] = float(_total_size) / self.count
            if self.additional.has_key(self.UnitCost):
                # _total_size defaults to 0, 
                # so should not break even if AverageSize is not set 
                self.additional[self.UnitCost] /= _total_size
        
        # recursively travese down to all children
        # will be skipped by leaf nodes
        for child in self.children:
            child.calculate_weights()

    @logAPICall
    def balance_weights(self):
        """
        adjust its weights to make sure it adds up to 100%
        """
        sum_weights = sum([child.weight for child in self.children])            
        total_children = len(self.children)        
        adj_factor = sum_weights / 100
        for child in self.children:
            if adj_factor == 0:
                child.weight = 100.0 / total_children
            else:
                child.weight = child.weight / adj_factor        

    # tree modifying methods
    ###########################
    @logAPICall
    def add(self, attr_vals, parse_order, level, additional_data={}):
        """ 
        recursively update statistic @ node and @ child nodes
        using attr_val, defaults, skips at idx
        """
        # increment count of current node
        self.count+=1
        
        # the ending condition for the recursive call
        # NOTE: is_leaf is not used here, this process should work on a empty tree
        if (len(parse_order) <= level):
            # leaf node also aggregate additional data
            self.increment_additonal(self.AverageSize, additional_data)            
            self.increment_additonal(self.UnitCost, additional_data)
            return
        
        logAPICall.log('processing %d %s' %(level, parse_order[level]), logAPICall.DEBUG)

        # get value to add/update children
        # NOTE: value for current node is already set by its parent
        # all processing/parsing is to work on its children        
        attr_name = parse_order[level]
        value = None
        for val in attr_vals:
            if val.attribute.name == attr_name:
                value = val
                break

        # handle default cases
        is_default = False                
        if value is None:
            is_default = True 
        elif value is not None and (str(value) == value.attribute.default or str(value) == value.attribute.group.default):
            value = None
            is_default = True                       
        
        logAPICall.log('\tnode:%s' %(value), logAPICall.DEBUG_L2)
        
        child_found = False
        # find children and add value/modifier
        for child in self.children:
            if (child.value is None and value is None) or str(child.value) == str(value):
                logAPICall.log('found child with %s' % value, logAPICall.DEBUG_L2)
                child_found = True                
                # recursive call to process next level
                child.add(attr_vals, parse_order, level+1, additional_data)
                return 

        # if no children found, then add new node for value and add modifier
        if not child_found:
            logAPICall.log('create new child with %s' % value, logAPICall.DEBUG_L2)
            child = StatisticNode(self, attr_name, value, self.level+1, is_default, False)
            self.children.append(child)
            # recursive call to process next level
            child.add(attr_vals, parse_order, level+1, additional_data)
        return        
    
    @logAPICall
    def eliminate_empty(self):
        """
        traverse current tree and eliminating nodes with value=None and no sibling
        """
        for child in self.children:
            child.eliminate_empty()
                        
        if len(self.children) == 1:
            child = self.children[0]
            if child.value is None:
                # eliminate
                self.children = []
                for _grandchild in child.children:
                    _grandchild.parent = self
                    self.children.append(_grandchild)
                    _grandchild.set_level_recursive(self.level+1)
                del child
                
    @logAPICall
    def get_modifiers(self, max_level):
        """
        generator providing access to all modifiers from node and children nodes
        up to given max_level
        """        
        if self.level <= max_level: #and not self.is_leaf:
            # own modifiers
            for idx, mod in enumerate(self.modifiers):
                # generator return
                yield self, idx, mod
            # traverse through children nodes
            for child in self.children:
                # recursively return children's modifiers with generator 
                for node, idx, mod in child.get_modifiers(max_level):                    
                    yield node, idx, mod
        # else
        #   reached leaf or modifier from max depth level defined.
        #   return

    @logAPICall
    def delete_node(self, child):
        """
        delete given node from children list, distribute its weight to
        sibling nodes equally
        throws exception if node is only child        
        """        
        # assert valid condition
        total_children = len(self.children)
        if total_children == 1:
            raise StatisticNodeError('only child. cannot be deleted')
        
        # delete, wrap in exception to catch miss-matched children
        try:
            # remove child
            weight = child.weight
            self.children.remove(child)
            total_children -= 1            
            # evenly distribute deleted weight to sibling
            for child in self.children:
                child.weight =  child.weight + (weight / total_children)
        except:
            raise StatisticNodeError('unknown error while deleting node')

    @logAPICall
    def add_modifier(self, val, mod_idx=0):
        """ update statistic for specified modifier """
        if len(self.modifiers) <= mod_idx:
            mod = StatisticModifier(self.name, self.level)
            mod.update(val)
            self.modifiers.append(mod)
        else:            
            self.modifiers[mod_idx].update(val)

    @logAPICall
    def set_level_recursive(self, level):
        """
        recursively set level of node and all children
        this allows node to be attached at random level in tree
        NOTE: use negative value for inc to decrease level
        """
        if level <= 0:
            raise StatisticNodeError('resulting level must be > 0')
        self.level = level
        
        # adjust children 
        if not self.is_leaf:            
            for child in self.children:
                child.set_level_recursive(level + 1)

    @logAPICall
    def matches(self, node):
        """
        test to see if node matches self or any descendant
        """
        if self == node:
            return True
        if self.is_leaf:
            return False
        for child in self.children:
            if (child.matches(node)):
                return True
        return False       
    
    @logAPICall
    def update_children(self, attribute, values, weights):
        """ 
        simply update children based on given values/weights without checking
        for position of values  
        """        
        if sum(weights) <> 100:        
            raise StatisticNodeError('weight does not equal to 100')
                    
        to_add = len(values) - len(self.children)   
        if to_add > 0:
            # need to add more nodes
            for i in range(to_add):
                child = StatisticNode(self, attribute, '', self.level+1)                
                self.children.append(child)
        elif to_add < 0:
            # need to delete nodes
            _start=len(values)
            for i in range(to_add):
                self.children.remove(self.children[_start+i])
        # set value/weights
        _idx = 0
        for _val, _weight in map(None, values, weights):         
            _child = self.children[_idx]
            _child.value = _val
            _child.weight = _weight            
            _idx += 1
        
    @logAPICall
    def update_children_complex(self, attribute, values, weights):
        """ 
        update children based on given values/weights         
        """
        # check to make sure given values/weights can be used to
        # update node's children
        # check for following conditions
        # 1. weights do not add up to 100. 
        #    FAIL, cannot update 
        # 2. values not changed, only weights were updated
        #    ALLOW, update children with new weights
        # 3. new values are added  
        #    ALLOW, add new value nodes, update all weights 
        # 4. some values are deleted 
        #    ALLOW, delete child node(s), update all weights
        
        sum_weight = 0  # for case 1

        # sum up weights, 
        # check for added/deleted nodes        
        added = [] 
        to_delete = []
        for v, w in map(None, values, weights):            
            # check deleted
            if w == 0:
                to_delete.append(v)
                continue
            # update sum
            sum_weight += w
            
            # check added
            child_found = False
            for child in self.children:
                if child.value == v:    
                    child_found = True
            if not child_found:
                added.append(v)

        # find additional child nodes already deleted
        for child in self.children:
            try:
                values.index(child.value)
            except: 
                if len(added) > 0:
                    # reuse to_delete to host the to_add
                    # this is can help in case a value is changed to another one
                    # the children of the node to delete can still be preserved
                    child.value = added[0] 
                    added.remove(child.value)
                else:
                    # nothing to add, remove the children
                    to_delete.append(child.value)
        
        # case 1
        if sum_weight <> 100:
            raise StatisticNodeError('weight does not equal to 100')

        # case 3, new values added
        for v in added:
            child = StatisticNode(self, attribute, v, self.level+1)                
            self.children.append(child)            
        
        # case 4, some values are deleted
        for v in to_delete:
            for child in self.children:
                if child.value == v:
                    self.delete_node(child)
        
        # after changes to node, the resulting
        # case 2, only weight update needed
        for child in self.children:
            try:
                weight = weights[values.index(child.value)]
            except:
                weight = 0
            child.weight = weight
            child.count = weight
        
    def set_modifier(self, modidx, modifier):
        """
        set modifier to given modidx if modidx is valid,
        otherwise, add modifier as new modifier to node's list          
        """        
        if modidx >= 0 and modidx < len(self.modifiers):
            self.modifiers[modidx] = modifier
        else:
            self.modifiers.append(modifier)
        
    def update_modifier(self, values, weights, modidx=-1):
        """ 
        update node's (modidx) modifier with given values/weights list
        raise exception if modidx is not valid index.
        if no modidx is given as input, a new modifier is created and attached to 
        the node 
        """
        # check to make sure given values/weights can be used to
        # update node's modifier
        # check for following conditions
        # 1. weights do not add up to 100. 
        #    FAIL, cannot update
        # 2. modidx exceed max index of node's modifier list 
        #    FAIL, cannot update         
        # 3. modidx is negative, 
        #    ALLOW, add new modifier with given values/weight
        # 4. modidx is correct index for node's modifier list
        #    ALLOW, update new  

        # test case 1        
        if sum(weights) <> 100:
            raise StatisticNodeError('weight does not equal to 100')
        
        # test case 2
        if len(self.modifiers) <= modidx:
            raise StatisticNodeError('modifier with index %s does not exist' % modidx)

        mod = StatisticModifier("User", self.level)
        for v, w in map(None, values, weights):
            mod.values[v]=w 
        #mod = {}
        #for v, w in map(None, values, weights):
        #    mod[v]=w
        
        if modidx < 0:
            # case 3
            self.modifiers.append(mod)
        else:
            # case 4
            self.modifiers[modidx] = mod
            
    def remove_modifier(self, modidx):
        """ 
        remove node's (modidx) modifier.
        raise exception if modidx is not valid index
        """
        if modidx < 0 or len(self.modifiers) <= modidx:
            raise StatisticNodeError('modifier with index %s does not exist' % modidx)
        del self.modifiers[modidx]
    
    def increment_additonal(self, key, values):
        if values.has_key(key):
            if not self.additional.has_key(key):
                self.additional[key]=0
            self.additional[key]+= values[key]
        
    
    def set_additional(self, key, value):
        if self.is_leaf:
            self.additional[key]=value
        else:
            for child in self.children:
                child.set_additional(key, value)

    def get_additional(self, key):
        return self.additional[key] if self.additional.has_key(key) else ''
    
    def get_additional_float(self, key):
        try:
            return float(self.additional[key])
        except:
            return 0