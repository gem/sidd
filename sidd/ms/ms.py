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
# Version: $Id: ms.py 18 2012-10-24 20:21:41Z zh $

"""
Module contains all mapping scheme handling class
"""

from xml.etree.ElementTree import ElementTree, fromstring

from sidd.constants import logAPICall
from sidd.exception import SIDDException
from sidd.taxonomy import get_taxonomy
from sidd.ms.statistic import Statistics, StatisticError

class MappingSchemeZone (object):
    """
    Zone representation object used to associate structural statistics
    distribution with an area
    """
    
    def __init__(self, name):
        """ constructor """
        self.name = name
        self.stats = None
    
    # TODO additional functionalities TBD
    
class MappingScheme (object):
    """
    Class for managing mapping schemes.
    A mapping scheme consist of a collection of pairs of statistic distribution
    (ms.Statistic object) associated with a zone (ms.MappingSchemeZone object)    
    """
    
    def __init__(self, taxonomy):
        """ Constructor """
        self.ms = {}
        self.taxonomy = taxonomy
        self.zones = []
    
    def __str__(self):
        """ Returns string representation of a mapping scheme """
        outstr = []
        #for zone, ms in self.ms.iteritems():
        #    outstr.append("zone %s\n%s\n" % (zone, ms))
        for zone in self.zones:
            outstr.append("zone %s\n%s\n"%(zone.name, zone.stats))
        return ''.join(outstr)
    
    @property
    def is_valid(self):
        """ verify that the mapping scheme is valid """
        return True;
    
    @logAPICall
    def read(self, xml_file):
        """ Construct a mapping scheme from given input file """
        tree = ElementTree()
        tree.parse(xml_file)
        self.from_xml_tree(tree)

    @logAPICall
    def from_text(self, xml_str):        
        try:
            tree = fromstring(xml_str)            
        except Exception as e:
            pass
        self.from_xml_tree(tree)
    
    def from_xml_tree(self, tree):
        # check to make sure it is correct.
        # use DTD???
        tax = tree.find('taxonomy')
        self.taxonomy = get_taxonomy(tax.find('name').text)
        self.ms = {}
        for zone in tree.findall("zone"):
            stats = Statistics(self.taxonomy)
            stats.from_xml(zone.find('node'))
            stats.finalized = True
            #stats.finalize()
            stats.attributes = stats.get_attributes(stats.get_tree())            

            #self.ms[zone.attrib['name']] = stats
            ms_zone = MappingSchemeZone(zone.attrib['name'])
            ms_zone.stats = stats
            self.zones.append(ms_zone)
                      
    
    @logAPICall
    def save(self, xml_file):
        """ Store mapping scheme into given input file """
        f = open(xml_file, 'w')
        f.write(self.to_xml())
        f.close()
    
    @logAPICall
    def to_xml(self):
        outstr = (
            '<mapping_scheme><taxonomy><name>%s</name><description>%s</description><version>%s</version></taxonomy>' %
            (self.taxonomy.name, self.taxonomy.description,self.taxonomy.version))
        for zone in self.zones:
            outstr += '<zone name="%s">'%(zone.name)
            outstr += zone.stats.to_xml()
            outstr += '</zone>'
        outstr += '</mapping_scheme>'
        return outstr    

    @logAPICall
    def append_branch(self, node, branch):
        """ append a branch (from library) to a node in a mapping scheme tree """

        stat_tree = None
        if type(node) == MappingSchemeZone:
            # selected node is zone
            # retrieve root node from stats tree
            stat_tree = self.get_assignment(node)
            node_to_attach = node.stats.get_tree()
        else:
            node_to_attach = node
            for zone, stat in self.assignments():
                if stat.has_node(node):
                    stat_tree = stat
                    break
        if stat_tree is None:
            raise SIDDException('selected node does not belong to mapping scheme')
            
        # add branch as child
        if type(branch) == MappingSchemeZone:
            # branch starts from zone node, so it is a full stats tree
            # add only the child nodes
            print 'branch is zone, add children'            
            for child in branch.stats.get_tree().children:                
                stat_tree.add_branch(node_to_attach, child)
        else:
            # branch is from a tree
            # add branch as child node
            print 'branch is node, add branch'            
            stat_tree.add_branch(node_to_attach, branch)

        # done

    @logAPICall
    def delete_branch(self, node):
        """ delete branch from mapping scheme tree """
        for zone, stat in self.assignments():
            if stat.has_node(node):
                stat.delete_branch(node)
                return 
        raise SIDDException('given node does not belong to mapping scheme')
        

    @logAPICall
    def assign(self, zone, statistics):
        """
        Associate given statistic with given zone.
        This method will override existing association for the given zone.
        """
        statistics.get_tree().value = zone.name
        zone.stats = statistics
        self.zones.append(zone)        
    
    @logAPICall
    def get_assignment(self, ms_zone):
        """
        Retrieve statistic associated with given zone
        (ms.MappingSchemeZone object)
        """
        return self.get_assignment_by_name(ms_zone.name)
    
    @logAPICall
    def get_assignment_by_name(self, zone_name):
        """ Retrieve statistic associated with given zone name """
        try:
            for zone in self.zones:                
                if (zone.name == zone_name):
                    return zone.stats
        except:
            return None
    
    @logAPICall
    def get_zones(self):
        """ Retrieve all zones in current mapping scheme """
        return self.zones
    
    @logAPICall
    def assignments(self):
        """
        Generator allowing traversing of all zone/statistic associations
        in current mapping scheme
        """
        for zone in self.zones:            
            yield zone, zone.stats

