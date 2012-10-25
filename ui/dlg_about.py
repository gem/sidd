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
# Version: $Id: dlg_about.py 17 2012-10-23 18:38:27Z zh $

"""
dialog showing about message
"""
from PyQt4.QtGui import *
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

    def retranslateUi(self, ui):
        self.setWindowTitle(get_ui_string("dlg.about.window.title"))
        self.ui.textEdit.setHtml(get_ui_string("dlg.about.message") % (SIDD_VERSION, 2012, 2012))
        self.ui.textEdit.setReadOnly(True)
