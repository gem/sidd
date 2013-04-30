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

from ui.constants import logUICall, get_ui_string
from ui.qt.dlg_search_feature_ui import Ui_searchFeatureDialog

class DialogSearchFeature(Ui_searchFeatureDialog, QDialog):
    """
    dialog for saving mapping scheme (single/multilevel) into
    mapping scheme library database
    """    
    # constructor
    ###############################    
    def __init__(self, fields):
        super(DialogSearchFeature, self).__init__()
        self.ui = Ui_searchFeatureDialog()
        self.ui.setupUi(self)
        self.retranslateUi(self.ui)
        self.ui.cb_attribute.clear()
        self.ui.cb_attribute.addItems(fields)
        
        self.ui.btn_find.clicked.connect(self.accept)
        self.ui.btn_close.clicked.connect(self.reject)
    
    @property
    def attribute(self):
        return str(self.ui.cb_attribute.currentText())
    
    @property
    def value(self):
        return str(self.ui.txt_value.text())

