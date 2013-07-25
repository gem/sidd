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
Module contains all mapping scheme handling class
"""

from xml.etree.ElementTree import ElementTree, fromstring
from operator import attrgetter

from utils.xml import get_node_attrib
from sidd.constants import logAPICall
from sidd.exception import SIDDException
from sidd.taxonomy import get_taxonomy
from sidd.ms.statistic import Statistics
from sidd.ms.node import StatisticNode

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
        for zone in self.zones:
            if not zone.stats.is_valid:
                return False
        return True
    
    @property
    def is_empty(self):
        for zone in self.zones:
            if len(zone.stats.root.children) > 0:
                return False
        return True 
    
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
        except Exception:
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
            ms_zone = MappingSchemeZone(get_node_attrib(zone, 'name'))
            ms_zone.stats = stats
            self.zones.append(ms_zone)
                      
        self.sort_zones()
    
    @logAPICall
    def save(self, xml_file, pretty=False):
        """ Store mapping scheme into given input file """
        f = open(xml_file, 'w')
        f.write(self.to_xml(pretty))
        f.close()
    
    @logAPICall
    def to_xml(self, pretty=False):
        outstr = (
            '<mapping_scheme><taxonomy><name>%s</name><description>%s</description><version>%s</version></taxonomy>' %
            (self.taxonomy.name, self.taxonomy.description,self.taxonomy.version))
        for zone in self.zones:
            outstr += '<zone name="%s">'%(zone.name)
            outstr += zone.stats.to_xml(pretty)
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
            stat_tree = self.get_assignment_by_node(node_to_attach)
            
        if stat_tree is None:
            raise SIDDException('selected node does not belong to mapping scheme')
            
        # add branch as child
        if type(branch) == MappingSchemeZone:
            # branch starts from zone node, so it is a full stats tree
            # add only the child nodes
            logAPICall.log('branch is zone, add children', logAPICall.DEBUG_L2)
            
            # test to make sure append is valid
            # exception will be thrown is case of error
            for child in branch.stats.get_tree().children:
                stat_tree.test_repeated_attribute(node_to_attach, child)
                stat_tree.test_repeated_value(node_to_attach, child)
                     
            for child in branch.stats.get_tree().children:                
                stat_tree.add_branch(node_to_attach, child, test_repeating=False, update_stats=False)
            node_to_attach.balance_weights()            
        else:
            # branch is from a tree
            # add branch as child node
            logAPICall.log('branch is node, add branch', logAPICall.DEBUG_L2)          
            stat_tree.add_branch(node_to_attach, branch)

        # done

    @logAPICall
    def delete_branch(self, node):
        """ delete branch from mapping scheme tree """        
        # for MappingSchemeZone delete entire stats tree
        # for StaticticNode delete node 
        if isinstance(node, MappingSchemeZone):
            for zone in self.zones:
                if zone == node:    # found
                    taxonomy = zone.stats.taxonomy 
                    del zone.stats
                    # create new empty tree 
                    zone.stats = Statistics(taxonomy)
                    zone.stats.finalize()
                    zone.stats.name = zone.name
                    return                
        elif isinstance(node, StatisticNode):
            for zone in self.zones: # found                
                if zone.stats.has_node(node):
                    zone.stats.delete_branch(node)
                    return 
        # node not correct type or not found in tree        
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
        self.sort_zones()     
    
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
    def get_assignment_by_node(self, node):
        """ Retrieve statistic contains given StatisticNode """
        if node is None:
            return None
        for assignment in self.assignments():
            stat = assignment[1]
            if stat.has_node(node):
                # found
                return stat
        # not found
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

    def sort_zones(self):
        self.zones.sort(key=attrgetter('name'))
