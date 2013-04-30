# Copyright (c) 2011-2013, ImageCat Inc.
#
# SIDD is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
#
"""
main program entry point
"""
import sys
import os
import types
import logging

from PyQt4.QtGui import QApplication
from qgis.core import QgsApplication

from sidd.appconfig import SIDDConfig
from sidd.constants import logAPICall 
from utils.system import get_app_dir

from ui.constants import logUICall
from ui.win_main import AppMainWindow
from ui.win_splash import AppSplashScreen 

# check for required environment parameters
#############################

errMsg = """
Environ variable %s is required for application.
Please see README.txt for more detail instructions
"""
env_keys = ['QGIS']
for _key in env_keys:
    if not os.environ.has_key(_key):
        print >> sys.stderr, errMsg % _key 
        sys.exit(1)

# start application 
############################# initialize QT
qtApp = QApplication(sys.argv)

splash = AppSplashScreen()
splash.show()
qtApp.processEvents()

# show splash screen for at least 1 second
from time import sleep
sleep(1)

# read configuration
sidd_config = SIDDConfig(get_app_dir() + '/app.cfg')

# initialize logging based on configuration
logging.basicConfig(level=logging.NOTSET)
logAPICall.setLevel(sidd_config.get('logging', 'core', 30, types.IntType))
logUICall.setLevel(sidd_config.get('logging', 'ui', 20, types.IntType))
os.environ['QGIS_DEBUG'] = sidd_config.get('logging', 'qgis', '-1')

# supply path to where is your qgis installed
QgsApplication.setPrefixPath(os.environ['QGIS'], True)
# load providers
QgsApplication.initQgis()

# initialize and show main window
mainWin = AppMainWindow(qtApp, sidd_config)
mainWin.show()

splash.finish(mainWin)

#exit
sys.exit(qtApp.exec_())
QgsApplication.exitQgis()

