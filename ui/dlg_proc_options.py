# Copyright (c) 2011-2013, ImageCat Inc.
#
# SIDD is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
#
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

    # internal helper methods
    ###############################    
    def retranslateUi(self, ui):
        """ set text for ui elements """
        # dialog title
        self.setWindowTitle(get_ui_string('dlg.options.ep.window.title'))
        # ui elements
        ui.box_extrapolate_options.setTitle(get_ui_string('dlg.options.ep.title'))
        ui.radio_random.setText(get_ui_string('dlg.options.ep.random'))
        ui.radio_actual.setText(get_ui_string('dlg.options.ep.fraction'))
        ui.radio_actual_rounded.setText(get_ui_string('dlg.options.ep.fraction.rounded'))        
        ui.btn_ok.setText(get_ui_string('app.dialog.button.ok'))
        ui.btn_close.setText(get_ui_string('app.dialog.button.close'))        
