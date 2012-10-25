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
# Version: $Id: join.py 18 2012-10-24 20:21:41Z zh $

"""
module contains class for creating mapping scheme from survey data
"""

import os

from PyQt4.QtCore import *
from qgis.core import *
from qgis.analysis import QgsOverlayAnalyzer 

from utils.shapefile import *
from utils.system import get_unique_filename

from sidd.constants import *
from sidd.operator import *


class ZoneGridMerger(Operator):
    """
    """

    # construction / destructor
    ###########################
    
    def __init__(self, options=None, name='Zone & Grid Merger'):
        super(ZoneGridMerger, self).__init__(options, name)        
        self._tmp_dir = options['tmp_dir']
        
    # self documenting method override
    ###########################
    
    @property
    def input_types(self):
        return [OperatorDataTypes.Zone,
                OperatorDataTypes.StringAttribute,
                OperatorDataTypes.StringAttribute,
                OperatorDataTypes.Grid]
        
    @property    
    def input_names(self):
        return ["Zone Layer",
                "Zone Field",
                "Building Count Field",
                "Grid Layer"]
    
    input_descriptions = input_names

    @property
    def output_types(self):
        return [OperatorDataTypes.Grid,
                OperatorDataTypes.Shapefile]
        
    @property    
    def output_names(self):
        return ["Grid with Zone and Count Attributes",
                "Grid Shapefile"]

    output_descriptions = output_names

    # public method override
    ###########################
    
    @logAPICall
    def do_operation(self):
        """ perform create mapping scheme operation """
        
        # input/output verification already performed during set input/ouput
        zone_layer = self.inputs[0].value
        zone_field = self.inputs[1].value        
        count_field = self.inputs[2].value
        grid_layer = self.inputs[3].value        
        
        # merge to create stats
        tmp_join = 'joined_%s' % get_unique_filename()
        tmp_join_file = '%s%s.shp' % (self._tmp_dir, tmp_join)        
        analyzer = QgsOverlayAnalyzer()        
        try:
            analyzer.intersection(grid_layer, zone_layer, tmp_join_file)
            tmp_join_layer = load_shapefile_verify(tmp_join_file, tmp_join,[zone_field, count_field])
        except AssertionError as err:
            raise OperatorError(str(err), self.__class__)
        except Exception as err:
            raise OperatorError(str(err), self.__class__)
        
        stats = layer_multifields_stats(tmp_join_layer, [zone_field, count_field])
        if stats == False:
            raise OperatorError("error creating statistic based on input files",
                                self.__class__)
        total_features = tmp_join_layer.featureCount()
        
        zone_idx = layer_field_index(tmp_join_layer, zone_field)
        count_idx = layer_field_index(tmp_join_layer, count_field)
        lon_idx = layer_field_index(tmp_join_layer, self._lon_field)
        lat_idx = layer_field_index(tmp_join_layer, self._lat_field)

        fields = {
            0 : QgsField(self._lon_field, QVariant.Double),
            1 : QgsField(self._lat_field, QVariant.Double),
            2 : QgsField(zone_field, QVariant.String),
            3 : QgsField(count_field, QVariant.Double)
        }
        grid_layername = 'grid_%s' % (get_unique_filename())
        grid_file = '%s%s.shp' % (self._tmp_dir, grid_layername)
        try:
            writer = QgsVectorFileWriter(grid_file, "utf-8", fields, QGis.WKBPoint, self._crs, "ESRI Shapefile")
            f = QgsFeature()
            for _f in layer_features(tmp_join_layer):
                lon = _f.attributeMap()[lon_idx].toDouble()[0]
                lat = _f.attributeMap()[lat_idx].toDouble()[0]
                zone_str = str(_f.attributeMap()[zone_idx].toString()).upper()
                count_val = _f.attributeMap()[count_idx].toDouble()[0]
                key = '%s_%d' % (zone_str, count_val)
                val = stats[key]
                
                f.setGeometry(QgsGeometry.fromPoint(QgsPoint(lon, lat)))
                f.addAttribute(0, QVariant(lon))
                f.addAttribute(1, QVariant(lat))
                f.addAttribute(2, QVariant(zone_str))            
                f.addAttribute(3, QVariant(count_val / total_features))
                writer.addFeature(f)
            
            del writer
        except Exception as err:
            remove_shapefile(grid_file)
            raise OperatorError("error creating joined grid: " % err, self.__class__)

        grid_layer = load_shapefile(grid_file, grid_layername)
        if not grid_layer:
            raise OperatorError('Error loading footprint centroid file' % (grid_file), self.__class__)
        
        # clean up
        del tmp_join_layer
        remove_shapefile(tmp_join_file)
        
        self.outputs[0].value = grid_layer
        self.outputs[1].value = grid_file

    # protected method override
    ###########################

    def _verify_inputs(self, inputs):
        """ perform operator specific input validation """
        pass
        
    def _verify_outputs(self, outputs):
        """ perform operator specific output validation """
        pass

