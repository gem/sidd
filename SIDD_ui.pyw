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
from utils.system import get_app_dir, check_environ, check_required_files

from ui.constants import logUICall
from ui.win_main import AppMainWindow
from ui.win_splash import AppSplashScreen 

if __name__=='__main__':
    # check for required environment parameters
    #############################
    try:            
        env_keys = ['QGIS']
        check_environ(env_keys)
    except Exception, err:
        errMsg = """
        Environ variable %s is required for application.
        Please see README.txt for more detail instructions
        """
        print >> sys.stderr, errMsg % err 
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
    
    # check required files 
    appDir = get_app_dir()
    try:    
        from sidd.project import FILE_PROJ_TEMPLATE 
        from ui.constants import FILE_MS_DB
        required_files = [
            FILE_PROJ_TEMPLATE,
            FILE_MS_DB,
        ]
        check_required_files(required_files, appDir)
    except Exception, err:
        errMsg = """
        Required file %s is missing. 
        Please make sure installation files are intact.  
        """
        print >> sys.stderr, errMsg % err 
        sys.exit(1)

    
    # read configuration
    sidd_config = SIDDConfig(appDir + '/app.cfg')
    
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
    
    # if project file given as part of parameter, 
    # open project file 
    if len(sys.argv) == 2:
        mainWin.openProjectFile(sys.argv[1])
    splash.finish(mainWin)
    
    #exit
    sys.exit(qtApp.exec_())
    QgsApplication.exitQgis()
