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
dialog for editing mapping scheme branches
"""
from PyQt4.QtGui import QDialog, QAbstractItemView
from PyQt4.QtCore import QString, pyqtSlot
from datetime import datetime

from ui.constants import logUICall, get_ui_string
from ui.qt.dlg_save_ms_ui import Ui_saveMSDialog
from ui.helper.ms_tree import MSTreeModel

class DialogSaveMS(Ui_saveMSDialog, QDialog):
    """
    dialog for saving mapping scheme (single/multilevel) into
    mapping scheme library database
    """    
    # constructor
    ###############################    
    def __init__(self, app):
        super(DialogSaveMS, self).__init__()
        self.ui = Ui_saveMSDialog()
        self.ui.setupUi(self)
        
        self.app =  app
        for region in self.app.msdb_dao.get_regions():
            self.ui.cb_ms_region.addItem(QString(region))

        # connect slots (ui event)
        self.ui.btn_save.clicked.connect(self.saveMS)
        self.ui.btn_close.clicked.connect(self.accept)

    # ui event handlers
    ###############################
    
    @logUICall
    @pyqtSlot()
    def saveMS(self):
        """ save current mapping schem into mapping scheme library database """
        try:
            #TODO: refactor call to main controller 
            self.app.msdb_dao.save_ms(
                str(self.ui.cb_ms_region.currentText()),
                str(self.ui.txt_ms_name.text()),
                str(self.ui.txt_ms_type.text()),
                str(self.ui.txt_ms_create_date.text()),
                str(self.ui.txt_ms_source.text()),
                str(self.ui.txt_ms_quality.text()),
                str(self.ui.txt_ms_notes.toPlainText()),
                self.ms_to_save.to_xml())
        except:
            pass
        self.accept()

    # public method
    ###############################
    
    @logUICall
    def setMS(self, ms, isBranch=False):
        """
        set mapping scheme to be saved
        set mapping scheme type as 'single-level' if isBranch=True
        set to 'multi-level' otherwise 
        """
        self.ms_to_save = ms
        self.ui.tree_ms_view.setModel(MSTreeModel(ms))
        self.ui.tree_ms_view.setSelectionMode(QAbstractItemView.NoSelection)
        
        self.ui.txt_ms_create_date.setText(datetime.now().strftime("%Y-%m-%d %H:%M"))
        self.ui.txt_ms_create_date.setReadOnly(True)
        
        if isBranch:
            self.ui.lb_title.setText(get_ui_string("dlg.savems.title.branch"))
            self.ui.txt_ms_type.setText(get_ui_string("app.mslibrary.user.singlelevel"))
        else:
            self.ui.lb_title.setText(get_ui_string("dlg.savems.title.tree"))
            self.ui.txt_ms_type.setText(get_ui_string("app.mslibrary.user.multilevel"))      

        self.ui.txt_ms_type.setReadOnly(True)
        