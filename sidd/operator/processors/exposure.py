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
# Version: $Id: exposure.py 21 2012-10-26 01:48:25Z zh $

"""
module contains class for applying mapping scheme
"""
import bsddb 

from PyQt4.QtCore import QVariant
from qgis.core import QGis, QgsVectorFileWriter, QgsFeature, QgsField, QgsGeometry, QgsPoint

from utils.shapefile import load_shapefile, layer_features, layer_field_index, remove_shapefile
from utils.system import get_unique_filename
from utils.grid import latlon_to_grid

from sidd.constants import logAPICall, \
                           ExtrapolateOptions, \
                           GID_FIELD_NAME, LON_FIELD_NAME, LAT_FIELD_NAME, CNT_FIELD_NAME, TAX_FIELD_NAME, ZONE_FIELD_NAME, \
                           DEFAULT_GRID_SIZE, MAX_FEATURES_IN_MEMORY
from sidd.operator import Operator, OperatorError, OperatorDataError
from sidd.operator.data import OperatorDataTypes

class GridMSApplier(Operator):    
    def __init__(self, options=None, name='Grid Mapping Scheme Applier'):
        super(GridMSApplier, self).__init__(options, name)
        self._tmp_dir = options['tmp_dir']
        if options.has_key('proc.extrapolation'):
            self._extrapolationOption = options['proc.extrapolation']
        else:
            self._extrapolationOption = ExtrapolateOptions.RandomWalk
            
        self._fields = {0: QgsField(GID_FIELD_NAME, QVariant.Int),
                        1: QgsField(LON_FIELD_NAME, QVariant.Double),
                        2: QgsField(LAT_FIELD_NAME, QVariant.Double),
                        3: QgsField(TAX_FIELD_NAME, QVariant.String),
                        4: QgsField(ZONE_FIELD_NAME, QVariant.String),
                        5: QgsField(CNT_FIELD_NAME, QVariant.Int)}        
        if self._extrapolationOption != ExtrapolateOptions.RandomWalk:
            self._fields[5]=QgsField(CNT_FIELD_NAME, QVariant.Double)
        
    # self documenting method override
    ###########################
    
    @property
    def input_types(self):
        return [OperatorDataTypes.Grid,
                OperatorDataTypes.StringAttribute,
                OperatorDataTypes.StringAttribute,
                OperatorDataTypes.MappingScheme]
        
    @property
    def input_names(self):
        return ["Grid Data Layer",
                "Zone field",
                "Building Count field"
                "Mapping Scheme"]
    
    input_descriptions = input_names

    @property
    def output_types(self):
        return [OperatorDataTypes.Exposure,
                OperatorDataTypes.Shapefile,]
        
    @property    
    def output_names(self):
        return ["Regional Exposure",
                "Regional Exposure Shapefile",]

    output_descriptions = output_names
    
    # public method override
    ###########################

    @logAPICall
    def do_operation(self):
        """ perform apply mapping scheme operation """
        
        # input/output data checking already done during property set
        src_layer = self.inputs[0].value
        zone_field = self.inputs[1].value
        count_field = self.inputs[2].value
        ms = self.inputs[3].value
        
        # make sure input is correct
        # NOTE: these checks cannot be performed at set input time
        #       because the data layer maybe is not loaded yet
        self._test_layer_loaded(src_layer)
        self._test_layer_field_exists(src_layer, zone_field)
        self._test_layer_field_exists(src_layer, count_field)
        
        # loop through all zones and assign mapping scheme
        # outputs
        exposure_layername = 'exp_%s' % get_unique_filename()
        exposure_file = '%sexp_%s.shp' % (self._tmp_dir, exposure_layername)

        # loop through all input features
        provider = src_layer.dataProvider()
        if provider is None:
            raise OperatorError("input layer not correctly loaded", self.__class__)
        zone_idx = layer_field_index(src_layer, zone_field)
        if zone_idx == -1:
            raise OperatorError("field %s not found in input layer" % zone_field, self.__class__)
        count_idx = layer_field_index(src_layer, count_field)
        if count_idx == -1:
            raise OperatorError("field %s not found in input layer" % count_field, self.__class__)
         
        provider.select(provider.attributeIndexes(), provider.extent())
        provider.rewind()

        default_stats = ms.get_assignment(ms.get_zones()[0])
        try:
            writer = QgsVectorFileWriter(exposure_file, "utf-8", self._fields, provider.geometryType(), self._crs, "ESRI Shapefile")
            out_feature = QgsFeature()
            
            gid = 0
            for in_feature in layer_features(src_layer):
                geom = in_feature.geometry()
                centroid = geom.centroid().asPoint ()
                zone_str = str(in_feature.attributeMap()[zone_idx].toString())
                count = in_feature.attributeMap()[count_idx].toDouble()[0]
                
                count = int(count+0.5)
                stats = ms.get_assignment_by_name(zone_str)
                
                # use default stats if missing
                if stats is None:
                    stats = default_stats
                    
                gid += 1
                for _l, _c in stats.get_samples(count, self._extrapolationOption).iteritems():
                    # write out if there are structures assigned
                    if _c > 0:
                        out_feature.setGeometry(geom)
                        #out_feature.addAttribute(0, QVariant(gid))
                        out_feature.addAttribute(0, QVariant(latlon_to_grid(centroid.y(), centroid.x())))
                        out_feature.addAttribute(1, QVariant(centroid.x()))
                        out_feature.addAttribute(2, QVariant(centroid.y()))
                        out_feature.addAttribute(3, QVariant(_l))
                        out_feature.addAttribute(4, QVariant(zone_str))
                        out_feature.addAttribute(5, QVariant(_c))
                        writer.addFeature(out_feature)
            del writer, out_feature
        except Exception as err:
            remove_shapefile(exposure_file)
            raise OperatorError("error creating exposure file: %s" % err, self.__class__)
            
        del src_layer
        
        # load shapefile as layer        
        exposure_layer = load_shapefile(exposure_file, exposure_layername)
        if not exposure_layer:            
            raise OperatorError('Error loading exposure file' % (exposure_file), self.__class__)
        
        # store data in output
        self.outputs[0].value = exposure_layer
        self.outputs[1].value = exposure_file
        
    # protected method override
    ###########################

    def _verify_inputs(self, inputs):
        """ perform operator specific input validation """        
        pass

    def _verify_outputs(self, outputs):
        """ perform operator specific output validation """
        pass

