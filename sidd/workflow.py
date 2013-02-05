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
# Version: $Id: workflow.py 21 2012-10-26 01:48:25Z zh $

"""
SIDD workflow manager
"""
from xml.etree.ElementTree import ElementTree, fromstring

from sidd.exception import WorkflowException
from sidd.constants import logAPICall, WorkflowErrors, \
                           FootprintTypes, ExportTypes, OutputTypes, SurveyTypes, ZonesTypes, \
                           CNT_FIELD_NAME
from sidd.ms import MappingScheme
from sidd.operator import *

class Workflow(object):
    """
    class for managing workflows
    workflows can be loaded from XML file. this allow the system to
    intelligently build workflow based on input data available
    """

    # constructor / destructor
    ##################################
    
    def __init__(self):
        """ constructor """
        self.reset()
        self.ready=False
        self.errors = []

    # public method
    ##################################
    @logAPICall
    def add_error(self, err_code):         
        self.errors.append(err_code)
    
    @logAPICall
    def has_error(self):
        return len(self.errors) > 0
    
    @logAPICall
    def from_xml_string(self, xmlstr):
        """ build workflow from xml string """
        self._build(fromstring(xmlstr))

    @logAPICall
    def from_xml_file(self, xml_file):
        """ build workflow from xml file """
        workflow = ElementTree()        
        self._build(workflow.parse(xml_file))

    @logAPICall        
    def nextstep(self):
        """ generator through each step in the workflow process """
        #for op_id, op in self.operators.iteritems():
        #    yield op
        for op in self.operators:
            yield op

    @logAPICall
    def process(self):
        """ process entire workflow according to step defined """
        if not self.ready:
            return
        for op in self.nextstep():
            op.do_operation()        

    # help functions
    ##################################
    
    def reset(self):
        """ reset operators and data """
        self.operator_data = {}
        self.operators = [] #{}
        
        self.cur_step = 0
        self.description = ""
        
    def _build(self, workflow_node):
        """ build workflow from given xml node """        
        self.reset()
        
        # check to make sure it is correct.
        # use DTD???
        for data_node in workflow_node.find('operator_data').findall("operator"):
            op_data = Operator(data_node.attrib['type'])
            op_data_id = data_node.attrib['id']
            for input_node in data_node.findall("param"):
                setattr(op_data, data_node.attrib['name'], data_node.attrib['value'])
            self.operator_data[op_data_id] = op_data

        for operator_node in workflow_node.find('operators').findall("operator"):
            op = Operator.get_operator(operator_node.attrib['name'])
            op_id = operator_node.attrib['id']
            for input_node in operator_node.findall("input"):
                op_data_id = input_node.attrib['id']    
                op.inputs.append(self.operator_data[op_data_id])

            for output_node in operator_node.findall("input"):
                op_data_id = output_node.attrib['id']    
                op.output.append(self.operator_data[op_data_id])                
            self.operators[op_id] = operator
        self.ready=False

