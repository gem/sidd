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
# Version: $Id: dlg_apply.py 18 2012-10-24 20:21:41Z zh $

"""
dialog showing about message
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import * 

from ui.constants import get_ui_string
from ui.qt.dlg_apply_ui import Ui_DialogApply

class DialogApply(Ui_DialogApply, QDialog):
    """
    dialog showing about message
    """
    
    def __init__(self, mainWin):
        """ constructor """
        QDialog.__init__(self)        
        self.ui = Ui_DialogApply()
        self.ui.setupUi(self)
        self.retranslateUi(self.ui)

    def retranslateUi(self, ui):
        self.setWindowTitle(get_ui_string("dlg.apply.window.title"))
        ui.lb_description.setText(get_ui_string("dlg.apply.message"))
