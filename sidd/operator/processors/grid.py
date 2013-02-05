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
# Version: $Id: grid.py 18 2012-10-24 20:21:41Z zh $

"""
module to support grid exposure database write out
"""
from math import floor, ceil

from PyQt4.QtCore import QVariant
from qgis.core import QGis, QgsVectorFileWriter, QgsFeature, QgsField, QgsGeometry, QgsPoint
from qgis.analysis import QgsOverlayAnalyzer

from utils.shapefile import load_shapefile, layer_features, layer_field_index, remove_shapefile
from utils.system import get_unique_filename

from sidd.constants import logAPICall, DEFAULT_GRID_SIZE 
from sidd.operator import Operator, OperatorError, OperatorDataError
from sidd.operator.data import OperatorDataTypes


class GridWriter(Operator):
    """ class to create exposure grid according to GED spec """
    
    def __init__(self, options=None, name="Grid Writer"):
        """ constructor """
        super(GridWriter, self).__init__(options, name)
        self._tmp_dir = options['tmp_dir']
        self._x_off = DEFAULT_GRID_SIZE
        self._y_off = DEFAULT_GRID_SIZE 
        
        self._fields = {
            0 : QgsField(self._lon_field, QVariant.Double),
            1 : QgsField(self._lat_field, QVariant.Double),
        }

        
    # self documenting method override
    ###########################

    @property
    def input_types(self):
        return [
            OperatorDataTypes.NumericAttribute,
            OperatorDataTypes.NumericAttribute,
            OperatorDataTypes.NumericAttribute,
            OperatorDataTypes.NumericAttribute,
        ]
        
    @property    
    def input_names(self):
        return ["X min", "Y min", "X max", "Y max"]
    
    input_descriptions = input_names

    @property
    def output_types(self):
        return [OperatorDataTypes.Grid,
                OperatorDataTypes.Shapefile]
        
    @property    
    def output_names(self):
        return ["Grid with Zone Attribute",
                "Grid Shapefile"]
    
    output_descriptions = output_names

    # public method override
    ###########################

    @logAPICall
    def do_operation(self):
        """ perform footprint load operation """
        
        # input/output data checking already done during property set
        grid_layername = 'grid_%s' % get_unique_filename()
        output_file = self._tmp_dir + grid_layername + '.shp'
        
        [x_min, y_min, x_max, y_max] = [x.value for x in self._inputs]
        try:
            self._write_grid_shapefile(output_file, 
                                       x_min, y_min, x_max, y_max,
                                       self._x_off, self._y_off)
        except:
            remove_shapefile(output_file)
            raise OperatorError('error creating grid', self.__class__)

        
        grid_layer = load_shapefile(output_file, grid_layername)
        if not grid_layer:
            raise OperatorError('Error loading result grid file' % (output_file), self.__class__)              

        self.outputs[0].value = grid_layer
        self.outputs[1].value = output_file
        
    # protected method override
    ###########################

    def _verify_inputs(self, inputs):
        """ perform operator specific input validation """ 
        for i in range(len(self.input_names)):
            if type(inputs[i].value) != float and type(inputs[i].value) != int:
                raise OperatorDataError("input %d must contain valid numeric value" % (i+1))

    def _verify_outputs(self, outputs):
        """ perform operator specific input validation """
        pass
    
    # helper methods
    ###########################
    
    def _write_grid_shapefile(self, path, x_min, y_min, x_max, y_max, x_off, y_off):
        x_off = self._x_off        
        y_off = self._y_off        
        x_min = floor(x_min / x_off) * x_off
        x_max = ceil(x_max / x_off) * x_off
        y_min = floor(y_min / y_off) * y_off
        y_max = ceil(y_max / y_off) * y_off
        
        xtotal = int((x_max - x_min) / x_off)
        ytotal = int((y_max - y_min) / y_off)        
        
        logAPICall.log('x_min %f x_max %f y_min %f y_max %f x_off %f y_off %f xtotal %d, ytotal %d'
                       % (x_min, x_max, y_min, y_max, x_off, y_off, xtotal, ytotal),
                       logAPICall.DEBUG_L2)
        
        writer = QgsVectorFileWriter(path, "utf-8", self._fields, QGis.WKBPoint, self._crs, "ESRI Shapefile")
        f = QgsFeature()
        for x in range(xtotal):
            for y in range(ytotal):
                lon = x_min + (x * x_off) + (x_off/2.0)
                lat = y_min + (y * y_off) + (y_off/2.0)                
                f.setGeometry(QgsGeometry.fromPoint(QgsPoint(lon, lat)))
                f.addAttribute(0, QVariant(lon))
                f.addAttribute(1, QVariant(lat))
                writer.addFeature(f)
        del writer

