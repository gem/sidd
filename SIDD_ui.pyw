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
# Version: $Id: SIDD_ui.pyw 18 2012-10-24 20:21:41Z zh $

"""
main program entry point
"""
import sys
import os
import types
import logging

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *

from sidd.appconfig import sidd_config
from sidd.constants import logAPICall 

from ui.constants import logUICall
from ui.win_main import AppMainWindow

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

# initialize logging based on configuration
logging.basicConfig(level=logging.NOTSET)
logAPICall.setLevel(sidd_config.get('logging', 'core', 30, types.IntType))
logUICall.setLevel(sidd_config.get('logging', 'ui', 20, types.IntType))
os.environ['QGIS_DEBUG'] = sidd_config.get('logging', 'qgis', '-1')

# start application 
#############################

# initialize QT
qtApp = QApplication(sys.argv)

# supply path to where is your qgis installed
QgsApplication.setPrefixPath(os.environ['QGIS'], True)
# load providers
QgsApplication.initQgis()

# initialize and show main window
mainWin = AppMainWindow(qtApp)
mainWin.show()

#exit
sys.exit(qtApp.exec_())
QgsApplication.exitQgis()

