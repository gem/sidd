# Copyright (c) 2011-2013, ImageCat Inc.
#
# SIDD is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
#
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
