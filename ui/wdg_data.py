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
# Version: $Id: wdg_data.py 22 2012-10-26 23:29:52Z zh $

"""
Widget (Panel) for specifying data inputs
"""

import os

from PyQt4.QtGui import QWidget, QMessageBox, QFileDialog, QPixmap
from PyQt4.QtCore import QSize, QPoint, pyqtSlot

from utils.shapefile import shapefile_fields, shapefile_projection
from utils.system import get_app_dir

from sidd.constants import logAPICall, \
                           FootprintTypes, OutputTypes, SurveyTypes, ZonesTypes, \
                           ProjectStatus

from ui.constants import logUICall, get_ui_string, UI_PADDING
from ui.qt.wdg_data_ui import Ui_widgetDataInput

class WidgetDataInput(Ui_widgetDataInput, QWidget):
    """
    Widget (Panel) for specifying data inputs
    """

    # internal decorator to perform common checks required
    # for many calls
    #############################
    class UICallChecker(object):        
        def __init__(self):
            self.project_is_required = False
            self.project = None

        def __call__(self, f):
            import functools
            @functools.wraps(f)
            def wrapper(*args, **kw):
                if self.project_is_required and self.project is None:
                    logUICall.log(get_ui_string("app.error.project.missing"), logUICall.ERROR)
                    QMessageBox.critical(None,
                                         get_ui_string("app.error.title"),
                                         get_ui_string("app.error.project.missing"))
                    return
                try:
                    logUICall.log('function call %s from module %s' % (f.__name__, f.__module__), logUICall.DEBUG)
                    return f(*args, **kw)
                except Exception as err:
                    logUICall.log(err, logUICall.ERROR)
            return wrapper

    uiCallChecker = UICallChecker()

    # constructor / destructor
    ###############################
    def __init__(self, app):
        """ constructor """
        super(WidgetDataInput, self).__init__()
        self._initilizing = True
        self.ui = Ui_widgetDataInput()
        self.ui.setupUi(self)
        self.retranslateUi(self.ui)
        self.app = app
        self.project = None
        WidgetDataInput.uiCallChecker.project_is_required = False

        # default input data setting
        self.ui.radio_fp_op1.setChecked(True)
        self.ui.radio_fp_op2.setEnabled(False)
        self.ui.radio_svy_op1.setChecked(True)
        self.ui.radio_zones_op1.setChecked(True)
        self.ui.radio_aggr_op1.setChecked(True)       

        # connect slots (ui event)
        # footprint
        self.ui.btn_fp_select_file.clicked.connect(self.openFootprintData)
        self.ui.radio_fp_op1.toggled.connect(self.setFootprintDataType)
        self.ui.radio_fp_op2.toggled.connect(self.setFootprintDataType)
        self.ui.radio_fp_op3.toggled.connect(self.setFootprintDataType)
        # survey
        self.ui.btn_svy_select_file.clicked.connect(self.openSurveyData)
        self.ui.radio_svy_op1.toggled.connect(self.setSurveyDataType)
        self.ui.radio_svy_op2.toggled.connect(self.setSurveyDataType)
        self.ui.radio_svy_op3.toggled.connect(self.setSurveyDataType)
        # zones
        self.ui.btn_zones_select_file.clicked.connect(self.openZoneData)
        self.ui.radio_zones_op1.toggled.connect(self.setZoneDataType)
        self.ui.radio_zones_op2.toggled.connect(self.setZoneDataType)
        self.ui.radio_zones_op3.toggled.connect(self.setZoneDataType)    
        self.ui.cb_zones_class_field.currentIndexChanged[str].connect(self.setZoneField)
        self.ui.cb_zones_count_field.currentIndexChanged[str].connect(self.setZoneCountField)  
        # aggregation
        self.ui.radio_aggr_op1.toggled.connect(self.setAggregateType)
        self.ui.radio_aggr_op2.toggled.connect(self.setAggregateType)
        # verify
        self.ui.btn_verify.clicked.connect(self.verifyInput)
        
    # UI event handling calls
    ###############################
    def resizeEvent(self, event):
        """ handle window resize """
        width_panel = (self.width() - UI_PADDING) / 2
        button_width = self.ui.btn_fp_select_file.width()         
        combo_width, combo_ht = width_panel * 0.3, self.ui.cb_fp_proj.height()        
        ht_input_panels = self.height() - self.ui.widgetFootprint.y() - UI_PADDING
        
        # footprint panel 
        self.ui.widgetFootprint.resize(QSize(width_panel, ht_input_panels * 0.4))
        self.ui.btn_fp_select_file.move(QPoint(width_panel-button_width-UI_PADDING, 
                                               self.ui.btn_fp_select_file.y()))
        self.ui.txt_fp_select_file.resize(QSize(self.ui.btn_fp_select_file.x()-self.ui.txt_fp_select_file.x()-UI_PADDING,
                                                self.ui.txt_fp_select_file.height()))
        self.ui.cb_fp_story_field.resize(QSize(combo_width, combo_ht))
        self.ui.cb_fp_story_field.move(QPoint(width_panel-combo_width-UI_PADDING, 
                                              self.ui.cb_fp_story_field.y()))         
        self.ui.cb_fp_proj.resize(QSize(combo_width, combo_ht))
        self.ui.cb_fp_proj.move(QPoint(width_panel-combo_width-UI_PADDING, 
                                       self.ui.cb_fp_proj.y()))         
        
        # survey panel
        self.ui.widgetSurvey.resize(QSize(width_panel, ht_input_panels * 0.3))
        self.ui.btn_svy_select_file.move(QPoint(width_panel-button_width-UI_PADDING, 
                                                self.ui.btn_svy_select_file.y()))
        self.ui.txt_svy_select_file.resize(QSize(self.ui.btn_svy_select_file.x()-self.ui.txt_svy_select_file.x()-UI_PADDING,
                                                 self.ui.txt_svy_select_file.height()))
        
        # aggregation panel
        self.ui.widgetAggr.resize(QSize(width_panel, ht_input_panels * 0.3))
        self.ui.btn_aggr_grid_select_file.move(QPoint(width_panel-button_width-UI_PADDING, 
                                                      self.ui.btn_aggr_grid_select_file.y()))
        self.ui.txt_aggr_grid_select_file.resize(QSize(self.ui.btn_aggr_grid_select_file.x()-self.ui.txt_aggr_grid_select_file.x()-UI_PADDING,
                                                       self.ui.txt_aggr_grid_select_file.height()))
        
        # right panel 
        self.ui.widgetZones.resize(QSize(width_panel, ht_input_panels * 0.5))
        self.ui.widgetZones.move(QPoint(width_panel+UI_PADDING, self.ui.widgetZones.y()))
        self.ui.btn_zones_select_file.move(QPoint(width_panel-button_width-UI_PADDING, 
                                                  self.ui.btn_zones_select_file.y()))
        self.ui.txt_zones_select_file.resize(QSize(self.ui.btn_zones_select_file.x()-self.ui.txt_zones_select_file.x()-UI_PADDING,
                                                   self.ui.txt_zones_select_file.height()))

        self.ui.cb_zones_class_field.resize(QSize(combo_width, combo_ht))
        self.ui.cb_zones_class_field.move(QPoint(width_panel-combo_width-UI_PADDING,
                                                 self.ui.cb_zones_class_field.y()))
        self.ui.cb_zones_count_field.resize(QSize(combo_width, combo_ht))
        self.ui.cb_zones_count_field.move(QPoint(width_panel-combo_width-UI_PADDING,
                                                 self.ui.cb_zones_count_field.y()))
                
        self.ui.cb_zones_proj.resize(QSize(combo_width, combo_ht))
        self.ui.cb_zones_proj.move(QPoint(width_panel-combo_width-UI_PADDING,
                                          self.ui.cb_zones_proj.y()))
        
        self.ui.widgetResult.resize(QSize(width_panel, ht_input_panels * 0.5))
        self.ui.widgetResult.move(QPoint(width_panel+UI_PADDING, self.ui.widgetResult.y()))        
        self.ui.txt_verify_text.resize(QSize(width_panel-self.ui.txt_verify_text.x()-UI_PADDING,
                                             self.ui.txt_verify_text.height()))
        self.ui.btn_verify.move(QPoint(width_panel-self.ui.btn_verify.width()-UI_PADDING,
                                       self.ui.btn_verify.y()))

        logUICall.log('resize done for %s' % self.__module__, logUICall.INFO)
            
    @uiCallChecker
    @pyqtSlot()
    def openFootprintData(self):
        """ show open file dialog box for selecting footprint data file"""
        filename = QFileDialog.getOpenFileName(self,
                                               get_ui_string("widget.input.fp.file.open"),
                                               get_app_dir(),
                                               get_ui_string("app.extension.shapefile"))
        if not filename.isNull() and os.path.exists(str(filename)):
            self.setFootprintFile(str(filename))     

    @logUICall
    @pyqtSlot(bool)
    def setFootprintDataType(self, checked=False):
        """ control UI based on footprint data radio button selected """        
        sender = self.sender()
        if sender.isChecked():            
            if sender == self.ui.radio_fp_op1:
                logUICall.log('\tno fp data', logUICall.DEBUG_L2)
                # update UI
                self.resetUI(resetFP=True)

                # update project if project exists
                if self.project is not None:
                    self.project.fp_type = FootprintTypes.None
                    self.project.fp_file = ''
                    self.project.fp_ht_field = ''
            elif sender == self.ui.radio_fp_op2:
                logUICall.log('\tfp with height', logUICall.DEBUG_L2)
                # update UI
                self.ui.txt_fp_select_file.setEnabled(True)
                self.ui.btn_fp_select_file.setEnabled(True)
                self.ui.cb_fp_story_field.setEnabled(True)
                self.ui.cb_fp_proj.setEnabled(True)
                
                # only allow grid output with footprint
                self.ui.radio_aggr_op1
                
                # update project if project exists 
                if self.project is not None:
                    self.project.fp_type = FootprintTypes.FootprintHt
            elif sender == self.ui.radio_fp_op3:
                logUICall.log('\tfp without height', logUICall.DEBUG_L2)
                # update UI
                self.ui.txt_fp_select_file.setEnabled(True)
                self.ui.btn_fp_select_file.setEnabled(True)
                self.ui.cb_fp_story_field.setEnabled(False)
                self.ui.cb_fp_proj.setEnabled(True)

                # only allow grid output with footprint
                self.ui.radio_aggr_op1
                
                # update project if project exists
                if self.project is not None:
                    self.project.fp_type = FootprintTypes.Footprint
            else:
                logUICall.log('\tdo nothing. should not even be here',
                              logUICall.WARNING)
        #else:
        #   ignore
    
    @uiCallChecker
    @pyqtSlot()
    def openSurveyData(self):
        """ show open file dialog box for selecting survey data file"""
        filename = QFileDialog.getOpenFileName(self,
                                               get_ui_string("widget.input.survey.file.open"),
                                               get_app_dir(),
                                               get_ui_string("app.extension.gemdb"))
        if not filename.isNull() and os.path.exists(str(filename)):
            self.setSurveyFile(str(filename))

    @uiCallChecker
    @pyqtSlot(bool)   
    def setSurveyDataType(self, checked=False):
        """ control UI based on survey data radio button selected """
        sender = self.sender()
        if sender.isChecked():            
            if sender == self.ui.radio_svy_op1:
                logUICall.log('\tno survey data ...', logUICall.DEBUG_L2)
                # update UI
                self.resetUI(resetSurvey=True)
                
                # update project if project exists
                if self.project is not None:
                    self.project.survey_type = SurveyTypes.None
                    self.project.survey_file = ''
            elif sender == self.ui.radio_svy_op2:
                logUICall.log('\cwith complete survey data ...', logUICall.DEBUG_L2)
                # update UI
                self.ui.txt_svy_select_file.setEnabled(True)
                self.ui.btn_svy_select_file.setEnabled(True)
                
                # update project if project exists
                if self.project is not None:
                    self.project.survey_type = SurveyTypes.CompleteSurvey
            elif sender == self.ui.radio_svy_op3:
                logUICall.log('\twith sampled survey data ...', logUICall.DEBUG_L2)
                # update UI
                self.ui.txt_svy_select_file.setEnabled(True)
                self.ui.btn_svy_select_file.setEnabled(True)
                
                # update project if project exists
                if self.project is not None:
                    self.project.survey_type = SurveyTypes.SampledSurvey
            else:
                logUICall.log('\tdo nothing. should not even be here',
                              logUICall.WARNING)
        #else:
        #   ignore
        
    @uiCallChecker
    @pyqtSlot()
    def openZoneData(self):
        """ show open file dialog box for selecting homogenous data file"""
        filename = QFileDialog.getOpenFileName(self,
                                               get_ui_string("widget.input.zone.file.open"),
                                               get_app_dir(),
                                               get_ui_string("app.extension.shapefile"))
        if not filename.isNull() and os.path.exists(str(filename)):
            self.setZonesFile(str(filename))
                
    @uiCallChecker
    @pyqtSlot(bool)
    def setZoneDataType(self, checked=False):
        """ control UI based on zone data radio button selected """
        sender = self.sender()
        if sender.isChecked():
            if sender == self.ui.radio_zones_op1:
                logUICall.log('\tno zone data ...', logUICall.DEBUG_L2)
                # update UI
                self.resetUI(resetZone=True)
                
                # update project if project exists
                if self.project is not None:
                    self.project.zone_type = ZonesTypes.None
                    self.project.zone_file = ''
                    self.project.zone_field = ''
                    self.project.zone_count_field = ''
            elif sender == self.ui.radio_zones_op2:
                logUICall.log('\tzone with class ...', logUICall.DEBUG_L2)
                # update UI
                self.ui.txt_zones_select_file.setEnabled(True)
                self.ui.btn_zones_select_file.setEnabled(True)
                self.ui.cb_zones_class_field.setEnabled(True)
                self.ui.cb_zones_count_field.setEnabled(False)
                self.ui.cb_zones_proj.setEnabled(True)
                
                # update project if project exists
                if self.project is not None:
                    self.project.zone_type = ZonesTypes.Landuse
            elif sender == self.ui.radio_zones_op3:
                logUICall.log('\tzone with class and count ...', logUICall.DEBUG_L2)
                # update UI
                self.ui.txt_zones_select_file.setEnabled(True)
                self.ui.btn_zones_select_file.setEnabled(True)
                self.ui.cb_zones_class_field.setEnabled(True)
                self.ui.cb_zones_count_field.setEnabled(True)
                self.ui.cb_zones_proj.setEnabled(True)
                
                # update project if project exists
                if self.project is not None:
                    self.project.zone_type = ZonesTypes.LanduseCount
            else:
                logUICall.log('\tdo nothing. should not even be here',
                              logUICall.WARNING)
        #else:
        #   ignore

    @uiCallChecker
    @pyqtSlot(int)
    def setZoneField(self, zone_field):
        # update project if project exists
        if self.project is not None:
            logUICall.log('\tset zone field %s ...' % zone_field, logUICall.DEBUG_L2)
            # update project if project exists
            if self.project is not None:
                self.project.zone_field = str(zone_field)            
    
    @uiCallChecker
    @pyqtSlot(int)
    def setZoneCountField(self, zone_count_field):        
        # update project if project exists
        if self.project is not None:
            logUICall.log('\tset zone count field %s ...' % zone_count_field, logUICall.DEBUG_L2)
            self.project.zone_count_field = str(zone_count_field)

    @uiCallChecker
    @pyqtSlot()
    def openAggGridData(self):
        """ show open file dialog box for selecting GED compatible grid file"""
        filename = QFileDialog.getOpenFileName(self,
                                               get_ui_string("widget.input.agg.file.open"),
                                               get_app_dir(),
                                               get_ui_string("app.extension.shapefile"))
        if not filename.isNull() and os.path.exists(str(filename)):
            self.setAggGridFile(str(filename))

    @uiCallChecker
    @pyqtSlot(bool)    
    def setAggregateType(self, checked=False):
        sender = self.sender()
        if sender.isChecked():            
            if sender == self.ui.radio_aggr_op1:
                logUICall.log('\tset output to zone ...', logUICall.DEBUG_L2)
                # update UI
                self.resetUI(resetOutput=True)

                # update project if project exists
                if self.project is not None:
                    self.project.output_type = OutputTypes.Zone
            elif sender == self.ui.radio_aggr_op2:
                logUICall.log('\tset output to grid ...', logUICall.DEBUG_L2)
                # update UI
                self.ui.txt_aggr_grid_select_file.setEnabled(True)
                self.ui.btn_aggr_grid_select_file.setEnabled(True)

                # update project if project exists
                if self.project is not None:
                    self.project.output_type = OutputTypes.Grid
            else:
                logUICall.log('\tdo nothing. should not even be here',
                              logUICall.WARNING)
        #else:
        #   ignore
    
    @uiCallChecker            
    @pyqtSlot()
    def verifyInput(self):
        """ determine if current input data set is enough to build exposure """
        # make sure all required input has been filled in
        # footprint 
        if (self.ui.radio_fp_op2.isChecked() or 
            self.ui.radio_fp_op3.isChecked()):
            # file set
            path = self.ui.txt_fp_select_file.text() 
            if path == '':
                QMessageBox.warning(self,
                                    get_ui_string('app.warning.title'),
                                    get_ui_string('widget.input.fp.file.missing'))
                return
            # file must exist
            if not os.path.exists(path):
                QMessageBox.warning(self,
                                    get_ui_string('app.warning.title'),
                                    get_ui_string('app.error.file.does.not.exist' % path))   
                return
        if self.ui.radio_fp_op3.isChecked():
            # story field set 
            if self.ui.cb_fp_story_field.currentText() == ' ':
                QMessageBox.warning(self,
                                    get_ui_string('app.warning.title'),
                                    get_ui_string('widget.input.fp.storyfield.missing'))
                return
        # survey 
        if (self.ui.radio_svy_op2.isChecked() or
            self.ui.radio_svy_op3.isChecked()):
            # file set
            path = self.ui.txt_svy_select_file.text() 
            if path == '':            
                QMessageBox.warning(self,
                                    get_ui_string('app.warning.title'),
                                    get_ui_string('widget.input.survey.file.missing'))
                return
            # file must exist
            if not os.path.exists(path):
                QMessageBox.warning(self,
                                    get_ui_string('app.warning.title'),
                                    get_ui_string('app.error.file.does.not.exist' % path))                
                return
        # zone 
        if (self.ui.radio_zones_op2.isChecked() or
            self.ui.radio_zones_op3.isChecked()):
            # file set
            path = self.ui.txt_zones_select_file.text() 
            if path == '':              
                QMessageBox.warning(self,
                                    get_ui_string('app.warning.title'),
                                    get_ui_string('widget.input.zone.file.missing'))
                return
            # file must exist
            if not os.path.exists(path):
                QMessageBox.warning(self,
                                    get_ui_string('app.warning.title'),
                                    get_ui_string('app.error.file.does.not.exist' % path))
                return               
            # zone field must be set
            if self.ui.cb_zones_class_field.currentText() == ' ':
                QMessageBox.warning(self,
                                    get_ui_string('app.warning.title'),
                                    get_ui_string('widget.input.zone.zonefield.missing'))
                return                        
        if (self.ui.radio_zones_op3.isChecked()):
            # count field must be set
            if self.ui.cb_zones_count_field.currentText() == ' ':
                QMessageBox.warning(self,
                                    get_ui_string('app.warning.title'),
                                    get_ui_string('widget.input.zone.countfield.missing'))            
                
        # delegate to main controller's verifyInput method for following reason
        # 1. verifyInput action can be invoked from maybe UI points
        # 2. verifyInput result updates multiple tabs        
        self.app.verifyInputs()

    # internal helper methods
    ###############################    
    def setFootprintFile(self, filename):
        # update UI
        logUICall.log('\tset footprint file to %s ...' % filename,logUICall.DEBUG_L2)
        self.ui.txt_fp_select_file.setText(filename)
        
        logUICall.log('\tupdate combo box ...',logUICall.DEBUG_L2)
        self.ui.cb_fp_story_field.clear()
        self.ui.cb_fp_story_field.addItems (shapefile_fields(filename))
        
        self.ui.cb_fp_proj.clear()
        self.ui.cb_fp_proj.addItem (shapefile_projection(filename))
        
        # update project if project exists
        if self.project is not None:
            self.project.fp_file = filename                        

    def setSurveyFile(self, filename):
        # update UI
        logUICall.log('\tset survey file to %s' % filename,logUICall.DEBUG_L2)
        self.ui.txt_svy_select_file.setText(filename)
        
        # update project if project exists
        if self.project is not None:
            self.project.survey_file = filename
        
    def setZonesFile(self, filename):
        # update UI
        logUICall.log('\tset zones file to %s ...' % filename,logUICall.DEBUG_L2)
        self.ui.txt_zones_select_file.setText(filename)
        
        logUICall.log('\tupdate combo box ...',logUICall.DEBUG_L2)
        fields = shapefile_fields(filename)
        self.ui.cb_zones_class_field.clear()
        self.ui.cb_zones_count_field.clear()
        self.ui.cb_zones_class_field.addItems([' '] + fields)
        self.ui.cb_zones_count_field.addItems([' '] + fields)

        self.ui.cb_zones_proj.clear()
        self.ui.cb_zones_proj.addItem (shapefile_projection(filename))
        
        # update project if project exists
        if self.project is not None:
            self.project.zone_file = filename

    def setAggrGridFile(self, filename):
        # update UI
        logUICall.log('\tset aggregate file to %s' % filename,logUICall.DEBUG_L2)
        self.ui.txt_aggr_grid_select_file.setText(filename)
        
        # update project if project exists
        if self.project is not None:
            self.project.grid_file = filename


    # public methods
    ###############################
    
    @logAPICall
    def setProject(self, project):
        self.project = None
        
        if project.fp_type == FootprintTypes.None:
            self.ui.radio_fp_op1.setChecked(True)
        elif project.fp_type == FootprintTypes.FootprintHt:
            self.ui.radio_fp_op2.setChecked(True)
            self.setFootprintFile(project.fp_file)             
        else:
            self.ui.radio_fp_op3.setChecked(True)
            self.setFootprintFile(project.fp_file)            
        
        if project.survey_type == SurveyTypes.None:
            self.ui.radio_svy_op1.setChecked(True)
        elif project.survey_type == SurveyTypes.CompleteSurvey:
            self.ui.radio_svy_op2.setChecked(True)
            self.setSurveyFile(project.survey_file)            
        else:
            self.ui.radio_svy_op3.setChecked(True)
            self.setSurveyFile(project.survey_file)            
            
        if project.zone_type == ZonesTypes.None:
            self.ui.radio_zones_op1.setChecked(True)
        elif project.zone_type == ZonesTypes.Landuse:
            self.ui.radio_zones_op2.setChecked(True)
            self.setZonesFile(project.zone_file)            
            self.ui.cb_zones_class_field.setCurrentIndex(
                self.ui.cb_zones_class_field.findText(project.zone_field))
        else:
            self.ui.radio_zones_op3.setChecked(True)
            self.setZonesFile(project.zone_file)            
            self.ui.cb_zones_class_field.setCurrentIndex(
                self.ui.cb_zones_class_field.findText(project.zone_field))
            self.ui.cb_zones_count_field.setCurrentIndex(
                self.ui.cb_zones_count_field.findText(project.zone_count_field))
        
        if project.output_type == OutputTypes.Zone:
            self.ui.radio_aggr_op1.setChecked(True)
        else:
            self.ui.radio_aggr_op2.setChecked(True)

        self.project = project
        WidgetDataInput.uiCallChecker.project = project        
        WidgetDataInput.uiCallChecker.project_is_required = True

    @logAPICall
    def showVerificationResults(self):
        NO_KEY = ":/imgs/icons/no.png"
        YES_KEY = ":/imgs/icons/yes.png"
        
        project = self.project # 
        if project.fp_type == FootprintTypes.None:
            self.ui.img_lb_verify_fp.setPixmap(QPixmap(NO_KEY))
        else:
            self.ui.img_lb_verify_fp.setPixmap(QPixmap(YES_KEY))

        if project.survey_type == SurveyTypes.None:
            self.ui.img_lb_verify_svy.setPixmap(QPixmap(NO_KEY))
        else:
            self.ui.img_lb_verify_svy.setPixmap(QPixmap(YES_KEY))
        
        if project.zone_type == ZonesTypes.None:
            self.ui.img_lb_verify_zones.setPixmap(QPixmap(NO_KEY))
        else:
            self.ui.img_lb_verify_zones.setPixmap(QPixmap(YES_KEY))
            
        if project.output_type == OutputTypes.Zone:
            self.ui.img_lb_verify_agg_zone.setPixmap(QPixmap(YES_KEY))
            self.ui.img_lb_verify_agg_grid.setPixmap(QPixmap(NO_KEY))
        else:
            self.ui.img_lb_verify_agg_grid.setPixmap(QPixmap(YES_KEY))
            self.ui.img_lb_verify_agg_zone.setPixmap(QPixmap(NO_KEY))
        
        if project.status == ProjectStatus.ReadyForExposure:
            self.ui.txt_verify_text.setText(get_ui_string('widget.input.verify.sucess'))
        elif project.status == ProjectStatus.ReadyForMS:
            self.ui.txt_verify_text.setText(get_ui_string('widget.input.verify.datarequired'))
            # append error messages
            for err in project.errors:                
                errMsg = get_ui_string('project.error.%s' % str(err))
                if errMsg == '':
                    errMsg = get_ui_string('widget.input.verify.unknownerror')                 
                self.ui.txt_verify_text.append('-%s' % errMsg)
                                                                
        else: #project.status == ProjectStatus.NotVerified:
            self.ui.txt_verify_text.setText(get_ui_string('widget.input.verify.noaction'))            
        
       
    @logAPICall
    def closeProject(self):
        self.project = None        
        WidgetDataInput.uiCallChecker.project_is_required = False
        WidgetDataInput.uiCallChecker.project = None
        
        self.resetUI(resetFP=True, resetZone=True, resetSurvey=True, resetOutput=True)


    def resetUI(self, resetFP=False, resetZone=False, resetSurvey=False, resetOutput=False):
        if resetFP:
            logUICall.log('\treset footprint inputs ...',logUICall.DEBUG_L2)
            self.ui.radio_fp_op1.setChecked(True)
            self.ui.txt_fp_select_file.setEnabled(False)
            self.ui.txt_fp_select_file.setText('')
            self.ui.btn_fp_select_file.setEnabled(False)
            self.ui.cb_fp_story_field.setEnabled(False)
            self.ui.cb_fp_story_field.clear()
            self.ui.cb_fp_proj.setEnabled(False)
            self.ui.cb_fp_proj.clear()
        
        if resetZone:
            logUICall.log('\treset zones inputs  ...',logUICall.DEBUG_L2)
            self.ui.radio_zones_op1.setChecked(True)
            self.ui.txt_zones_select_file.setEnabled(False)
            self.ui.txt_zones_select_file.setText('')
            self.ui.btn_zones_select_file.setEnabled(False)
            self.ui.cb_zones_class_field.setEnabled(False)
            self.ui.cb_zones_class_field.clear()
            self.ui.cb_zones_count_field.setEnabled(False)
            self.ui.cb_zones_count_field.clear()
            self.ui.cb_zones_proj.setEnabled(False)
            self.ui.cb_zones_proj.clear()
        
        if resetSurvey:
            logUICall.log('\treset survey inputs ...',logUICall.DEBUG_L2)
            self.ui.radio_svy_op1.setChecked(True)
            self.ui.txt_svy_select_file.setEnabled(False)
            self.ui.txt_svy_select_file.setText('')
            self.ui.btn_svy_select_file.setEnabled(False)
            
        if resetOutput:
            logUICall.log('\treset output inputs ...',logUICall.DEBUG_L2)
            self.ui.radio_aggr_op1.setChecked(False)
            self.ui.radio_aggr_op2.setChecked(False)
            self.ui.txt_aggr_grid_select_file.setEnabled(False)
            self.ui.txt_aggr_grid_select_file.setText('')
            self.ui.btn_aggr_grid_select_file.setEnabled(False)
            # update project if project exists

    def retranslateUi(self, ui):
        # widget header related
        ui.lb_panel_title.setText(get_ui_string("widget.input.header.title"))
        ui.txt_panel_description.setHtml(get_ui_string("widget.input.header.description"))

        # survey related
        ui.lb_svy_title.setText(get_ui_string("widget.input.survey.title"))
        ui.lb_svy_desc.setText(get_ui_string("widget.input.survey.description"))
        ui.lb_svy_select_file.setText(get_ui_string("app.file.select"))
        ui.btn_svy_select_file.setText(get_ui_string("app.file.button"))
        ui.radio_svy_op1.setText(get_ui_string("widget.input.survey.option1"))
        ui.radio_svy_op2.setText(get_ui_string("widget.input.survey.option2"))
        ui.radio_svy_op3.setText(get_ui_string("widget.input.survey.option3"))

        # footprint related
        ui.lb_fp_title.setText(get_ui_string("widget.input.fp.title"))
        ui.lb_fp_desc.setText(get_ui_string("widget.input.fp.description"))
        ui.lb_fp_select_file.setText(get_ui_string("app.file.select"))
        ui.btn_fp_select_file.setText(get_ui_string("app.file.button"))
        ui.lb_fp_proj.setText(get_ui_string("widget.input.fp.projection"))
        ui.lb_fp_story_field.setText(get_ui_string("widget.input.fp.storyfield"))
        ui.radio_fp_op1.setText(get_ui_string("widget.input.fp.op1"))
        ui.radio_fp_op2.setText(get_ui_string("widget.input.fp.op2"))
        ui.radio_fp_op3.setText(get_ui_string("widget.input.fp.op3"))

        # zone related        
        ui.lb_zones_title.setText(get_ui_string("widget.input.zone.title"))
        ui.lb_zones_desc.setText(get_ui_string("widget.input.zone.description"))
        ui.lb_zones_select_file.setText(get_ui_string("app.file.select"))
        ui.btn_zones_select_file.setText(get_ui_string("app.file.button"))
        ui.lb_zones_proj.setText(get_ui_string("widget.input.zone.projection"))
        ui.lb_zones_class_field.setText(get_ui_string("widget.input.zone.zonefield"))
        ui.lb_zones_count_field.setText(get_ui_string("widget.input.zone.countfield"))
        ui.radio_zones_op1.setText(get_ui_string("widget.input.zone.op1"))
        ui.radio_zones_op2.setText(get_ui_string("widget.input.zone.op2"))
        ui.radio_zones_op3.setText(get_ui_string("widget.input.zone.op3"))

        # data aggregation related
        ui.lb_aggr_title.setText(get_ui_string("widget.input.agg.title"))
        ui.lb_aggr_desc.setText(get_ui_string("widget.input.agg.description"))
        ui.lb_aggr_grid_select_file.setText(get_ui_string("app.file.select"))
        ui.btn_aggr_grid_select_file.setText(get_ui_string("app.file.button"))
        ui.radio_aggr_op1.setText(get_ui_string("widget.input.agg.op1"))
        ui.radio_aggr_op2.setText(get_ui_string("widget.input.agg.op2"))
        
        # data verification related
        ui.btn_verify.setText(get_ui_string("widget.input.verify.button"))
        ui.lb_verify_title.setText(get_ui_string("widget.input.verify.title"))
        ui.lb_verify_fp.setText(get_ui_string("widget.input.verify.footprint"))
        ui.lb_verify_svy.setText(get_ui_string("widget.input.verify.survey"))
        ui.lb_verify_zones.setText(get_ui_string("widget.input.verify.zones"))
        ui.lb_verify_aggregation.setText(get_ui_string("widget.input.verify.aggregation"))
        ui.lb_verify_agg_zone.setText(get_ui_string("widget.input.verify.agg.zone"))
        ui.lb_verify_agg_grid.setText(get_ui_string("widget.input.verify.agg.grid"))
        ui.txt_verify_text.setHtml("")   
        