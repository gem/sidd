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
# Version: $Id: zones.py 18 2012-10-24 20:21:41Z zh $

"""
module constains class for loading zone shapefiles
"""

from os.path import exists

from PyQt4.QtCore import *
from qgis.core import *

from utils.shapefile import *
from utils.system import get_unique_filename

from sidd.constants import logAPICall
from sidd.operator import *

class ZoneLoader(Operator):
    """ load zone shapefile """
    
    def __init__(self, options=None, name='Homogenous Zones'):
        """ constructor """
        super(ZoneLoader, self).__init__(options, name)
        self._tmp_dir = options['tmp_dir']
    
    # self documenting method override
    ###########################
    
    @property
    def input_types(self):
        return [OperatorDataTypes.Shapefile,
                OperatorDataTypes.StringAttribute]
        
    @property    
    def input_names(self):
        return ["Zones Input Shapefile",
                "Zone Field"]
    
    input_descriptions = input_names

    @property
    def output_types(self):
        return [OperatorDataTypes.Zone,
                OperatorDataTypes.Shapefile]
        
    @property    
    def output_names(self):
        return ["Homogenous Zones Layer",
                "Homogenous Zones Shapefile",
                "Zone Statistic"]

    output_descriptions = output_names

    # public method override
    ###########################

    @logAPICall
    def do_operation(self):
        """ perform zone loading operation """
        # input/output data checking already done during property set
        # load data
        zone_file = self.inputs[0].value
        zone_field = self.inputs[1].value
        
        zone_layername = 'zone_%s' % get_unique_filename()
        try:
            tmp_zone_layer = load_shapefile_verify(zone_file, zone_layername,
                                                   [zone_field])
        except AssertionError as err:
            raise OperatorError(str(err), self.__class__)

        logAPICall.log('tmp_zone_layer.crs().epsg() %s ' % tmp_zone_layer.crs().epsg(), logAPICall.DEBUG)
        if tmp_zone_layer.crs().epsg() != self._crs.epsg():
            transform = QgsCoordinateTransform(tmp_zone_layer.crs(), self._crs)
            transform_required = True
        else:
            transform_required = False
        
        # output grid
        output_file = '%szone_%s.shp' % (self._tmp_dir, get_unique_filename())
        logAPICall.log('create outputfile %s ... ' % output_file, logAPICall.DEBUG)
        try:
            findices = self._getFieldIndices(tmp_zone_layer)
            fields = self._getFields()
            writer = QgsVectorFileWriter(output_file, "utf-8", fields, QGis.WKBPolygon, self._crs, "ESRI Shapefile")
            f = QgsFeature()
            for _f in layer_features(tmp_zone_layer):
                geom = _f.geometry()
                if transform_required:
                    geom.transform(transform)
                
                # write to file
                f.setGeometry(geom)
                for fkey, fidx in map(None, fields.keys(), findices):
                    f.addAttribute(fkey, _f.attributeMap()[fidx])
                writer.addFeature(f)
                
            del writer
        except Exception as err:
            remove_shapefile(output_file)
            raise OperatorError("error creating zone: %s" % err, self.__class__)

        zone_layer = load_shapefile(output_file, zone_layername)
        if not zone_layer:
            raise OperatorError('Error loading footprint centroid file' % (output_file), self.__class__)        
        
        # clean up
        del tmp_zone_layer

        # store data in output
        self.outputs[0].value = zone_layer
        self.outputs[1].value = output_file

    # protected method override
    ###########################

    def _verify_inputs(self, inputs):
        """ perform operator specific input validation """
        if not exists(inputs[0].value):
            raise OperatorDataError("input file %s does not exist" % (inputs[0].value))
        if '' == inputs[1].value:
            raise OperatorDataError("zone field name cannot be empty")        
    
    def _verify_outputs(self, outputs):
        """ perform operator specific output validation """
        pass
    
    def _getFields(self):
        return {
            0 : QgsField(self.inputs[1].value, QVariant.String),
        }
    
    def _getFieldNames(self):
        return [
            self.inputs[1].value, # zone_field
        ]
    
    def _getFieldIndices(self, layer):        
        return [
            layer_field_index(layer, self.inputs[1].value), # zone_field
        ]    
    
class ZoneCountLoader(ZoneLoader):
    """ load zone shapefile with building counts """
    
    def __init__(self, options=None, name='Homogenous Zones with Building Counts'):
        """ constructor """
        super(ZoneCountLoader, self).__init__(options, name)

    # self documenting method override
    ###########################
    
    @property
    def input_types(self):
        return [OperatorDataTypes.Shapefile,
                OperatorDataTypes.StringAttribute,
                OperatorDataTypes.StringAttribute]
        
    @property    
    def input_names(self):
        return ["Zones Input Shapefile",
                "Zone Field",
                "Building Count Field"]
    
    input_descriptions = input_names
       
    # protected method override
    ###########################
    def _verify_inputs(self, inputs):
        """ perform operator specific output validation """
        super(ZoneCountLoader, self)._verify_inputs(inputs)
        if '' == inputs[2].value:
            raise OperatorDataError("building count field name cannot be empty")

    def _getFieldNames(self):
        return [
            self.inputs[1].value, # zone_field
            self.inputs[2].value, # count_field
        ]
    
    def _getFields(self):
        return {
            0 : QgsField(self.inputs[1].value, QVariant.String),
            1 : QgsField(self.inputs[2].value, QVariant.String),
        }
    
    def _getFieldIndices(self, layer):        
        return [
            layer_field_index(layer, self.inputs[1].value), # zone_field
            layer_field_index(layer, self.inputs[2].value), # count_field
        ]    