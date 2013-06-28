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
from PyQt4.QtGui import QDialog
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

