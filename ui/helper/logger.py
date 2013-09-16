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
configurable logging system for SIDD application
"""
from PyQt4.QtGui import QMessageBox
from sidd.logger import SIDDLogging

class SIDDUILogging(SIDDLogging):
    def __init__(self, name, level=0):
        super(SIDDUILogging, self).__init__(name, level)
        self.get_ui_string = None
    
    def log(self, msg, level=SIDDLogging.INFO):
        """ write log message according to internal configuration """
        super(SIDDUILogging, self).log(msg, level)
        if self.get_ui_string is None:
            from ui.constants import get_ui_string  # this call is intentionally placed in the function
                                                    # because SIDDUILogging object is defined in ui.constants module
                                                    # this line avoids the circular include
            self.get_ui_string = get_ui_string
        if level == self.WARNING:
            QMessageBox.warning(None, self.get_ui_string("app.error.unexpected"), str(msg))
        if level == self.ERROR:            
            QMessageBox.critical(None, self.get_ui_string("app.error.ui"), str(msg))
