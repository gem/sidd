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
import os
import logging

from utils.system import get_random_name

# import sidd packages for testing
from sidd.appconfig import SIDDConfig, types
from sidd.ms import MappingScheme
from sidd.constants import logAPICall, \
                           SurveyTypes, ZonesTypes, OutputTypes, FootprintTypes, SyncModes, \
                           WorkflowErrors
from sidd.project import Project
from sidd.workflow import WorkflowBuilder
from sidd.taxonomy import get_taxonomy

from common import SIDDTestCase
class ProjectTestCase(SIDDTestCase):

    # run for everytesy
    ##################################
    
    def setUp(self):
        super(ProjectTestCase, self).setUp()
        
        self.taxonomy = get_taxonomy("gem")
        self.test_config = SIDDConfig(self.test_data_dir + '/test.cfg')
        
        self.proj_file = self.test_data_dir +  'test.db'
        self.proj_file3 = self.test_data_dir +  'test3.db'
        
        self.fp_path = self.test_data_dir +  'footprints3.shp'
        self.survey_path = self.test_data_dir +  "survey3.gemdb"
        self.zone_path = self.test_data_dir +  "zones3.shp"
        self.zone_field = 'LandUse'
        self.bldgcount_field = 'NumBldg'

        self.zone2_path = self.test_data_dir +  "zones2.shp"
        self.zone2_field = "ZONE"
        
        self.operator_options = {
            'tmp_dir': self.test_tmp_dir,
            'taxonomy':self.taxonomy,
            'skips': self.test_config.get('options', 'skips', [], types.ListType),     
        }

    # tests
    ##################################
    
    def test_CreateProject(self, skipTest=False):
        logging.debug('test_CreateProject %s' % skipTest)
        
        proj_file = '%stest.db' % self.test_tmp_dir
        proj = Project(self.test_config, self.taxonomy)
        proj.set_project_path(proj_file)
        proj.operator_options = self.operator_options        
        if skipTest:
            return (proj, proj_file)
        
        # clean up
        del proj
        os.remove(proj_file)

    def test_LoadProject(self, skipTest=False):
        logging.debug('test_LoadProject %s' % skipTest)
        
        proj = Project(self.test_config, self.taxonomy)
        proj.set_project_path(self.proj_file)
        proj.sync(SyncModes.Read)
        if skipTest:
            return proj
    
    def test_WorkflowBuilder(self):
        logging.debug('test_BuildWorkflow')
        
        def get_run_exception(func, param):
            try:
                func(param)
            except Exception as ex:
                import traceback
                traceback.print_exc() 
                return ex
            return None

        # empty proj/ms should be enough for testing
        (proj, proj_file) = self.test_CreateProject(True)
        ms = MappingScheme(self.taxonomy) 
        
        builder = WorkflowBuilder(self.operator_options)

        # test cases raising exception
        ###################
        # test case, empty project, should have errors NeedsZone, NeedsCount, NeedsMS
        workflow = builder.build_workflow(proj)
        self.assertTrue(not workflow.ready)
        self.assertEqual(len(workflow.errors), 3)
        self.assertListEqual(workflow.errors, [WorkflowErrors.NeedsZone, 
                                               WorkflowErrors.NeedsCount, 
                                               WorkflowErrors.NeedsMS])
        
        # test case, only zone, should raise exception need count
        proj.set_zones(ZonesTypes.Landuse, self.zone2_path, self.zone2_field)
        workflow = builder.build_workflow(proj)        
        self.assertTrue(not workflow.ready)
        self.assertEqual(len(workflow.errors), 2)
        self.assertListEqual(workflow.errors, [WorkflowErrors.NeedsCount, 
                                               WorkflowErrors.NeedsMS])
        
        # test case, zone / footprint, should raise exception need ms 
        proj.set_footprint(FootprintTypes.Footprint, self.fp_path)
        workflow = builder.build_workflow(proj)        
        self.assertTrue(not workflow.ready)
        self.assertEqual(len(workflow.errors), 1)
        self.assertListEqual(workflow.errors, [WorkflowErrors.NeedsMS])

        # complete footprint / zone / ms to zone, no exception
        proj.ms = ms 
        proj.set_output_type(OutputTypes.Zone)
        workflow = builder.build_workflow(proj)
        self.assertTrue(workflow.ready)
        self.assertEqual(len(workflow.errors), 0)
        
        # test cases no exception
        ###################

        # complete footprint / zone / ms to grid, no exception 
        proj.set_output_type(OutputTypes.Grid)
        workflow = builder.build_workflow(proj)
        self.assertTrue(workflow.ready)
        self.assertEqual(len(workflow.errors), 0)

        # test case, zonecount and ms to grid, no exception
        proj.set_footprint(FootprintTypes.None) # remove footprint
        proj.set_zones(ZonesTypes.LanduseCount, self.zone_path, self.zone_field, self.bldgcount_field)
        proj.ms = ms
        proj.set_output_type(OutputTypes.Grid)
        workflow = builder.build_workflow(proj)
        self.assertTrue(workflow.ready)
        self.assertEqual(len(workflow.errors), 0)
        
        # test case, zonecount and ms to zone, no exception        
        proj.set_output_type(OutputTypes.Zone)
        workflow = builder.build_workflow(proj)
        self.assertTrue(workflow.ready)
        self.assertEqual(len(workflow.errors), 0)

        # test case, complete survey, no exception
        proj.set_survey(SurveyTypes.CompleteSurvey, self.survey_path)
        workflow = builder.build_workflow(proj)
        self.assertTrue(workflow.ready)
        self.assertEqual(len(workflow.errors), 0)
        
        # clean up
        del proj
        os.remove(proj_file)

    def test_BuildExposure(self):
        logging.debug('test_BuildWorkflow')        
        
        logAPICall.setLevel(logAPICall.DEBUG_L2)
        
        # create temp dir for project data
        proj_tmp_dir = '%s/%s/' % (self.test_tmp_dir, get_random_name())
        if not os.path.exists(proj_tmp_dir):
            os.mkdir(proj_tmp_dir)
        
        proj = Project(self.test_config, self.taxonomy)
        proj.set_project_path(self.proj_file3)
        proj.sync(SyncModes.Read)
        
        proj.operator_options['tmp_dir'] = proj_tmp_dir
        proj.temp_dir = proj_tmp_dir
        proj.fp_file = '%s%s' % (self.test_data_dir, 'footprints3.shp')
        proj.survey_file = '%s%s' % (self.test_data_dir, 'survey3.gemdb')
        proj.zone_file = '%s%s' % (self.test_data_dir, 'zones3.shp')
        
        proj.verify_data()
        proj.build_exposure()
        self.assertTrue(os.path.exists(proj.exposure_file))
        del proj
        