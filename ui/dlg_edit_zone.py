# Copyright (c) 2011-2013, ImageCat Inc.
#
# SIDD is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
#
"""
dialog for editing secondary modifiers
"""
from PyQt4.QtGui import QDialog
from PyQt4.QtCore import pyqtSlot

from ui.qt.dlg_edit_zone_ui import Ui_editZoneNameDialog

class DialogEditZoneName(Ui_editZoneNameDialog, QDialog):
    """
    dialog specifying options for creating mapping scheme
    """
    BUILD_EMPTY, BUILD_FROM_SURVEY=range(2)
    
    def __init__(self, zone_name=''):
        """ constructor """
        super(DialogEditZoneName, self).__init__()
        self.ui = Ui_editZoneNameDialog()
        self.ui.setupUi(self)
        self.setFixedSize(self.size())
        
        self.ui.buttonBox.accepted.connect(self.accept)
        self.ui.buttonBox.rejected.connect(self.reject)
        
        self.set_zone_name(zone_name)
    
    def set_zone_name(self, zone_name):
        self.ui.txt_zone.setText(zone_name)
        
    def get_zone_name(self):
        return self.ui.txt_zone.text()