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
from ui.qt.dlg_about_ui import Ui_DialogAbout

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
