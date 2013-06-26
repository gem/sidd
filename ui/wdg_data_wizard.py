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
Widget (Panel) for specifying data inputs
"""

from PyQt4.QtGui import QWizard, QDoubleValidator
from PyQt4.QtCore import pyqtSlot

from sidd.constants import ZonesTypes, FootprintTypes

from ui.qt.wdg_data_wizard_ui import Ui_widgetDataWizard
from ui.wdg_data import WidgetDataInput

class WidgetDataWizard(Ui_widgetDataWizard, QWizard, WidgetDataInput):
    """
    Data Widget for specifying data inputs
    This wizard will guide user through different inputs pages by redirecting to 
    appropriate next input based on user data availability      
    """
    PAGE_ZONE, PAGE_FOOTPRINT, PAGE_POPGRID, PAGE_SURVEY, PAGE_AGGREGATE, PAGE_VERIFY = range(6)    
    def __init__(self, app, project):
        """
        constructor
        - initialize UI elements
        - connect UI elements to callback            
        """
        QWizard.__init__(self)
        
        self._initilizing = True
        self.ui = Ui_widgetDataWizard()
        self.ui.setupUi(self)
        
        self.setFixedSize(self.size())
        self.setOption(QWizard.HelpButtonOnRight, False)
        self.setOption(QWizard.HaveHelpButton, False)        

        self.app = app
        self.project = project

        self.showPopgrid = (app.app_config.get('options', 'allow_popgrid', 0, int) == 1)
        if not self.showPopgrid:
            self.ui.img_lb_verify_pop.setVisible(False)
            self.ui.lb_verify_pop.setVisible(False)
            self.ui.img_lb_verify_svy.move(self.ui.img_lb_verify_svy.x(), self.ui.img_lb_verify_pop.y())
            self.ui.lb_verify_svy.move(self.ui.lb_verify_svy.x(), self.ui.lb_verify_pop.y())            
        
        # connect slots (ui event)
        # footprint
        self.ui.btn_fp_select_file.clicked.connect(self.openFootprintData)
        self.ui.radio_fp_no_data.toggled.connect(self.setFootprintDataType)
        self.ui.radio_fp_height.toggled.connect(self.setFootprintDataType)
        self.ui.radio_fp_only.toggled.connect(self.setFootprintDataType)
        self.ui.cb_fp_story_field.currentIndexChanged[str].connect(self.setFootprintHtField)
        # survey
        self.ui.btn_svy_select_file.clicked.connect(self.openSurveyData)
        self.ui.radio_svy_no_data.toggled.connect(self.setSurveyDataType)
        self.ui.radio_svy_complete.toggled.connect(self.setSurveyDataType)
        self.ui.radio_svy_sampled.toggled.connect(self.setSurveyDataType)
        # zones
        self.ui.btn_zones_select_file.clicked.connect(self.openZoneData)
        self.ui.radio_zones_no_data.toggled.connect(self.setZoneDataType)
        self.ui.radio_zones_only.toggled.connect(self.setZoneDataType)
        self.ui.radio_zones_count.toggled.connect(self.setZoneDataType)    
        self.ui.cb_zones_class_field.currentIndexChanged[str].connect(self.setZoneField)
        self.ui.cb_zones_count_field.currentIndexChanged[str].connect(self.setZoneCountField)  
        # population grid
        self.ui.btn_pop_select_file.clicked.connect(self.openPopGridData)
        self.ui.radio_pop_no_data.toggled.connect(self.setPopGridType)
        self.ui.radio_pop_grid.toggled.connect(self.setPopGridType)  
        self.ui.cb_pop_pop_field.currentIndexChanged[str].connect(self.setPopField)
        self.ui.txt_pop_bldg_ratio.setValidator(QDoubleValidator(0, 10000000,  2, self))
        self.ui.txt_pop_bldg_ratio.editingFinished.connect(self.setPopToBldg)
        # aggregation
        self.ui.radio_aggr_zones.toggled.connect(self.setAggregateType)
        self.ui.radio_aggr_grid.toggled.connect(self.setAggregateType)
        
        # verify
        # self.ui.btn_verify.clicked.connect(self.verifyInput)
            
    def resizeEvent(self, event):
        QWizard.resizeEvent(self, event)
        for page_id in self.pageIds():            
            self.page(page_id).resizeEvent(event)        

    @pyqtSlot(bool)
    def setFootprintDataType(self, checked=False):
        super(WidgetDataWizard, self).setFootprintDataType(checked)
            
    @pyqtSlot()
    def openFootprintData(self):    
        super(WidgetDataWizard, self).openFootprintData()

    @pyqtSlot(int)
    def setFootprintHtField(self, ht_field):
        super(WidgetDataWizard, self).setFootprintHtField(ht_field)

    @pyqtSlot(bool)
    def setSurveyDataType(self, checked=False):
        super(WidgetDataWizard, self).setSurveyDataType(checked)

    @pyqtSlot()
    def openSurveyData(self):
        super(WidgetDataWizard, self).openSurveyData()

    @pyqtSlot()
    def openZoneData(self):
        super(WidgetDataWizard, self).openZoneData()

    @pyqtSlot(bool)
    def setZoneDataType(self, checked=False):
        super(WidgetDataWizard, self).setZoneDataType(checked)

    @pyqtSlot(int)
    def setZoneField(self, ht_field):
        super(WidgetDataWizard, self).setZoneField(ht_field)
    
    @pyqtSlot(int)
    def setZoneCountField(self, count_field):
        super(WidgetDataWizard, self).setZoneCountField(count_field)

    @pyqtSlot()
    def openPopGridData(self):
        super(WidgetDataWizard, self).openPopGridData()
                
    @pyqtSlot(bool)
    def setPopGridType(self, checked=False):
        super(WidgetDataWizard, self).setPopGridType(checked)

    @pyqtSlot(str)
    def setPopField(self, pop_field):
        super(WidgetDataWizard, self).setPopField(pop_field)
    
    @pyqtSlot()
    def setPopToBldg(self):
        super(WidgetDataWizard, self).setPopToBldg()
        
    @pyqtSlot(bool)
    def setAggregateType(self, checked=False):
        super(WidgetDataWizard, self).setAggregateType(checked) 
    
    def nextId(self):
        """
        find appropriate page to display next based on current
        data combination
        this method is implicitly invokes by the wizard when 
        "Next" button is clicked.
        """
        cur_id = self.currentId()
        # make sure input data set has correct combination
        # and all the files specified do exist
        if not self.dataIsVerified():
            return cur_id
        
        # go to appropriate page based on input
        if cur_id == self.PAGE_ZONE:
            if self.project.zone_type == ZonesTypes.None:
                next_id = self.PAGE_SURVEY            
            else:
                next_id = self.PAGE_FOOTPRINT
        elif cur_id == self.PAGE_FOOTPRINT:
            if self.project.fp_type != FootprintTypes.None and self.showPopgrid:
                next_id = self.PAGE_POPGRID
            else:
                next_id = self.PAGE_SURVEY
        elif cur_id == self.PAGE_SURVEY:
            if self.project.zone_type == ZonesTypes.None:
                next_id = self.PAGE_VERIFY
            else:
                next_id = self.PAGE_AGGREGATE
        elif cur_id == self.PAGE_AGGREGATE:
            next_id = self.PAGE_VERIFY
        else: # cur_id == self.PAGE_VERIFY:
            next_id = -1 # finish
        
        # verify data 
        if next_id == self.PAGE_VERIFY:
            self.project.verify_data()
            self.showVerificationResults()
        return next_id
        