class WorkflowBuilder(object):
    """
    class for building workflow from project    
    """

    # constructor / destructor
    ##################################
    
    def __init__(self, operator_options):
        self._operator_options = operator_options
        
        # process chian encodes the decision logic determining
        # steps to create exposure (or not) from 
        # - input data available
        # - and output type
        #
        # NOTE: the order of the chain determines action path to be taken
        #       this takes care of situations when multiple path exists
        #       the order should be based on best quality of result
        
        self._process_chains = [
            (['survey_file', 'survey_is_complete'], OutputTypes.Grid, self._completesurvey_to_grid_workflow),
            (['fp', 'zone',], OutputTypes.Grid, self._footprint_to_grid_workflow),
            (['fp', 'zone',], OutputTypes.Zone, self._footprint_to_zone_workflow),
            (['zone', 'zone_count_field'], OutputTypes.Zone, self._zonecount_to_zone_workflow),
            (['zone', 'zone_count_field'], OutputTypes.Grid, self._zonecount_to_grid_workflow),
        ]

    # public method
    ##################################
    def build_load_fp_workflow(self, project):
        workflow = Workflow()
        workflow.ready=True
        if project.fp_type == FootprintTypes.FootprintHt:
            self.load_footprint(project, workflow, True)
        elif project.fp_type == FootprintTypes.Footprint:
            self.load_footprint(project, workflow, False)
        else:
            workflow.ready=False        
        return workflow

    def build_load_survey_workflow(self, project):
        workflow = Workflow()
        workflow.ready=True
        if project.survey_type == SurveyTypes.CompleteSurvey:
            self.load_survey(project, workflow, True)
        elif project.survey_type == SurveyTypes.SampledSurvey:
            self.load_survey(project, workflow, False)
        else:
            workflow.ready=False        
        return workflow
    
    def build_load_zones_workflow(self, project):
        workflow = Workflow()
        workflow.ready=True
        if project.zone_type == ZonesTypes.LanduseCount:
            self.load_zone(project, workflow, True)
        elif project.zone_type == ZonesTypes.Landuse:
            self.load_zone(project, workflow, False)
        else:
            workflow.ready=False
        return workflow        
        
    @logAPICall
    def build_ms_workflow(self, project, isEmpty=False):
        workflow = Workflow()
        
        logAPICall.log('creating survey loader ...', logAPICall.DEBUG_L2)
        if not isEmpty:
            self.load_survey(project, workflow, False)

        if project.zone_type == ZonesTypes.None:
            if isEmpty:
                logAPICall.log('creating empty mapping scheme ...', logAPICall.DEBUG_L2)
                ms_creator = EmptyMSCreator(self._operator_options)
                ms_creator.inputs = []
            else:
                logAPICall.log('creating mapping scheme from survey only ...', logAPICall.DEBUG_L2)            
                ms_creator = SurveyOnlyMSCreator(self._operator_options)
                ms_creator.inputs = [workflow.operator_data['survey'],]
        else:
            self.load_zone(project, workflow, False)
            if isEmpty:                
                logAPICall.log('creating empty mapping scheme from zones ...', logAPICall.DEBUG_L2)
                ms_creator = EmptyZonesMSCreator(self._operator_options)
                ms_creator.inputs = [
                    workflow.operator_data['zone'],
                    workflow.operator_data['zone_field'],]
            else:
                logAPICall.log('creating mapping scheme from survey and zones ...', logAPICall.DEBUG_L2)
                workflow.operator_data['zone_field'] = OperatorData(OperatorDataTypes.StringAttribute, project.zone_field)
                ms_creator = SurveyZonesMSCreator(self._operator_options)
                ms_creator.inputs = [
                    workflow.operator_data['survey'],
                    workflow.operator_data['zone'],
                    workflow.operator_data['zone_field'],]
        
        workflow.operator_data['ms'] = OperatorData(OperatorDataTypes.MappingScheme)
        ms_creator.outputs = [workflow.operator_data['ms'],]
        workflow.operators.append(ms_creator)
        workflow.ready=True
        
        return workflow
        
    @logAPICall
    def build_workflow(self, project):
        workflow = Workflow()
        still_needs_count = True
        still_needs_zone = True
        still_needs_ms = True
            
        # footprint loading
        logAPICall.log('checking footprint data', logAPICall.DEBUG)        
        if project.fp_type == FootprintTypes.FootprintHt:
            self.load_footprint(project, workflow, True)
            still_needs_count = False
        elif project.fp_type == FootprintTypes.Footprint:
            self.load_footprint(project, workflow, False)
            still_needs_count = False

        # survey loading
        logAPICall.log('checking survey data', logAPICall.DEBUG)        
        if project.survey_type == SurveyTypes.CompleteSurvey:
            self.load_survey(project, workflow, True)
            still_needs_count = False
            still_needs_zone = False
            still_needs_ms = False
        elif project.survey_type == SurveyTypes.SampledSurvey:
            self.load_survey(project, workflow, False)
        
        # zones loading
        logAPICall.log('checking zone data', logAPICall.DEBUG)
        if project.zone_type == ZonesTypes.LanduseCount:
            self.load_zone(project, workflow, True)            
            still_needs_count = False
            still_needs_zone = False
            
        elif project.zone_type == ZonesTypes.Landuse:
            self.load_zone(project, workflow, False)        
            still_needs_zone = False

        # need to load MS
        logAPICall.log('checking ms', logAPICall.DEBUG)
        if getattr(project, 'ms', None) is not None and type(project.ms) == MappingScheme:
            workflow.operator_data['ms'] = OperatorData(OperatorDataTypes.MappingScheme, project.ms)
            still_needs_ms = False

        logAPICall.log('checking if dataset is complete', logAPICall.DEBUG)

        if still_needs_zone:
            workflow.add_error(WorkflowErrors.NeedsZone)
        if still_needs_count:
            workflow.add_error(WorkflowErrors.NeedsCount)            
        if still_needs_ms:
            workflow.add_error(WorkflowErrors.NeedsMS)
        
        # if data set is not complete
        # return a workflow that is not ready
        if workflow.has_error():
            return workflow

        logAPICall.log('add exposure building operation', logAPICall.DEBUG)
        
        # select appropriate operator(s) to apply mapping scheme
        try:
            self._build_processing_chain(project, workflow)            
            workflow.ready=True
        except WorkflowException as err:
            # error building processing chain
            # workflow is not ready 
            workflow.add_error(err.error)
        
        return workflow

    def build_export_workflow(self, project):
        workflow = Workflow()
        
        workflow.operator_data['exposure_file'] = OperatorData(OperatorDataTypes.Shapefile, project.exposure_file)
        workflow.operator_data['export_file'] = OperatorData(OperatorDataTypes.File, project.export_file)
        export_type = project.export_type
        if export_type == ExportTypes.Shapefile:
            export_operator = ExposureSHPWriter(self._operator_options)
        elif export_type == ExportTypes.KML:
            export_operator = ExposureKMLWriter(self._operator_options)
        elif export_type == ExportTypes.NRML:
            export_operator = ExposureNRMLWriter(self._operator_options)
        else:
            return
        export_operator.inputs= [workflow.operator_data['exposure_file'],
                                 workflow.operator_data['export_file'],]        
        workflow.operators.append(export_operator)
        workflow.ready=True
        
        return workflow


    # workflow helper methods - build data loading operator
    ##################################

    @logAPICall
    def load_footprint(self, project, workflow, withHt):
        """ create operator for loading footprint data and add to workflow """
        # required operator_data for additional processing
        workflow.operator_data['fp_input_file'] = OperatorData(OperatorDataTypes.Shapefile, project.fp_file)
        if withHt:
            workflow.operator_data['fp_ht_field'] = OperatorData(OperatorDataTypes.StringAttribute, project.fp_ht_field)

        # skip if already loaded
        if getattr(project, 'fp', None) is not None and getattr(project, 'fp_tmp_file', None) is not None:
            workflow.operator_data['fp'] = OperatorData(OperatorDataTypes.Footprint, project.fp)
            workflow.operator_data['fp_file'] = OperatorData(OperatorDataTypes.Shapefile, project.fp_tmp_file)
            return
        
        # inputs / outputs
        workflow.operator_data['fp'] = OperatorData(OperatorDataTypes.Footprint)
        workflow.operator_data['fp_file'] = OperatorData(OperatorDataTypes.Shapefile)
        
        # operator
        if withHt:
            fp_loader = FootprintHtLoader(self._operator_options)            
            fp_loader.inputs = [workflow.operator_data['fp_input_file'],
                                workflow.operator_data['fp_ht_field']]
        else:
            fp_loader = FootprintLoader(self._operator_options)
            fp_loader.inputs = [workflow.operator_data['fp_input_file']]        
        fp_loader.outputs = [workflow.operator_data['fp'],
                             workflow.operator_data['fp_file']]

        # add to workflow
        workflow.operators.append(fp_loader)        

    @logAPICall
    def load_zone(self, project, workflow, withCount):
        """ create operator for loading zone data and add to workflow """
        # required operator_data for additional processing
        workflow.operator_data['zone_input_file'] = OperatorData(OperatorDataTypes.Shapefile, project.zone_file)
        workflow.operator_data['zone_field'] = OperatorData(OperatorDataTypes.StringAttribute, project.zone_field)

        # skip loading operator if project already has data loaded
        if getattr(project, 'zone', None) is not None and getattr(project, 'zone_tmp_file', None) is not None:
            workflow.operator_data['zone'] = OperatorData(OperatorDataTypes.Footprint, project.zone)
            workflow.operator_data['zone_file'] = OperatorData(OperatorDataTypes.Shapefile, project.zone_tmp_file)
            return

        # inputs / outputs
        workflow.operator_data['zone'] = OperatorData(OperatorDataTypes.Zone)
        workflow.operator_data['zone_file'] = OperatorData(OperatorDataTypes.Shapefile)
        if withCount:
            workflow.operator_data['zone_count_field'] = OperatorData(OperatorDataTypes.StringAttribute, project.zone_count_field)
        
        # operator 
        if withCount:
            zone_loader = ZoneCountLoader(self._operator_options)
            zone_loader.inputs = [workflow.operator_data['zone_input_file'],
                                  workflow.operator_data['zone_field'],
                                  workflow.operator_data['zone_count_field'],]
        else:
            zone_loader = ZoneLoader(self._operator_options)
            zone_loader.inputs = [workflow.operator_data['zone_input_file'],
                                  workflow.operator_data['zone_field'],]        
        zone_loader.outputs = [workflow.operator_data['zone'],
                               workflow.operator_data['zone_file'],]

        # add to workflow
        workflow.operators.append(zone_loader)
    
    def load_survey(self, project, workflow, isComplete):
        # required operator_data for additional processing
        workflow.operator_data['survey_input_file'] = OperatorData(OperatorDataTypes.File, project.survey_file)
        if isComplete:
            workflow.operator_data['survey_is_complete'] = OperatorData(OperatorDataTypes.StringAttribute, 'Yes')
        
        # skip if already loaded
        if getattr(project, 'survey', None) is not None and getattr(project, 'survey_tmp_file', None) is not None:
            workflow.operator_data['survey'] = OperatorData(OperatorDataTypes.Survey, project.survey)
            workflow.operator_data['survey_file'] = OperatorData(OperatorDataTypes.Shapefile, project.survey_tmp_file)
            return
                
        # inputs / outputs
        workflow.operator_data['survey'] = OperatorData(OperatorDataTypes.Survey)
        workflow.operator_data['survey_file'] = OperatorData(OperatorDataTypes.Shapefile)
        
        # operator 
        if (project.survey_format == "CSV"):
            svy_loader = CSVSurveyLoader(self._operator_options)
        else:
            svy_loader = GEMDBSurveyLoader(self._operator_options)
        svy_loader.inputs = [workflow.operator_data['survey_input_file'],
                             OperatorData(OperatorDataTypes.StringAttribute, project.survey_format),]
        svy_loader.outputs = [workflow.operator_data['survey'],
                              workflow.operator_data['survey_file'],]

        workflow.operators.append(svy_loader)
    
    # workflow helper methods - build processing operation chain 
    ##################################

    def _build_processing_chain(self, project, workflow):
        for [data, out_type, func] in self._process_chains:
            # match all inputs
            input_matches = True
            logAPICall.log('\tcheck data input chain %s %s=> %s' % (data, out_type, func.__name__),
                           logAPICall.DEBUG_L2)
            for _data in data:
                if not workflow.operator_data.has_key(_data):
                    input_matches = False
                    break
            if not input_matches:
                continue
            
            # match output type
            if out_type != project.output_type:
                continue
            
            # build process chain
            func(project, workflow)
            
            # done
            return
        
        # no match for input and output type
        # cannot do anything with given data
        raise WorkflowException(WorkflowErrors.NoActionDefined)

    def _footprint_to_grid_workflow(self, project, workflow):
        """ create exposure aggregated into ged grid with footprint data """
        
        # action (operator) required
        # 1 join footprint with zone to attache zone attribute
        # 2 aggregate footprint centroids
        # 3 apply mapping scheme to grid
        ###################################
        
        # 1 join footprint with zone to attache zone attribute
        workflow.operator_data['centroids'] = OperatorData(OperatorDataTypes.Footprint)
        workflow.operator_data['centroids_file'] = OperatorData(OperatorDataTypes.Shapefile)
        
        merger = ZoneFootprintMerger(self._operator_options)
        merger.inputs = [workflow.operator_data['zone'],
                         workflow.operator_data['zone_field'],
                         workflow.operator_data['fp'],]
        merger.outputs = [workflow.operator_data['centroids'],
                          workflow.operator_data['centroids_file'],]
        
        workflow.operators.append(merger)

        # 2. aggregate footprint centroids
        workflow.operator_data['grid'] = OperatorData(OperatorDataTypes.Grid)
        workflow.operator_data['grid_file'] = OperatorData(OperatorDataTypes.Shapefile)

        fp_agg = FootprintAggregator(self._operator_options)
        fp_agg.inputs = [workflow.operator_data['centroids'],
                         workflow.operator_data['zone_field'],]
        fp_agg.outputs = [workflow.operator_data['grid'],
                          workflow.operator_data['grid_file'],]
        
        workflow.operators.append(fp_agg)
        
        # 3 apply mapping scheme to grid
        workflow.operator_data['exposure'] = OperatorData(OperatorDataTypes.Exposure)
        workflow.operator_data['exposure_file'] = OperatorData(OperatorDataTypes.Shapefile)
        
        ms_applier = GridMSApplier(self._operator_options)
        ms_applier.inputs = [
            workflow.operator_data['grid'],
            workflow.operator_data['zone_field'],
            OperatorData(OperatorDataTypes.StringAttribute, CNT_FIELD_NAME),
            workflow.operator_data['ms'],
        ]
        ms_applier.outputs = [workflow.operator_data['exposure'],
                              workflow.operator_data['exposure_file'],]
        
        workflow.operators.append(ms_applier)              
        
    def _footprint_to_zone_workflow(self, project, workflow):
        """ create exposure aggregated into ged grid with footprint data """
        
        # action (operator) required
        # 1 attach footprint counts to zones
        # 2 process additional steps as _zonecount_to_zone_workflow
        ###################################
        workflow.operator_data['zone2'] = OperatorData(OperatorDataTypes.Zone)
        workflow.operator_data['zone_file2'] = OperatorData(OperatorDataTypes.Shapefile)
        workflow.operator_data['zone_count_field'] = OperatorData(OperatorDataTypes.StringAttribute, 
                                                                  CNT_FIELD_NAME)
        merger = ZoneFootprintCounter(self._operator_options)
        merger.inputs = [workflow.operator_data['zone'],
                         workflow.operator_data['zone_field'],
                         workflow.operator_data['zone_count_field'],
                         workflow.operator_data['fp'],]
        merger.outputs = [workflow.operator_data['zone2'],
                          workflow.operator_data['zone_file2'],]
        
        workflow.operator_data['zone'] = workflow.operator_data['zone2']
        workflow.operator_data['zone_file'] = workflow.operator_data['zone_file2']
        
        workflow.operators.append(merger)
        self._zonecount_to_zone_workflow(project, workflow)
        
                
    def _zonecount_to_zone_workflow(self, project, workflow):
        """ create exposure aggregated into original zone with zone/count """
        
        # action (operator) required
        # 1 apply mapping scheme to zone
        ###################################
        
        # 1 apply mapping scheme to zone
        workflow.operator_data['exposure'] = OperatorData(OperatorDataTypes.Exposure)
        workflow.operator_data['exposure_file'] = OperatorData(OperatorDataTypes.Shapefile)
        
        ms_applier = ZoneMSApplier(self._operator_options)
        ms_applier.inputs = [
            workflow.operator_data['zone'],
            workflow.operator_data['zone_field'],
            workflow.operator_data['zone_count_field'],
            workflow.operator_data['ms'],]
        ms_applier.outputs = [workflow.operator_data['exposure'],
                              workflow.operator_data['exposure_file'],]

        workflow.operators.append(ms_applier)

    def _zonecount_to_grid_workflow(self, project, workflow):
        """ create exposure aggregated into ged grid with zone/count """
        
        # action (operator) required
        # 1 create grid from zones
        # 2 merge grids and zones to get grid with count
        # 3 apply mapping scheme to grid
        ###################################
        
        # 1 create grid from zones
        workflow.operator_data['grid'] = OperatorData(OperatorDataTypes.Grid)
        workflow.operator_data['grid_file'] = OperatorData(OperatorDataTypes.Shapefile)
        
        grid_writer = GridFromRegionWriter(self._operator_options)
        grid_writer.inputs = [workflow.operator_data['zone'],]
        grid_writer.outputs =[workflow.operator_data['grid'],
                              workflow.operator_data['grid_file'],]
        
        workflow.operators.append(grid_writer)
        
        # 2 merge grids from zones to get building count
        workflow.operator_data['merged_grid'] = OperatorData(OperatorDataTypes.Grid)
        workflow.operator_data['merged_grid_file'] = OperatorData(OperatorDataTypes.Shapefile)        

        grid_zone_merger = ZoneGridMerger(self._operator_options)
        grid_zone_merger.inputs = [workflow.operator_data['zone'],
                                   workflow.operator_data['zone_field'],
                                   workflow.operator_data['zone_count_field'],
                                   workflow.operator_data['grid'],]
        grid_zone_merger.outputs = [workflow.operator_data['merged_grid'],
                                    workflow.operator_data['merged_grid_file'],]

        workflow.operators.append(grid_zone_merger)                
        
        # 3 apply mapping scheme to grid
        workflow.operator_data['exposure'] = OperatorData(OperatorDataTypes.Exposure)
        workflow.operator_data['exposure_file'] = OperatorData(OperatorDataTypes.Shapefile)

        ms_applier = GridMSApplier(self._operator_options)
        ms_applier.inputs = [workflow.operator_data['merged_grid'],
                             workflow.operator_data['zone_field'],
                             workflow.operator_data['zone_count_field'],
                             workflow.operator_data['ms'],]
        ms_applier.outputs = [workflow.operator_data['exposure'],
                              workflow.operator_data['exposure_file'],]

        workflow.operators.append(ms_applier)

    def _completesurvey_to_grid_workflow(self, project, workflow):
        """ create exposure aggregated into ged grid with zone/count """

        workflow.operator_data['exposure'] = OperatorData(OperatorDataTypes.Exposure)
        workflow.operator_data['exposure_file'] = OperatorData(OperatorDataTypes.Shapefile)
        
        svy_agg = SurveyAggregator(self._operator_options)
        svy_agg.inputs = [workflow.operator_data['survey'],]
        svy_agg.outputs = [workflow.operator_data['exposure'],
                           workflow.operator_data['exposure_file'],]
        workflow.operators.append(svy_agg)
        
    