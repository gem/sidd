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
dialog showing about message
"""
from PyQt4.QtGui import QDialog 
from ui.qt.dlg_about_ui import Ui_DialogAbout
from sidd.constants import SIDD_VERSION, SIDD_LASTUPDATED
from string import Template

class DialogAbout(Ui_DialogAbout, QDialog):
    """
    dialog showing about message
    """    
    def __init__(self, mainWin):
        """ constructor """
        super(DialogAbout, self).__init__()
        self.ui = Ui_DialogAbout()
        self.ui.setupUi(self)
        # fixed dialog size
        self.setFixedSize(self.size())        
        # connect slot (ui event)
        self.ui.buttonBox.accepted.connect(self.accept)        
        
        desc = Template(str(self.ui.lb_description.text()))
        self.ui.lb_description.setText(desc.safe_substitute(version=SIDD_VERSION, lastupdate=SIDD_LASTUPDATED))
