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
# Version: $Id: node.py 18 2012-10-24 20:21:41Z zh $

"""
Module class for statistic node handling
"""

import random
from copy import deepcopy

from sidd.constants import logAPICall
from sidd.taxonomy import (TaxonomyAttributeMulticodeValue,
                           TaxonomyAttributePairValue,
                           TaxonomyAttributeSinglecodeValue)

from sidd.ms.exceptions import StatisticError, StatisticNodeError 

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
        for i in range(self.level):
            outstr.append('  ')
        # add current node        
        outstr.append('%s:[%s=%s (%s, %s, %2.1f%% - %d)]'
                      % (self.level, self.name, self.value, self.is_default,
                         self.is_skipped, self.weight, self.count))
        # add modifiers for current node
        for mod in self.modifiers:
            outstr.append('( ')
            for k, v in mod.iteritems():
                outstr.append("%s: %2.1f%%  " % (k, v))
            outstr.append(')')
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
        outstr.append('%s<node value="%s" level="%d" is_default="%s" is_skipped="%s" weight="%f">%s'
                      % (pad, self.value, self.level, self.is_default,
                         self.is_skipped, self.weight, line_break))
        outstr.append('%s  <modifiers>%s' % (pad, line_break))
        for mod in self.modifiers:
            if (len(mod.keys())>=1):
                outstr.append('%s  <modifier>%s' % (pad, line_break))
                for k, v in mod.iteritems():
                    outstr.append('%s    <modifiervalue value="%s" weight="%s" />%s'
                                  % (pad, k, v, line_break))
                outstr.append('%s  </modifier>%s' % (pad, line_break))
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
        self.value = xmlnode.attrib['value']
        self.level = int(xmlnode.attrib['level'])
        self.weight = float(xmlnode.attrib['weight'])
        self.count = self.weight
        self.is_default = str(xmlnode.attrib['is_default']).upper()=='TRUE'
        self.is_skipped = str(xmlnode.attrib['is_skipped']).upper()=='TRUE'
        
        for mod_nodes in xmlnode.findall('modifiers/modifier'):
            mod = {}
            for mod_node in mod_nodes.findall('modifiervalue'):
                if mod_node.attrib['value'] == 'None':
                    val = None
                else:
                    val = mod_node.attrib['value']            
                mod[val]=float(mod_node.attrib['weight'])
            self.modifiers.append(mod)
            
        for childnode in xmlnode.findall('children/node'):
            logAPICall.log('created new child with xmlnode %s' % childnode, logAPICall.DEBUG_L2)
            node = StatisticNode(self)
            node.from_xml(childnode)
            self.children.append(node)

    # readonly methods
    ###########################
   
    @logAPICall
    def random_walk(self, separator, parent="", skip_modifiers=False):                
        """
        generate string by randomly sampling among node's children and modifiers
        """
        val = ""
        if not skip_modifiers:
            # use modifiers
            for mod in self.modifiers:
                # use a random number _idx to pick a modifier 
                # NOTE: modifier(dictionary) key contains the actual value,
                #       modifier(dictionary) value contains count 
                # if count exceeds _idx, then use key
                idx = random.random() * self.count
                for d, c in mod.iteritems():            
                    if c < idx:
                        # go to next 
                        idx -= c
                        continue
                    # found
                    if ( d is not None):
                        # key is not None, add to tax_str
                        if not self.is_default:
                            val += self.value + self.separator + d + separator
                        else:
                            # key is default, no need to add to result string
                            val += d + separator
                            
                    elif not self.is_default:
                        # key is None, no need to add to result string
                        val += self.value + separator
                    break
        else:
            # do not use modifiers
            if self.level > 0 and not self.is_default:
                val += self.value + separator
        
        # reached leaf, return result string
        if self.is_leaf:
            return parent + val
        
        # pick random child and append additional values
        rand_weight = random.random() * 100.0
        for child in self.children:
            # skip if _idx < _children count 
            #if child.count < idx:
            if child.weight < rand_weight:
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
            for k in mod.keys():
                mod[k] = mod[k] * 100.0 / self.count 
        
        # recursively travese down to all children
        # will be skipped by leaf nodes
        for child in self.children:
            child.calculate_weights()        
    

    # tree modifying methods
    ###########################

    @logAPICall
    def add(self, attr_vals, idx, attributes, defaults, skips):
        """        
        recursively update statistic @ node and @ child nodes
        using attr_val, defaults, skips at idx
        """
        # increment count of current node
        self.count+=1
        
        # the ending condition for the recursive call
        # NOTE: is_leaf is not used here, this process should work on a empty tree
        if (len(attr_vals) <= idx):
            return
        
        logAPICall.log('processing %d %s %s' %(idx, attr_vals[idx], skips[idx]), logAPICall.DEBUG)
        
        # get value to add
        attr_name = attributes[idx]
        attr_val = attr_vals[idx]
        modifiers = None
        is_default = False        
        if attr_val.is_empty:
            # case attrbitue not set
            # - default value node's count should be incremented
            # - no modifier
            value = defaults[idx]
            is_default=True
        elif skips[idx]:
            # case attribute should be skipped
            # - default value node's count should be incremented
            # - attribute value in set as modifier
            value = defaults[idx]
            is_default = value == defaults[idx]
            if isinstance(attr_val, TaxonomyAttributeMulticodeValue):
                modifiers =  self.separator.join(sorted( attr_val.codes ))
            elif isinstance(attr_val, TaxonomyAttributePairValue):
                modifiers = str(attr_val)
        else:
            # normal case
            if isinstance(attr_val, TaxonomyAttributeMulticodeValue):
                # multiple codes for same attribute 
                # - node determeined by first code value
                # - all other code values aggregated as modifier
                value = attr_val.codes[0]
                is_default = value == defaults[idx]
                if len(attr_val.codes)>1:
                    modifiers = self.separator.join(sorted( attr_val.codes[1:] ))
            elif isinstance(attr_val, TaxonomyAttributePairValue):
                # code/value pair for attribute 
                # - node determeined by code value
                # - no modifier
                value = str(attr_val)
                is_default = value == defaults[idx]
            elif isinstance(attr_val, TaxonomyAttributeSinglecodeValue):
                # single code attribute 
                # - node determeined by code value
                # - no modifier
                value = attr_val.code
                is_default = value == defaults[idx]
        
        logAPICall.log('\tnode:%s, modifier:%s' %(value, modifiers), logAPICall.DEBUG_L2)
        
        child_found = False
        # find children and add value/modifier
        for child in self.children:
            if (child.value == value):
                logAPICall.log('found child with %s' % value, logAPICall.DEBUG_L2)
                child_found = True
                child.add_modifier(modifiers)
                
                # recursive call to process next level
                child.add(attr_vals, idx+1, attributes, defaults, skips)
                return 

        # if no children found, then add new node for value and add modifier
        if not child_found:
            logAPICall.log('create new child with %s' % value, logAPICall.DEBUG_L2)
            child = StatisticNode(self, attr_name, value, self.level+1, is_default, skips[idx])
            self.children.append(child)
            child.add_modifier(modifiers)

            # recursive call to process next level
            child.add(attr_vals, idx+1, attributes, defaults, skips)
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
            #print 'skipped', self.value
            node = parent            
        else:
            #print 'added', self.value, 
            node = StatisticNode(parent, self.name, self.value, level,
                                 self.is_default, self.is_skipped)            
            node.count = self.count
            parent.children.append(node)
            level+=1
        
        # remove modifiers with only None values
        mod_to_remove = []
        for mod in self.modifiers:
            if len(mod) == 1 and mod.keys()[0] is None:                
                mod_to_remove.append(mod)
        for mod in mod_to_remove:
            self.modifiers.remove(mod)

        if len(self.modifiers)>0:
            #print '\tadded modifiers'
            node.modifiers.append(self.modifiers[0])
        
        if self.is_leaf:
            return
        else:
            #print '\tadd %d children' % len( self.children )
            for child in self.children:                
                child.collapse_tree(node, level)

    @logAPICall
    def get_modifiers(self, max_level):
        """
        generator providing access to all modifiers from node and children nodes
        up to given max_level
        """        
        if self.level <= max_level and not self.is_leaf:
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
    def add_child(self, child, defaults):
        """
        attach default values under the child
        and add the child node to children list        
        """
        level = child.level
        parent = child
        for i in range(len(defaults)-1):
            if i < level:
                continue
            node = StatisticNode(parent, defaults[i], level+1, True, False)
            node.weight = 100
            parent.children.append(node)
            level+=1
        self.children.append(child)

    @logAPICall
    def add_modifier(self, val, mod_idx=0):
        """ update statistic for specified modifier """
        if len(self.modifiers) <= mod_idx:
            mod = {}
            mod[val]=1
            self.modifiers.append(mod)
        else:
            if not self.modifiers[mod_idx].has_key(val):
                self.modifiers[mod_idx][val]=1
            else:
                self.modifiers[mod_idx][val]+= 1

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
    def update_children(self, values, weights):
        """ update children based on given values/weights """
        # check to make sure given values/weights can be used to
        # update node's children
        # check for following conditions
        # 1. weights do not add up to 100. 
        #    FAIL, cannot update 
        # 2. some values not in children 
        #    ALLOW, add new value nodes and update new weights        
        # 3. values == children
        #    ALLOW, update children with new weights
        sum_weight = 0  # for case 1
        not_in_children = [] # for case 2/3
        child_name = ''
        
        for v, w in map(None, values, weights):
            # if node is leaf, then all values are new
            sum_weight += w
            child_found = False
            for child in self.children:
                child_name = child.name
                if child.value == v:
                    child_found = True
            if not child_found:
                not_in_children.append(v)
                
        # case 1
        if sum_weight <> 100:
            raise StatisticNodeError('weight does not equal to 100')
        
        # case 2
        if len(not_in_children) > 0:
            # add new value nodes
            for _val in not_in_children:
                child = StatisticNode(self, child_name, _val, self.level+1)                
                self.children.append(child)
            # once all values not in children are added in,  
            # case 2 becomes case 3
            
        # case 3
        for child in self.children:
            try:
                weight = weights[values.index(child.value)]
            except:
                weight = 0
            child.weight = weight
            child.count = weight
        self.count = 100

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

        mod = {}
        for v, w in map(None, values, weights):
            mod[v]=w
        
        if modidx < 0:
            # case 3
            self.modifiers.append(mod)
        else:
            # case 4
            self.modifiers[modidx] = mod
            
    def removeModifier(self, modidx):
        """ 
        remove node's (modidx) modifier.
        raise exception if modidx is not valid index
        """
        if modidx < 0 or len(self.modifiers) <= modidx:
            raise StatisticNodeError('modifier with index %s does not exist' % modidx)
        del self.modifiers[modidx]
            