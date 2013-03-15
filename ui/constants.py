# Copyright (c) 2011-2013, ImageCat Inc.
#
# SIDD is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
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
    "project.error.NotEnoughData":QApplication.translate('project.error', 'No action is defined for type of data provided', None, QApplication.UnicodeUTF8),
    "project.error.sampling":QApplication.translate('project.error', """Error Creating Mapping Scheme with Stratified Sampling method:\n%s\nPlease use deselect "Use Stratified sampling" option and try again.""", None, QApplication.UnicodeUTF8),
    # common messages
    ######################
    "app.extension.shapefile":QApplication.translate('app.extension', 'Shapefile (*.shp)', None, QApplication.UnicodeUTF8),
    "app.extension.csv":QApplication.translate('app.extension', 'CSV data(*.csv)', None, QApplication.UnicodeUTF8),
    "app.extension.db":QApplication.translate('app.extension', 'DB file(*.db)', None, QApplication.UnicodeUTF8),
    "app.extension.kml":QApplication.translate('app.extension', 'KML (*.kml)', None, QApplication.UnicodeUTF8),
    "app.extension.xml":QApplication.translate('app.extension', 'XML(*.xml)', None, QApplication.UnicodeUTF8),
    "app.extension.nrml":QApplication.translate('app.extension', 'NRML(*.xml)', None, QApplication.UnicodeUTF8),
    "app.extension.gemdb":QApplication.translate('app.extension', 'GEMDB(*.gemdb)', None, QApplication.UnicodeUTF8),
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
    "app.popup.delete.confirm":QApplication.translate('app.common', '', None, QApplication.UnicodeUTF8),
    # status messages
    ######################
    "app.status.ready":QApplication.translate('app.status',' ready', None, QApplication.UnicodeUTF8),
    "app.status.project.created":QApplication.translate('app.status', 'Project Created', None, QApplication.UnicodeUTF8),  
    "app.status.project.loaded":QApplication.translate('app.status', 'Project Loaded', None, QApplication.UnicodeUTF8),
    "app.status.project.saved":QApplication.translate('app.status', 'Project Saved', None, QApplication.UnicodeUTF8),
    "app.status.project.closed":QApplication.translate('app.status', 'Project Closed', None, QApplication.UnicodeUTF8),
    "app.status.input.verified":QApplication.translate('app.status', 'Input Verification Completed', None, QApplication.UnicodeUTF8),
    "app.status.ms.created":QApplication.translate('app.status', 'Mapping Scheme Created', None, QApplication.UnicodeUTF8),
    "app.status.ms.modified":QApplication.translate('app.status', 'Mapping Scheme Modified', None, QApplication.UnicodeUTF8),
    "app.status.ms.exported":QApplication.translate('app.status', 'Building Distribution Exported', None, QApplication.UnicodeUTF8),
    "app.status.exposure.created":QApplication.translate('app.status', 'Exposure Created', None, QApplication.UnicodeUTF8),    
    "app.status.cancelled":QApplication.translate('app.status', 'Process Cancelled', None, QApplication.UnicodeUTF8),
    "app.status.processing":QApplication.translate('app.status', 'Processing ...', None, QApplication.UnicodeUTF8),
    # common UI messages
    ######################
    "app.mslibrary.default":QApplication.translate('app.mslibrary', 'PAGER', None, QApplication.UnicodeUTF8),
    "app.mslibrary.user.multilevel":QApplication.translate('app.mslibrary', 'User-defined Multi-level', None, QApplication.UnicodeUTF8),
    "app.mslibrary.user.singlelevel":QApplication.translate('app.mslibrary', 'User-defined Single Level', None, QApplication.UnicodeUTF8),
    # main window
    ######################
    "app.window.title":QApplication.translate('app.window', 'SIDD', None, QApplication.UnicodeUTF8),
    # menu
    "app.window.menu.file":QApplication.translate('app.window', 'File', None, QApplication.UnicodeUTF8),
    "app.window.menu.view":QApplication.translate('app.window', 'View', None, QApplication.UnicodeUTF8),
    "app.window.menu.option":QApplication.translate('app.window', 'Options', None, QApplication.UnicodeUTF8),
    "app.window.menu.help":QApplication.translate('app.window', 'Help', None, QApplication.UnicodeUTF8),
    "app.window.menu.file.create":QApplication.translate('app.window', 'Create Project ...', None, QApplication.UnicodeUTF8),
    "app.window.menu.file.open":QApplication.translate('app.window', 'Open Project ...', None, QApplication.UnicodeUTF8),
    "app.window.menu.file.save":QApplication.translate('app.window', 'Save Project', None, QApplication.UnicodeUTF8),
    "app.window.menu.file.exit":QApplication.translate('app.window', 'Exit', None, QApplication.UnicodeUTF8),
    "app.window.menu.view.input":QApplication.translate('app.window', 'Data Input', None, QApplication.UnicodeUTF8),
    "app.window.menu.view.ms":QApplication.translate('app.window', 'Mapping Schemes', None, QApplication.UnicodeUTF8),
    "app.window.menu.view.result":QApplication.translate('app.window', 'Preview', None, QApplication.UnicodeUTF8),
    "app.window.menu.option.processing":QApplication.translate('app.window', 'Processing Options', None, QApplication.UnicodeUTF8),
    "app.window.menu.help.about":QApplication.translate('app.window', 'About', None, QApplication.UnicodeUTF8),
    # tabs
    "app.window.tab.input":QApplication.translate('app.window', 'Data Input', None, QApplication.UnicodeUTF8),
    "app.window.tab.ms":QApplication.translate('app.window', 'Mapping Scheme', None, QApplication.UnicodeUTF8),
    "app.window.tab.mod":QApplication.translate('app.window', 'Modifiers', None, QApplication.UnicodeUTF8),
    "app.window.tab.result":QApplication.translate('app.window', 'Preview', None, QApplication.UnicodeUTF8),
    # messages
    "app.window.msg.project.create":QApplication.translate('app.window', 'Create New Project', None, QApplication.UnicodeUTF8),
    "app.window.msg.project.open":QApplication.translate('app.window', 'Open Project File', None, QApplication.UnicodeUTF8),
    # main window / data input tab
    ######################
    # title
    "widget.input.header.title":QApplication.translate('app.input', 'Define required input data', None, QApplication.UnicodeUTF8),
    "widget.input.header.description":QApplication.translate('app.input', """
        <p>
        Specify input data <br/>
        Different combination of data can be used toward generating mapping schemes and exposure.
        </p>
    """, None, QApplication.UnicodeUTF8),
    # survey
    "widget.input.survey.title":QApplication.translate('app.input', 'Survey & field data', None, QApplication.UnicodeUTF8),
    "widget.input.survey.description":QApplication.translate('app.input', 'What type of survey / field data do you have?', None, QApplication.UnicodeUTF8),
    "widget.input.survey.file.open":QApplication.translate('app.input', 'Open Survey File', None, QApplication.UnicodeUTF8),
    "widget.input.survey.option1":QApplication.translate('app.input', 'No Data', None, QApplication.UnicodeUTF8),
    "widget.input.survey.option2":QApplication.translate('app.input', 'Complete building stock/survey area', None, QApplication.UnicodeUTF8),
    "widget.input.survey.option3":QApplication.translate('app.input', 'Sampled buildings from survey area', None, QApplication.UnicodeUTF8),
    "widget.input.survey.file.missing":QApplication.translate('app.input', 'Survey File not specified', None, QApplication.UnicodeUTF8),
    # footprint
    "widget.input.fp.title":QApplication.translate('app.input', 'Building footprint data', None, QApplication.UnicodeUTF8),
    "widget.input.fp.description":QApplication.translate('app.input', 'What type of data do you have for building footprints?', None, QApplication.UnicodeUTF8),
    "widget.input.fp.file.open":QApplication.translate('app.input', 'Open Footprint File', None, QApplication.UnicodeUTF8),
    "widget.input.fp.projection":QApplication.translate('app.input', 'Verify projection', None, QApplication.UnicodeUTF8),
    "widget.input.fp.storyfield":QApplication.translate('app.input', 'Select field containing number of stories', None, QApplication.UnicodeUTF8),
    "widget.input.fp.op1":QApplication.translate('app.input', 'No Data', None, QApplication.UnicodeUTF8),
    "widget.input.fp.op2":QApplication.translate('app.input', 'Building footprints with number of stories', None, QApplication.UnicodeUTF8),
    "widget.input.fp.op3":QApplication.translate('app.input', 'Building footprints without number of stories', None, QApplication.UnicodeUTF8),
    "widget.input.fp.file.missing":QApplication.translate('app.input', 'Footprint File not specified', None, QApplication.UnicodeUTF8),
    "widget.input.fp.storyfield.missing":QApplication.translate('app.input', 'Number of stories field not specified', None, QApplication.UnicodeUTF8),
    # zones
    "widget.input.zone.title":QApplication.translate('app.input', 'Homogenous zones data', None, QApplication.UnicodeUTF8),
    "widget.input.zone.description":QApplication.translate('app.input', 'What type of data do you have for zones?', None, QApplication.UnicodeUTF8),
    "widget.input.zone.file.open":QApplication.translate('app.input', 'Open Homogenous Zone File', None, QApplication.UnicodeUTF8),
    "widget.input.zone.projection":QApplication.translate('app.input', 'Verify projection', None, QApplication.UnicodeUTF8),
    "widget.input.zone.zonefield":QApplication.translate('app.input', 'Select field containing zone identifier', None, QApplication.UnicodeUTF8),
    "widget.input.zone.countfield":QApplication.translate('app.input', 'Select field containing building count', None, QApplication.UnicodeUTF8),
    "widget.input.zone.op1":QApplication.translate('app.input', 'No Data', None, QApplication.UnicodeUTF8),
    "widget.input.zone.op2":QApplication.translate('app.input', 'Homogenous zones', None, QApplication.UnicodeUTF8),
    "widget.input.zone.op3":QApplication.translate('app.input', 'Homogenous zones with building count', None, QApplication.UnicodeUTF8),
    "widget.input.zone.file.missing":QApplication.translate('app.input', 'Homogenous zone input file not specified', None, QApplication.UnicodeUTF8),
    "widget.input.zone.zonefield.missing":QApplication.translate('app.input', 'Land use/class field not specified', None, QApplication.UnicodeUTF8),
    "widget.input.zone.countfield.missing":QApplication.translate('app.input', 'Building count field not specified', None, QApplication.UnicodeUTF8),
    # aggregation
    "widget.input.agg.title":QApplication.translate('app.input', 'Aggregation', None, QApplication.UnicodeUTF8),
    "widget.input.agg.file.open":QApplication.translate('app.input', 'Open GED compatible Grid', None, QApplication.UnicodeUTF8),
    "widget.input.agg.description":QApplication.translate('app.input', 'How do you wish to aggregate your output data?', None, QApplication.UnicodeUTF8),
    "widget.input.agg.op1":QApplication.translate('app.input', 'Output into defined zones', None, QApplication.UnicodeUTF8),
    "widget.input.agg.op2":QApplication.translate('app.input', 'GED Compatible 30 arc-second grid', None, QApplication.UnicodeUTF8),
    # data verification
    "widget.input.verify.title":QApplication.translate('app.input', 'You have supplied the following types of data', None, QApplication.UnicodeUTF8),
    "widget.input.verify.button":QApplication.translate('app.input', 'Verify input data', None, QApplication.UnicodeUTF8),
    "widget.input.verify.footprint":QApplication.translate('app.input', 'Footprint', None, QApplication.UnicodeUTF8),
    "widget.input.verify.survey":QApplication.translate('app.input', 'Survey', None, QApplication.UnicodeUTF8),
    "widget.input.verify.zones":QApplication.translate('app.input', 'Zone', None, QApplication.UnicodeUTF8),
    "widget.input.verify.aggregation":QApplication.translate('app.input', 'Output data aggregation', None, QApplication.UnicodeUTF8),
    "widget.input.verify.agg.zone":QApplication.translate('app.input', 'Zone', None, QApplication.UnicodeUTF8),
    "widget.input.verify.agg.grid":QApplication.translate('app.input', 'GED Grid', None, QApplication.UnicodeUTF8),
    # verification messages
    "widget.input.verify.sucess":QApplication.translate('app.input', 'Datasets complete\nProceed to create exposure', None, QApplication.UnicodeUTF8),
    "widget.input.verify.datarequired":QApplication.translate('app.input', 'Following dataset required for building exposure', None, QApplication.UnicodeUTF8),
    "widget.input.verify.noaction":QApplication.translate('app.input', 'No action is defined for type of data provided', None, QApplication.UnicodeUTF8),
    "widget.input.verify.unknownerror":QApplication.translate('app.input', 'Unknown error while verifying input data', None, QApplication.UnicodeUTF8),
    # help messages
    "help.input.footprint":QApplication.translate('app.help', 'Footprint data', None, QApplication.UnicodeUTF8),
    "help.input.survey":QApplication.translate('app.help', 'Survey data', None, QApplication.UnicodeUTF8),
    "help.input.zones":QApplication.translate('app.help', 'Zones data', None, QApplication.UnicodeUTF8),
    "help.input.output":QApplication.translate('app.help', 'Output Aggregation', None, QApplication.UnicodeUTF8),    
    # main window / ms tab
    ######################
    "widget.ms.title":QApplication.translate('app.ms', 'Manage Mapping Schemes', None, QApplication.UnicodeUTF8),
    "widget.ms.tree.title":QApplication.translate('app.ms', 'Mapping Scheme', None, QApplication.UnicodeUTF8),
    "widget.ms.distribution.title":QApplication.translate('app.ms', 'Building Distribution', None, QApplication.UnicodeUTF8),
    "widget.ms.distribution.zones":QApplication.translate('app.ms', 'Select zone', None, QApplication.UnicodeUTF8),
    "widget.ms.distribution.mod":QApplication.translate('app.ms', 'Include Modifiers', None, QApplication.UnicodeUTF8),
    "widget.ms.library.title":QApplication.translate('app.ms', 'Mapping Scheme Library', None, QApplication.UnicodeUTF8),
    "widget.ms.library.regions":QApplication.translate('app.ms', 'Region', None, QApplication.UnicodeUTF8),
    "widget.ms.library.types":QApplication.translate('app.ms', 'Source', None, QApplication.UnicodeUTF8),    
    "widget.ms.library.names":QApplication.translate('app.ms', 'Available Mapping Schemes', None, QApplication.UnicodeUTF8),
    "widget.ms.library.date":QApplication.translate('app.ms', 'Date Created', None, QApplication.UnicodeUTF8),
    "widget.ms.library.quality":QApplication.translate('app.ms', 'Percentage of', None, QApplication.UnicodeUTF8),
    "widget.ms.library.datasource":QApplication.translate('app.ms', 'Data Source', None, QApplication.UnicodeUTF8),
    "widget.ms.library.notes":QApplication.translate('app.ms', 'Use Notes', None, QApplication.UnicodeUTF8),
    "widget.ms.library.enable":QApplication.translate('app.ms', 'Enable Mapping Scheme Library', None, QApplication.UnicodeUTF8),
    "widget.ms.library.delete.denied":QApplication.translate('app.ms', 'Only allowed to delete user-defined mapping scheme', None, QApplication.UnicodeUTF8),
    "widget.ms.modifier":QApplication.translate('app.ms', 'Modifiers', None, QApplication.UnicodeUTF8),
    "widget.ms.build":QApplication.translate('app.ms', 'Build Exposure', None, QApplication.UnicodeUTF8),
    "widget.ms.warning.deletebranch":QApplication.translate('app.ms', 'Deleting a node cannot be undone.\nAre you sure that you want to continue?', None, QApplication.UnicodeUTF8),
    "widget.ms.warning.node.required":QApplication.translate('app.ms', 'Node from Mapping Scheme Tree must be selected first', None, QApplication.UnicodeUTF8),
    "widget.ms.warning.node.invalid":QApplication.translate('app.ms', 'Selected Node from Mapping Scheme Tree is Invalid', None, QApplication.UnicodeUTF8),
    # main window / mod tab
    ######################
    "widget.mod.title":QApplication.translate('app.mod', 'Manage Modifiers', None, QApplication.UnicodeUTF8),
    "widget.mod.build":QApplication.translate('app.mod', 'Build Exposure', None, QApplication.UnicodeUTF8),
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
    "widget.result.title":QApplication.translate('app.result', 'Preview', None, QApplication.UnicodeUTF8),
    "widget.result.layers.selector":QApplication.translate('app.result', 'Selected Layer', None, QApplication.UnicodeUTF8),    
    "widget.result.layer.exposure":QApplication.translate('app.result', 'Exposure', None, QApplication.UnicodeUTF8),
    "widget.result.layer.exposure_grid":QApplication.translate('app.result', 'Exposure Grid', None, QApplication.UnicodeUTF8),    
    "widget.result.layer.survey":QApplication.translate('app.result', 'Surveys', None, QApplication.UnicodeUTF8),
    "widget.result.layer.footprint":QApplication.translate('app.result', 'Footprints', None, QApplication.UnicodeUTF8),
    "widget.result.layer.zones":QApplication.translate('app.result', 'Zones', None, QApplication.UnicodeUTF8),
    "widget.result.layers.theme.title":QApplication.translate('app.result', 'Change Thematic for %s', None, QApplication.UnicodeUTF8),
    "widget.result.info.notfound":QApplication.translate('app.result', 'Nothing not found at location', None, QApplication.UnicodeUTF8),
    "widget.result.export.title":QApplication.translate('app.result', 'Export Exposure', None, QApplication.UnicodeUTF8),
    "widget.result.export.format":QApplication.translate('app.result', 'Select Export Data Format', None, QApplication.UnicodeUTF8),
    "widget.result.export.path.dialog":QApplication.translate('app.result', 'Select Export Destination Folder', None, QApplication.UnicodeUTF8),
    "widget.result.export.button":QApplication.translate('app.result', 'Export', None, QApplication.UnicodeUTF8),
    # data quality messages
    "widget.result.dq.title":QApplication.translate('app.result', 'Data Quality Tests', None, QApplication.UnicodeUTF8),
    "widget.result.dq.warning":QApplication.translate('app.result', 'Warning', None, QApplication.UnicodeUTF8),
    "widget.result.dq.total_tests":QApplication.translate('app.result', '%s tests run on result', None, QApplication.UnicodeUTF8),
    "widget.result.dq.method":QApplication.translate('app.result', 'Exposure generated using %s method', None, QApplication.UnicodeUTF8),
    "widget.result.dq.tests.count":QApplication.translate('app.result', 'Verifying Building Count', None, QApplication.UnicodeUTF8),
    "widget.result.dq.tests.count.total_source":QApplication.translate('app.result', 'Total Buildings in Source Data: %.0f', None, QApplication.UnicodeUTF8),
    "widget.result.dq.tests.count.total_exposure":QApplication.translate('app.result', 'Total Buildings in Generated Exposure: %.0f', None, QApplication.UnicodeUTF8),
    "widget.result.dq.tests.fragmentation":QApplication.translate('app.result', 'Number of Fractional Records', None, QApplication.UnicodeUTF8),
    "widget.result.dq.tests.fragmentation.record_count":QApplication.translate('app.result', 'Total Records in Generated Exposure: %.0f', None, QApplication.UnicodeUTF8),
    "widget.result.dq.tests.fragmentation.fraction_count":QApplication.translate('app.result', 'Total Records with Fractional Building Count: %.0f', None, QApplication.UnicodeUTF8),
    # about dialog
    ######################
    'dlg.about.window.title':QApplication.translate('app.about', 'About SIDD', None, QApplication.UnicodeUTF8),
    'dlg.about.message':QApplication.translate('app.about',"""
        <p>
            Version: %s <br/>
            Last updated: February 2013
        </p>
        <p>
           SIDD is developed from GEM Inventory and Damage Capture Tools effort. It is part of a collection of tools that
           can be used for development of exposure datasets and models at the sub-national level, for exposure dataset 
           development per-building and to capture earthquake consequences per-building 
        </p>
        """, None, QApplication.UnicodeUTF8),
    'dlg.about.copyright':QApplication.translate('app.about',"""<p>Copyright &reg; ImageCat Inc. 2013.</p>""", None, QApplication.UnicodeUTF8),
    # build progress dialog
    ######################
    "dlg.apply.window.title":QApplication.translate('app.apply', 'Building Exposure', None, QApplication.UnicodeUTF8),
    "dlg.apply.message": QApplication.translate('app.apply', 'SIDD is applying mapping schemes and generating exposure.\nThis may takes some time. Plese check the console below to see what is being processed.', None, QApplication.UnicodeUTF8),
    # build ms dialog
    ######################
    "dlg.buildms.title":QApplication.translate('app.buildms', 'Create Mapping Scheme', None, QApplication.UnicodeUTF8),
    "dlg.buildms.attributes":QApplication.translate('app.buildms', 'Attributes to include', None, QApplication.UnicodeUTF8),
    "dlg.buildms.attributes.not_included":QApplication.translate('app.buildms', 'Attributes not included', None, QApplication.UnicodeUTF8),
    "dlg.buildms.use.sampling":QApplication.translate('app.buildms', 'Use Stratified Sampling method', None, QApplication.UnicodeUTF8),
    "dlg.buildms.notes":QApplication.translate('app.buildms', 'Attribute with * symbol can be grouped into ranges', None, QApplication.UnicodeUTF8),    
    "dlg.buildms.option.empty":QApplication.translate('app.buildms', 'Create Empty Mapping Scheme', None, QApplication.UnicodeUTF8),
    "dlg.buildms.option.survey":QApplication.translate('app.buildms', 'Build from Survey Data', None, QApplication.UnicodeUTF8),
    "dlg.buildms.button.moveup":QApplication.translate('app.buildms', 'Move up', None, QApplication.UnicodeUTF8),
    "dlg.buildms.button.movedown":QApplication.translate('app.buildms', 'Move Down', None, QApplication.UnicodeUTF8),
    "dlg.buildms.button.movetop":QApplication.translate('app.buildms', 'Move to Top', None, QApplication.UnicodeUTF8),
    "dlg.buildms.button.movebottom":QApplication.translate('app.buildms', 'Move to Bottom', None, QApplication.UnicodeUTF8),
    "dlg.buildms.button.range":QApplication.translate('app.buildms', 'Edit Grouping', None, QApplication.UnicodeUTF8),    
    # edit mapping scheme branch dialog
    ######################
    "dlg.msbranch.edit.window.title":QApplication.translate('app.msbranch', 'Edit Mapping Scheme Branch', None, QApplication.UnicodeUTF8),
    "dlg.msbranch.edit.title":QApplication.translate('app.msbranch', 'Edit Mapping Scheme Branch', None, QApplication.UnicodeUTF8), 
    "dlg.msbranch.edit.tableheader.value":QApplication.translate('app.msbranch', 'Value', None, QApplication.UnicodeUTF8),
    "dlg.msbranch.edit.tableheader.weight":QApplication.translate('app.msbranch', 'Percentage', None, QApplication.UnicodeUTF8),
    "dlg.msbranch.edit.attribute.name":QApplication.translate('app.msbranch', 'Attribute Name', None, QApplication.UnicodeUTF8),
    "dlg.msbranch.edit.weight.total":QApplication.translate('app.msbranch', 'Sum of Weights', None, QApplication.UnicodeUTF8),
    "dlg.msbranch.edit.warning.invalidweight":QApplication.translate('app.msbranch', 'weight value must be a numeric value between 0 and 100', None, QApplication.UnicodeUTF8),
    "dlg.msbranch.edit.warning.node.required":QApplication.translate('app.msbranch', 'Node from Mapping Scheme Tree must be selected first', None, QApplication.UnicodeUTF8),
    "dlg.msbranch.button.add":QApplication.translate('app.msbranch', 'Add Value', None, QApplication.UnicodeUTF8), 
    "dlg.msbranch.button.delete":QApplication.translate('app.msbranch', 'Delete Selected Value', None, QApplication.UnicodeUTF8), 
    "dlg.msbranch.button.save":QApplication.translate('app.msbranch', 'Save Mapping Scheme Branch', None, QApplication.UnicodeUTF8), 
    "dlg.msbranch.error.attribute.exists": QApplication.translate('app.msbranch', 'Attribute value %s is already defined in same level', None, QApplication.UnicodeUTF8),
    # save mapping scheme dialog
    ######################
    "dlg.savems.window.title":QApplication.translate('app.savems', 'Save Mapping Scheme', None, QApplication.UnicodeUTF8),
    "dlg.savems.title.tree":QApplication.translate('app.savems', 'Save Mapping Scheme Tree', None, QApplication.UnicodeUTF8),
    "dlg.savems.title.branch":QApplication.translate('app.savems', 'Save Mapping Scheme Branch', None, QApplication.UnicodeUTF8),
    "dlg.savems.date":QApplication.translate('app.savems', 'Date Created', None, QApplication.UnicodeUTF8),
    "dlg.savems.source":QApplication.translate('app.savems', 'Source', None, QApplication.UnicodeUTF8),
    "dlg.savems.quality":QApplication.translate('app.savems', 'Percentage of', None, QApplication.UnicodeUTF8),
    "dlg.savems.notes":QApplication.translate('app.savems', 'Notes', None, QApplication.UnicodeUTF8),
    "dlg.savems.name":QApplication.translate('app.savems', 'Name', None, QApplication.UnicodeUTF8),
    "dlg.savems.type":QApplication.translate('app.savems', 'Source', None, QApplication.UnicodeUTF8),
    "dlg.savems.region":QApplication.translate('app.savems', 'Region', None, QApplication.UnicodeUTF8),
    # secondary modifiers dialog
    ######################
    "dlg.mod.window.title":QApplication.translate('app.editmod', 'Editing Modifier', None, QApplication.UnicodeUTF8),
    "dlg.mod.title":QApplication.translate('app.editmod', 'Edit Building Distribution Modifier', None, QApplication.UnicodeUTF8),
    "dlg.mod.ms_tree":QApplication.translate('app.editmod', 'Mapping Scheme', None, QApplication.UnicodeUTF8),
    "dlg.mod.mod_values":QApplication.translate('app.editmod', 'Modifier Detail', None, QApplication.UnicodeUTF8),
    "dlg.mod.attributes":QApplication.translate('app.editmod', 'Attribute', None, QApplication.UnicodeUTF8),
    "dlg.mod.totalweights":QApplication.translate('app.editmod', 'Total', None, QApplication.UnicodeUTF8),
    "dlg.mod.button.add":QApplication.translate('app.editmod', 'Add Modifier', None, QApplication.UnicodeUTF8),
    "dlg.mod.button.delete":QApplication.translate('app.editmod', 'Delete Selected Modifier', None, QApplication.UnicodeUTF8),
    # attribute ranges dialog
    ######################
    "dlg.attr.range.window.title":QApplication.translate('app.attributes', 'Set Value Grouping', None, QApplication.UnicodeUTF8),
    "dlg.attr.title":QApplication.translate('app.attributes', 'Attribute Value Groups', None, QApplication.UnicodeUTF8),
    "dlg.attr.label.attribute":QApplication.translate('app.attributes', 'Attribute', None, QApplication.UnicodeUTF8),
    "dlg.attr.min_value":QApplication.translate('app.attributes', 'Minimum Value', None, QApplication.UnicodeUTF8),
    "dlg.attr.max_value":QApplication.translate('app.attributes', 'Maximum Value', None, QApplication.UnicodeUTF8),
    "dlg.attr.error.max":QApplication.translate('app.attributes', 'Max value %s must be larger than %s', None, QApplication.UnicodeUTF8),
    "dlg.attr.error.range":QApplication.translate('app.attributes', 'Minimum value %s must be (%s + 1)', None, QApplication.UnicodeUTF8),
    "dlg.attr.value.error":QApplication.translate('app.attributes', 'Only integer value is accepted', None, QApplication.UnicodeUTF8),
    "dlg.attr.button.add":QApplication.translate('app.attributes', 'Add a group', None, QApplication.UnicodeUTF8),
    "dlg.attr.button.delete":QApplication.translate('app.attributes', 'Delete a group', None, QApplication.UnicodeUTF8),
    # processing options dialog    
    ######################
    "dlg.options.ep.window.title":QApplication.translate('app.options', 'Processing Options', None, QApplication.UnicodeUTF8),
    "dlg.options.ep.title":QApplication.translate('app.options', 'Extrapolation Options', None, QApplication.UnicodeUTF8),
    "dlg.options.ep.random":QApplication.translate('app.options', 'Monte-Carlo Simulation', None, QApplication.UnicodeUTF8),
    "dlg.options.ep.fraction":QApplication.translate('app.options', 'Building Distribution Fraction', None, QApplication.UnicodeUTF8),
    "dlg.options.ep.fraction.rounded":QApplication.translate('app.options', 'Building Distribution Fraction Rounded', None, QApplication.UnicodeUTF8),
    # result detailed info dialog    
    ######################
    "dlg.result.window.title":QApplication.translate('app.result.info', 'Feature Information', None, QApplication.UnicodeUTF8),
    "dlg.result.title":QApplication.translate('app.result.info', 'Detailed Information for Selected Feature ', None, QApplication.UnicodeUTF8),
    "dlg.result.bldgcount":QApplication.translate('app.result.info', 'Building Count', None, QApplication.UnicodeUTF8),
    # result feature seach dialog    
    ######################
    "dlg.result.search.window.title":QApplication.translate('app.result.seach', 'Zoom to Feature', None, QApplication.UnicodeUTF8),
    "dlg.result.search.title":QApplication.translate('app.result.seach', 'Zoom to Feature', None, QApplication.UnicodeUTF8),
    "dlg.result.search.button.find":QApplication.translate('app.result.seach', 'Zoom to', None, QApplication.UnicodeUTF8),
    "dlg.result.search.button.close":QApplication.translate('app.result.seach', 'Close', None, QApplication.UnicodeUTF8),
    "dlg.result.search.attribute":QApplication.translate('app.result.seach', 'Attribute', None, QApplication.UnicodeUTF8),
    "dlg.result.search.value":QApplication.translate('app.result.seach', 'Value', None, QApplication.UnicodeUTF8),
    # operator processing messages
    ######################
    "message.sidd.operator.loaders.footprint.FootprintLoader":QApplication.translate('app.processing', 'Loading Building Footprints ...', None, QApplication.UnicodeUTF8),
    "message.sidd.operator.loaders.footprint.FootprintHtLoader":QApplication.translate('app.processing', 'Loading Building Footprints with Heights  ...', None, QApplication.UnicodeUTF8),
    "message.sidd.operator.loaders.ms.MappingSchemeLoader":QApplication.translate('app.processing', 'Loading Mapping Scheme  ...', None, QApplication.UnicodeUTF8),
    "message.sidd.operator.loaders.survey.GEMDBSurveyLoader":QApplication.translate('app.processing', 'Loading Survey from GEMDB ...', None, QApplication.UnicodeUTF8),
    "message.sidd.operator.loaders.survey.CSVSurveyLoader":QApplication.translate('app.processing', 'Loading Survey from CSV ...', None, QApplication.UnicodeUTF8),
    "message.sidd.operator.loaders.zones.ZoneLoader":QApplication.translate('app.processing', 'Loading Zones ...', None, QApplication.UnicodeUTF8),
    "message.sidd.operator.loaders.zones.ZoneCountLoader":QApplication.translate('app.processing', 'Loading Zones with Building Counts ...', None, QApplication.UnicodeUTF8),
    "message.sidd.operator.processors.aggregate.FootprintAggregator":QApplication.translate('app.processing', 'Counting Footprints for GEM grids ...', None, QApplication.UnicodeUTF8),
    "message.sidd.operator.processors.exposure.GridMSApplier":QApplication.translate('app.processing', 'Applying Mapping Scheme ...', None, QApplication.UnicodeUTF8),
    "message.sidd.operator.processors.exposure.ZoneMSApplier":QApplication.translate('app.processing', 'Applying Mapping Scheme ...', None, QApplication.UnicodeUTF8),
    "message.sidd.operator.processors.exposure.SurveyAggregator":QApplication.translate('app.processing', 'Aggregating Survey ...', None, QApplication.UnicodeUTF8),    
    "message.sidd.operator.processors.grid.GridWriter":QApplication.translate('app.processing', 'Generating GEM grid ...', None, QApplication.UnicodeUTF8),
    "message.sidd.operator.processors.grid.GridFromRegionWriter":QApplication.translate('app.processing', 'Generating GEM grid ...', None, QApplication.UnicodeUTF8),
    "message.sidd.operator.processors.grid.GridGeometryWriter":QApplication.translate('app.processing', 'Generating GEM grid Geometry ...', None, QApplication.UnicodeUTF8),
    "message.sidd.operator.processors.join.ZoneGridMerger":QApplication.translate('app.processing', 'Assigning GEM Grids to Zones ...', None, QApplication.UnicodeUTF8),
    "message.sidd.operator.processors.join.ZoneFootprintMerger":QApplication.translate('app.processing', 'Assigning Footprints to Zones ...', None, QApplication.UnicodeUTF8),
    "message.sidd.operator.processors.join.ZoneFootprintCounter":QApplication.translate('app.processing', 'Counting Footprints to in Zones ...', None, QApplication.UnicodeUTF8),
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
