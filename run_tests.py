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
#

import sys
import os
import unittest
import getopt
import logging

logging.basicConfig(level=logging.ERROR)

from qgis.core import QgsApplication

from tests import *

def suite():
    suite = unittest.TestSuite()

    # ms test cases
    #suite.addTest(MSTestCase('test_BuildMS'))    
    #suite.addTest(MSTestCase('test_SaveMS'))
    #suite.addTest(MSTestCase('test_LoadMS'))    
    #suite.addTest(MSTestCase('test_StatsAddBranch'))
    #suite.addTest(MSTestCase('test_StatsRandomWalk'))
    #suite.addTest(MSTestCase('test_StatsLeaves'))
    suite.addTest(MSTestCase('test_Sampling'))
    
    # operator tests
    #suite.addTest(OperatorTestCase('test_LoadZone'))
    #suite.addTest(OperatorTestCase('test_LoadZone2'))
    #suite.addTest(OperatorTestCase('test_MakeGrid'))
    #suite.addTest(OperatorTestCase('test_ZoneGridJoin'))
    #suite.addTest(OperatorTestCase('test_CreateMSFromSurveyZone'))
    #suite.addTest(OperatorTestCase('test_CreateMSFromSurveyOnly'))
    #suite.addTest(OperatorTestCase('test_ApplyMS'))
    #suite.addTest(OperatorTestCase('test_LoadGEMDBSurvey'))
    #suite.addTest(OperatorTestCase('test_VerifyExposure'))
    #suite.addTest(OperatorTestCase('test_MakeGridGeometry'))
    #suite.addTest(OperatorTestCase('test_StratifiedSampleMS'))
    #suite.addTest(OperatorTestCase('test_ZoneFootprintToGridJoin'))
    #suite.addTest(OperatorTestCase('test_ZoneToGridJoin'))
    #suite.addTest(OperatorTestCase('test_ZonePopGridJoin'))
    
    # taxonomy tests    
    #suite.addTest(TaxonomyTestCase('test_Load'))
    #suite.addTest(TaxonomyTestCase('test_Parse'))
    
    # project tests
    #suite.addTest(ProjectTestCase('test_WorkflowBuilder'))
    #suite.addTest(ProjectTestCase('test_BuildExposure'))
    
    # other tests
    #suite.addTest(MSDBTestCase('test_Read'))
    #suite.addTest(MSDBTestCase('test_SaveDelete'))
    
    #suite.addTest(UtilsTestCase('test_Grid'))
    return suite

if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "s", ["test suite"])
    except getopt.GetoptError, err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        sys.exit(2)

    os.environ['QGIS_DEBUG'] = '-1'
    
    # supply path to where is your qgis installed
    QgsApplication.setPrefixPath(os.environ['QGIS'], True)
    # load providers
    QgsApplication.initQgis()

    run_test_case=False
    for o, a in opts:
        if o == "-s":
            run_test_case=True

    if run_test_case:
        print 'Running custom test suite ... '
        print '----------------------------------------------------------------------'
        runner = unittest.TextTestRunner(verbosity=2)
        runner.run(suite())            
    else:            
        print 'Running all test cases ... '
        print '----------------------------------------------------------------------'
        unittest.main(verbosity=2)

    QgsApplication.exitQgis()
    