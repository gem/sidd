# Copyright (c) 2011-2013, ImageCat Inc.
#
# SIDD is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
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
        