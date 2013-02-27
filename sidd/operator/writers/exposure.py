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
# Version: $Id: exposure.py 18 2012-10-24 20:21:41Z zh $

"""
module to support exposure export 
"""
import bsddb
import os
import csv

from PyQt4.QtCore import QVariant
from qgis.core import QgsVectorFileWriter, QgsFeature, QgsField

from utils.shapefile import copy_shapefile, shapefile_to_kml, load_shapefile, layer_features, layer_field_index
from utils.system import get_unique_filename

from sidd.constants import logAPICall, GID_FIELD_NAME, MAX_FEATURES_IN_MEMORY
from sidd.operator import OperatorError
from sidd.operator.data import OperatorDataTypes

from writer import NullWriter

class ExposureSHPWriter(NullWriter):
    def __init__(self, options=None, name="Grid Writer"):
        """ constructor """
        super(ExposureSHPWriter, self).__init__(options, name)
        self._tmp_dir = options['tmp_dir']

    # self documenting method override
    ###########################

    @property
    def input_types(self):
        return [OperatorDataTypes.Shapefile,
                OperatorDataTypes.File,]
        
    @property    
    def input_names(self):
        return ["Exposure shapefile",
                "Output path",]
    
    input_descriptions = input_names

    @logAPICall
    def do_operation(self):
        """ perform export operation """        
        # input/output data checking already done during property set
        input_file = self.inputs[0].value
        output_folder = self.inputs[1].value
        
        try:
            exp_layer = load_shapefile(input_file, 'exposure_%s' % get_unique_filename())
            
            # store id of distinct features            
            total_features = exp_layer.dataProvider().featureCount()
            if total_features > MAX_FEATURES_IN_MEMORY:
                # use bsddb to store id in case number of features is too large
                tmp_db_file = '%sdb_%s.db' % (self._tmp_dir, get_unique_filename())
                db = bsddb.btopen(tmp_db_file, 'c')
                use_db = True
            else:
                # in memory dictionary, should be much faster, but could fail
                # if memory is limited
                db = {}
                use_db = False
                        
            # get field index for GID
            gid_idx = layer_field_index(exp_layer, GID_FIELD_NAME)
            fields = {
                0: QgsField(GID_FIELD_NAME, QVariant.Int),
            }            
            writer = QgsVectorFileWriter('%s/exposure.shp' % output_folder, "utf-8", fields, 
                                         exp_layer.dataProvider().geometryType(), 
                                         exp_layer.crs(), "ESRI Shapefile")
            out_feature = QgsFeature()
            for feature in layer_features(exp_layer):
                gid = feature.attributeMap()[gid_idx].toInt()[0]
                
                # only write out once 
                if not db.has_key(gid):
                    db[gid]=1
                    out_feature.addAttribute(0, gid)
                    out_feature.setGeometry(feature.geometry())
                    writer.addFeature(out_feature)
                    
            # clean up
            del writer                
            if use_db:
                db.close()
                os.remove(tmp_db_file)
                
        except Exception as err:
            raise OperatorError("error creating shapefile: %s" % err, self.__class__)
        # copy associated attribute file
        copy_shapefile(input_file, '%s/exposure_attribute.dbf'%output_folder, extensions=['.dbf'])

class ExposureCSVWriter(ExposureSHPWriter):
    def __init__(self, options=None, name="Grid Writer"):
        """ constructor """
        super(ExposureCSVWriter, self).__init__(options, name)

    def do_operation(self):
        """ perform export operation """        
        # input/output data checking already done during property set
        input_file = self.inputs[0].value
        output_folder = self.inputs[1].value
                
        try:
            exp_layer = load_shapefile(input_file, 'exposure_%s' % get_unique_filename())
            # get field headers/types
            fields = exp_layer.dataProvider().fields()
            csvfile = open('%s/exposure.csv' % output_folder, 'wb')
            csvwriter = csv.writer(csvfile, delimiter=',',
                                   quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
            csvwriter.writerow([f.name() for f in fields.values()])
            for feature in layer_features(exp_layer):
                row = []
                for fidx, value in feature.attributeMap().iteritems():
                    # retrieve data according to field type
                    if fields[fidx].type() == QVariant.Int:
                        row.append(str(value.toInt()[0]))
                    elif fields[fidx].type() == QVariant.Double:
                        row.append(str(value.toDouble()[0]))
                    else:
                        row.append(str(value.toString()))
                csvwriter.writerow(row)
            csvfile.close()
        except Exception as err:
            raise OperatorError("error exporting CSV: %s" % err, self.__class__)    
        
class ExposureKMLWriter(ExposureSHPWriter):    
    def __init__(self, options=None, name="Grid Writer"):
        """ constructor """
        super(ExposureKMLWriter, self).__init__(options, name)

    def do_operation(self):
        """ perform export operation """        
        # input/output data checking already done during property set
        input_file = self.inputs[0].value
        output_folder = self.inputs[1].value
        
        shapefile_to_kml(input_file, '%s/exposure.kml'%output_folder)

class ExposureNRMLWriter(ExposureSHPWriter):
    def __init__(self, options=None, name="Grid Writer"):
        """ constructor """
        super(ExposureKMLWriter, self).__init__(options, name)

