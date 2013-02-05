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
    "app.file.button":'...',
    "app.dialog.button.ok":"OK",
    "app.dialog.button.cancel":"Cancel",
    "app.dialog.button.close":"Close",
    "app.dialog.button.apply":"Apply",
    "app.popup.delete.confirm":"",
    # common UI messages
    ######################        
    "app.mslibrary.default":"PAGER",
    "app.mslibrary.user.multilevel":"User-defined Multi-level",
    "app.mslibrary.user.singlelevel":"User-defined Single Level",
    # main application window
    ######################
    "app.window.title":'SIDD',
    "app.window.status.ready":'Application ready',    
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
    "app.window.menu.view.result":'Results',
    "app.window.menu.help.about":'About',
    # tabs
    "app.window.tab.input":'Data Input',
    "app.window.tab.ms":'Mapping Scheme',
    "app.window.tab.mod":'Modifiers',
    "app.window.tab.result":'Results',
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
    "widget.input.zone.zonefield":'Select field containing zone classification identifier',
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
    "widget.input.verify.button":'Verify data',
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
    "widget.mod.tableheader.level1":'',
    "widget.mod.tableheader.level2":'',
    "widget.mod.tableheader.level3":'',
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
    "widget.result.export.title":'Export Results',
    "widget.result.export.format":'Select Export Data Format',
    "widget.result.export.file.open":'Open Export File',
    "widget.result.export.button":'Export',
    "widget.result.dq.title":'Data Quality Tests',
    "widget.result.dq.warning":'Warning',
    "widget.result.dq.description":'Exposure generated using Monte-Carlo simulation',
    # about dialog
    ######################
    'dlg.about.window.title': 'About SIDD',
    'dlg.about.message': '''
        <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.0//EN" "http://www.w3.org/TR/REC-html40/strict.dtd">
        <html>
        <head><style type="text/css">
        p { font-family:"MS Shell Dlg 2"; font-weight:400; font-style:normal; font-size:8.25pt; }
        </style></head>
        <body>
        <p align="center">SIDD Version %s</p>
        <p align="center">Last updated %s</p>
        <p align="center"></p>
        <p align="center">Copyright &reg; ImageCat Inc. %s</p>
        </body>
        </html>
        ''',
    # build progress dialog
    ######################
    "dlg.apply.window.title": 'Building Exposure',
    "dlg.apply.message": 'SIDD is applying mapping schemes and generating exposure.\nThis may takes some time. Plese check the console below to see what is being processed.',
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
}

def get_ui_string(key):
    return SIDD_UI_STRINGS[key] if SIDD_UI_STRINGS.has_key(key) else  ""
