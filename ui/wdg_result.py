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
# Version: $Id: wdg_result.py 18 2012-10-24 20:21:41Z zh $

"""
Widget (Panel) for result review
"""

import sys
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from qgis.core import *
from qgis.gui import *

from utils.shapefile import *

from sidd.constants import *

from ui.constants import logUICall, get_ui_string
from ui.dlg_result import DialogResult
from ui.qt.wdg_result_ui import Ui_widgetResult

class WidgetResult(Ui_widgetResult, QWidget):
    """
    Widget (Panel) for result review
    """
    
    SEARCH_BUFFER = DEFAULT_GRID_SIZE/2.1
    EXPORT_FORMATS = {
        get_ui_string("app.extension.shapefile"):ExportTypes.Shapefile,
        get_ui_string("app.extension.kml"):ExportTypes.KML,
        get_ui_string("app.extension.nrml"):ExportTypes.NRML,
    };

    # constructor / destructor
    ###############################
    
    def __init__(self, mainWin):
        """ constructor """
        QWidget.__init__(self)        
        self.ui = Ui_widgetResult()
        self.ui.setupUi(self)
        self.retranslateUi(self.ui)

        # create canvas
        self.canvas = QgsMapCanvas(self.ui.widget_map)
        self.canvas.setGeometry(QRect(
            10, # x
            50, # y  
            self.ui.widget_map.width() - 20,  # width
            self.ui.widget_map.height() - 60  # height
            ))
        self.canvas.setCanvasColor(Qt.white)
        self.canvas.enableAntiAliasing(True)
        
        # create the map tools
        self.toolPan = QgsMapToolPan(self.canvas)
        self.toolZoomIn = QgsMapToolZoom(self.canvas, False) # false = in
        self.toolZoomOut = QgsMapToolZoom(self.canvas, True) # true = out
        self.toolInfo = QgsMapToolEmitPoint(self.canvas)
        QObject.connect(self.toolInfo, SIGNAL("canvasClicked(QgsPoint, Qt::MouseButton)"), self.canvasClicked)
        
        self.mainWin = mainWin
        
        self.dlgResultDetail = DialogResult()
        self.dlgResultDetail.setModal(True)
        self.project = None
        self.layer = None

        # default export setting
        self.export_format = ExportTypes.Shapefile


    # public methods
    ###############################
    @logUICall
    def showResult(self, project):
        """ do export data """
        layer = project.exposure        
        self.showResultLayer(layer)
        self.project = project

        
    @logUICall
    def showResultFile(self, pathtofile):
        """ do export data """        
        layer = load_shapefile(pathtofile, 'result')
        self.showResultLayer(layer)

    @logUICall
    def closeResult(self):
        if getattr(self, 'layer', None) is not None:
            try:
                registry = QgsMapLayerRegistry.instance()
                registry.removeMapLayer(self.layer.getLayerID(), False)
            except: pass
            del self.layer
        self.layer = None
        self.project = None
        
    @logUICall    
    def showResultLayer(self, layer):
        """ display result layer """
        if layer is None:
            return
        self.closeResult()
        
        registry = QgsMapLayerRegistry.instance()
        registry.addMapLayer(layer)
        layerSet = []
        for lyr in registry.mapLayers():
            layerSet.append(QgsMapCanvasLayer(registry.mapLayer(lyr)))
        self.canvas.setLayerSet(layerSet)
        self.canvas.setExtent(layer.extent())
        self.layer = layer

    # UI event handling calls
    ###############################
    
    @logUICall
    def mapPan(self):
        """ pan map """
        self.canvas.setMapTool(self.toolPan)

    @logUICall
    def mapZoomIn(self):
        """ zoom in on map """
        self.canvas.setMapTool(self.toolZoomIn)
        
    @logUICall
    def mapZoomOut(self):
        """ zoom out on map """
        self.canvas.setMapTool(self.toolZoomOut)
        
    @logUICall
    def mapZoomFull(self):
        """ zoom to full map """
        self.canvas.zoomToFullExtent()    
        
    @logUICall
    def mapIdentify(self):
        """ identify item on map """
        self.canvas.setMapTool(self.toolInfo)
        
    @logUICall
    def selectExportFile(self):
        """ open save file dialog box to select file name for export """
        filename = QFileDialog.getSaveFileName(self,
                                               get_ui_string("widget.result.export.file.open"),
                                               get_app_dir(),
                                               self.ui.cb_export_format.currentText())
        if not filename.isNull():
            self.ui.txt_export_select_file.setText(filename)            
    
    @logUICall
    def exportFormatChanged(self, FormatText):
        self.export_format = self.EXPORT_FORMATS[str(FormatText)]
        self.ui.txt_export_select_file.setText("")
    
    @logUICall
    def exportData(self):
        """ do export data """
        export_file = str(self.ui.txt_export_select_file.text())
        self.project.set_export(self.export_format, export_file)
        self.project.export_data()
        
    @logUICall    
    def canvasClicked(self, point, mouseButton):
        """ point-polygon search on result layer with clicked location """
        if not self.layer:
            return
        provider = self.layer.dataProvider()
        provider.rewind()
        feature = QgsFeature()
        colonIndexes = provider.attributeIndexes()
        fieldDict = provider.fields()
        
        provider.select(colonIndexes,
                        QgsRectangle(point.x()-self.SEARCH_BUFFER,
                                     point.y()-self.SEARCH_BUFFER,
                                     point.x()+self.SEARCH_BUFFER,
                                     point.y()+self.SEARCH_BUFFER),
                        False)        
        selected = []        
        while provider.nextFeature(feature):
            attrs = feature.attributeMap()
            selected.append(feature.attributeMap())

        if len(selected)>0:
            self.dlgResultDetail.showDetail(provider.fields(), selected)
            self.dlgResultDetail.exec_()
        else:
            QMessageBox.information(None, "nothing", "nothing there")

    def retranslateUi(self, ui):
        """ set constant strings """
        ui.lb_panel_title.setText(get_ui_string("widget.result.title"))
        ui.lb_export_title.setText(get_ui_string("widget.result.export.title"))
        ui.lb_export_format.setText(get_ui_string("widget.result.export.format"))
        ui.lb_export_select_file.setText(get_ui_string("app.file.select"))
        ui.btn_export_select_file.setText(get_ui_string("app.file.button"))
        ui.btn_export.setText(get_ui_string("widget.result.export.button"))

        ui.lbl_dq_test_title.setText(get_ui_string("widget.result.dq.title"))
        ui.lb_dq_test_warning.setText(get_ui_string("widget.result.dq.warning"))
   
        # populate export list
        ui.cb_export_format.clear()
        ui.cb_export_format.addItem(get_ui_string("app.extension.shapefile"))
        ui.cb_export_format.addItem(get_ui_string("app.extension.kml"))
        #ui.cb_export_format.addItem(get_ui_string("app.extension.nrml"))
        