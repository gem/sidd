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
# Version: $Id: wdg_result.py 21 2012-10-26 01:48:25Z zh $

"""
Widget (Panel) for result review
"""
from os.path import exists  

from PyQt4.QtGui import QWidget, QMessageBox, QFileDialog
from PyQt4.QtCore import Qt, QObject, QPoint, pyqtSlot
from qgis.gui import QgsMapCanvas, QgsMapCanvasLayer, \
                     QgsMapToolPan, QgsMapToolZoom, QgsMapToolEmitPoint, \
                     QgsRendererV2PropertiesDialog
from qgis.core import QGis, QgsMapLayerRegistry, QgsStyleV2, \
                      QgsCoordinateReferenceSystem, QgsCoordinateTransform, \
                      QgsFeature, QgsRectangle

from utils.shapefile import load_shapefile
from sidd.constants import ExportTypes, ExtrapolateOptions

from ui.constants import logUICall, get_ui_string, UI_PADDING
from ui.dlg_result import DialogResult
from ui.qt.wdg_result_ui import Ui_widgetResult

class WidgetResult(Ui_widgetResult, QWidget):
    """
    Widget (Panel) for result review
    """
    
    ''' buffer around clicked point for point in polygon query ''' 
    SEARCH_BUFFER = 20.0
    ''' supported export formats '''
    EXPORT_FORMATS = {
        get_ui_string("app.extension.shapefile"):ExportTypes.Shapefile,
        get_ui_string("app.extension.kml"):ExportTypes.KML,
        #get_ui_string("app.extension.nrml"):ExportTypes.NRML,
        get_ui_string("app.extension.csv"):ExportTypes.CSV,
    };
    ''' ennumaration of Layer to be previewed '''
    EXPOSURE, EXPOSURE_GRID, SURVEY, FOOTPRINT, ZONES = range(5);
    ''' name for Layer to be previewed '''
    LAYER_NAMES = [
        get_ui_string("widget.result.layer.exposure"),
        get_ui_string("widget.result.layer.exposure_grid"),
        get_ui_string("widget.result.layer.survey"),
        get_ui_string("widget.result.layer.footprint"),
        get_ui_string("widget.result.layer.zones"),
    ];    
    
    # constructor / destructor
    ###############################
    
    def __init__(self, app):
        """ constructor """
        QWidget.__init__(self)
        self.ui = Ui_widgetResult()
        self.ui.setupUi(self)
        self.retranslateUi(self.ui)

        # create canvas
        self.canvas = QgsMapCanvas(self.ui.widget_map)
        self.canvas.setGeometry(
            0,                                                                # x
            self.ui.widget_map_menu_l.x()+self.ui.widget_map_menu_l.height(), # y  
            self.ui.widget_map.width() - 2*UI_PADDING,  # width
            self.ui.widget_map.width() - 2*UI_PADDING   # height
            )
        
        self.canvas.setCanvasColor(Qt.white)
        self.canvas.enableAntiAliasing(True)
        self.canvas.mapRenderer().setProjectionsEnabled(True)
        self.canvas.mapRenderer().setDestinationCrs(QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.PostgisCrsId))
        self.map_layers = [None] * len(self.LAYER_NAMES)
        self.map_layer_renderer = [None] * len(self.LAYER_NAMES)

        # populate export list
        self.ui.cb_export_format.clear()
        for export_format in self.EXPORT_FORMATS.keys():
            self.ui.cb_export_format.addItem(export_format)
                    
        # style object required for QgsRendererV2PropertiesDialog
        self.style = QgsStyleV2()
        
        # create the map tools
        self.toolPan = QgsMapToolPan(self.canvas)
        self.toolZoomIn = QgsMapToolZoom(self.canvas, False) # false = in
        self.toolZoomOut = QgsMapToolZoom(self.canvas, True) # true = out
        self.toolInfo = QgsMapToolEmitPoint(self.canvas)
        self.toolInfo.canvasClicked.connect(self.showInfo)
        
        # additional         
        self.dlgResultDetail = DialogResult()
        self.dlgResultDetail.setModal(True)

        # set link to application main controller
        self.app = app
        
        # reset project
        self._project = None
        
        # default export setting
        self.export_format = ExportTypes.Shapefile
        
        # connect slots (ui event)
        self.ui.btn_zoom_full.clicked.connect(self.mapZoomFull)
        self.ui.btn_zoom_in.clicked.connect(self.mapZoomIn)
        self.ui.btn_zoom_out.clicked.connect(self.mapZoomOut)
        self.ui.btn_zoom_layer.clicked.connect(self.mapZoomLayer)
        self.ui.btn_pan.clicked.connect(self.mapPan)
        self.ui.btn_theme.clicked.connect(self.mapEditTheme)
        self.ui.btn_info.clicked.connect(self.mapIdentify)
        
        self.ui.cb_export_format.currentIndexChanged[str].connect(self.exportFormatChanged)
        self.ui.btn_export.clicked.connect(self.exportData)
        self.ui.btn_export_select_path.clicked.connect(self.selectExportFile)

    # UI event handling calls (Qt slots)
    ###############################
    
    @pyqtSlot(QObject)
    def resizeEvent(self, event):
        """ handle window resize """ 
        # find left coordinate for right side panels
        x_right_side = self.width()-self.ui.widget_export.width()-UI_PADDING
        # adjust right side panels
        self.ui.widget_export.move(x_right_side, 30)
        self.ui.widget_dq_test.move(x_right_side, self.ui.widget_export.y()+self.ui.widget_export.height()+UI_PADDING)
        # adjust map panel (left side)        
        self.ui.widget_map.resize(x_right_side-UI_PADDING, self.height()-2*UI_PADDING)
        # adjust map canvas within the map panel        
        map_top = self.ui.widget_map_menu_l.x()+self.ui.widget_map_menu_l.height()+UI_PADDING        
        self.canvas.resize(
            x_right_side-UI_PADDING,                            # same width as self.ui.widget_map
            self.ui.widget_map.height()-map_top-2*UI_PADDING)   # height        
        # adjust map menu
        self.ui.widget_map_menu_r.move(
            self.ui.widget_map.width()-self.ui.widget_map_menu_r.width(),   # right align with map panel 
            0)

    @logUICall
    @pyqtSlot()
    def mapPan(self):
        """ event handler for btn_pan - pan map """
        self.canvas.setMapTool(self.toolPan)

    @logUICall
    @pyqtSlot()
    def mapZoomIn(self):
        """ event handler for btn_zoom_in - zoom in on map """
        self.canvas.setMapTool(self.toolZoomIn)

    @logUICall
    @pyqtSlot()
    def mapZoomOut(self):
        """ event handler for btn_zoom_out - zoom out on map """
        self.canvas.setMapTool(self.toolZoomOut)
        
    @logUICall
    @pyqtSlot()
    def mapZoomFull(self):
        """ event handler for btn_zoom_full - zoom to full map """
        self.canvas.zoomToFullExtent()

    @logUICall
    @pyqtSlot()
    def mapZoomLayer(self):
        cur_layer_name = self.ui.cb_layer_selector.currentText()                
        self.zoomToLayer(self.map_layers[self.LAYER_NAMES.index(cur_layer_name)])
        
    @logUICall
    @pyqtSlot()
    def mapEditTheme(self):
        """ event handler for btn_edit - identify item on map """
        cur_layer = self.ui.cb_layer_selector.currentText()
        try:
            cur_layer_idx = self.LAYER_NAMES.index(cur_layer)            

            # create property dialog box for current layer
            dlg_render = QgsRendererV2PropertiesDialog(self.map_layers[cur_layer_idx], self.style)            
            answer = dlg_render.exec_()
            if answer == QMessageBox.Accepted:
                self.map_layer_renderer[cur_layer_idx] = None
                self.map_layer_renderer[cur_layer_idx] = self.map_layers[cur_layer_idx].rendererV2().clone()             
                self.canvas.refresh()
            dlg_render.destroy()            
        except Exception as err:
            print err
            
    @logUICall
    @pyqtSlot()
    def mapIdentify(self):
        """ 
        event handler for btn_info 
        This only enables map querying, method connected to canvasClicked signal does
        the actual point-polygon query     
        """
        self.canvas.setMapTool(self.toolInfo)

    @logUICall
    @pyqtSlot()
    def selectExportFile(self):
        """
        event handler for btn_export_select_path 
        - open save file dialog box to select file name for export 
        """     
        folder = QFileDialog.getExistingDirectory(self, get_ui_string("widget.result.export.path.dialog"))            
        if not folder.isNull():
            self.ui.txt_export_select_path.setText(folder)
        
    @logUICall
    @pyqtSlot(str)
    def exportFormatChanged(self, selected_val):
        """
        event handler for cb_export_format 
        - update selected file after format change
        """
        self.export_format = self.EXPORT_FORMATS[str(selected_val)]
        
    @logUICall
    @pyqtSlot()
    def exportData(self):
        """ 
        event handler for btn_export
        - do export data 
        """
        export_path = str(self.ui.txt_export_select_path.text())
        if export_path == "":
            QMessageBox.critical(self, 
                                 get_ui_string("app.warning.title"), 
                                 get_ui_string("app.error.path.is.null"))
            return
        self._project.set_export(self.export_format, export_path)
        self._project.export_data()
        
    @logUICall
    @pyqtSlot(QPoint, QObject)
    def showInfo(self, point, mouseButton):
        """
        event handler for toolInfo
        @see QGIS tutorial for detail
        point-polygon search on currently selected layer  
        """
        cur_layer_name = self.ui.cb_layer_selector.currentText()
        try:
            cur_layer_idx = self.LAYER_NAMES.index(cur_layer_name)
            cur_layer = self.map_layers[cur_layer_idx]
            
            # if layer is not in same projection as map canvas
            # need to project query point
            if cur_layer.crs() != self.canvas.mapRenderer().destinationCrs():
                transform = QgsCoordinateTransform(self.canvas.mapRenderer().destinationCrs(), cur_layer.crs())
                point = transform.transform(point)
            
            # do query
            provider = cur_layer.dataProvider() 
            provider.rewind()
            feature = QgsFeature()
            colonIndexes = provider.attributeIndexes()
        
            # search using point as center of rectangle polygon
            search_buffer_x = self.canvas.extent().width() * self.SEARCH_BUFFER / self.canvas.width()
            search_buffer_y = self.canvas.extent().height() * self.SEARCH_BUFFER / self.canvas.height()
            provider.select(colonIndexes,
                            QgsRectangle(point.x()-search_buffer_x,
                                         point.y()-search_buffer_y,
                                         point.x()+search_buffer_x,
                                         point.y()+search_buffer_y),
                            True)
            # get selected and display in result detail dialog box 
            selected = []        
            while provider.nextFeature(feature):            
                # for polygons, only show geometry containing query point            
                if cur_layer.geometryType() == QGis.Polygon:                
                    if feature.geometry() is not None and not feature.geometry().contains (point):
                        continue
                selected.append(feature.attributeMap())

            if len(selected)>0:
                # display result
                if cur_layer_idx == self.EXPOSURE:
                    self.dlgResultDetail.showExposureData(provider.fields(), selected)                    
                else:
                    self.dlgResultDetail.showInfoData(provider.fields(), selected)
                self.dlgResultDetail.exec_()
            else:
                QMessageBox.information(self, 
                                        get_ui_string("app.warning.title"), 
                                        get_ui_string("widget.result.info.notfound"))
        except Exception as err:
            print err       
        
    # public methods
    ###############################
    def set_project(self, project):
        ''' set project to preview. force refresh view on set'''        
        self._project = project
        if project is None:
            return   
        self.refreshView()       
        logUICall.log("Project preview initialized sucessfully", logUICall.INFO)
        
    def get_project(self):
        return self._project
    
    # property access to project
    project = property(get_project, set_project)
    
    def refreshView(self):
        if self._project is None:
            return
        # display layers if exists                
        if self._project.fp_file is not None and exists(self._project.fp_file):
            if self.map_layers[self.FOOTPRINT] is None or self.map_layers[self.FOOTPRINT].source() != self._project.fp_file:                            
                self.map_layers[self.FOOTPRINT] = load_shapefile(self._project.fp_file, 'footprint')
                self.showDataLayer(self.map_layers[self.FOOTPRINT], self.map_layer_renderer[self.FOOTPRINT])
        else:            
            self.removeDataLayer(self.FOOTPRINT)
        
        if self._project.zone_file is not None and exists(self._project.zone_file):
            if self.map_layers[self.ZONES] is None or self.map_layers[self.ZONES].source() != self._project.zone_file:
                self.map_layers[self.ZONES] = load_shapefile(self._project.zone_file, 'zones')
                self.showDataLayer(self.map_layers[self.ZONES], self.map_layer_renderer[self.ZONES])
        else:            
            self.removeDataLayer(self.ZONES)
            
        if self._project.survey_file is not None and exists(self._project.survey_file):
            if getattr(self._project, 'survey', None) is None:
                self._project.load_survey()
                self.map_layers[self.SURVEY] = self._project.survey 
                self.showDataLayer(self.map_layers[self.SURVEY], self.map_layer_renderer[self.SURVEY])
        else:            
            self.removeDataLayer(self.SURVEY)
        
        # set export options
        for idx, export_format in enumerate(self.EXPORT_FORMATS.values()):
            if export_format == self._project.export_type:
                self.ui.cb_export_format.setCurrentIndex(idx)
        self.ui.txt_export_select_path.setText(self._project.export_path)
        self.refreshResult()

    def refreshResult(self):        
        exposure = getattr(self._project, 'exposure', None)
        if exposure is not None:
            # display exposure layer
            #self.map_layers[self.EXPOSURE] = exposure 
            #self.showDataLayer(self.map_layers[self.EXPOSURE], self.map_layer_renderer[self.EXPOSURE])
            
            # build quality report 
            report_lines = []
            if self._project.operator_options.has_key("proc.extrapolation"):
                proc_option = self._project.operator_options["proc.extrapolation"]
                if proc_option == ExtrapolateOptions.RandomWalk:
                    proc_method = get_ui_string("widget.result.dq.method", get_ui_string("dlg.options.ep.random"))
                elif proc_option == ExtrapolateOptions.Fraction:
                    proc_method = get_ui_string("widget.result.dq.method", get_ui_string("dlg.options.ep.fraction"))
                elif proc_option == ExtrapolateOptions.FractionRounded:
                    proc_method = get_ui_string("widget.result.dq.method", get_ui_string("dlg.options.ep.fraction.rounded"))
            else:
                proc_method = get_ui_string("widget.result.dq.method", get_ui_string("dlg.options.ep.random")) 
            report_lines.append(proc_method)
            report_lines.append('')
            
            # total tests
            report_lines.append(get_ui_string('widget.result.dq.total_tests', len(self._project.quality_reports.keys())))
            report_lines.append('')
            
            # detail for each test
            for key, report in self._project.quality_reports.iteritems():
                report_lines.append(get_ui_string('widget.result.dq.tests.%s' % key))
                for title, value in report.iteritems():
                    report_lines.append( get_ui_string('widget.result.dq.tests.%s.%s' % (key, title), value) )
                report_lines.append('')                    
            
            self.ui.txt_dq_test_details.setText("\n".join(report_lines))
            has_result = True
        else:
            #self.map_layers[self.EXPOSURE] = None 
            #self.removeDataLayer(self.EXPOSURE)
            has_result = False

        exposure_grid = getattr(self._project, 'exposure_grid', None)
        if exposure_grid is not None:
            self.map_layers[self.EXPOSURE_GRID]=exposure_grid
            self.showDataLayer(self.map_layers[self.EXPOSURE_GRID], self.map_layer_renderer[self.EXPOSURE_GRID]) 
        else:
            self.map_layers[self.EXPOSURE_GRID] = None 
            self.removeDataLayer(self.EXPOSURE_GRID)
            
        self.ui.btn_export.setEnabled(has_result)
        self.ui.widget_dq_test.setVisible(has_result)
        self.ui.txt_export_select_path.setEnabled(has_result)
        self.ui.btn_export_select_path.setEnabled(has_result)
        self.ui.cb_export_format.setEnabled(has_result)        
            
    @logUICall
    def closeResult(self):
        self.removeDataLayer(self.EXPOSURE)
        self.removeDataLayer(self.EXPOSURE_GRID)

    def closeAll(self):
        self.ui.cb_layer_selector.clear()
        if getattr(self, 'registry', None) is None:
            self.registry = QgsMapLayerRegistry.instance()
        try:
            for i in range(5):
                self.removeDataLayer(i)
            self.registry.removeAllMapLayers ()
        except:            
            pass    # exception will is thrown when registry is empty
        finally:
            self.canvas.setLayerSet([])
            self.canvas.refresh()
                
    # internal helper methods
    ###############################
    @logUICall    
    def showDataLayer(self, layer, renderer=None, zoom_to=True):
        """ display result layer """
        if getattr(self, 'registry', None) is None:
            self.registry = QgsMapLayerRegistry.instance()
        try:
            # add to QGIS registry and refresh view
            self.registry.addMapLayer(layer)
            if renderer is not None:
                layer.setRendererV2(renderer)            
            self.refreshLayers()
            if (zoom_to):
                self.zoomToLayer(layer)
        except:
            return None

    def removeDataLayer(self, index):
        if getattr(self, 'registry', None) is None:
            self.registry = QgsMapLayerRegistry.instance()
        layer = self.map_layers[index]
        self.map_layers[index] = None        
        if layer is not None:                
            try:    
                self.canvas.clear()
                self.canvas.setLayerSet([])
                self.registry.removeMapLayer(layer.getLayerID(), False)            
            except:
                pass # do nothing if it fails. probably already deleted
            self.refreshLayers()        

    def zoomToLayer(self, layer):
        """ zoom canvas to extent of given layer """
        try:
            lyr_extent = layer.extent()            
            if layer.crs() != self.canvas.mapRenderer().destinationCrs():
                transform = QgsCoordinateTransform(layer.crs(), self.canvas.mapRenderer().destinationCrs())
                lyr_extent = transform.transform(lyr_extent)
                            
            self.canvas.setExtent(lyr_extent)
            self.canvas.zoomByFactor(1.1)
            self.canvas.refresh()
        except:
            self.mapZoomFull()
            
    def refreshLayers(self):
        """ refresh all layers """
        # add each layer according to order
        layerSet = []
        self.ui.cb_layer_selector.clear()
        for idx, lyr in enumerate(self.map_layers):
            if lyr is not None:
                layerSet.append(QgsMapCanvasLayer(lyr))
                self.ui.cb_layer_selector.addItem(self.LAYER_NAMES[idx])
        self.canvas.setLayerSet(layerSet)
        self.canvas.refresh()

    def retranslateUi(self, ui):
        """ set text for ui elements """
        # ui elements    
        ui.lb_panel_title.setText(get_ui_string("widget.result.title"))
        ui.lb_layer_selector.setText(get_ui_string("widget.result.layers.selector"))
        ui.lb_export_title.setText(get_ui_string("widget.result.export.title"))
        ui.lb_export_format.setText(get_ui_string("widget.result.export.format"))
        ui.lb_export_select_path.setText(get_ui_string("app.folder.select"))
        ui.lbl_dq_test_title.setText(get_ui_string("widget.result.dq.title"))
        ui.btn_export_select_path.setText(get_ui_string("app.file.button"))
        ui.btn_export.setText(get_ui_string("widget.result.export.button"))
        # tooltip for icon buttons
        ui.btn_zoom_in.setToolTip(get_ui_string("widget.result.button.zoomin"))
        ui.btn_zoom_out.setToolTip(get_ui_string("widget.result.button.zoomout"))
        ui.btn_zoom_layer.setToolTip(get_ui_string("widget.result.button.zoomlayer"))
        ui.btn_pan.setToolTip(get_ui_string("widget.result.button.pan"))
        ui.btn_zoom_full.setToolTip(get_ui_string("widget.result.button.zoomfull"))
        ui.btn_theme.setToolTip(get_ui_string("widget.result.button.theme"))
        ui.btn_info.setToolTip(get_ui_string("widget.result.button.info"))
        