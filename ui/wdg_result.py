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
Widget (Panel) for result review
"""
from os.path import exists  

from PyQt4.QtGui import QWidget, QFileDialog, QDialog, QDialogButtonBox
from PyQt4.QtCore import Qt, QObject, QPoint, QRect, pyqtSlot
from PyQt4.QtXml import QDomDocument
from qgis.gui import QgsMapCanvas, QgsMapCanvasLayer, \
                     QgsMapToolPan, QgsMapToolZoom, QgsMapToolEmitPoint, \
                     QgsRendererV2PropertiesDialog
from qgis.core import QGis, QgsMapLayerRegistry, QgsCoordinateReferenceSystem, \
                      QgsCoordinateTransform, QgsFeature, QgsRectangle, \
                      QgsStyleV2, QgsFeatureRendererV2

from utils.shapefile import load_shapefile, layer_field_index, layer_features
from sidd.constants import ExportTypes, ExtrapolateOptions

from ui.constants import logUICall, get_ui_string, UI_PADDING
from ui.dlg_result import DialogResult
from ui.qt.wdg_result_ui import Ui_widgetResult
from ui.dlg_search_feature import DialogSearchFeature

class WidgetResult(Ui_widgetResult, QWidget):
    """
    Widget (Panel) for result review
    """
    
    ''' buffer around clicked point for point in polygon query ''' 
    SEARCH_BUFFER = 20.0
    ''' supported export formats '''
    EXPORT_FORMATS = {
        get_ui_string("app.extension.shapefile"):ExportTypes.Shapefile,
        #get_ui_string("app.extension.kml"):ExportTypes.KML,
        #get_ui_string("app.extension.nrml"):ExportTypes.NRML,
        get_ui_string("app.extension.csv"):ExportTypes.CSV,
    };
    ''' enumeration of Layer to be previewed '''
    EXPOSURE, SURVEY, POP_GRID, FOOTPRINT, ZONES = range(5);
    ''' name for Layer to be previewed '''
    LAYER_NAMES = [
        get_ui_string("widget.result.layer.exposure"),        
        get_ui_string("widget.result.layer.survey"),
        get_ui_string("widget.result.layer.popgrid"),
        get_ui_string("widget.result.layer.footprint"),        
        get_ui_string("widget.result.layer.zones"),
    ];    
    LAYER_STYLES = [
        '<!DOCTYPE renderer><renderer-v2 symbollevels="0" type="singleSymbol"><symbols><symbol outputUnit="MM" alpha="1" type="fill" name="0"><layer pass="0" class="SimpleLine" locked="0"><prop k="capstyle" v="square"/><prop k="color" v="0,0,0,255"/><prop k="customdash" v="5;2"/><prop k="joinstyle" v="bevel"/><prop k="offset" v="0"/><prop k="penstyle" v="solid"/><prop k="use_custom_dash" v="0"/><prop k="width" v="0.26"/></layer></symbol></symbols><rotation field=""/><sizescale field=""/></renderer-v2>',
        '<!DOCTYPE renderer><renderer-v2 symbollevels="0" type="singleSymbol"><symbols><symbol outputUnit="MM" alpha="1" type="marker" name="0"><layer pass="0" class="SimpleMarker" locked="0"><prop k="angle" v="0"/><prop k="color" v="0,0,255,255"/><prop k="color_border" v="0,0,255,255"/><prop k="name" v="circle"/><prop k="offset" v="0,0"/><prop k="size" v="2"/></layer></symbol></symbols><rotation field=""/><sizescale field=""/></renderer-v2>',
        '<!DOCTYPE renderer><renderer-v2 symbollevels="0" type="singleSymbol"><symbols><symbol outputUnit="MM" alpha="1" type="marker" name="0"><layer pass="0" class="SimpleMarker" locked="0"><prop k="angle" v="0"/><prop k="color" v="0,255,0,255"/><prop k="color_border" v="0,255,0,255"/><prop k="name" v="rectangle"/><prop k="offset" v="0,0"/><prop k="size" v="4"/></layer></symbol></symbols><rotation field=""/><sizescale field=""/></renderer-v2>',
        '<!DOCTYPE renderer><renderer-v2 symbollevels="0" type="singleSymbol"><symbols><symbol outputUnit="MM" alpha="1" type="fill" name="0"><layer pass="0" class="SimpleFill" locked="0"><prop k="color" v="170,250,170,255"/><prop k="color_border" v="0,0,0,255"/><prop k="offset" v="0,0"/><prop k="style" v="solid"/><prop k="style_border" v="solid"/><prop k="width_border" v="0.26"/></layer></symbol></symbols><rotation field=""/><sizescale field=""/></renderer-v2>',
        '<!DOCTYPE renderer><renderer-v2 symbollevels="0" type="singleSymbol"><symbols><symbol outputUnit="MM" alpha="1" type="fill" name="0"><layer pass="0" class="SimpleFill" locked="0"><prop k="color" v="211,211,158,200"/><prop k="color_border" v="0,0,0,255"/><prop k="offset" v="0,0"/><prop k="style" v="solid"/><prop k="style_border" v="solid"/><prop k="width_border" v="0.26"/></layer></symbol></symbols><rotation field=""/><sizescale field=""/></renderer-v2>',
    ]
    
    # constructor / destructor
    ###############################
    
    def __init__(self, app):
        """
        constructor
        - initialize UI elements
        - connect UI elements to callback            
        """
        super(WidgetResult, self).__init__()
        self.ui = Ui_widgetResult()
        self.ui.setupUi(self)
                
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
        self.canvas.zoomNextStatusChanged.connect(self.checkRendering)
        self.map_layers = [None] * len(self.LAYER_NAMES)
        self.map_layer_renderer = [None] * len(self.LAYER_NAMES)
        for idx, str_style in enumerate(self.LAYER_STYLES):
            rdoc = QDomDocument("renderer")
            rdoc.setContent(str_style)        
            self.map_layer_renderer[idx] = QgsFeatureRendererV2.load(rdoc.firstChild().toElement())

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
        self.canvas.setMapTool(self.toolPan)
        
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
        self.ui.btn_stop.clicked.connect(self.stopRendering)
        self.ui.btn_zoom_layer.clicked.connect(self.mapZoomLayer)        
        self.ui.btn_pan.clicked.connect(self.mapPan)
        self.ui.btn_theme.clicked.connect(self.mapEditTheme)
        self.ui.btn_info.clicked.connect(self.mapIdentify)
        
        self.ui.btn_zoom_to_feature.clicked.connect(self.searchFeature)
        
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
        self.ui.widget_export.move(x_right_side, self.ui.widget_map.y()+30)
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
        # logo
        self.ui.lb_gem_logo.move(self.width()-self.ui.lb_gem_logo.width(), self.ui.lb_gem_logo.y())

    @logUICall
    @pyqtSlot()
    def mapPan(self):
        """ event handler for btn_pan - pan map """
        self.canvas.unsetMapTool(self.toolInfo)
        self.canvas.setMapTool(self.toolPan)

    @logUICall
    @pyqtSlot()
    def mapZoomIn(self):
        """ event handler for btn_zoom_in - zoom in on map """
        self.canvas.unsetMapTool(self.toolInfo)
        self.canvas.setMapTool(self.toolZoomIn)

    @logUICall
    @pyqtSlot()
    def mapZoomOut(self):
        """ event handler for btn_zoom_out - zoom out on map """
        self.canvas.unsetMapTool(self.toolInfo)
        self.canvas.setMapTool(self.toolZoomOut)

    @logUICall
    @pyqtSlot()
    def mapZoomFull(self):
        """ event handler for btn_zoom_full - zoom to full map """
        self.canvas.zoomToFullExtent()

    def checkRendering(self, changed):
        self.canvas.setRenderFlag(True)
        
    @logUICall
    @pyqtSlot()
    def stopRendering(self):        
        self.canvas.setRenderFlag(False)

    @logUICall
    @pyqtSlot()
    def mapZoomLayer(self):
        self.canvas.unsetMapTool(self.toolInfo)
        cur_layer_name = self.ui.cb_layer_selector.currentText()                
        self.zoomToLayer(self.map_layers[self.LAYER_NAMES.index(cur_layer_name)])
        
    @logUICall
    @pyqtSlot()
    def mapEditTheme(self):
        """ event handler for btn_edit - identify item on map """
        cur_layer = self.ui.cb_layer_selector.currentText()
        try:
            cur_layer_idx = self.LAYER_NAMES.index(cur_layer)
            
            # build layer render property Dialog for selected layer  
            dlg_render = QDialog()
            dlg_render.setWindowTitle(get_ui_string('widget.result.renderer.settings'))
            dlg_render.setModal(True)
            dlg_render.setFixedSize(530, 370)
            dlg_render.renderer = QgsRendererV2PropertiesDialog(self.map_layers[cur_layer_idx], self.style, True)
            dlg_render.renderer.setParent(dlg_render)        
            dlg_render.renderer.setGeometry(QRect(10, 10, 510, 325))
            dlg_render.buttonBox = QDialogButtonBox(dlg_render)
            dlg_render.buttonBox.setGeometry(QRect(10, 335, 510, 25))
            dlg_render.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
            dlg_render.buttonBox.accepted.connect(dlg_render.accept)
            dlg_render.buttonBox.accepted.connect(dlg_render.renderer.onOK)
            dlg_render.buttonBox.rejected.connect(dlg_render.reject)
            dlg_render.setVisible(True)

            # get user input and update renderer
            answer = dlg_render.exec_()
            if answer == QDialog.Accepted:
                self.map_layer_renderer[cur_layer_idx] = None
                self.map_layer_renderer[cur_layer_idx] = self.map_layers[cur_layer_idx].rendererV2().clone()             
                self.canvas.refresh()
            dlg_render.destroy()
            del dlg_render
        except Exception as err:
            # thematic is not-critical, allow continue on exception
            logUICall.log(str(err), logUICall.WARNING)

    @logUICall
    @pyqtSlot()
    def searchFeature(self):        
        cur_layer = self.ui.cb_layer_selector.currentText()
        try:
            cur_layer_idx = self.LAYER_NAMES.index(cur_layer)            
            layer = self.map_layers[cur_layer_idx]
            fields = []
            for fidx in layer.dataProvider().fields():
                fields.append(layer.dataProvider().fields()[fidx].name())
            dlg_search = DialogSearchFeature(fields)           
            answer = dlg_search.exec_()
            if answer == QDialog.Accepted:
                extent = self.findFeatureExtentByAttribute(layer, dlg_search.attribute, dlg_search.value)
                if extent is not None:
                    self.zoomToExtent(extent)
                else:
                    logUICall.log(get_ui_string("widget.result.info.notfound"), logUICall.WARNING)
            dlg_search.destroy()
        except Exception as err:
            # thematic is not-critical, allow continue on exception
            logUICall.log(str(err), logUICall.WARNING)
            
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
        """        filename = QFileDialog.getSaveFileName(self,
                                               get_ui_string("widget.result.export.file.open"),
                                               ".", 
                                               self.ui.cb_export_format.currentText())
        if not filename.isNull():
            self.ui.txt_export_select_path.setText(filename) 
                    
    @logUICall
    @pyqtSlot(str)
    def exportFormatChanged(self, selected_val):
        """
        event handler for cb_export_format 
        - update selected file after format change
        """
        self.ui.txt_export_select_path.setText("")
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
            logUICall.log(get_ui_string("app.error.path.is.null"), logUICall.WARNING)
            return
        self.app.exportResults(self.export_format, export_path)

        
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
                # display result if exists
                if cur_layer_idx == self.EXPOSURE:
                    self.dlgResultDetail.showExposureData(provider.fields(), selected)                    
                else:
                    self.dlgResultDetail.showInfoData(provider.fields(), selected)
                self.dlgResultDetail.exec_()
            else:
                logUICall.log(get_ui_string("widget.result.info.notfound"), logUICall.WARNING)
        except Exception as err:
            # point-in-polygon search is not critical, continue on error 
            logUICall.log(str(err), logUICall.WARNING)
        
    # public methods
    ###############################
    def set_project(self, project):
        ''' set project to preview. force refresh view on set'''        
        self._project = project
        if project is None:
            return
        self.canvas.setRenderFlag(False)
        self.refreshView()
        self.canvas.setRenderFlag(True)        
        logUICall.log("Project preview initialized sucessfully", logUICall.INFO)
        
    def get_project(self):
        return self._project
    
    # property access to project
    project = property(get_project, set_project)
    
    def refreshView(self):
        ''' reload all QGIS layers in currently defined project '''
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
        
        if self._project.popgrid_file is not None and exists(self._project.popgrid_file):
            if getattr(self._project, 'popgrid', None) is None:
                self.map_layers[self.POP_GRID] = load_shapefile(self._project.popgrid_file, 'popgrid') 
                self.showDataLayer(self.map_layers[self.POP_GRID], self.map_layer_renderer[self.POP_GRID])
        else:            
            self.removeDataLayer(self.POP_GRID)
        
        # set export options
        for idx, export_format in enumerate(self.EXPORT_FORMATS.values()):
            if export_format == self._project.export_type:
                self.ui.cb_export_format.setCurrentIndex(idx)
        self.ui.txt_export_select_path.setText(self._project.export_path)
        self.refreshResult()

    def refreshResult(self):
        ''' reload result QGIS layer and data quality reports in currently defined project '''
        exposure = getattr(self._project, 'exposure', None)
        exposure_layer = self.EXPOSURE
        exposure_renderer = self.EXPOSURE

        if exposure is not None:
            self.map_layers[exposure_layer] = exposure 
            self.showDataLayer(self.map_layers[exposure_layer], self.map_layer_renderer[exposure_renderer])
            has_result = True            
        else:
            self.map_layers[exposure_layer] = None 
            self.removeDataLayer(exposure_layer)
            has_result = False
        
        if has_result:
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


        self.ui.btn_export.setEnabled(has_result)
        self.ui.widget_dq_test.setVisible(has_result)
        self.ui.txt_export_select_path.setEnabled(has_result)
        self.ui.btn_export_select_path.setEnabled(has_result)
        self.ui.cb_export_format.setEnabled(has_result)        
            
    @logUICall
    def closeResult(self):
        ''' remove from map result QGIS layer and reset quality report display '''
        self.removeDataLayer(self.EXPOSURE)
        self.ui.txt_dq_test_details.setText("")

    @logUICall
    def closeAll(self):
        ''' remove from map all QGIS layer in currently defined project '''
        self.ui.cb_layer_selector.clear()
        if getattr(self, 'registry', None) is None:
            self.registry = QgsMapLayerRegistry.instance()
        try:
            for i in range(5):
                self.removeDataLayer(i)
            self.registry.removeAllMapLayers ()
            self.ui.txt_dq_test_details.setText("")
        except:            
            pass    # exception will is thrown when registry is empty
        finally:
            self.canvas.setLayerSet([])
            self.canvas.refresh()
    
    # internal helper methods
    ###############################
    def showDataLayer(self, layer, renderer=None, refreshCanvas=True):
        """ display given QGIS layer on map """
        if getattr(self, 'registry', None) is None:
            self.registry = QgsMapLayerRegistry.instance()
        try:
            # add to QGIS registry and refresh view
            self.registry.addMapLayer(layer)
            if renderer is not None:
                layer.setRendererV2(renderer)
            if refreshCanvas:
                self.refreshLayers()
                self.zoomToLayer(layer)
        except:
            return None

    def removeDataLayer(self, index):
        """ remove from map the layer identified with index """
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

    def findFeatureExtentByAttribute(self, layer, field, value):
        """ 
        find extent of all objects in QGIS layer matching condition "field=value"         
        """
        fidx = layer_field_index(layer, field)
        if fidx == -1:
            return None
        xmin, xmax, ymin, ymax = 180, -180, 90, -90
        extent = QgsRectangle(xmin, ymin, xmax, ymax)
        need_transform = layer.crs() != self.canvas.mapRenderer().destinationCrs()
        if need_transform:
            transform = QgsCoordinateTransform(layer.crs(), self.canvas.mapRenderer().destinationCrs())
        for feature in layer_features(layer):
            if str(value) == feature.attributeMap()[fidx].toString():
                f_extent = feature.geometry().boundingBox()
                if need_transform:
                    f_extent = transform.transform(f_extent)
                xmin = min(f_extent.xMinimum(), xmin)
                xmax = max(f_extent.xMaximum(), xmax)
                ymin = min(f_extent.yMinimum(), ymin)
                ymax = max(f_extent.yMaximum(), ymax)
        extent.set (xmin, ymin, xmax, ymax)
        return extent

    def zoomToLayer(self, layer):
        """ zoom canvas to extent of given layer """
        try:
            lyr_extent = layer.extent()            
            if layer.crs() != self.canvas.mapRenderer().destinationCrs():
                transform = QgsCoordinateTransform(layer.crs(), self.canvas.mapRenderer().destinationCrs())
                lyr_extent = transform.transform(lyr_extent)
            self.zoomToExtent(lyr_extent)
        except:
            pass
    
    def zoomToExtent(self, extent):
        """ zoom canvas to given extent """
        try:
            self.canvas.setExtent(extent)
            self.canvas.zoomByFactor(1.1)
            self.canvas.refresh()
        except:
            self.mapZoomFull()
    
    def refreshLayers(self, refreshCanvas=True):
        """ refresh all layers in canvas """
        # add each layer according to order
        layerSet = []
        self.ui.cb_layer_selector.clear()
        for idx, lyr in enumerate(self.map_layers):
            if lyr is not None:
                layerSet.append(QgsMapCanvasLayer(lyr))
                self.ui.cb_layer_selector.addItem(self.LAYER_NAMES[idx])
        self.canvas.setLayerSet(layerSet)
        if refreshCanvas:
            self.canvas.refresh()
