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