class GridFromRegionWriter(GridWriter):
    """ class to create exposure grid according to GED spec """
    
    def __init__(self, options=None, name="Grid Writer"):
        """ constructor """
        super(GridFromRegionWriter, self).__init__(options, name)
        
    # self documenting method override
    ###########################

    @property
    def input_types(self):
        return [
            OperatorDataTypes.Zone
        ]
        
    @property    
    def input_names(self):
        return ["Zone boundary"]
    
    input_descriptions = input_names

    # public method override
    ###########################

    @logAPICall
    def do_operation(self):
        """ perform footprint load operation """
        
        # input/output data checking already done during property set         
        zone_layer = self.inputs[0].value        
        x_off = self._x_off
        y_off = self._y_off

        extent = zone_layer.extent()
        [x_min, y_min, x_max, y_max] = [extent.xMinimum(), extent.yMinimum(), extent.xMaximum(), extent.yMaximum()]

        # create grid based on extent of given region 
        tmp_grid1 = 'grid_' + get_unique_filename()
        tmp_grid1_file = self._tmp_dir + tmp_grid1 + '.shp'

        try:
            self._write_grid_shapefile(tmp_grid1_file,
                                       x_min, y_min, x_max, y_max,
                                       x_off, y_off)
        except:
            remove_shapefile(tmp_grid1_file)
            raise OperatorError('error creating temporary grid', self.__class__)        
        
        tmp_grid1_layer = load_shapefile(tmp_grid1_file, tmp_grid1)
        
        # temporary grid for joined shape with all grid points not within region removed 
        tmp_grid2 = 'grid_' + get_unique_filename()
        tmp_grid2_file = self._tmp_dir + tmp_grid2 + '.shp'
        tmp_grid2_layer = None
        try:
            analyzer = QgsOverlayAnalyzer()        
            analyzer.intersection(tmp_grid1_layer, zone_layer, tmp_grid2_file)
            tmp_grid2_layer = load_shapefile(tmp_grid2_file, tmp_grid2)
        except:
            raise OperatorError('error creating grid', self.__class__)

        # create result layer
        grid_layername = 'grid_%s' % get_unique_filename()
        grid_file = self._tmp_dir + grid_layername + '.shp'
        try:
            writer = QgsVectorFileWriter(grid_file, "utf-8", self._fields,
                                         QGis.WKBPoint, self._crs, "ESRI Shapefile")
            f = QgsFeature()
            lon_idx = layer_field_index(tmp_grid2_layer, self._lon_field)
            lat_idx = layer_field_index(tmp_grid2_layer, self._lat_field)        
            for _f in layer_features(tmp_grid2_layer):
                lon = _f.attributeMap()[lon_idx].toDouble()[0]
                lat = _f.attributeMap()[lat_idx].toDouble()[0]
                
                f.setGeometry(QgsGeometry.fromPoint(QgsPoint(lon, lat)))
                f.addAttribute(0, QVariant(lon))
                f.addAttribute(1, QVariant(lat))
                writer.addFeature(f)                
            del writer
        except  Exception as err:
            logAPICall.log(str(err), logAPICall.ERROR)
            raise OperatorError('error writing out grid', self.__class__)

        grid_layer = load_shapefile(grid_file, grid_layername)
        if not grid_layer:
            raise OperatorError('Error loading result grid file' % (grid_file), self.__class__)        
        
        # clean up
        del analyzer, tmp_grid1_layer, tmp_grid2_layer
        remove_shapefile(tmp_grid1_file)
        remove_shapefile(tmp_grid2_file)
        
        self.outputs[0].value = grid_layer
        self.outputs[1].value = grid_file

    # protected method override
    ###########################
    def _verify_inputs(self, inputs):
        """ perform operator specific input validation """
        pass
