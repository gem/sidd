@echo off

REM Change LIB_HOME to root directory of Quantum GIS installation
REM The following are example installation directories
REM - use local package (when available as part of local packaging)
REN SET LIB_HOME=%CD%
REM - as part of OSGeo packages
SET LIB_HOME=C:\OSGeo4W
REM - as Stand-alone installation
REM SET LIB_HOME=C:\Program Files\Quantum GIS\

REM
REM Do not change following environments
REM
SET QT_PLUGIN_PATH=%LIB_HOME%\apps\qt4\
SET QT_RASTER_CLIP_LIMIT=4096
SET PROJ_LIB=%LIB_HOME%\share\proj\
SET GEOTIFF_CSV=%LIB_HOME%\share\epsg_csv\

SET QGIS=%LIB_HOME%\apps\qgis\
SET QGIS_DEBUG=0
SET PYTHONHOME=%LIB_HOME%\apps\python27\
SET PYTHONPATH=%PYTHONHOME%\LIB;%LIB_HOME%\apps\qgis\python

PATH=%LIB_HOME%\bin;%QGIS%\bin;%PATH%;

@echo on

%1 %2 %3 %4 %5