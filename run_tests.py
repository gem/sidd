#
# SeismiCat: an on-line seismic risk assessment tool for 
# building property owners, lenders, insurers and municipal analysts. 
# 
# @copyright  (c)2012 ImageCat inc, All rights reserved
# @link       http://www.seismicat.com
# @since      SeismiCat v1.0
# @license    
# @version    $Id: run_tests.py 18 2012-10-24 20:21:41Z zh $
#

import sys
import os
import unittest
import getopt
import shutil

import logging
logging.basicConfig(level=logging.ERROR)

from qgis.core import QgsApplication

from tests import *

def suite():
    suite = unittest.TestSuite()

    # ms test cases
    #suite.addTest(MSTestCase('test_BuildMS'))    
    #suite.addTest(MSTestCase('test_SaveMS'))
    suite.addTest(MSTestCase('test_LoadMS'))    
    #suite.addTest(MSTestCase('test_StatsAddBranch'))
    #suite.addTest(MSTestCase('test_StatsRandomWalk'))
    #suite.addTest(MSTestCase('test_StatsLeaves'))
    
    # operator tests
    #suite.addTest(OperatorTestCase('test_LoadZone'))
    #suite.addTest(OperatorTestCase('test_MakeGrid'))
    #suite.addTest(OperatorTestCase('test_CreateMSFromSurveyZone'))
    #suite.addTest(OperatorTestCase('test_CreateMSFromSurveyOnly'))
    #suite.addTest(OperatorTestCase('test_ApplyMS'))    
    #suite.addTest(OperatorTestCase('test_LoadGEMDBSurvey'))
    #suite.addTest(OperatorTestCase('test_VerifyExposure'))
    #suite.addTest(OperatorTestCase('test_MakeGridGeometry'))
    
    #suite.addTest(TaxonomyTestCase('test_Parse'))
    
    #suite.addTest(MSDBTestCase('test_Read'))
    #suite.addTest(MSDBTestCase('test_SaveDelete'))
    
    #suite.addTest(ProjectTestCase('test_WorkflowBuilder'))
    #suite.addTest(ProjectTestCase('test_BuildExposure'))
        
    return suite

if __name__ == '__main__':
    try:
        opts, args = getopt.getopt(sys.argv[1:], "s", ["test suite"])
    except getopt.GetoptError, err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        sys.exit(2)

    os.environ['QGIS_DEBUG'] = '-1'
    
    required_dirs = ['tests/tmp']
    for dir_path in required_dirs:
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
    
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

    for dir_path in required_dirs:
        try:
            shutil.rmtree(dir_path)
        except:
            pass
    QgsApplication.exitQgis()
    