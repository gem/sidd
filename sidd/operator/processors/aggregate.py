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
# Version: $Id: aggregate.py 18 2012-10-24 20:21:41Z zh $

"""
module contains class for creating mapping scheme from survey data
"""

import bsddb

from PyQt4.QtCore import *
from qgis.core import *

from utils.shapefile import *
from utils.system import get_unique_filename

from sidd.operator import *
from sidd.constants import *

class FootprintAggregator(Operator):
    def __init__(self, options=None, name='Footprint Aggregator'):
        super(FootprintAggregator, self).__init__(options, name)
        
        self._tmp_dir = options['tmp_dir']

    # self documenting method override
    ###########################
    
    @property
    def input_types(self):
        return [OperatorDataTypes.Footprint,
                OperatorDataTypes.StringAttribute,]
        
    @property    
    def input_names(self):
        return ["Footprint centroid layer", "Zone Field"]
    
    input_descriptions = input_names

    @property
    def output_types(self):
        return [OperatorDataTypes.Grid,
                OperatorDataTypes.Shapefile]
        
    @property    
    def output_names(self):
        return ["Grid with Zone and Building Counts",
                "Grid Shapefile"]
    
    output_descriptions = output_names

    # public method override
    ###########################
    
    @logAPICall
    def do_operation(self):
        """ perform create mapping scheme operation """
        
        # input/output verification already performed during set input/ouput
        fp_layer = self.inputs[0].value
        zone_field = self.inputs[1].value

        # aggregate footprint into grids
        logAPICall.log('aggregate statistic for grid ...', logAPICall.DEBUG)
        total_features = fp_layer.dataProvider().featureCount()
        if total_features > MAX_FEATURES_IN_MEMORY:
            # use bsddb to store temporary lat/lon
            tmp_db_file = '%sdb_%s.db' % (self._tmp_dir, get_unique_filename())
            db = bsddb.btopen(tmp_db_file, 'c')
            use_db = True
        else:
            db = {}
            use_db = False

        zone_idx = layer_field_index(fp_layer, zone_field)
        for f in layer_features(fp_layer):
            geom = f.geometry()
            zone_str = str(f.attributeMap()[zone_idx].toString())
            centroid  = geom.centroid().asPoint()                        
            x = round(centroid.x() / DEFAULT_GRID_SIZE)
            y = round(centroid.y() / DEFAULT_GRID_SIZE)            
            key = '%s %d %d' % (zone_str, x,y)
            if db.has_key(key):
                db[key] = str(int(db[key]) + 1)
            else:
                db[key] = '1'
        
        # output grid
        logAPICall.log('create grid ...', logAPICall.DEBUG)
        fields = {
            0 : QgsField(self._lon_field, QVariant.Double),
            1 : QgsField(self._lat_field, QVariant.Double),
            2 : QgsField(CNT_FIELD_NAME, QVariant.Double),
            3 : QgsField(zone_field, QVariant.String),
        }
        grid_layername = 'grid_%s' % get_unique_filename()
        grid_file = '%s%s.shp' % (self._tmp_dir, grid_layername)
        try:
            writer = QgsVectorFileWriter(grid_file, "utf-8", fields, QGis.WKBPoint , self._crs, "ESRI Shapefile")
            f = QgsFeature()
            for key, val in db.iteritems():
                (zone_str, x, y) = key.split(' ')
                point = QgsPoint(int(x)*DEFAULT_GRID_SIZE, int(y)*DEFAULT_GRID_SIZE)
                
                f.setGeometry(QgsGeometry.fromPoint(point))
                f.addAttribute(0, QVariant(point.x()))
                f.addAttribute(1, QVariant(point.y()))
                f.addAttribute(2, QVariant(val))
                f.addAttribute(3, QVariant(zone_str))
                writer.addFeature(f)
            del writer
        except Exception as err:
            remove_shapefile(grid_file)
            raise OperatorError("error creating joined grid: " % err, self.__class__)
        
        grid_layer = load_shapefile(grid_file, grid_layername)
        if not grid_layer:
            raise OperatorError('Error loading created grid file' % (grid_file), self.__class__)
                
        # clean up                
        if use_db:
            db.close()
            os.remove(tmp_db_file)
            
        # done
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
