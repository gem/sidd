# Copyright (c) 2011-2013, ImageCat Inc.
#
# SIDD is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
#
"""
main SIDD application controller
"""

import os
import bsddb
import shutil
import types
import json

from utils.enum import makeEnum
from utils.system import get_temp_dir, get_random_name
from utils.shapefile import remove_shapefile

from sidd.constants import logAPICall, \
                           FILE_PROJ_TEMPLATE, \
                           FootprintTypes, OutputTypes, SurveyTypes, ZonesTypes, \
                           ProjectStatus, ExtrapolateOptions, SyncModes, ExportTypes, \
                           ProjectErrors
from sidd.ms import MappingScheme
from sidd.exception import SIDDException, SIDDProjectException, WorkflowException
from sidd.workflow import Workflow, WorkflowBuilder

class Project (object):
    """
    SIDD project contains data and operators necessary to create an exposure
    database from given dataset
    """
    # constructor / destructor
    ##################################

    def __init__(self, app_config, taxonomy):
        """ constructor """
        self.temp_dir = get_temp_dir('tmp%s'%get_random_name())
        self.app_config = app_config
        self.operator_options = {
            'tmp_dir': self.temp_dir,
            'taxonomy':taxonomy,
            'skips': app_config.get('options', 'skips', [], types.ListType),            
        }
        self.reset()

        self.project_file = None
        self.db = None
        self.require_save = False
    
    def __del__(self):
        """ 
        destructor that perform cleanup
        NOTE: based on python behavior, there is no guarantee this method will ever to called
        """
        self.clean_up()
        
    def clean_up(self):
        """ cleanup """
        try:            
            logAPICall.log('attempt to delete project temp dir %s' % self.temp_dir, logAPICall.DEBUG)
            if os.path.exists(self.temp_dir):                
                del self.workflow
                if self.exposure is not None:
                    del self.exposure   # must delete layer, otherwise exposure_file becomes locked
                                        # and will generate error on shutil.rmtree
                shutil.rmtree(self.temp_dir)
        except Exception as err:            
            logAPICall.log('failed to delete temporary directory: %s' % str(err), logAPICall.WARNING)
        try:
            if self.project_file is not None and self.db is not None:
                self.db.close()
        except Exception:
            pass
    
    # data setter methods
    ##################################
    @logAPICall
    def set_project_path(self, project_file):
        try:
            if (not os.path.exists(project_file)):
                shutil.copyfile(FILE_PROJ_TEMPLATE, project_file)
            self.db = bsddb.btopen(project_file, 'c')
            self.version_major = self._get_project_data('version_major')
            self.version_minor = self._get_project_data('version_minor')
            logAPICall.log('opening project file version %s.%s' %(self.version_major, self.version_minor),
                           logAPICall.INFO)
            self.project_file = project_file
            self.require_save = True
        except:
            raise SIDDProjectException(ProjectErrors.FileFormatError)                
    
    @logAPICall
    def set_footprint(self, fp_type, fp_file='', ht_field=''):
        self.fp_file = fp_file
        self.fp_type = fp_type
        self.fp_ht_field = ht_field
        self.require_save = True

    @logAPICall
    def set_zones(self, zone_type, zone_file='', zone_field='', zone_count_field=''):
        """ load zone data """
        self.zone_file = zone_file
        self.zone_type = zone_type
        self.zone_field = zone_field
        self.zone_count_field = zone_count_field
        self.require_save = True        

    @logAPICall
    def set_survey(self, survey_type, survey_file='', survey_format='GEMDB'):
        """ load survey data """
        self.survey_file = survey_file
        self.survey_type = survey_type
        self.survey_format = survey_format
        self.require_save = True
        
    @logAPICall
    def set_output_type(self, output_type):
        self.output_type = output_type
        self.require_save = True

    @logAPICall
    def set_export(self, export_type, export_path):
        self.export_type = export_type
        self.export_path = export_path
        self.require_save = True

    @logAPICall
    def reset(self, sync=False):
        """
        reset project to default values, with option to also clear underlying db
        """
        self.fp_type = FootprintTypes.None
        self.fp_file = ''
        self.fp_ht_field = ''
        
        self.survey_type = SurveyTypes.None
        self.survey_file = ''
        self.survey_format = 'GEMDB' #'CSV'
        
        self.zone_type = ZonesTypes.None
        self.zone_file = ''
        self.zone_field = '' 
        self.zone_count_field = ''
        
        self.ms = None
        self.output_type = OutputTypes.Grid

        self.exposure = None
        
        self.export_type = ExportTypes.Shapefile
        self.export_path = ''

        # empty workflow
        self.workflow = Workflow()
        
        # clear status
        self.status = ProjectStatus.NotVerified
        self.errors = []
        
        self.require_save = True
        if sync:
            self.sync(SyncModes.Write)

    # exposure processing methods
    ##################################
    @logAPICall
    def load_footprint(self):
        # only load if all required fields exists
        if self.fp_type == FootprintTypes.None:
            return
        if self.fp_file == '':
            return
        if self.fp_type == FootprintTypes.FootprintHt and self.fp_ht_field == '':
            return            
        
        self.fp, self.fp_tmp_file = self._load_data('fp_file', 'fp', 'fp_file')
        return

    @logAPICall
    def load_zones(self):
        # only load if all required fields exists
        if self.zone_type == ZonesTypes.None:
            return
        if self.zone_file == '' or self.zone_field == '':
            return
        if self.fp_type ==  ZonesTypes.LanduseCount and self.zone_count_field == '':
            return
                
        self.zone, self.zone_tmp_file = self._load_data('zone_file', 'zone', 'zone_file') 
        return 

    @logAPICall
    def load_survey(self):
        self.survey, self.survey_tmp_file = self._load_data('survey_file', 'survey', 'survey_file') 
        return 
    
    @logAPICall
    def verify_data(self):
        """ verify existing data and create workflow """
        # build workflow based on current data
        builder = WorkflowBuilder(self.operator_options)
        self.workflow = builder.build_workflow(self)    
        
        if self.workflow.ready:
            self.status = ProjectStatus.ReadyForExposure
        else:
            self.status = ProjectStatus.ReadyForMS
        self.errors = self.workflow.errors
        self.exposure = None
        logAPICall.log('input verification completed', logAPICall.INFO)
        

    @logAPICall
    def build_exposure(self):
        """ building exposure database from workflow """
        for step in self.build_exposure_steps():
            step.do_operation()

    @logAPICall
    def build_exposure_steps(self):
        """ building exposure database from workflow """
        if not self.workflow.ready:
            raise SIDDException('cannot create exposure with current datasets')
        
        if getattr(self, 'exposure', None) is not None:
            del self.exposure
            remove_shapefile(self.exposure_file)
        
        for op in self.workflow.nextstep():
            yield op
        
        # when all steps are completed, set resulting exposure
        self.exposure = self.workflow.operator_data['exposure'].value
        self.exposure_file = self.workflow.operator_data['exposure_file'].value
        if self.workflow.operator_data.has_key('exposure_grid'):
            self.exposure_grid = self.workflow.operator_data['exposure_grid'].value
        
        logAPICall.log('exposure data created %s' % self.exposure_file, logAPICall.INFO)        

    @logAPICall
    def build_ms(self):
        """ build mapping scheme from survey data """
        # make sure survey exists
        if (self.survey_type == SurveyTypes.None):
            raise SIDDException('survey is required for creating mapping scheme')        
        # try to create ms using random
        try: 
            use_sampling = self.operator_options['stratified.sampling']
            return self._build_ms(isEmpty=False, useSampling=use_sampling)
        except Exception as err:
            self._build_ms(isEmpty=True)
            raise SIDDException('Unable to create Mapping Scheme:%s' % str(err))

    @logAPICall
    def create_empty_ms(self):
        # build mapping scheme
        return self._build_ms(isEmpty=True)

    @logAPICall
    def export_data(self):
        builder = WorkflowBuilder(self.operator_options)
        try:
            export_workflow = builder.build_export_workflow(self)
            # process workflow 
            for step in export_workflow.nextstep():
                step.do_operation()
            logAPICall.log('data export completed', logAPICall.INFO)            
        except WorkflowException:
            return False
        except Exception as err:
            logAPICall.log(err, logAPICall.ERROR)
            return False
    
    @logAPICall
    def export_ms_leaves(self, folder):
        if self.ms is None:
            raise SIDDException('Mapping Scheme is required for this action')
        
        builder= WorkflowBuilder(self.operator_options)
        try:
            export_workflow = builder.build_export_distribution_workflow(self, folder)
            # process workflow
            for step in export_workflow.nextstep():
                step.do_operation()
            logAPICall.log('data export completed', logAPICall.INFO)
        except WorkflowException:
            return False
        except Exception as err:
            logAPICall.log(err, logAPICall.ERROR)
            return False
    
    @logAPICall
    def verify_result(self):
        builder = WorkflowBuilder(self.operator_options)
        try:
            verify_workflow = builder.build_verify_result_workflow(self)
            # process workflow
            for step in verify_workflow.nextstep():
                step.do_operation()
            
            self.quality_reports={}
            if verify_workflow.operator_data.has_key('frag_report'):
                self.quality_reports['fragmentation'] = verify_workflow.operator_data['frag_report'].value
            if verify_workflow.operator_data.has_key('count_report'):
                self.quality_reports['count'] = verify_workflow.operator_data['count_report'].value
            logAPICall.log('result verification completed', logAPICall.INFO)
        except WorkflowException:
            return False
        except Exception as err:
            logAPICall.log(err, logAPICall.ERROR)
            return False

    # project database access methods
    ##################################
    
    @logAPICall
    def sync(self, direction=SyncModes.Read):
        """ synchorize data with DB """
        if self.project_file is None or self.db is None:
            raise SIDDProjectException(ProjectErrors.FileNotSet)
        
        if (direction == SyncModes.Read):
            logAPICall.log("reading existing datasets from DB", logAPICall.DEBUG)
            
            # load footprint
            _fp_type = self._get_project_data('data.footprint')
            if _fp_type is None:
                self.footprint = None
                self.fp_file = None
                self.fp_type = FootprintTypes.None
            else:
                if (_fp_type == str(FootprintTypes.FootprintHt)):
                    self.set_footprint(FootprintTypes.FootprintHt,
                                       self._get_project_data('data.footprint.file'),
                                       self._get_project_data('data.footprint.ht_field'))
                else:
                    self.set_footprint(FootprintTypes.Footprint,
                                       self._get_project_data('data.footprint.file'))
            # load survey
            _survey_type = self._get_project_data('data.survey')
            if _survey_type is None:
                self.survey = None
                self.survey_file = None
                self.survey_type = SurveyTypes.None
            else:                
                if self._get_project_data('data.survey.is_complete') == 'True':
                    self.set_survey(SurveyTypes.CompleteSurvey,
                                    self._get_project_data('data.survey.file'))
                else:
                    self.set_survey(SurveyTypes.SampledSurvey,
                                    self._get_project_data('data.survey.file'))
            
            # load zone
            _zone_type = self._get_project_data('data.zones')
            if _zone_type is None:
                self.zones = None
                self.zone_file = None                
                self.zone_type = ZonesTypes.None
            else:
                if _zone_type == str(ZonesTypes.Landuse):                    
                    self.set_zones(ZonesTypes.Landuse,
                                   self._get_project_data('data.zones.file'),
                                   self._get_project_data('data.zones.class_field'))
                else:
                    self.set_zones(ZonesTypes.LanduseCount,
                                   self._get_project_data('data.zones.file'),
                                   self._get_project_data('data.zones.class_field'),
                                   self._get_project_data('data.zones.count_field'))
            # load output type
            _output_type = self._get_project_data('data.output')
            if _output_type == "Zone":
                self.output_type = OutputTypes.Zone
            else:
                self.output_type = OutputTypes.Grid
            
            # load mapping scheme
            _ms_str = self._get_project_data('data.ms')
            if _ms_str is not None:
                self.ms = MappingScheme(None)
                self.ms.from_text(_ms_str)

            use_sampling = self._get_project_data('stratified.sampling')
            if use_sampling is None:
                self.operator_options['stratified.sampling']=True   # default to use sampling method
            else:
                self.operator_options['stratified.sampling']= (use_sampling == "True")
                
            # load taxonomy related options
            attr_order = self._get_project_data('attribute.order')
            if attr_order is not None:
                self.operator_options['attribute.order'] = json.loads(attr_order)                
            for attr in self.operator_options['taxonomy'].attributes:
                _attr_options = self._get_project_data(attr.name)
                if _attr_options is not None:
                    self.operator_options[attr.name] = json.loads(_attr_options)
               
            extrapolation = self._get_project_data("proc.extrapolation")
            if extrapolation is not None:
                # NOTE: converting extrapolation to enum is required
                #       because comparison of str vs. enum is not valid            
                self.operator_options["proc.extrapolation"] = makeEnum(ExtrapolateOptions, extrapolation)
            else:
                self.operator_options["proc.extrapolation"] = ExtrapolateOptions.RandomWalk
            
            # load export settings 
            export_type = self._get_project_data('export.type')
            if export_type is not None:
                self.export_type = makeEnum(ExportTypes, export_type)
            export_path = self._get_project_data('export.path')
            if export_path is not None:
                self.export_path = export_path
            
        else:
            if not self.require_save:
                logAPICall.log("nothing changed since last save", logAPICall.DEBUG)
                return 
                
            logAPICall.log("store existing datasets into DB", logAPICall.DEBUG)            
            # store footprint            
            if self.fp_type == FootprintTypes.None:
                self._save_project_data('data.footprint', None)
                self._save_project_data('data.footprint.file', None)
                self._save_project_data('data.footprint.ht_field', None)
            else:
                self._save_project_data('data.footprint', self.fp_type)
                self._save_project_data('data.footprint.file', self.fp_file)
                if self.fp_type == FootprintTypes.FootprintHt:
                    self._save_project_data('data.footprint.ht_field', self.fp_ht_field)
                else:
                    self._save_project_data('data.footprint.ht_field', None)
                
            # store survey
            if self.survey_type == SurveyTypes.None:
                self._save_project_data('data.survey', None)
                self._save_project_data('data.survey.file', None)
            else:
                self._save_project_data('data.survey', self.survey_type)
                self._save_project_data('data.survey.file', self.survey_file)
                self._save_project_data('data.survey.is_complete', (self.survey_type == SurveyTypes.CompleteSurvey))

            # store zone
            if self.zone_type == ZonesTypes.None:
                self._save_project_data('data.zones', None)
                self._save_project_data('data.zones.file', None)
                self._save_project_data('data.zones.class_field', None)
                self._save_project_data('data.zones.count_field', None)
            else:
                self._save_project_data('data.zones', self.zone_type)
                self._save_project_data('data.zones.file', self.zone_file)
                self._save_project_data('data.zones.class_field', self.zone_field)
                if self.zone_type == ZonesTypes.LanduseCount:
                    self._save_project_data('data.zones.count_field', self.zone_count_field)
                else:
                    self._save_project_data('data.zones.count_field', None)
            
            # store output type
            self._save_project_data('data.output', self.output_type)
            
            # store mapping scheme
            if self.ms is None:
                self._save_project_data('data.ms', None)
            else:
                self._save_project_data('data.ms', self.ms.to_xml())
            
            if self.operator_options.has_key('stratified.sampling'):
                self._save_project_data('stratified.sampling',  self.operator_options['stratified.sampling'])            

            # save taxonomy order 
            if self.operator_options.has_key('attribute.order'):
                self._save_project_data('attribute.order',  json.dumps(self.operator_options['attribute.order']))
            for attr in self.operator_options['taxonomy'].attributes:
                if self.operator_options.has_key(attr.name):
                    self._save_project_data(attr.name, json.dumps(self.operator_options[attr.name]))
            
            # save processing attributes
            if self.operator_options.has_key("proc.extrapolation"):
                self._save_project_data("proc.extrapolation", self.operator_options["proc.extrapolation"])
            
            # save export settings
            self._save_project_data('export.type', getattr(self, 'export_type', None))
            self._save_project_data('export.path', getattr(self, 'export_path', None))
            
            # flush to disk
            self.db.sync()
        
        # after each sync 
        # project is same as db, so save no longer required
        self.require_save = False

    # bsddb help functions
    ##################################    
    def _get_project_data(self, attrib):        
        if self.db.has_key(attrib):
            logAPICall.log('read from db %s => %s ' % (attrib, str(self.db[attrib])[0:25]), logAPICall.DEBUG_L2)
            return self.db[attrib]
        else:
            logAPICall.log('%s does not exist in db' % attrib, logAPICall.DEBUG_L2)
            return None

    def _save_project_data(self, attrib, value):
        if value is None:
            # delete
            logAPICall.log('delete from db %s ' % (attrib), logAPICall.DEBUG_L2)
            if self.db.has_key(attrib):
                del self.db[attrib]
        else:
            logAPICall.log('save to db %s => %s ' % (attrib, str(value)[0:25]), logAPICall.DEBUG_L2)
            self.db[attrib]=str(value)

    # protected helper functions
    ##################################
    
    def _load_data(self, input_param, layer, output_file):
        input_file = getattr(self, input_param, None)
        if input_file is not None:
            builder = WorkflowBuilder(self.operator_options)
            try:
                # create workflow
                if input_param == 'fp_file':
                    workflow = builder.build_load_fp_workflow(self)
                elif input_param == 'zone_file':
                    workflow = builder.build_load_zones_workflow(self)
                elif input_param == 'survey_file':
                    workflow = builder.build_load_survey_workflow(self)
                else:
                    raise Exception('Data Type Not Recognized %s' % input_param)
                
                if not workflow.ready:
                    raise Exception('Cannot load data with %s' % input_param)
                workflow.process()
                
                logAPICall.log('data file %s loaded' % input_file, logAPICall.INFO)
                return workflow.operator_data[layer].value, workflow.operator_data[output_file].value
            except WorkflowException:
                logAPICall.log('Error Loading file %s' % input_file, logAPICall.ERROR)
            except Exception as err:
                logAPICall.log(err, logAPICall.ERROR)
                return False           

    def _build_ms(self, isEmpty=False, useSampling=False):
        """ create mapping scheme """
        builder = WorkflowBuilder(self.operator_options)
        # force reload existing survey
        self.survey = None
        
        # create workflow 
        if useSampling:
            ms_workflow = builder.build_sampling_ms_workflow(self)
        else:
            ms_workflow = builder.build_ms_workflow(self, isEmpty)
        if not ms_workflow.ready:
            raise SIDDException(ms_workflow.errors)
        
        # process workflow 
        for step in ms_workflow.nextstep():
            step.do_operation()
        self.ms = ms_workflow.operator_data['ms'].value
        if useSampling:
            self.zone_stats = ms_workflow.operator_data['zone_stats'].value
        for zone, stats in self.ms.assignments():
            stats.get_leaves(True)
            
        logAPICall.log('mapping scheme created', logAPICall.INFO)
        self.require_save = True
