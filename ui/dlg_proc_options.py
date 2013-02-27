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
# Version: $Id: dlg_mod_input.py 21 2012-10-26 01:48:25Z zh $

"""
dialog for editing secondary modifiers
"""
from PyQt4.QtGui import QDialog

from ui.constants import get_ui_string 
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
        self.retranslateUi(self.ui)
        self.setFixedSize(self.size())        
        
        self.app = app        
        
        # connect slot (ui event)
        self.ui.btn_ok.clicked.connect(self.accept)
        self.ui.btn_close.clicked.connect(self.reject)        

    def __dir__(self):
        return ['extrapolation']

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
            return ExtrapolateOptions.RandomWalk
    
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
            self.ui.radio_random.setChecked(True)
    
    def retranslateUi(self, ui):
        self.setWindowTitle(get_ui_string('dlg.options.window.title'))
        ui.box_extrapolate_options.setTitle(get_ui_string('dlg.options.ep.title'))
        ui.radio_random.setText(get_ui_string('dlg.options.ep.random'))
        ui.radio_actual.setText(get_ui_string('dlg.options.ep.fraction'))
        ui.radio_actual_rounded.setText(get_ui_string('dlg.options.ep.fraction.rounded'))
        
        ui.btn_ok.setText(get_ui_string('app.dialog.button.ok'))
        ui.btn_close.setText(get_ui_string('app.dialog.button.close'))        


