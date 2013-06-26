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

    # separator character for each level
    separator = "_"
    # default values for each level. used for comparison
    defaults = []
    
    @staticmethod
    def set_separator(separator):
        """ set separator character for each level """
        StatisticNode.separator = separator
    
    @staticmethod
    def set_defaults(defaults):
        """ set default values for each level """
        StatisticNode.defaults = defaults
        
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
    def max_level(self):
        """ get max level under current node """
        if self.is_leaf:
            return self.level
        else:
            return self.children[0].max_depth()
    
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
            names = self.children[0].descendant_names
            names.insert(0, self.children[0].name)
            return names
        
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
    def leaves(self, separator, with_modifier=True, parent="", parent_weight = 1.0):
        branches = {'':1.0}
        # modifier values attach to the node's value using mod_separator symbol. 
        # but if the modifier is for a different attribute than the node
        # separator symbol is used instead.
        # NOTE: modifier of different attribute) can happend after collapsed  
        #       if multiple modifier exist, they are always for different attributes, 
        #       and concatenated using given separator
        #       if multiple modifier and modifier for same attribute exists, it is always
        #       the first modifier
        mod_is_same_attribute = False
        # generate modifier branch if requested
        if with_modifier:
            for mod in self.modifiers:
                # we found same modifier
                if self.name==mod.name:
                    mod_is_same_attribute = True
                # each modifier value will generate convolution with branch X modifiers.values
                _branches = {}
                for _mod_val, _mod_weight in mod.iteritems():   # loop through modifiers.values
                    _mod_weight /= 100.0
                    for branch, value in branches.iteritems():  # loop through existing branches
                        # case that can occur are
                        # 1. modifier value is not None 
                        #    1.1 for first modifier, add new branch with modifier values
                        #    1.2 for next modifiers, append modifier value
                        # 2. modifier value is not None
                        #    No new branch is created in this case. the weight of the branch is 
                        #    updated with modifier value  
                        if ( _mod_val is not None ):
                            if branch != "":    # case 1.1                   
                                _branches[branch + separator + _mod_val] = value * _mod_weight
                            else:               # case 1.2
                                _branches[_mod_val] = value * _mod_weight
                        else:                   # case 2
                            _branches[branch] = value * _mod_weight
                branches = _branches
                
        for _val, _weight in branches.iteritems():
            # update leaf value using the following 
            # - parent: the taxonomy string generated by its parent node
            #           separator is needed if parent is not null
            # - self.value: node's own taxonomy value
            # - _val: generated from node's modifiers
            #         mod_separator needed if 
            if parent != "":
                leaf_value = parent + separator  
            else:
                leaf_value = "" 
            leaf_value += self.value 
            # 
            if _val != "":
                # modifiers for same attribute are attached (see description of mod_is_same_attribute)
                if not with_modifier:
                    mod_separator = ""
                elif (mod_is_same_attribute):
                    mod_separator = self.separator
                else:
                    mod_separator = separator
                leaf_value += mod_separator + _val

            if (self.is_leaf):
                yield leaf_value, parent_weight * self.weight / 100.0 * _weight, self
            
            for _child in self.children:
                #print '\t','child leaf', _child.value                
                for _l in _child.leaves(separator, with_modifier, leaf_value, parent_weight * self.weight / 100.0 * _weight):
                    yield _l
                       
    @logAPICall
    def random_walk(self, separator, parent="", skip_modifiers=False):                
        """
        generate string by randomly sampling among node's children and modifiers
        """
        val = ""
        mod_val = ''
        
        if not skip_modifiers:
            # use modifiers
            for mod in self.modifiers:
                # use a random number _idx to pick a modifier 
                # NOTE: modifier(dictionary) key contains the actual value,
                #       modifier(dictionary) value contains count 
                # if count exceeds _idx, then use key
                idx = random.random() * 100.0
                
                # modifiers for same attribute are attached 
                # using a different separator as modifier of different attribute
                # NOTE: (modifier of different attribute) can happend after collapsed  
                if (self.name==mod.name):
                    mod_separator = self.separator
                else:
                    mod_separator = separator
                    
                for d, c in mod.iteritems():
                    if c < idx:
                        # go to next 
                        idx -= c
                        continue
                    # found
                    if ( d is not None):
                        mod_val += mod_separator + d
                    break
            
        # do not use modifiers
        if self.level > 0 and not self.is_default:
            val += self.value  + mod_val + separator 
        
        # reached leaf, return result string
        if self.is_leaf:
            return parent + val
        
        # pick random child and append additional values
        rand_weight = random.random() * 100.0
        for child in self.children:
            # skip if _idx < _children count 
            #if child.count < idx:
            if child.weight <= rand_weight:
                rand_weight -= child.weight
                continue
            return child.random_walk(separator, parent+val, skip_modifiers)


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

    # tree modifying methods
    ###########################
    @logAPICall
    def add(self, attr_vals, level, parse_order, default_attributes, parse_modifiers=True, additional_data={}):
        """ 
        recursively update statistic @ node and @ child nodes
        using attr_val, defaults, skips at idx
        """

        # get attribute value
        def _get_attr(attribute_name, values, default_attributes):
            _attrib = None
            # find appropriate value in attr_val
            for _attr in values:
                if _attr.attribute.name == attribute_name:
                    _attrib = _attr
                    break
            # if not found, then get default
            if _attrib is None:
                for _attr in default_attributes:
                    if _attr.attribute.name == attribute_name:
                        _attrib = _attr
                        break
            return _attrib

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
        attr_val = _get_attr(attr_name, attr_vals, default_attributes)
        modifiers = None
        is_default = str(attr_val) == attr_val.attribute.default

        # normal case
        if isinstance(attr_val, TaxonomyAttributeMulticodeValue):
            # multiple codes for same attribute 
            # - node determined by first code value
            # - all other code values aggregated as modifier
            if parse_modifiers:
                value = attr_val.codes[0]
                if len(attr_val.codes)>1:
                    modifiers = self.separator.join(sorted( attr_val.codes[1:] ))
            else:
                value = str(attr_val)
        elif isinstance(attr_val, TaxonomyAttributePairValue):
            # code/value pair for attribute 
            # - node determined by code value
            # - no modifier
            value = str(attr_val)
        elif isinstance(attr_val, TaxonomyAttributeSinglecodeValue):
            # single code attribute 
            # - node determined by code value
            # - no modifier
            value = str(attr_val.code)        
        logAPICall.log('\tnode:%s, modifier:%s' %(value, modifiers), logAPICall.DEBUG_L2)
        
        child_found = False
        # find children and add value/modifier
        for child in self.children:
            if (child.value == value):
                logAPICall.log('found child with %s' % value, logAPICall.DEBUG_L2)
                child_found = True                
                child.add_modifier(modifiers)
                
                # recursive call to process next level
                child.add(attr_vals, level+1, parse_order, default_attributes, parse_modifiers, additional_data)
                return 

        # if no children found, then add new node for value and add modifier
        if not child_found:
            logAPICall.log('create new child with %s' % value, logAPICall.DEBUG_L2)
            child = StatisticNode(self, attr_name, value, self.level+1, is_default, False)
            self.children.append(child)
            child.add_modifier(modifiers)

            # recursive call to process next level
            child.add(attr_vals, level+1, parse_order, default_attributes, parse_modifiers, additional_data)
        return
    
    @logAPICall
    def collapse_tree(self, parent, level=0):
        """
        construct a new tree under parent node by traversing
        current tree and eliminating all levels marked to be 
        skipped during add
        """
        if (level==0):
            node = parent
            node.count = self.count
            level = 1
        elif self.is_skipped:
            node = parent
        else:
            node = StatisticNode(parent, self.name, self.value, level,
                                 self.is_default, self.is_skipped)            
            node.count = self.count
            parent.children.append(node)
            level+=1
        
        # remove modifiers with only None values
        mod_to_remove = []
        for mod in self.modifiers:
            if mod.is_default:                
                mod_to_remove.append(mod)
        for mod in mod_to_remove:
            self.modifiers.remove(mod)

        if len(self.modifiers)>0:
            #print '\tadded modifiers'
            node.modifiers.append(self.modifiers[0])
        
        if self.is_leaf:
            node.additional = self.additional
            return
        else:
            self.children.sort(key=attrgetter('value'))
            for child in self.children:                
                child.collapse_tree(node, level)

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
    def has_child_node(self, node):
        if self == node:
            return True
        if self.is_leaf:
            return False
        for child in self.children:
            if (child.has_child_node(node)):
                return True
        return False       
    
    @logAPICall
    def update_children(self, attribute, values, weights):
        """ update children based on given values/weights """
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