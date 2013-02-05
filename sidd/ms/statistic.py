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
# Version: $Id: statistic.py 18 2012-10-24 20:21:41Z zh $

"""
Module class for statistic tree handling
"""
from xml.etree import ElementTree

from sidd.constants import logAPICall
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
    def add_case(self, taxstr):
        """
        add new case of the strutural type (taxstr) to the distribution tree
        """
        # assert valid condition
        if self.finalized:
            raise StatisticError('stat is already finalized and cannot be modified')
        
        attribute_names = [x.name for x in self.taxonomy.attributes]
        try:
            bldg_attrs = self.taxonomy.parse(taxstr)
            self.root.add(bldg_attrs, 0, attribute_names, self.defaults, self.skips)
        except Exception as err:
            logAPICall.log("error adding case %s, %s" % (str(taxstr), str(err)), logAPICall.WARNING)         

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
    def get_leaves(self, refresh=False):
        if refresh:
            self.leaves = []
            for _child in self.root.children:
                for _val, _wt in _child.leaves(self.taxonomy.attribute_separator, ""):                    
                    self.leaves.append([_val, _wt])
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
    def add_child(self, node, child):
        """
        add a child to the node
        attach default values under the child
        """
        # assert valid condition
        if not self.finalized:
            raise StatisticError('stat must be finalized before modification')
            
        node.add_child(child, self.defaults_collapsed)
    
    @logAPICall
    def add_branch(self, node, branch):
        """
        add branch to node as child
        only limitation is that the same attribute does not appear
        multiple times along the path from top to bottom
        """
        # assert valid condition
        if not self.finalized:
            raise StatisticError('stat must be finalized before modification')
        
        attributes = self.get_attributes(branch)
        # make sure attributes above node does not have the attribute
        # already defined
        for attr in self.attributes[0:node.level]:
            try:
                attributes.index(attr)
                # if attr already in attribute list, it means repeat
                # which in this case is an error
                raise StatisticError('Branche attributes %s cannot be added at node, Parent attribute [%s] already exists' % (attributes, attr))
            except ValueError:
                # error means attr not in attributes
                # which is the acceptable condition
                pass
        
        # no exception means no repeating attributes
        # add branch to node as child        
        
        # clone branch
        branch_to_add = branch.clone
        branch_to_add.set_level_recursive(node.level+1)
        branch_to_add.parent = node
        node.children.append(branch_to_add)
    
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
        names = []
        node = rootnode
        while not node.is_leaf:            
            if (node.level > 0):
                attr_values = self.taxonomy.parse(node.value)                
                for attr_val, attr in map(None, attr_values, self.taxonomy.attributes):                    
                    if not attr_val.is_empty:
                        names.append(attr.name)
                        break            
            node = node.children[0]
        return names
    
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
    def get_samples(self, n):
        """
        create n samples using statistic tree
        pre-condition: finalize() must be called first
        """
        samples = {}
        _sample = ''
        for i in range(n):
            #while _sample == '':
            _sample = self.get_sample_walk(False)
            if samples.has_key(_sample):
                samples[_sample]+=1
            else:
                samples[_sample]=1
        return samples
    
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
    def get_sample_walk(self, skip_details=True):
        """ get one sample from underlying tree """
        return self.root.random_walk(self.taxonomy.attribute_separator,
                                     "",
                                     skip_details)

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