class ZoneMSApplier(GridMSApplier):
    def __init__(self, options=None, name='Zone Mapping Scheme Applier'):
        super(ZoneMSApplier, self).__init__(options, name)    
        
    # self documenting method override
    ###########################
    
    @property
    def input_types(self):
        return [OperatorDataTypes.Zone,
                OperatorDataTypes.StringAttribute,
                OperatorDataTypes.StringAttribute,
                OperatorDataTypes.MappingScheme]
        
    @property
    def input_names(self):
        return ["Zone data Layer",
                "Zone field",
                "Building Count field"
                "Mapping Scheme"]
    
class SurveyAggregator(GridMSApplier):
    def __init__(self, options=None, name='Complete Survey Aggregator'):
        super(SurveyAggregator, self).__init__(options, name)
    
    # self documenting method override
    ###########################
    
    @property
    def input_types(self):
        return [OperatorDataTypes.Survey,]
        
    @property    
    def input_names(self):
        return ["Complete Survey data"]
    
    input_descriptions = input_names

    # public method override
    ###########################
    
    @logAPICall
    def do_operation(self):
        """ perform create mapping scheme operation """
        
        # input/output verification already performed during set input/ouput
        svy_layer = self.inputs[0].value

        # make sure input is correct
        # NOTE: these checks cannot be performed at set input time
        #       because the data layer maybe is not loaded yet
        self._test_layer_loaded(svy_layer)
        
        total_features = svy_layer.dataProvider().featureCount()
        if total_features > MAX_FEATURES_IN_MEMORY:
            # use bsddb to store temporary lat/lon
            tmp_db_file = '%sdb_%s.db' % (self._tmp_dir, get_unique_filename())
            db = bsddb.btopen(tmp_db_file, 'c')
        else:
            db = {}

        tax_idx = layer_field_index(svy_layer, TAX_FIELD_NAME)
        for f in layer_features(svy_layer):
            geom = f.geometry()
            tax_str = str(f.attributeMap()[tax_idx].toString())
            centroid  = geom.centroid().asPoint()                        
            x = round(centroid.x() / DEFAULT_GRID_SIZE)
            y = round(centroid.y() / DEFAULT_GRID_SIZE)            
            key = '%s %d %d' % (tax_str, x,y)
            if db.has_key(key):
                db[key] = str(int(db[key]) + 1)
            else:
                db[key] = '1'

        # loop through all zones and assign mapping scheme
        # outputs
        exposure_layername = 'exp_%s' % get_unique_filename()
        exposure_file = '%sexp_%s.shp' % (self._tmp_dir, exposure_layername)

        try:
            writer = QgsVectorFileWriter(exposure_file, "utf-8", self._fields, QGis.WKBPoint, self._crs, "ESRI Shapefile")
            f = QgsFeature()
            
            gid = 0
            for key, val in db.iteritems():
                (tax_str, x, y) = key.split(' ')
                point = QgsPoint(int(x)*DEFAULT_GRID_SIZE, int(y)*DEFAULT_GRID_SIZE)
                f.setGeometry(QgsGeometry.fromPoint(point))
                #f.addAttribute(0, QVariant(gid))
                f.addAttribute(0, QVariant(latlon_to_grid(point.y(), point.x())))
                f.addAttribute(1, QVariant(point.x()))
                f.addAttribute(2, QVariant(point.y()))
                f.addAttribute(3, QVariant(tax_str))
                f.addAttribute(4, QVariant(''))
                f.addAttribute(5, QVariant(val))
                writer.addFeature(f)
                gid += 1
            del writer, f
        except Exception as err:
            remove_shapefile(exposure_file)
            raise OperatorError("error creating exposure file: %s" % err, self.__class__)
        
        # load shapefile as layer        
        exposure_layer = load_shapefile(exposure_file, exposure_layername)
        if not exposure_layer:            
            raise OperatorError('Error loading exposure file %s' % (exposure_file), self.__class__)
        
        # store data in output
        self.outputs[0].value = exposure_layer
        self.outputs[1].value = exposure_file
