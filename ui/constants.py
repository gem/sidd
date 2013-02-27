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
# Version: $Id: constants.py 22 2012-10-26 23:29:52Z zh $

"""
UI constants
"""
from utils.system import get_app_dir
from sidd.logger import SIDDLogging

# decorator and loggeer for UI function calls
logUICall = SIDDLogging('ui')

# constant file names
###########################
FILE_MS_DB = '%s/data/ms.db' % get_app_dir()

# constant UI widget padding
UI_PADDING = 10

#####################
SIDD_UI_STRINGS = {
    # Errors
    ######################    
    "app.error.title":'Application Error',
    "app.error.unexpected":'Unexpected Error',
    "app.error.project.missing":'Must open project or create new project',
    "app.error.model":'Error Processing Request',
    'app.error.ui':'Error Processing Request',
    'app.error.file.does.not.exist':'File %s cannot be found',
    'app.error.path.is.null':'Path cannot be null',
    'app.warning.title':'Warning',    
    # project errors
    ######################
    "project.error.NeedsCount":'Building count must be set either through footprint or Zone with count',
    "project.error.NeedsZone":'Homogenous zone is needed',
    "project.error.NeedsMS":'Mapping Scheme is needed',
    "project.error.NeedSurvey":'Survey data is required',
    "project.error.NoActionDefined":'No action is defined for type of data provided',
    "project.error.NotEnoughData":'No action is defined for type of data provided',
    # common messages
    ######################
    "app.extension.shapefile":'Shapefile (*.shp)',
    "app.extension.csv":'CSV data(*.csv)',
    "app.extension.db":'DB file(*.db)',
    "app.extension.kml":'KML (*.kml)',
    "app.extension.xml":'XML(*.xml)',
    "app.extension.nrml":'NRML(*.xml)',
    "app.extension.gemdb":'GEMDB(*.gemdb)',
    # common UI messages
    ######################    
    "app.file.select":'Select file',
    "app.folder.select":'Select folder',
    "app.file.button":'...',
    "app.dialog.button.ok":"OK",
    "app.dialog.button.cancel":"Cancel",
    "app.dialog.button.close":"Close",
    "app.dialog.button.apply":"Apply",
    "app.popup.delete.confirm":"",
    # status messages
    ######################
    "app.status.ready":'Application ready',
    "app.status.project.created":'Project Created',  
    "app.status.project.loaded":'Project Loaded',
    "app.status.project.saved":'Project Saved',
    "app.status.project.closed":'Project Closed',
    "app.status.input.verified":'Input Verification Completed',
    "app.status.ms.created":'Mapping Scheme Created',
    "app.status.ms.modified":'Mapping Scheme Modified',
    "app.status.ms.exported":'Building Distribution Exported',
    "app.status.exposure.created":'Exposure Created',    
    "app.status.cancelled":'Process Cancelled',
    "app.status.processing":'Processing ...',
    # common UI messages
    ######################        
    "app.mslibrary.default":"PAGER",
    "app.mslibrary.user.multilevel":"User-defined Multi-level",
    "app.mslibrary.user.singlelevel":"User-defined Single Level",
    # main application window
    ######################
    "app.window.title":'SIDD',
    # menu
    "app.window.menu.file":'File',
    "app.window.menu.view":'View',
    "app.window.menu.help":'Help',
    "app.window.menu.file.create":'Create Project ...',
    "app.window.menu.file.open":'Open Project ...',
    "app.window.menu.file.save":'Save Project',
    "app.window.menu.file.exit":'Exit',
    "app.window.menu.view.input":'Data Input',
    "app.window.menu.view.ms":'Mapping Schemes',
    "app.window.menu.view.result":'Preview',
    "app.window.menu.help.about":'About',
    # tabs
    "app.window.tab.input":'Data Input',
    "app.window.tab.ms":'Mapping Scheme',
    "app.window.tab.mod":'Modifiers',
    "app.window.tab.result":'Preview',
    # messages
    "app.window.msg.project.create":'Create New Project',
    "app.window.msg.project.open":'Open Project File',
    # main application window / data input tab
    ######################
    # title
    "widget.input.header.title":'Define required input data',
    "widget.input.header.description":'Input data required for exposure/mapping scheme creation',
    # survey
    "widget.input.survey.title":'Survey & field data',
    "widget.input.survey.description":'What type of survey / field data do you have?',
    "widget.input.survey.file.open":'Open Survey File',
    "widget.input.survey.option1":'No Data',
    "widget.input.survey.option2":'Complete building stock/survey area',
    "widget.input.survey.option3":'Sampled buildings from survey area',
    "widget.input.survey.file.missing":'Survey File not specified',
    # footprint
    "widget.input.fp.title":'Building footprint data',
    "widget.input.fp.description":'What type of data do you have for building footprints?',
    "widget.input.fp.file.open":'Open Footprint File',
    "widget.input.fp.projection":'Verify projection',
    "widget.input.fp.storyfield":'Select field containing number of stories',
    "widget.input.fp.op1":'No Data',
    "widget.input.fp.op2":'Building footprints with number of stories',
    "widget.input.fp.op3":'Building footprints without number of stories',
    "widget.input.fp.file.missing":'Footprint File not specified',
    "widget.input.fp.storyfield.missing":'Number of stories field not specified',
    # zones
    "widget.input.zone.title":'Homogenous zones data',
    "widget.input.zone.description":'What type of data do you have for zones?',
    "widget.input.zone.file.open":'Open Homogenous Zone File',
    "widget.input.zone.projection":'Verify projection',
    "widget.input.zone.zonefield":'Select field containing zone identifier',
    "widget.input.zone.countfield":'Select field containing building count',
    "widget.input.zone.op1":'No Data',
    "widget.input.zone.op2":'Homogenous zones',
    "widget.input.zone.op3":'Homogenous zones with building count',
    "widget.input.zone.file.missing":'Homogenous zone input file not specified',
    "widget.input.zone.zonefield.missing":'Land use/class field not specified',
    "widget.input.zone.countfield.missing":'Building count field not specified',
    # aggregation
    "widget.input.agg.title":'Aggregation',
    "widget.input.agg.file.open":'Open GED compatible Grid',
    "widget.input.agg.description":'How do you wish to aggregate your output data?',
    "widget.input.agg.op1":'Output into defined zones',
    "widget.input.agg.op2":'GED Compatible 30 arc-second grid',
    # data verification
    "widget.input.verify.title":'You have supplied the following types of data',
    "widget.input.verify.button":'Verify input data',
    "widget.input.verify.footprint":'Footprint',
    "widget.input.verify.survey":'Survey',
    "widget.input.verify.zones":'Zone',
    "widget.input.verify.aggregation":'Output data aggregation',
    "widget.input.verify.agg.zone":'Zone',
    "widget.input.verify.agg.grid":'GED Grid',
    # verification messages
    "widget.input.verify.sucess":'Datasets complete\nProceed to create exposure',
    "widget.input.verify.datarequired":'Following dataset required for building exposure',
    "widget.input.verify.noaction":'No action is defined for type of data provided',
    "widget.input.verify.unknownerror":'Unknown error while verifying input data',    
    # main application window / ms tab
    ######################
    "widget.ms.title":'Manage Mapping Schemes',
    "widget.ms.tree.title":'Mapping Scheme',
    "widget.ms.distribution.title":'Building Distribution',
    "widget.ms.distribution.zones":'Select zone',
    "widget.ms.library.title":'Mapping Scheme Library',
    "widget.ms.library.regions":'Region',
    "widget.ms.library.types":'Source',    
    "widget.ms.library.names":'Available Mapping Schemes',
    "widget.ms.library.date":'Date Created',
    "widget.ms.library.quality":'Percentage of',
    "widget.ms.library.datasource":'Data Source',
    "widget.ms.library.notes":'Use Notes',
    "widget.ms.library.enable":'Enable Mapping Scheme Library',
    "widget.ms.library.delete.denied":'Only allowed to delete user-defined mapping scheme',
    "widget.ms.modifier":'Modifiers',
    "widget.ms.build":'Build Exposure',
    "widget.ms.warning.deletebranch":'Deleting a node cannot be undone.\nAre you sure that you want to continue?',
    "widget.ms.warning.node.required":'Node from Mapping Scheme Tree must be selected first',
    "widget.ms.warning.node.invalid":'Selected Node from Mapping Scheme Tree is Invalid',
    # main application window / mod tab
    ######################
    "widget.mod.title":'Manage Modifiers',
    "widget.mod.build":'Build Exposure',
    "widget.mod.warning.delete":'Deleting modifier cannot be undone.\nAre you sure that you want to continue?',
    "widget.mod.tableheader.zone":'Zone',
    "widget.mod.tableheader.path":'Building Type',
    "widget.mod.tableheader.value":'Value',
    "widget.mod.tableheader.weight":'Percentage',
    # main application window / result tab
    ######################
    "widget.result.title":'Preview Exposure',
    "widget.result.layers.selector":"Selected Layer",    
    "widget.result.layer.exposure":"Exposure",
    "widget.result.layer.survey":"Surveys",
    "widget.result.layer.footprint":"Footprints",
    "widget.result.layer.zones":"Zones",
    "widget.result.layers.theme.title":"Change Thematic for %s",
    "widget.result.info.notfound":'Nothing not found at location',
    "widget.result.export.title":'Export Exposure',
    "widget.result.export.format":'Select Export Data Format',
    "widget.result.export.path.dialog":'Select Export Destination Folder',
    "widget.result.export.button":'Export',
    # data quality messages
    "widget.result.dq.title":'Data Quality Tests',
    "widget.result.dq.warning":'Warning',
    "widget.result.dq.total_tests":'%s tests run on result',
    "widget.result.dq.method":'Exposure generated using %s method',
    "widget.result.dq.tests.count":'Verifying Building Count',
    "widget.result.dq.tests.count.total_source":'Total Buildings in Source Data: %.0f',
    "widget.result.dq.tests.count.total_exposure":'Total Buildings in Generated Exposure: %.0f',
    "widget.result.dq.tests.fragmentation":'Number of Fractional Records',
    "widget.result.dq.tests.fragmentation.record_count":'Total Records in Generated Exposure: %.0f',
    "widget.result.dq.tests.fragmentation.fraction_count":'Total Records with Fractional Building Count: %.0f',
    # about dialog
    ######################
    'dlg.about.window.title': 'About SIDD',
    # build progress dialog
    ######################
    "dlg.apply.window.title": 'Building Exposure',
    "dlg.apply.message": 'SIDD is applying mapping schemes and generating exposure.\nThis may takes some time. Plese check the console below to see what is being processed.',
    # build ms dialog
    ######################
    "dlg.buildms.title": 'Create Mapping Scheme',
    "dlg.buildms.attributes": 'Taxonomy Attributes',
    "dlg.buildms.option.empty": 'Create Empty Mapping Scheme',
    "dlg.buildms.option.survey": 'Build from Survey Data',
    # edit mapping scheme branch dialog
    ######################
    "dlg.msbranch.edit.window.title":'Edit Mapping Scheme Branch',
    "dlg.msbranch.edit.title":'Edit Mapping Scheme Branch', 
    "dlg.msbranch.edit.tableheader.value":'Value',
    "dlg.msbranch.edit.tableheader.weight":'Percentage',
    "dlg.msbranch.edit.attribute.name":'Attribute Name',
    "dlg.msbranch.edit.weight.total":'Sum of Weights',
    "dlg.msbranch.edit.warning.invalidweight":'weight value must be a numeric value between 0 and 100',
    "dlg.msbranch.edit.warning.node.required":'Node from Mapping Scheme Tree must be selected first',
    # save mapping scheme dialog
    ######################
    "dlg.savems.window.title":'Save Mapping Scheme',
    "dlg.savems.title.tree":'Save Mapping Scheme Tree',
    "dlg.savems.title.branch":'Save Mapping Scheme Branch',
    "dlg.savems.date":'Date Created',
    "dlg.savems.source":'Source',
    "dlg.savems.quality":'Percentage of',
    "dlg.savems.notes":'Notes',
    "dlg.savems.name":'Name',
    "dlg.savems.type":'Source',
    "dlg.savems.region":'Region',
    # secondary modifiers dialog
    ######################
    "dlg.mod.window.title":'Secondary Modifiers',
    "dlg.mod.title":'Manage Secondary Modifiers',
    "dlg.mod.zone":'Zone',
    "dlg.mod.mod_values":'Modifier Values',
    "dlg.mod.level1":'Level1',
    "dlg.mod.level2":'Level2',
    "dlg.mod.level3":'Level3',
    "dlg.mod.build":'Build From Survey',
    # attribute ranges dialog
    ######################
    "dlg.attr.range.window.title":'Attribute Ranges',
    "dlg.attr.title":'Attribute Ranges',
    "dlg.attr.min_value":'Minimum Values',
    "dlg.attr.max_value":'Maximum Values',
    "dlg.attr.value.error":'Only numeric value is accepted',
    # processing options dialog    
    ######################
    "dlg.options.ep.window.title":'Processing Options',
    "dlg.options.ep.title":'Extrapolation Options',
    "dlg.options.ep.random":'Monte-Carlo Simulation',
    "dlg.options.ep.fraction":'Building Distribution Fraction',
    "dlg.options.ep.fraction.rounded":'Building Distribution Fraction Rounded',
    "dlg.options.param.window.title":'Additional Parameters',    
    "dlg.options.param.title":'Additional Parameters',
    "dlg.options.param.apply":'Generate additional parameters',
    "dlg.options.param.pop":'Average number of people per building',
    "dlg.options.param.sqft":'Average Size of building',
    "dlg.options.param.repval":'Average replacemnet cost per Sqft',
    # main application window / mod tab
    ######################
    "help.input.footprint":"""Footprint data""",
    "help.input.survey":"""Survey data""",
    "help.input.zones":"""Zones data""",
    "help.input.output":"""Output Aggregation""",
    # operator processing messages
    ######################
    "message.sidd.operator.loaders.footprint.FootprintLoader":'Loading Building Footprints ...',
    "message.sidd.operator.loaders.footprint.FootprintHtLoader":'Loading Building Footprints with Heights  ...',
    "message.sidd.operator.loaders.ms.MappingSchemeLoader":'Loading Mapping Scheme  ...',
    "message.sidd.operator.loaders.survey.GEMDBSurveyLoader":'Loading Survey from GEMDB ...',
    "message.sidd.operator.loaders.survey.CSVSurveyLoader":'Loading Survey from CSV ...',
    "message.sidd.operator.loaders.zones.ZoneLoader":'Loading Zones ...',
    "message.sidd.operator.loaders.zones.ZoneCountLoader":'Loading Zones with Building Counts ...',
    "message.sidd.operator.processors.aggregate.FootprintAggregator":'Counting Footprints for GEM grids ...',
    "message.sidd.operator.processors.exposure.GridMSApplier":'Applying Mapping Scheme ...',
    "message.sidd.operator.processors.exposure.ZoneMSApplier":'Applying Mapping Scheme ...',
    "message.sidd.operator.processors.exposure.SurveyAggregator":'Aggregating Survey ...',    
    "message.sidd.operator.processors.grid.GridWriter":'Generating GEM grid ...',
    "message.sidd.operator.processors.grid.GridFromRegionWriter":'Generating GEM grid ...',
    "message.sidd.operator.processors.grid.GridGeometryWriter":'Generating GEM grid Geometry ...',
    "message.sidd.operator.processors.join.ZoneGridMerger":'Assigning GEM Grids to Zones ...',
    "message.sidd.operator.processors.join.ZoneFootprintMerger":'Assigning Footprints to Zones ...',
    "message.sidd.operator.processors.join.ZoneFootprintCounter":'Counting Footprints to in Zones ...',
    "message.sidd.operator.processors.ms_create.EmptyMSCreator":'Creating Empty Mapping Scheme ...',
    "message.sidd.operator.processors.ms_create.EmptyZonesMSCreator":'Creating Empty Mapping Scheme ...',
    "message.sidd.operator.processors.ms_create.SurveyZonesMSCreator":'Creating Mapping Scheme from Survey ...',
    "message.sidd.operator.processors.ms_create.SurveyOnlyMSCreator":'Creating Mapping Scheme from Survey ...',
    "message.sidd.operator.verify.exposure.ExposureFragmentationAnalyzer":'Performing Building Count Fragmentation Analysis ...',
    "message.sidd.operator.verify.exposure.ExposureZoneCountAnalyzer":'Performing Total Building Count Analysis ...',
    "message.sidd.operator.verify.exposure.ExposureFootprintCountAnalyzer":'Performing Total Building Count Analysis ...',
    "message.sidd.operator.writers.exposure.ExposureSHPWriter":'Writings Exposure to Shapefile ...',
    "message.sidd.operator.writers.exposure.ExposureCSVWriter":'Writings Exposure to CSV ...',
    "message.sidd.operator.writers.exposure.ExposureKMLWriter":'Writings Exposure to KML ...',
    "message.sidd.operator.writers.exposure.ExposureNRMLWriter":'Writings Exposure to NRML ...',    
    "message.sidd.operator.writers.ms.MSLeavesCSVWriter":'Writings Mapping Scheme to CSV ...',
}

def get_ui_string(key):
    return SIDD_UI_STRINGS[key] if SIDD_UI_STRINGS.has_key(key) else  ""

