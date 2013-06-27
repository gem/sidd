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
constants used by UI
"""
from PyQt4.QtGui import QApplication
from utils.system import get_app_dir
from ui.helper.logger import SIDDUILogging

# decorator and loggeer for UI function calls
logUICall = SIDDUILogging('ui')

# constant file names
###########################
FILE_MS_DB = '%s/data/ms.db' % get_app_dir()

# constant UI widget padding
UI_PADDING = 10

# constant display text
# QApplication translate can be used to generate 
# translation files using the pylupdate4 
#####################
SIDD_UI_STRINGS = {
    # Errors
    ######################
    "app.error.title": QApplication.translate('app.error',  'Error', None, QApplication.UnicodeUTF8),
    "app.error.unexpected":QApplication.translate('app.error', 'Unexpected Error', None, QApplication.UnicodeUTF8),
    "app.error.project.missing":QApplication.translate('app.error', 'Must open project or create new project', None, QApplication.UnicodeUTF8),
    "app.error.model":QApplication.translate('app.error', 'Error Processing Request', None, QApplication.UnicodeUTF8),
    "app.error.ui":QApplication.translate('app.error', 'Error Processing Request', None, QApplication.UnicodeUTF8),
    "app.error.file.does.not.exist":QApplication.translate('app.error', 'File %s cannot be found', None, QApplication.UnicodeUTF8),
    "app.error.path.is.null":QApplication.translate('app.error', 'Path cannot be null', None, QApplication.UnicodeUTF8),
    "app.warning.title":QApplication.translate('app.error', 'Warning', None, QApplication.UnicodeUTF8),    
    # project errors
    ######################
    "project.error.NeedsCount":QApplication.translate('project.error', 'Building count must be set either through footprint or Zone with count', None, QApplication.UnicodeUTF8),
    "project.error.NeedsZone":QApplication.translate('project.error', 'Homogenous zone is needed', None, QApplication.UnicodeUTF8),
    "project.error.NeedsMS":QApplication.translate('project.error', 'Mapping Scheme is needed', None, QApplication.UnicodeUTF8),
    "project.error.NeedSurvey":QApplication.translate('project.error', 'Survey data is required', None, QApplication.UnicodeUTF8),
    "project.error.NoActionDefined":QApplication.translate('project.error', 'No action is defined for type of data provided', None, QApplication.UnicodeUTF8),
    "project.error.NotEnoughData":QApplication.translate('project.error', 'Missing required data for exposure processing', None, QApplication.UnicodeUTF8),
    "project.error.sampling":QApplication.translate('project.error', """Error Creating Mapping Scheme with Stratified Sampling method:\n%s\nPlease use deselect "Use Stratified sampling" option and try again.""", None, QApplication.UnicodeUTF8),
    # common messages
    ######################
    "app.extension.shapefile":QApplication.translate('app.extension', 'Shapefile (*.shp)', None, QApplication.UnicodeUTF8),
    "app.extension.csv":QApplication.translate('app.extension', 'CSV file(*.csv)', None, QApplication.UnicodeUTF8),
    "app.extension.db":QApplication.translate('app.extension', 'SIDD file(*.sidd)', None, QApplication.UnicodeUTF8),
    "app.extension.kml":QApplication.translate('app.extension', 'KML (*.kml)', None, QApplication.UnicodeUTF8),
    "app.extension.xml":QApplication.translate('app.extension', 'XML(*.xml)', None, QApplication.UnicodeUTF8),
    "app.extension.nrml":QApplication.translate('app.extension', 'NRML(*.xml)', None, QApplication.UnicodeUTF8),
    "app.extension.gemdb":QApplication.translate('app.extension', 'DB3(*.db3)', None, QApplication.UnicodeUTF8),
    # common UI messages
    ######################    
    "app.file.select":QApplication.translate('app.common', 'Select file', None, QApplication.UnicodeUTF8), 
    "app.folder.select":QApplication.translate('app.common', 'Select folder', None, QApplication.UnicodeUTF8),
    "app.file.button":QApplication.translate('app.common', '...', None, QApplication.UnicodeUTF8),
    "app.dialog.button.ok":QApplication.translate('app.common', 'OK', None, QApplication.UnicodeUTF8),
    "app.dialog.button.cancel":QApplication.translate('app.common', 'Cancel', None, QApplication.UnicodeUTF8),
    "app.dialog.button.go":QApplication.translate('app.common', 'Go', None, QApplication.UnicodeUTF8),
    "app.dialog.button.close":QApplication.translate('app.common', 'Close', None, QApplication.UnicodeUTF8),
    "app.dialog.button.apply":QApplication.translate('app.common', 'Apply', None, QApplication.UnicodeUTF8),
    # status messages
    ######################
    "app.status.ready":QApplication.translate('app.status',' ready', None, QApplication.UnicodeUTF8),
    "app.status.project.created":QApplication.translate('app.status', 'Project Created', None, QApplication.UnicodeUTF8),
    "app.status.project.loading":QApplication.translate('app.status', 'Loading Project ...', None, QApplication.UnicodeUTF8),  
    "app.status.project.loaded":QApplication.translate('app.status', 'Project Loaded', None, QApplication.UnicodeUTF8),
    "app.status.project.saved":QApplication.translate('app.status', 'Project Saved', None, QApplication.UnicodeUTF8),
    "app.status.project.closed":QApplication.translate('app.status', 'Project Closed', None, QApplication.UnicodeUTF8),
    "app.status.input.verified":QApplication.translate('app.status', 'Input Verification Completed', None, QApplication.UnicodeUTF8),
    "app.status.ms.created":QApplication.translate('app.status', 'Mapping Scheme Created', None, QApplication.UnicodeUTF8),
    "app.status.ms.modified":QApplication.translate('app.status', 'Mapping Scheme Modified', None, QApplication.UnicodeUTF8),
    "app.status.ms.exported":QApplication.translate('app.status', 'Building Distribution Exported', None, QApplication.UnicodeUTF8),
    "app.status.exposure.created":QApplication.translate('app.status', 'Exposure Created', None, QApplication.UnicodeUTF8),    
    "app.status.exposure.exported":QApplication.translate('app.status', 'Exposure Exported', None, QApplication.UnicodeUTF8),
    "app.status.cancelled":QApplication.translate('app.status', 'Process Cancelled', None, QApplication.UnicodeUTF8),
    "app.status.processing":QApplication.translate('app.status', 'Processing ...', None, QApplication.UnicodeUTF8),
    "app.confirm.title":QApplication.translate('app.status', 'SIDD', None, QApplication.UnicodeUTF8),
    "app.confirm.build.exposure":QApplication.translate('app.status', 'Continue to build exposure?', None, QApplication.UnicodeUTF8),
    # common UI messages
    ######################
    "app.mslibrary.default":QApplication.translate('app.mslibrary', 'PAGER', None, QApplication.UnicodeUTF8),
    "app.mslibrary.user.multilevel":QApplication.translate('app.mslibrary', 'User-defined Multi-level', None, QApplication.UnicodeUTF8),
    "app.mslibrary.user.singlelevel":QApplication.translate('app.mslibrary', 'User-defined Single Level', None, QApplication.UnicodeUTF8),
    # main window
    ######################
    # tabs
    "app.window.tab.input":QApplication.translate('app.window', 'Data Input', None, QApplication.UnicodeUTF8),
    "app.window.tab.ms":QApplication.translate('app.window', 'Mapping Scheme', None, QApplication.UnicodeUTF8),
    "app.window.tab.mod":QApplication.translate('app.window', 'Modifiers', None, QApplication.UnicodeUTF8),
    "app.window.tab.result":QApplication.translate('app.window', 'Preview', None, QApplication.UnicodeUTF8),
    # messages
    "app.window.msg.project.create":QApplication.translate('app.window', 'Create New Project', None, QApplication.UnicodeUTF8),
    "app.window.msg.project.open":QApplication.translate('app.window', 'Open Project File', None, QApplication.UnicodeUTF8),
    "app.window.msg.project.not_saved":QApplication.translate('app.window', 'Project has unsaved changes', None, QApplication.UnicodeUTF8),
    "app.window.msg.project.save_or_not":QApplication.translate('app.window', 'Do you want to save these changes', None, QApplication.UnicodeUTF8),
    # main window / data input tab
    ######################
    # survey
    "widget.input.survey.file.open":QApplication.translate('app.input', 'Open Survey File', None, QApplication.UnicodeUTF8),
    "widget.input.survey.file.missing":QApplication.translate('app.input', 'Survey File not specified', None, QApplication.UnicodeUTF8),
    # footprint
    "widget.input.fp.file.open":QApplication.translate('app.input', 'Open Footprint File', None, QApplication.UnicodeUTF8),
    "widget.input.fp.file.missing":QApplication.translate('app.input', 'Footprint File not specified', None, QApplication.UnicodeUTF8),
    "widget.input.fp.storyfield.missing":QApplication.translate('app.input', 'Number of stories field not specified', None, QApplication.UnicodeUTF8),
    # zones
    "widget.input.zone.file.open":QApplication.translate('app.input', 'Open Homogeneous Zone File', None, QApplication.UnicodeUTF8),
    "widget.input.zone.file.missing":QApplication.translate('app.input', 'Homogeneous zone input file not specified', None, QApplication.UnicodeUTF8),
    "widget.input.zone.zonefield.missing":QApplication.translate('app.input', 'Land use/class field not specified', None, QApplication.UnicodeUTF8),
    "widget.input.zone.countfield.missing":QApplication.translate('app.input', 'Building count field not specified', None, QApplication.UnicodeUTF8),
    # pop grid
    "widget.input.popgrid.file.open":QApplication.translate('app.input', 'Open Population Grid File', None, QApplication.UnicodeUTF8),
    "widget.input.popgrid.file.missing":QApplication.translate('app.input', 'Population Grid file not specified', None, QApplication.UnicodeUTF8),
    "widget.input.popgrid.popfield.missing":QApplication.translate('app.input', 'Population field not specified', None, QApplication.UnicodeUTF8),
    "widget.input.popgrid.poptobldg.missing":QApplication.translate('app.input', 'Average Person per Building not specified', None, QApplication.UnicodeUTF8),
    # verification messages
    "widget.input.verify.sucess":QApplication.translate('app.input', 'Datasets complete\nProceed to create exposure', None, QApplication.UnicodeUTF8),
    "widget.input.verify.datarequired":QApplication.translate('app.input', 'Following dataset required for building exposure', None, QApplication.UnicodeUTF8),
    "widget.input.verify.noaction":QApplication.translate('app.input', 'No action is defined for type of data provided', None, QApplication.UnicodeUTF8),
    "widget.input.verify.unknownerror":QApplication.translate('app.input', 'Unknown error while verifying input data', None, QApplication.UnicodeUTF8),
    # help messages
    # main window / ms tab
    ######################
    "widget.ms.tree.title":QApplication.translate('app.ms', 'Mapping Scheme', None, QApplication.UnicodeUTF8),
    "widget.ms.distribution.title":QApplication.translate('app.ms', 'Building Distribution', None, QApplication.UnicodeUTF8),
    "widget.ms.distribution.value":QApplication.translate('app.ms', 'Value', None, QApplication.UnicodeUTF8),
    "widget.ms.distribution.weight":QApplication.translate('app.ms', 'Percentage', None, QApplication.UnicodeUTF8),
    "widget.ms.distribution.size":QApplication.translate('app.ms', 'Size', None, QApplication.UnicodeUTF8),
    "widget.ms.distribution.cost":QApplication.translate('app.ms', 'Cost', None, QApplication.UnicodeUTF8),
    "widget.ms.distribution.value.desc":QApplication.translate('app.ms', 'Building Type Taxonomy String', None, QApplication.UnicodeUTF8),
    "widget.ms.distribution.weight.desc":QApplication.translate('app.ms', 'Percentage of Exposure', None, QApplication.UnicodeUTF8),
    "widget.ms.distribution.size.desc":QApplication.translate('app.ms', 'Average Size of Building (m2)', None, QApplication.UnicodeUTF8),
    "widget.ms.distribution.cost.desc":QApplication.translate('app.ms', 'Replacement Cost of Size Unit', None, QApplication.UnicodeUTF8),

    "widget.ms.library.title":QApplication.translate('app.ms', 'Mapping Scheme Library', None, QApplication.UnicodeUTF8),
    "widget.ms.library.enable":QApplication.translate('app.ms', 'Enable Mapping Scheme Library', None, QApplication.UnicodeUTF8),
    "widget.ms.library.delete.denied":QApplication.translate('app.ms', 'Only allowed to delete user-defined mapping scheme', None, QApplication.UnicodeUTF8),
    "widget.ms.file.open":QApplication.translate('app.ms', 'Open Mapping Scheme File', None, QApplication.UnicodeUTF8),
    "widget.ms.warning.replace":QApplication.translate('app.ms', 'This will replace current Mapping Scheme.\nAre you sure that you want to continue?', None, QApplication.UnicodeUTF8),
    "widget.ms.warning.deletebranch":QApplication.translate('app.ms', 'Deleting a node cannot be undone.\nAre you sure that you want to continue?', None, QApplication.UnicodeUTF8),
    "widget.ms.warning.node.required":QApplication.translate('app.ms', 'Please select source node from Mapping Scheme library and destination node on Mapping Scheme Tree', None, QApplication.UnicodeUTF8),
    "widget.ms.warning.node.invalid":QApplication.translate('app.ms', 'Selected Node from Mapping Scheme Tree is Invalid', None, QApplication.UnicodeUTF8),
    # main window / mod tab
    ######################
    "widget.mod.warning.delete":QApplication.translate('app.mod', 'Deleting modifier cannot be undone.\nAre you sure that you want to continue?', None, QApplication.UnicodeUTF8),
    "widget.mod.tableheader.zone":QApplication.translate('app.mod', 'Zone', None, QApplication.UnicodeUTF8),
    "widget.mod.tableheader.path":QApplication.translate('app.mod', 'Building Type', None, QApplication.UnicodeUTF8),
    "widget.mod.tableheader.value":QApplication.translate('app.mod', 'Value', None, QApplication.UnicodeUTF8),
    "widget.mod.tableheader.weight":QApplication.translate('app.mod', 'Percentage', None, QApplication.UnicodeUTF8),    
    "widget.mod.button.add":QApplication.translate('app.mod', 'Add Modifier', None, QApplication.UnicodeUTF8),
    "widget.mod.button.delete":QApplication.translate('app.mod', 'Delete Selected Modifier', None, QApplication.UnicodeUTF8),
    "widget.mod.button.edit":QApplication.translate('app.mod', 'Edit Selected Modifier', None, QApplication.UnicodeUTF8),
    # main window / result tab
    ######################
    "widget.result.renderer.settings":QApplication.translate('app.result', 'Layer Rendering Settings', None, QApplication.UnicodeUTF8),
    "widget.result.layer.exposure":QApplication.translate('app.result', 'Exposure', None, QApplication.UnicodeUTF8),
    "widget.result.layer.survey":QApplication.translate('app.result', 'Surveys', None, QApplication.UnicodeUTF8),
    "widget.result.layer.footprint":QApplication.translate('app.result', 'Footprints', None, QApplication.UnicodeUTF8),
    "widget.result.layer.zones":QApplication.translate('app.result', 'Zones', None, QApplication.UnicodeUTF8),
    "widget.result.layer.popgrid":QApplication.translate('app.result', 'Population Grid', None, QApplication.UnicodeUTF8),    
    "widget.result.layers.theme.title":QApplication.translate('app.result', 'Change Thematic for %s', None, QApplication.UnicodeUTF8),
    "widget.result.info.notfound":QApplication.translate('app.result', 'Nothing not found at location', None, QApplication.UnicodeUTF8),
    
    # data quality messages
    "widget.result.dq.title":QApplication.translate('app.result', 'Data Quality Tests', None, QApplication.UnicodeUTF8),
    "widget.result.dq.warning":QApplication.translate('app.result', 'Warning', None, QApplication.UnicodeUTF8),
    "widget.result.dq.total_tests":QApplication.translate('app.result', '%s tests run on result', None, QApplication.UnicodeUTF8),
    "widget.result.dq.method":QApplication.translate('app.result', 'Exposure generated using %s method', None, QApplication.UnicodeUTF8),
    "widget.result.dq.tests.count":QApplication.translate('app.result', 'Verifying Building Count', None, QApplication.UnicodeUTF8),
    "widget.result.dq.tests.count.total_source":QApplication.translate('app.result', 'Total Buildings in Source Data: %.0f', None, QApplication.UnicodeUTF8),
    "widget.result.dq.tests.count.total_exposure":QApplication.translate('app.result', 'Total Buildings in Generated Exposure: %.0f', None, QApplication.UnicodeUTF8),
    "widget.result.dq.tests.count._note":QApplication.translate('app.result', 'NOTE: Distribution from Zone to Grid could cause minor error in total count.', None, QApplication.UnicodeUTF8),
    "widget.result.dq.tests.fragmentation":QApplication.translate('app.result', 'Number of Fractional Records', None, QApplication.UnicodeUTF8),
    "widget.result.dq.tests.fragmentation.record_count":QApplication.translate('app.result', 'Total Records in Generated Exposure: %.0f', None, QApplication.UnicodeUTF8),
    "widget.result.dq.tests.fragmentation.fraction_count":QApplication.translate('app.result', 'Total Records with Fractional Building Count: %.0f', None, QApplication.UnicodeUTF8),
    

    # data input wizard (wizard re-uses a lot of message from widget data input 
    ######################
    "widget.datawizard.window.title":QApplication.translate('app.inputwizard', 'Data Wizard', None, QApplication.UnicodeUTF8),
    # edit mapping scheme branch dialog
    ######################
    "dlg.msbranch.edit.tableheader.value":QApplication.translate('app.msbranch', 'Value', None, QApplication.UnicodeUTF8),
    "dlg.msbranch.edit.tableheader.weight":QApplication.translate('app.msbranch', 'Percentage', None, QApplication.UnicodeUTF8),
    "dlg.msbranch.edit.tableheader.size":QApplication.translate('app.msbranch', 'Average Size', None, QApplication.UnicodeUTF8),
    "dlg.msbranch.edit.tableheader.cost":QApplication.translate('app.msbranch', 'Unit Cost', None, QApplication.UnicodeUTF8),
    "dlg.msbranch.edit.warning.invalidweight":QApplication.translate('app.msbranch', 'weight value must be a numeric value between 0 and 100', None, QApplication.UnicodeUTF8),
    "dlg.msbranch.edit.warning.node.required":QApplication.translate('app.msbranch', 'Node from Mapping Scheme Tree must be selected first', None, QApplication.UnicodeUTF8),
    "dlg.msbranch.error.attribute.exists": QApplication.translate('app.msbranch', 'Attribute value %s is already defined in same level', None, QApplication.UnicodeUTF8),
    # attribute ranges dialog
    ######################
    "dlg.attr.error.max":QApplication.translate('app.attributes', 'Max value %s must be larger than %s', None, QApplication.UnicodeUTF8),
    "dlg.attr.error.range":QApplication.translate('app.attributes', 'Minimum value %s must be (%s + 1)', None, QApplication.UnicodeUTF8),
    "dlg.attr.value.error":QApplication.translate('app.attributes', 'Only integer value is accepted', None, QApplication.UnicodeUTF8),
    # result detailed info dialog    
    ######################
    "dlg.result.window.title":QApplication.translate('app.result.info', 'Feature Information', None, QApplication.UnicodeUTF8),
    "dlg.result.title":QApplication.translate('app.result.info', 'Detailed Information for Selected Feature ', None, QApplication.UnicodeUTF8),
    "dlg.result.bldgcount":QApplication.translate('app.result.info', 'Building Count', None, QApplication.UnicodeUTF8),
    # operator processing messages
    ######################
    "message.sidd.operator.loaders.footprint.FootprintLoader":QApplication.translate('app.processing', 'Loading Building Footprints ...', None, QApplication.UnicodeUTF8),
    "message.sidd.operator.loaders.footprint.FootprintHtLoader":QApplication.translate('app.processing', 'Loading Building Footprints with Heights  ...', None, QApplication.UnicodeUTF8),
    "message.sidd.operator.loaders.ms.MappingSchemeLoader":QApplication.translate('app.processing', 'Loading Mapping Scheme  ...', None, QApplication.UnicodeUTF8),
    "message.sidd.operator.loaders.survey.GEMDBSurveyLoader":QApplication.translate('app.processing', 'Loading Survey from GEMDB ...', None, QApplication.UnicodeUTF8),
    "message.sidd.operator.loaders.survey.CSVSurveyLoader":QApplication.translate('app.processing', 'Loading Survey from CSV ...', None, QApplication.UnicodeUTF8),
    "message.sidd.operator.loaders.popgrid.PopGridLoader":QApplication.translate('app.processing', 'Loading Population Grid ...', None, QApplication.UnicodeUTF8),
    "message.sidd.operator.loaders.zones.ZoneLoader":QApplication.translate('app.processing', 'Loading Zones ...', None, QApplication.UnicodeUTF8),
    "message.sidd.operator.loaders.zones.ZoneCountLoader":QApplication.translate('app.processing', 'Loading Zones with Building Counts ...', None, QApplication.UnicodeUTF8),
    "message.sidd.operator.processors.aggregate.FootprintAggregator":QApplication.translate('app.processing', 'Counting Footprints for GEM grids ...', None, QApplication.UnicodeUTF8),
    "message.sidd.operator.processors.exposure.GridMSApplier":QApplication.translate('app.processing', 'Applying Mapping Scheme ...', None, QApplication.UnicodeUTF8),
    "message.sidd.operator.processors.exposure.ZoneMSApplier":QApplication.translate('app.processing', 'Applying Mapping Scheme ...', None, QApplication.UnicodeUTF8),
    "message.sidd.operator.processors.exposure.SurveyAggregator":QApplication.translate('app.processing', 'Aggregating Survey ...', None, QApplication.UnicodeUTF8),    
    "message.sidd.operator.processors.grid.GridWriter":QApplication.translate('app.processing', 'Generating GEM grid ...', None, QApplication.UnicodeUTF8),
    "message.sidd.operator.processors.grid.GridFromRegionWriter":QApplication.translate('app.processing', 'Generating GEM grid ...', None, QApplication.UnicodeUTF8),
    "message.sidd.operator.processors.grid.GridGeometryWriter":QApplication.translate('app.processing', 'Generating GEM grid Geometry ...', None, QApplication.UnicodeUTF8),
    "message.sidd.operator.processors.grids.ZoneToGrid":QApplication.translate('app.processing', 'Creating Grid from Zone ...', None, QApplication.UnicodeUTF8),
    "message.sidd.operator.processors.grids.FootprintZoneToGrid":QApplication.translate('app.processing', 'Creating Grid from Footprint and Zone ...', None, QApplication.UnicodeUTF8),
    "message.sidd.operator.processors.grids.PopgridZoneToGrid":QApplication.translate('app.processing', 'Creating Grid from Population Grid and Zone ...', None, QApplication.UnicodeUTF8),
    "message.sidd.operator.processors.join.ZoneGridMerger":QApplication.translate('app.processing', 'Assigning GEM Grids to Zones ...', None, QApplication.UnicodeUTF8),
    "message.sidd.operator.processors.join.ZoneFootprintMerger":QApplication.translate('app.processing', 'Assigning Footprints to Zones ...', None, QApplication.UnicodeUTF8),
    "message.sidd.operator.processors.join.ZoneFootprintCounter":QApplication.translate('app.processing', 'Counting Footprints to in Zones ...', None, QApplication.UnicodeUTF8),
    "message.sidd.operator.processors.join.ZonePopgridCounter":QApplication.translate('app.processing', 'Aggregating Population into Zones ...', None, QApplication.UnicodeUTF8),
    "message.sidd.operator.processors.ms_create.EmptyMSCreator":QApplication.translate('app.processing', 'Creating Empty Mapping Scheme ...', None, QApplication.UnicodeUTF8),
    "message.sidd.operator.processors.ms_create.EmptyZonesMSCreator":QApplication.translate('app.processing', 'Creating Empty Mapping Scheme ...', None, QApplication.UnicodeUTF8),
    "message.sidd.operator.processors.ms_create.SurveyZonesMSCreator":QApplication.translate('app.processing', 'Creating Mapping Scheme from Survey ...', None, QApplication.UnicodeUTF8),
    "message.sidd.operator.processors.ms_create.SurveyOnlyMSCreator":QApplication.translate('app.processing', 'Creating Mapping Scheme from Survey ...', None, QApplication.UnicodeUTF8),
    "message.sidd.operator.verify.exposure.ExposureFragmentationAnalyzer":QApplication.translate('app.processing', 'Performing Building Count Fragmentation Analysis ...', None, QApplication.UnicodeUTF8),
    "message.sidd.operator.verify.exposure.ExposureZoneCountAnalyzer":QApplication.translate('app.processing', 'Performing Total Building Count Analysis ...', None, QApplication.UnicodeUTF8),
    "message.sidd.operator.verify.exposure.ExposureFootprintCountAnalyzer":QApplication.translate('app.processing', 'Performing Total Building Count Analysis ...', None, QApplication.UnicodeUTF8),
    "message.sidd.operator.writers.exposure.ExposureSHPWriter":QApplication.translate('app.processing', 'Writings Exposure to Shapefile ...', None, QApplication.UnicodeUTF8),
    "message.sidd.operator.writers.exposure.ExposureCSVWriter":QApplication.translate('app.processing', 'Writings Exposure to CSV ...', None, QApplication.UnicodeUTF8),
    "message.sidd.operator.writers.exposure.ExposureKMLWriter":QApplication.translate('app.processing', 'Writings Exposure to KML ...', None, QApplication.UnicodeUTF8),
    "message.sidd.operator.writers.exposure.ExposureNRMLWriter":QApplication.translate('app.processing', 'Writings Exposure to NRML ...', None, QApplication.UnicodeUTF8),    
    "message.sidd.operator.writers.ms.MSLeavesCSVWriter":QApplication.translate('app.processing', 'Writings Mapping Scheme to CSV ...', None, QApplication.UnicodeUTF8),
}

def get_ui_string(key, params=None):
    """
    retrieve display text based on a key
    - params will be addd into string if set.
      NOTE: params must match placeholders in the retrieved text using python                 
    """
    ui_string = ""
    if SIDD_UI_STRINGS.has_key(key):
        ui_string = str(SIDD_UI_STRINGS[key])
        if params is not None:
            # try to add param to text
            try:
                ui_string = ui_string % params
            except:
                pass 
    # done
    return ui_string
