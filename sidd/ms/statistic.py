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
Module class for statistic tree handling
"""
import copy
from xml.etree import ElementTree
from random import random 

from utils.enum import Enum

from sidd.constants import logAPICall, ExtrapolateOptions
from sidd.taxonomy import TaxonomyParseError
from sidd.ms.exceptions import StatisticError
from sidd.ms.node import StatisticNode

class Statistics (object):
    """
    stores regional statistic of structural characteristics
    statistic are stored in tree format
    """
    
    # default values for each level. used for comparison
    defaults = []
    # determine weather a level of taxonomy should be skipped during evaluation
    skips = []
    
    @logAPICall
    def __init__(self, taxonomy):
        """
        initialize empty statistic using given format file
        format file indicates the order of characteristics in the tree
        """
        self.root = StatisticNode(None, 'root', 'root')
        self.attributes = []
        self.leaves = []
        self.taxonomy = taxonomy
        self.skips.append(False)
        self.finalized = False
        
        for attr in self.taxonomy.attributes:
            self.defaults.append(attr.default)
            self.skips.append(False)
        StatisticNode.set_separator(taxonomy.level_separator)
        StatisticNode.set_defaults(self.defaults)

    @logAPICall
    def __str__(self):
        """ return string representation of the underlying tree  """        
        return str(self.root)
    
    @logAPICall
    def set_attribute_skip(self, level, skip):
        """ change skip condition for given level """        
        if level > len(self.skips):
            raise StatisticError("index exceeds number of attributes")
        self.skips[level] = skip

    @logAPICall
    def has_node(self, node):
        return self.root.has_child_node(node)

    @logAPICall
    def add_case(self, taxstr, parse_order=None, parse_modifiers=True, additional_data={}):
        """
        add new case of the strutural type (taxstr) to the distribution tree
        """
        # assert valid condition
        if self.finalized:
            raise StatisticError('stat is already finalized and cannot be modified')
        
        if parse_order is None:
            parse_order = [x.name for x in self.taxonomy.attributes]

        bldg_attrs = self.taxonomy.parse(taxstr)
        self.root.add(bldg_attrs, 0, parse_order, self.taxonomy.defaults, parse_modifiers, additional_data)

    @logAPICall
    def finalize(self):
        """
        collapse the statistic tree and create weights
        required step before sampling and modification can be performed
        """
        if self.finalized:
            return
        
        new_root = StatisticNode(None, 'root')
        self.root.collapse_tree(new_root)
        new_root.calculate_weights()
        self.root = new_root
        self.attributes = self.get_attributes(self.root)
        
        defaults = []
        for skip, default in map(None, self.skips, self.defaults):            
            if not skip:
                defaults.append(default)
        self.defaults_collapsed = defaults
        self.finalized = True        

    @logAPICall
    def refresh_leaves(self, with_modifier=True, order_attributes=False, fill_missing=True):         
        self.leaves = []
        for _child in self.root.children:
            for _val, _wt, _node in _child.leaves(self.taxonomy.attribute_separator, with_modifier):                    
                self.leaves.append([_val, _wt, _node])
        
        if order_attributes:
            def _sort_key(val):
                return val.attribute.order            
            try:
                #_default_order = [a.name for a in self.taxonomy.attributes]
                _separator = str(self.taxonomy.separator(self.taxonomy.Separators.Attribute))
                _ordered_leaves = []                        
                for _val, _wt, _node in self.leaves:
                    _attr_vals = self.taxonomy.parse(_val)                        
                    if fill_missing:
                        # must deep copy defaults, slow
                        _ordered_vals = copy.deepcopy(self.taxonomy.defaults)
                        _order_index = -1
                        for _attr_val in _attr_vals:
                            for idx, _default in enumerate(_ordered_vals):
                                if _attr_val.attribute.name == _default.attribute.name:
                                    _order_index = idx
                                    break
                            #assignment done here, because for loop uses iterator (inmutable in theory)                    
                            _ordered_vals[_order_index] = _attr_val
                        _val = _separator.join([str(v) for v in _ordered_vals])                        
                    else:
                        # this method is much quicker
                        _attr_vals = self.taxonomy.parse(_val)
                        _attr_vals.sort(key=_sort_key)
                        _val = _separator.join([str(v) for v in _attr_vals])
                    
                    _ordered_leaves.append([_val, _wt, _node])
                        
                self.leaves = _ordered_leaves                
            except Exception, err:
                import traceback
                traceback.print_exc()
        return self.leaves
    
    @logAPICall
    def find_node(self, values):
        """
        find a node following the path of given values
        return node if found, None otherwise
        """
        if len(values) == 0:
            return None
        node = self.root
        for value in values:
            for child in node.children:
                if value == child.value:
                    node = child
                    break        
        if node == self.root:
            return None
        return node
    
    @logAPICall
    def delete_node(self, node):
        """
        delete given node, distribute its weight to sibling nodes equally
        throws exception if node is only child
        """
        # assert valid condition
        if not self.finalized:
            raise StatisticError('stat must be finalized before modification')
        parent = node.parent
        parent.delete_node(node)
    
    @logAPICall
    def add_branch(self, node, branch, not_allow_repeat=True, update_stats=True):
        """
        add branch to node as child
        only limitation is that the same attribute does not appear
        multiple times along the path from top to bottom
        """
        # assert valid condition
        if not self.finalized:
            raise StatisticError('stat must be finalized before modification')
        
        if not_allow_repeat:
            #attributes = self.get_attributes(branch)
            # make sure attributes above node does not have the attribute
            # already defined
            existing_attributes = node.ancestor_names
            existing_attributes.append(node.name)
            attributes_to_insert = branch.descendant_names
            attributes_to_insert.insert(0, branch.name)
                        
            for attr in attributes_to_insert:
                try:
                    existing_attributes.index(attr)
                    # if attr already in attribute list, it means repeat
                    # which in this case is an error
                    raise StatisticError('Cannot perform append to node, Repeating attributes\nexisting attributes %s\nnew attributes %s' % (existing_attributes, attributes_to_insert))
                except ValueError:
                    # error means attr not in attributes
                    # which is the acceptable condition
                    pass
        
        # no exception means no repeating attributes or repeating not checked
        # add branch to node as child
        
        # clone branch
        branch_to_add = branch.clone
        branch_to_add.set_level_recursive(node.level+1)
        branch_to_add.parent = node
        node.children.append(branch_to_add)
        # adjust weights proportionally
        if update_stats:
            sum_weights = sum([child.weight for child in node.children])
            total_children = len(node.children)                
            adj_factor = sum_weights / 100
            for child in node.children:
                if adj_factor == 0:
                    child.weight = 100.0 / total_children
                else:
                    child.weight = child.weight / adj_factor
    
    @logAPICall
    def delete_branch(self, node):
        """
        recursively delete node and all its children
        redistribute its weight amongst its siblings
        """
        # assert valid condition
        if not self.finalized:
            raise StatisticError('stat must be finalized before modification')
        
        parent = node.parent
        parent.children.remove(node)
        children_count = len(parent.children)
        if  children_count > 1:
            weight_to_distribute = node.weight / float(children_count)
            for child in parent.children:
                child.weight += weight_to_distribute
    
    @logAPICall
    def get_attributes(self, rootnode):
        """ get name of all attributes in the tree"""
        return rootnode.descendant_names
        """
        names = []
        node = rootnode
        found_leaf = False
        while not found_leaf:
            if (node.level > 0):
                attr_values = self.taxonomy.parse(node.value)                
                for attr_val, attr in map(None, attr_values, self.taxonomy.attributes):                    
                    if not attr_val.is_empty:
                        names.append(attr.name)
                        break                        
            if node.is_leaf:
                found_leaf=True
            else:
                node = node.children[0]
        return names
        """
    
    @logAPICall
    def set_child_weights(self, node, weights):
        """
        change the weight for a node in the tree.        
        """
        # assert valid condition
        if not self.finalized:
            raise StatisticError('stat must be finalized before modification')
        # TODO assert node is in tree        
        node.set_child_weights(weights)
    
    @logAPICall
    def get_samples(self, total, method):
        """
        create n samples using statistic tree
        pre-condition: finalize() must be called first
        """
        samples = {}
        _sample = ''
        
        if len(self.leaves)==0:
            self.refresh_leaves(with_modifier=True, order_attributes=True)
        
        if method == ExtrapolateOptions.Fraction or method == ExtrapolateOptions.FractionRounded:            
            # multiple weights, size and replacement cost
            for _val, _wt, _node in self.leaves:
                t_count = _wt * total
                if method == ExtrapolateOptions.FractionRounded:
                    t_count = round(t_count)
                _size = _node.get_additional_float(StatisticNode.AverageSize)
                _cost = _node.get_additional_float(StatisticNode.UnitCost)
                samples[_val] = (_val, t_count, t_count*_size, t_count*_size*_cost)
        else: 
            # method=ExtrapolateOptions.RandomWalk
            def get_leaf(leaves, thresh):                                
                for _val, _wt, _node in leaves:
                    if _wt < thresh:
                        thresh -= _wt
                    else:
                        return _val, _node
                return _val, _node
            
            for i in range(total):
                _val, _node = get_leaf(self.leaves, random())
                _size = _node.get_additional_float(StatisticNode.AverageSize)
                _cost = _node.get_additional_float(StatisticNode.UnitCost)   
                if samples.has_key(_val):
                    t_val, t_count, t_size, t_cost = samples[_val]
                    samples[_val] = (_val, t_count+1, t_size+_size, t_cost+t_size+_cost)
                else:
                    samples[_val]=(_val, _size, _size, _size+_cost)
        return samples.values()
    
    @logAPICall
    def get_tree(self):
        """ get underlying tree """
        return self.root

    @logAPICall
    def get_modifiers(self, max_level):
        """ get list of modifiers up to max_level """
        for node, idx, mod in self.root.get_modifiers(max_level):            
            yield node, idx, mod

    @logAPICall
    def get_depth(self):
        """ get depth for underlying tree """
        return self.root.max_level()

    @logAPICall
    def to_xml(self, pretty=False):
        """
        serialize underlying statistic tree into XML.
        this representation is recommended to use for storing tree to file 
        """
        return self.root.to_xml(pretty)
    
    @logAPICall
    def from_xml(self, xmlnode):
        """ construct statistic tree from given XML document """
        # perform checking on the node
        if not isinstance(xmlnode, ElementTree._ElementInterface):
            raise StatisticError('input must be of type xml.etree.ElementTree.Element'); 
        
        # clean existing stats
        del self.root
        
        # create new stats tree
        self.root = StatisticNode(None, 'root')
        self.root.from_xml(xmlnode)
    
    @logAPICall
    def from_xml_str(self, xmlstr):
        """ construct statistic tree from given XML string """
        if not isinstance(xmlstr, str):
            raise StatisticError('input must be string')
        self.from_xml(ElementTree.fromstring(xmlstr))

