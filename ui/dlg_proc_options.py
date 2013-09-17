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
dialog for editing secondary modifiers
"""
from PyQt4.QtGui import QDialog

from sidd.constants import ExtrapolateOptions
from ui.qt.dlg_proc_options_ui import Ui_procOptionsDialog

class DialogProcessingOptions(Ui_procOptionsDialog, QDialog):
    """
    dialog specifying options for creating mapping scheme
    """
    def __init__(self, app):
        """ constructor """
        super(DialogProcessingOptions, self).__init__()
        self.ui = Ui_procOptionsDialog()
        self.ui.setupUi(self)
        self.setFixedSize(self.size())        
        
        self.app = app        
        
        # connect slot (ui event)
        self.ui.btn_ok.clicked.connect(self.accept)
        self.ui.btn_close.clicked.connect(self.reject)        

    def __dir__(self):
        return ['extrapolation']

    def resetOptions(self):
        self.extrapolation = ExtrapolateOptions.Fraction

    @property
    def extrapolation(self):
        if self.ui.radio_random.isChecked():
            return ExtrapolateOptions.RandomWalk
        elif self.ui.radio_actual.isChecked():
            return ExtrapolateOptions.Fraction
        elif self.ui.radio_actual_rounded.isChecked():
            return ExtrapolateOptions.FractionRounded
        else:
            # default case
            return ExtrapolateOptions.Fraction
    
    @extrapolation.setter
    def extrapolation(self, value):
        if value == ExtrapolateOptions.RandomWalk:
            self.ui.radio_random.setChecked(True)
        elif value == ExtrapolateOptions.Fraction:
            self.ui.radio_actual.setChecked(True)
        elif value == ExtrapolateOptions.FractionRounded:
            self.ui.radio_actual_rounded.setChecked(True)
        else:
            # default case
            self.ui.radio_actual.setChecked(True)
