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
module constains class for loading footprint shapefiles
"""
from os.path import exists

from PyQt4.QtCore import QVariant
from qgis.core import QGis, QgsCoordinateReferenceSystem, QgsCoordinateTransform, \
                      QgsVectorFileWriter, QgsFeature, QgsField, QgsGeometry

from utils.shapefile import load_shapefile, remove_shapefile, layer_features, layer_field_exists, layer_field_index
from utils.system import get_unique_filename

from sidd.constants import logAPICall, \
                           GID_FIELD_NAME, LON_FIELD_NAME, LAT_FIELD_NAME, AREA_FIELD_NAME, HT_FIELD_NAME                         
from sidd.operator import Operator,OperatorError, OperatorDataError
from sidd.operator.data import OperatorDataTypes

class FootprintLoader(Operator):
    """ operator for loading footprint shapefile """
    
    def __init__(self, options=None, name='Footprint Loader'):
        """ constructor """
        super(FootprintLoader, self).__init__(options, name)        
        self._tmp_dir = options['tmp_dir']
        self._fp_ht_field = None
        
    # self documenting method override
    ###########################
    @property
    def input_types(self):
        return [OperatorDataTypes.Shapefile]
        
    @property    
    def input_names(self):
        return ["Footprint Input Shapefile"]
    
    input_descriptions = input_names

    @property
    def output_types(self):
        return [OperatorDataTypes.Footprint, OperatorDataTypes.Shapefile]
        
    @property    
    def output_names(self):
        return ["Footprint centroid layer", "Footprint centroid file"]

    output_descriptions = output_names

    # public method override
    ###########################
    
    @logAPICall
    def do_operation(self):
        """ perform footprint load operation """
        
        # input/output data checking already done during property set        
        # load and verify
        infile = self.inputs[0].value
        
        tmp_fp_layername = 'fp_%s' % get_unique_filename()
        tmp_fp_layer = load_shapefile(infile, tmp_fp_layername)
        if not tmp_fp_layer:
            raise OperatorError('Error loading footprint file' % (infile), self.__class__)

        if self._fp_ht_field is not None:
            ht_idx = layer_field_index(tmp_fp_layer, self._fp_ht_field)
        else:
            ht_idx = -1
        logAPICall.log('tmp_fp_layer.crs().epsg() %s ' % tmp_fp_layer.crs().epsg(),
                       logAPICall.DEBUG)
        if tmp_fp_layer.crs().epsg() != self._crs.epsg():
            transform = QgsCoordinateTransform(tmp_fp_layer.crs(), self._crs)
            transform_required = True
        else:
            transform_required = False
        
        mercator_crs = QgsCoordinateReferenceSystem()
        #mercator_crs.createFromProj4("+proj=merc +lon_0=0 +k=1 +x_0=0 +y_0=0 +ellps=WGS84 +datum=WGS84 +units=m +no_defs")
        mercator_crs.createFromEpsg(3395)        
        mercator_transform = QgsCoordinateTransform(tmp_fp_layer.crs(), mercator_crs)
        
        # output grid
        fields = {
            0 : QgsField(GID_FIELD_NAME, QVariant.Int),
            1 : QgsField(LON_FIELD_NAME, QVariant.Double),
            2 : QgsField(LAT_FIELD_NAME, QVariant.Double),
            3 : QgsField(AREA_FIELD_NAME, QVariant.Double),
            4 : QgsField(HT_FIELD_NAME, QVariant.Int),
        }
        output_file = '%sfpc_%s.shp' % (self._tmp_dir, get_unique_filename())
        logAPICall.log('create outputfile %s ... ' % output_file, logAPICall.DEBUG)        
        try:
            writer = QgsVectorFileWriter(output_file, "utf-8", fields, QGis.WKBPoint, self._crs, "ESRI Shapefile")
            f = QgsFeature()
            gid = 0
            for _f in layer_features(tmp_fp_layer):
                # NOTE: geom.transform does projection in place to underlying
                #       C object, for some reason, multiple projection does not
                #       work correctly. following is a work-around
                 
                # 1. get geometry
                geom = _f.geometry()
                # 2. get original centroid point and project is required
                centroid  = geom.centroid().asPoint()
                if transform_required:
                    t_centroid = transform.transform(centroid)
                else:
                    t_centroid = centroid
                
                # 3. project into mercator and get area in m2
                geom.transform(mercator_transform)
                area = geom.area()
                
                # write to file
                gid += 1
                f.setGeometry(QgsGeometry.fromPoint(t_centroid))
                f.addAttribute(0, QVariant(gid))
                f.addAttribute(1, QVariant(t_centroid.x()))
                f.addAttribute(2, QVariant(t_centroid.y()))
                f.addAttribute(3, QVariant(area))
                if ht_idx != -1:
                    f.addAttribute(4, _f.attributeMap()[ht_idx])
                else:
                    f.addAttribute(4, QVariant(0))
                writer.addFeature(f)            
            del writer, f
        except Exception as err:
            remove_shapefile(output_file)
            raise OperatorError("error creating footprint centroids: %s" % err, self.__class__)

        fp_layer = load_shapefile(output_file, tmp_fp_layername)
        if not fp_layer:
            raise OperatorError('Error loading footprint centroid file' % (output_file), self.__class__)        
        
        # clean up
        del tmp_fp_layer
        
        # store data in output
        self.outputs[0].value = fp_layer
        self.outputs[1].value = output_file

    # protected method override
    ###########################

    def _verify_inputs(self, inputs):
        """ perform operator specific input validation """

        # assert input file exists
        if not exists(inputs[0].value):
            raise OperatorDataError("input file %s does not exist" % (inputs[0].value))

    def _verify_outputs(self, outputs):
        """ perform operator specific input validation """
        pass

class FootprintHtLoader(FootprintLoader):
    """ operator for loading footprint with building height """
    
    def __init__(self, options=None, name='Footprint with Height Loader'):
        """ constructor """
        super(FootprintHtLoader, self).__init__(options, name)

    # self documenting method override
    ###########################
    
    @property
    def input_types(self):
        return [OperatorDataTypes.Shapefile, OperatorDataTypes.StringAttribute]
        
    @property    
    def input_names(self):
        return ["Footprint Input Shapefile", "Height Field"]
    
    input_descriptions = input_names

    # public method override
    ###########################
    
    @logAPICall
    def do_operation(self):
        """ perform footprint loading operation """
        self._fp_ht_field = self.inputs[1].value
        # reuse super class load operation
        super(FootprintHtLoader, self).do_operation()

        # make sure height field exists
        if not layer_field_exists(self.outputs[0].value, HT_FIELD_NAME):            
            print 'exception here'
            raise OperatorError('failed to load %s with height field %s' % (self.inputs[0].value, self._fp_ht_field),
                                self.__class__)
        