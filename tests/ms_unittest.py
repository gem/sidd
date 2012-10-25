#
# SeismiCat: an on-line seismic risk assessment tool for 
# building property owners, lenders, insurers and municipal analysts. 
# 
# @copyright  (c)2012 ImageCat inc, All rights reserved
# @link       http://www.seismicat.com
# @since      SeismiCat v1.0
# @license    
# @version    $Id: ms_unittest.py 19 2012-10-25 01:06:59Z zh $
#

import os
import sys
import unittest
import logging

# import sidd packages for testing
from sidd.ms import *
from utils.system import get_app_dir 

class MSTestCase(unittest.TestCase):

    # run for everytesy
    ##################################
    
    def setUp(self):
        from sidd.taxonomy import get_taxonomy
        self.taxonomy = get_taxonomy("gem")
        self.survey_file = get_app_dir() + "/tests/data/survey.csv"
        self.ms_file = get_app_dir() + '/tests/data/ms.xml'
        self.tmp_ms_file = get_app_dir() + '/tests/data/tmp_ms.xml'

    # tests
    ##################################
    
    def test_BuildMS(self):
        import csv
        survey = csv.reader(open(self.survey_file , 'r'), delimiter=',', quotechar='"')
        header = survey.next()

        stats = Statistics(self.taxonomy)
        stats.set_attribute_skip(3, True)
        stats.set_attribute_skip(4, True)
        stats.set_attribute_skip(5, True)
        stats.set_attribute_skip(6, True)
        _count=0

        for row in survey:
            tax_string = row[2]
            stats.add_case(tax_string)
        stats.finalize()
        
        ms = MappingScheme(self.taxonomy)
        ms_zone = MappingSchemeZone('ALL')
        ms.assign(ms_zone, stats)

        ms2 = MappingScheme(self.taxonomy)
        ms2.read(self.ms_file)

        self.assertEqual(
            ms.get_assignment_by_name("ALL").to_xml().strip().__len__(),
            ms2.get_assignment_by_name("ALL").to_xml().strip().__len__()
        )

    def test_SaveMS(self):
        import csv
        survey = csv.reader(open(self.survey_file, 'r'), delimiter=',', quotechar='"')
        header = survey.next()

        stats = Statistics(self.taxonomy)
        stats.set_attribute_skip(3, True)
        stats.set_attribute_skip(4, True)
        stats.set_attribute_skip(5, True)
        stats.set_attribute_skip(6, True)
        _count=0

        for row in survey:
            tax_string = row[2]
            stats.add_case(tax_string)
        stats.finalize()
        
        ms = MappingScheme(self.taxonomy)
        ms_zone = MappingSchemeZone('ALL')
        ms.assign(ms_zone, stats)
        ms.save(self.tmp_ms_file)
        
        self.assertTrue(os.path.exists(self.tmp_ms_file))
        os.remove(self.tmp_ms_file)

    def test_LoadMS(self):
        ms = MappingScheme(self.taxonomy)
        ms.read(self.ms_file)
        
        stats = ms.get_assignment_by_name("ALL")
        attributes = stats.get_attributes(stats.get_tree())
        expected = ['Material', 'Lateral Load-Resisting System', 'Roof']
        self.assertEqual(attributes, expected)
        
    def test_MSAddBranch(self):
        ms = MappingScheme(self.taxonomy)
        ms.read(self.ms_file)
        
        stats = ms.get_assignment_by_name("ALL")
        
        # cannot add tree to self because of conflicting attributes
        with self.assertRaises(StatisticError):
            stats.add_branch(stats.get_tree().children[0], stats.get_tree())

        # sure be able to add new node
        node = stats.get_tree().children[0]
        new_node = StatisticNode(None, "nothing", "val", 0)
        stats.add_branch(node, new_node)
        
        self.assertEquals(len(node.children), 2)
    
        