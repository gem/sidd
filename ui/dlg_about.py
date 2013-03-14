# Copyright (c) 2011-2013, ImageCat Inc.
#
# SIDD is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
#
"""
dialog showing about message
"""
from PyQt4.QtGui import QDialog, QDialogButtonBox
from sidd.constants import SIDD_VERSION

from ui.constants import get_ui_string
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
        self.retranslateUi(self.ui)        
        # fixed dialog size
        self.setFixedSize(self.size())        
        # connect slot (ui event)
        self.ui.buttonBox.accepted.connect(self.accept)        

    def retranslateUi(self, ui):
        """ set text for ui elements """
        # dialog title
        self.setWindowTitle(get_ui_string("dlg.about.window.title"))
        # ui elements
        ui.lb_description.setText(get_ui_string("dlg.about.message", SIDD_VERSION))
        ui.lb_copyright.setText(get_ui_string("dlg.about.copyright"))
        ui.buttonBox.button(QDialogButtonBox.Ok).setText(get_ui_string("app.dialog.button.ok"))
