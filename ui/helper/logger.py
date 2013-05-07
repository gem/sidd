# Copyright (c) 2011-2013, ImageCat Inc.
#
# SIDD is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
#
"""
configurable logging system for SIDD application
"""
from PyQt4.QtGui import QMessageBox
from sidd.logger import SIDDLogging

class SIDDUILogging(SIDDLogging):
    def __init__(self, name, level=0):
        super(SIDDUILogging, self).__init__(name, level)
    
    def log(self, msg, level=SIDDLogging.INFO):
        """ write log message according to internal configuration """
        from ui.constants import get_ui_string  # this call is intentionally placed in the function
                                                # because SIDDUILogging object is defined in ui.constants module
                                                # this line avoids the circular include
        super(SIDDUILogging, self).log(msg, level)                
        if level == self.WARNING:
            QMessageBox.warning(None, get_ui_string("app.error.unexpected"), str(msg))
        if level == self.ERROR:            
            QMessageBox.critical(None, get_ui_string("app.error.ui"), str(msg))
