# Copyright (c) 2011-2013, ImageCat Inc.
#
# SIDD is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
#
"""
dialog showing about message
"""
from PyQt4.QtGui import QDialog
from ui.qt.dlg_apply_ui import Ui_DialogApply

class DialogApply(Ui_DialogApply, QDialog):
    """
    dialog showing about message
    """
    
    def __init__(self, mainWin):
        """ constructor """
        QDialog.__init__(self)        
        self.ui = Ui_DialogApply()
        self.ui.setupUi(self)

