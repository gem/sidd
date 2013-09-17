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
module constains class for loading zone shapefiles
"""
from os.path import exists

from PyQt4.QtCore import QVariant
from qgis.core import QGis, QgsCoordinateTransform, QgsVectorFileWriter, QgsFeature, QgsField

from utils.shapefile import load_shapefile_verify, remove_shapefile, layer_features, layer_field_index, load_shapefile
from utils.system import get_unique_filename

from sidd.constants import logAPICall, GID_FIELD_NAME

from sidd.operator import Operator,OperatorError, OperatorDataError
from sidd.operator.data import OperatorDataTypes

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
                "Homogenous Zones Shapefile"]

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
            # get the indices to use
            findices = self._getFieldIndices(tmp_zone_layer)
            # get the output fields            
            fields = self._getFields(tmp_zone_layer)
            fields2 = fields.copy()
            fields2[0] = QgsField(GID_FIELD_NAME, QVariant.Int) # add GID field
            writer = QgsVectorFileWriter(output_file, "utf-8", fields2, QGis.WKBPolygon, self._crs, "ESRI Shapefile")
            
            # loop and create output file
            f = QgsFeature()
            gid=0
            for _f in layer_features(tmp_zone_layer):
                geom = _f.geometry()
                if transform_required:
                    geom.transform(transform)
                
                # write to file
                f.setGeometry(geom)
                gid+=1
                f.addAttribute(0, QVariant(gid))
                # copy data from all fields
                for fkey, fidx in map(None, fields.keys(), findices):
                    if fidx >= 0:    # area field could be missing 
                        f.addAttribute(fkey, _f.attributeMap()[fidx])
                writer.addFeature(f)
            
            del writer, f
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
    
    def _getFields(self, layer):
        return {
            1 : QgsField(self.inputs[1].value, QVariant.String),
        }
    
    def _getFieldNames(self, layer):
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
                OperatorDataTypes.StringAttribute,
                OperatorDataTypes.StringAttribute]
        
    @property    
    def input_names(self):
        return ["Zones Input Shapefile",
                "Zone Field",
                "Building Count Field",
                "Building Area Field"]
    
    input_descriptions = input_names
       
    # protected method override
    ###########################
    def _verify_inputs(self, inputs):
        """ perform operator specific output validation """
        super(ZoneCountLoader, self)._verify_inputs(inputs)
        if '' == inputs[2].value:
            raise OperatorDataError("building count field name cannot be empty")

    def _getFieldNames(self, layer):
        if layer_field_index(layer, self.inputs[3].value) > 0:
            return [
                self.inputs[1].value, # zone_field
                self.inputs[2].value, # count_field
                self.inputs[3].value, # area_field
            ]
        else:
            return [
                self.inputs[1].value, # zone_field
                self.inputs[2].value, # count_field
            ]
    
    def _getFields(self, layer):
        if layer_field_index(layer, self.inputs[3].value) > 0:
            return {
                1 : QgsField(self.inputs[1].value, QVariant.String),
                2 : QgsField(self.inputs[2].value, QVariant.Double),
                3 : QgsField(self.inputs[3].value, QVariant.Double),
            }
        else:
            return {
                1 : QgsField(self.inputs[1].value, QVariant.String),
                2 : QgsField(self.inputs[2].value, QVariant.Double),
            }            
    
    def _getFieldIndices(self, layer):
        if layer_field_index(layer, self.inputs[3].value) > 0:
            return [
                layer_field_index(layer, self.inputs[1].value), # zone_field
                layer_field_index(layer, self.inputs[2].value), # count_field            
                layer_field_index(layer, self.inputs[3].value), # area_field
            ]
        else:
            return [
                layer_field_index(layer, self.inputs[1].value), # zone_field
                layer_field_index(layer, self.inputs[2].value), # count_field            
            ]
            