class ZoneFootprintMerger(Operator):
    def __init__(self, options=None, name='Zone & Footprint Merger'):
        super(ZoneFootprintMerger, self).__init__(options, name)
        self._tmp_dir = options['tmp_dir']
        
    # self documenting method override
    ###########################
    
    @property
    def input_types(self):
        return [OperatorDataTypes.Zone,
                OperatorDataTypes.StringAttribute,
                OperatorDataTypes.Footprint]
        
    @property    
    def input_names(self):
        return ["Homogenous Zone", "Zone Field", "Building Footprint"]
    
    input_descriptions = input_names

    @property
    def output_types(self):
        return [OperatorDataTypes.Footprint,
                OperatorDataTypes.Shapefile]
        
    @property    
    def output_names(self):
        return ["Footprint with Zone Attribute",
                "Footprint Shapefile"]

    output_descriptions = output_names

    output_descriptions = output_names

    # public method override
    ###########################
    
    @logAPICall
    def do_operation(self):
        """ perform create mapping scheme operation """
        
        # input/output verification already performed during set input/ouput
        zone_layer = self.inputs[0].value
        zone_field = self.inputs[1].value                
        fp_layer = self.inputs[2].value
        
        # merge with zone to get assignment
        tmp_join = 'joined_%s' % get_unique_filename()
        tmp_join_file = '%s%s.shp' % (self._tmp_dir, tmp_join)        
        analyzer = QgsOverlayAnalyzer()        
        try:
            analyzer.intersection(fp_layer, zone_layer, tmp_join_file)
            tmp_join_layer = load_shapefile_verify(tmp_join_file, tmp_join,[zone_field])
        except AssertionError as err:
            raise OperatorError(str(err), self.__class__)
        except Exception as err:
            raise OperatorError(str(err), self.__class__)
        
        fields = {
            0 : QgsField(self._lon_field, QVariant.Double),
            1 : QgsField(self._lat_field, QVariant.Double),
            2 : QgsField(zone_field, QVariant.String),
        }
        zone_idx = layer_field_index(tmp_join_layer, zone_field)
        fp_layername = 'fpc_%s' % get_unique_filename()
        fp_file = '%s%s.shp' % (self._tmp_dir, fp_layername)
        try:
            writer = QgsVectorFileWriter(fp_file, "utf-8", fields, QGis.WKBPoint, self._crs, "ESRI Shapefile")
            f = QgsFeature()
            for _f in layer_features(tmp_join_layer):                
                centroid = _f.geometry().centroid().asPoint()
                lon = centroid.x()
                lat = centroid.y()
                zone_str = str(_f.attributeMap()[zone_idx].toString()).upper()

                f.setGeometry(QgsGeometry.fromPoint(QgsPoint(lon, lat)))
                f.addAttribute(0, QVariant(lon))
                f.addAttribute(1, QVariant(lat))
                f.addAttribute(2, QVariant(zone_str))
                writer.addFeature(f)
            
            del writer
        except Exception as err:
            logAPICall.log(err, logAPICall.ERROR)
            remove_shapefile(fp_file)
            raise OperatorError("error creating joined grid: %s" % err, self.__class__)
        
        # load shapefile as layer
        fp_layer = load_shapefile(fp_file, fp_layername)
        if not fp_layer:
            raise OperatorError('Error loading footprint centroid file' % (fp_file), self.__class__)        
                
        # clean up
        del tmp_join_layer        
        remove_shapefile(tmp_join_file)
        
        self.outputs[0].value = fp_layer
        self.outputs[1].value = fp_file

    # protected method override
    ###########################

    def _verify_inputs(self, inputs):
        """ perform operator specific input validation """
        pass
        
    def _verify_outputs(self, outputs):
        """ perform operator specific output validation """
        pass    