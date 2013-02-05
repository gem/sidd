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
# Version: $Id: win_main.py 21 2012-10-26 01:48:25Z zh $

"""
Main application window
"""
from PyQt4.QtGui import QSplashScreen, QPixmap
from PyQt4.QtCore import Qt 

class AppSplashScreen(QSplashScreen):
    def __init__(self):
        splash_pix = QPixmap(':/imgs/logo.png')
        super(AppSplashScreen, self).__init__(splash_pix, Qt.WindowStaysOnTopHint)
        self.setMask(splash_pix.mask())
