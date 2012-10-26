# Copyright (c) 2011-2012, ImageCat Inc.
#
# SIDD is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License version 3
# only, as published by the Free Software Foundation.
#
# SIDD is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License version 3 for more details
# (a copy is included in the LICENSE file that accompanied this code).
#
# You should have received a copy of the GNU Lesser General Public License
# version 3 along with SIDD.  If not, see
# <http://www.gnu.org/licenses/lgpl-3.0.txt> for a copy of the LGPLv3 License.
#
# Version: $Id: dlg_save_ms.py 21 2012-10-26 01:48:25Z zh $

"""
dialog for editing mapping scheme brances
"""
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from datetime import datetime

from sidd.ms import *

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
        self.retranslateUi(self.ui)
        
        self.app =  app
        for region in self.app.msdb_dao.get_regions():
            self.ui.cb_ms_region.addItem(QString(region))

    # ui event handlers
    ###############################
        
    @logUICall
    def saveMS(self):
        """ save current mapping schem into mapping scheme library database """
        # TODO: error handling
        self.app.msdb_dao.save_ms(
            str(self.ui.cb_ms_region.currentText()),
            str(self.ui.txt_ms_name.text()),
            str(self.ui.txt_ms_type.text()),
            str(self.ui.txt_ms_create_date.text()),
            str(self.ui.txt_ms_source.text()),
            str(self.ui.txt_ms_quality.text()),
            str(self.ui.txt_ms_notes.toPlainText()),
            self.ms_to_save.to_xml())
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

    # internal helper methods
    ###############################
            
    def retranslateUi(self, ui):
        self.setWindowTitle(get_ui_string("dlg.savems.window.title"))
        ui.lb_ms_create_date.setText(get_ui_string("dlg.savems.date"))
        ui.lb_ms_source.setText(get_ui_string("dlg.savems.source"))
        ui.lb_ms_quality.setText(get_ui_string("dlg.savems.quality"))
        ui.lb_ms_notes.setText(get_ui_string("dlg.savems.notes"))
        ui.lb_ms_name.setText(get_ui_string("dlg.savems.name"))
        ui.lb_ms_type.setText(get_ui_string("dlg.savems.type"))
        ui.lb_ms_region.setText(get_ui_string("dlg.savems.region"))

        ui.btn_save.setText(get_ui_string("app.dialog.button.ok"))
        ui.btn_close.setText(get_ui_string("app.dialog.button.close"))
