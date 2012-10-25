#
# SeismiCat: an on-line seismic risk assessment tool for 
# building property owners, lenders, insurers and municipal analysts. 
# 
# @copyright  (c)2012 ImageCat inc, All rights reserved
# @link       http://www.seismicat.com
# @since      SeismiCat v1.0
# @license    
# @version    $Id: proj_unittest.py 18 2012-10-24 20:21:41Z zh $
#

import os
import sys
import unittest
import logging

from utils.system import get_random_name

# import sidd packages for testing
from sidd.ms import *
from sidd.constants import *
from sidd.exception import SIDDException, WorkflowException
from sidd.project import Project
from sidd.workflow import WorkflowBuilder

class ProjectTestCase(unittest.TestCase):

    # run for everytesy
    ##################################
    
    def setUp(self):
        from sidd.taxonomy import get_taxonomy
        self.taxonomy = get_taxonomy("gem")
        self.test_data_dir = str(os.getcwd()) +  "/tests/data/"
        self.test_tmp_dir = str(os.getcwd()) +  "/tests/tmp/"
        
        self.proj_file = self.test_data_dir +  'test.db'
        self.fp_path = self.test_data_dir +  'footprint.shp'
        self.survey_path = self.test_data_dir +  "survey.csv"
        self.zone_path = self.test_data_dir +  "zones.shp"
        self.zone_field = 'LandUse'
        self.bldgcount_field = 'NumBldg'

        self.zone2_path = self.test_data_dir +  "zones2.shp"
        self.zone2_field = "ZONE"
        
        self.operator_options = {
            'tmp_dir': self.test_tmp_dir,
            'taxonomy':'gem',
            'skips':[1,2,3,4,5,6],
        }

    # tests
    ##################################
    
    def test_CreateProject(self, skipTest=False):
        logging.debug('test_CreateProject %s' % skipTest)
        
        proj_file = '%stest.db' % self.test_tmp_dir
        proj = Project(proj_file)
        proj.operator_options = self.operator_options        
        if skipTest:
            return (proj, proj_file)
        
        # clean up
        del proj
        os.remove(proj_file)

    def test_LoadProject(self, skipTest=False):
        logging.debug('test_LoadProject %s' % skipTest)
        
        proj = Project(self.proj_file)
        proj.operator_options = self.operator_options        
        if skipTest:
            return proj
    
    def test_WorkflowBuilder(self):
        logging.debug('test_BuildWorkflow')
        
        def get_run_exception(func, param):
            try:
                func(param)
            except Exception as ex:
                import traceback
                #traceback.print_exc() 
                return ex
            return None

        # empty proj/ms should be enough for testing
        (proj, proj_file) = self.test_CreateProject(True)
        ms = MappingScheme(self.taxonomy) 
        
        builder = WorkflowBuilder(self.operator_options)

        # test cases raising exception
        ###################
        
        # test case, empty project, should raise exception need zone        
        ex = get_run_exception(builder.build_workflow, (proj))
        self.assertEqual(type(ex), WorkflowException)
        self.assertEqual(ex.error, WorkflowErrors.NeedsZone)

        # test case, only zone, should raise exception need count
        proj.set_zones(ZonesTypes.Landuse, self.zone2_path, self.zone2_field)
        ex = get_run_exception(builder.build_workflow, (proj))
        self.assertEqual(type(ex), WorkflowException)        
        self.assertEqual(ex.error, WorkflowErrors.NeedsCount)

        # test case, zone / footprint, should raise exception need ms 
        proj.set_footprint(FootprintTypes.Footprint, self.fp_path)
        ex = get_run_exception(builder.build_workflow, (proj))
        self.assertEqual(type(ex), WorkflowException)        
        self.assertEqual(ex.error, WorkflowErrors.NeedsMS)

        # complete footprint / zone / ms to zone, should raise exception no action
        proj.ms = ms 
        proj.set_output_type(OutputTypes.Zone)
        ex = get_run_exception(builder.build_workflow, (proj))        
        self.assertEqual(type(ex), WorkflowException)        
        self.assertEqual(ex.error, WorkflowErrors.NoActionDefined)

        # test cases no exception
        ###################

        # complete footprint / zone / ms to grid, no exception 
        proj.set_output_type(OutputTypes.Grid)
        ex = get_run_exception(builder.build_workflow, (proj))        
        self.assertEqual(ex, None)        

        # test case, zonecount and ms to grid, no exception
        proj.set_footprint(FootprintTypes.None) # remove footprint
        proj.set_zones(ZonesTypes.LanduseCount, self.zone_path, self.zone_field, self.bldgcount_field)
        proj.ms = ms
        proj.set_output_type(OutputTypes.Grid)
        ex = get_run_exception(builder.build_workflow, (proj))
        self.assertEqual(ex, None)
        
        # test case, zonecount and ms to zone, no exception        
        proj.set_output_type(OutputTypes.Zone)
        ex = get_run_exception(builder.build_workflow, (proj))
        self.assertEqual(ex, None)

        # test case, complete survey, no exception
        proj.set_survey(SurveyTypes.CompleteSurvey, self.survey_path)
        ex = get_run_exception(builder.build_workflow, (proj))
        self.assertEqual(ex, None)
        
        # clean up
        del proj
        os.remove(proj_file)

    def test_BuildExposure(self):
        logging.debug('test_BuildWorkflow')
        
        
        logAPICall.setLevel(logAPICall.DEBUG)
        
        # create temp dir for project data
        proj_tmp_dir = '%s/%s/' % (self.test_tmp_dir, get_random_name())
        if not os.path.exists(proj_tmp_dir):
            os.mkdir(proj_tmp_dir)  
        
        proj = self.test_LoadProject(True)
        proj.operator_options['tmp_dir'] = proj_tmp_dir
        proj.temp_dir = proj_tmp_dir
        
        proj.sync(SyncModes.Read)
        
        proj.build_exposure()
        self.assertTrue(os.path.exists(proj.exposure_file))
        del proj
        