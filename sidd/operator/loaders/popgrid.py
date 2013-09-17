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
from qgis.core import QGis, QgsCoordinateTransform, \
                      QgsVectorFileWriter, QgsFeature, QgsField

from utils.shapefile import load_shapefile, load_shapefile_verify, remove_shapefile, \
                      layer_features, layer_field_index
from utils.system import get_unique_filename

from sidd.constants import logAPICall, \
                           GID_FIELD_NAME, CNT_FIELD_NAME                         
from sidd.operator import Operator,OperatorError, OperatorDataError
from sidd.operator.data import OperatorDataTypes

class PopGridLoader(Operator):
    """ operator for loading footprint shapefile """
    
    def __init__(self, options=None, name='Footprint Loader'):
        """ constructor """
        super(PopGridLoader, self).__init__(options, name)        
        self._tmp_dir = options['tmp_dir']
        self._fp_ht_field = None
        
    # self documenting method override
    ###########################
    @property
    def input_types(self):
        return [OperatorDataTypes.Shapefile, 
                OperatorDataTypes.StringAttribute]
        
    @property    
    def input_names(self):
        return ["Population Grid Shapefile",
                "Population Field"]
    
    input_descriptions = input_names

    @property
    def output_types(self):
        return [OperatorDataTypes.Population, OperatorDataTypes.Shapefile]
        
    @property    
    def output_names(self):
        return ["Population layer", "Population Grid file"]

    output_descriptions = output_names

    # public method override
    ###########################
    
    @logAPICall
    def do_operation(self):
        """ perform footprint load operation """
        
        # input/output data checking already done during property set        
        # load and verify
        popgrid_file = self.inputs[0].value
        pop_field = self.inputs[1].value
        
        popgrid_layername = 'zone_%s' % get_unique_filename()
        try:
            tmp_popgrid_layer = load_shapefile_verify(popgrid_file, popgrid_layername,
                                                   [pop_field])
        except AssertionError as err:
            raise OperatorError(str(err), self.__class__)
        
        logAPICall.log('tmp_fp_layer.crs().epsg() %s ' % tmp_popgrid_layer.crs().epsg(),
                       logAPICall.DEBUG)
        if tmp_popgrid_layer.crs().epsg() != self._crs.epsg():
            transform = QgsCoordinateTransform(tmp_popgrid_layer.crs(), self._crs)
            transform_required = True
        else:
            transform_required = False
        
        # output grid
        fields = {
            0 : QgsField(GID_FIELD_NAME, QVariant.Int),
            1 : QgsField(CNT_FIELD_NAME, QVariant.Double),
        }
        pop_idx = layer_field_index(tmp_popgrid_layer, pop_field)
        output_file = '%spop_grid_%s.shp' % (self._tmp_dir, get_unique_filename())
        logAPICall.log('create outputfile %s ... ' % output_file, logAPICall.DEBUG)        
        try:
            writer = QgsVectorFileWriter(output_file, "utf-8", fields, QGis.WKBPoint, self._crs, "ESRI Shapefile")
            f = QgsFeature()
            gid = 0
            for _f in layer_features(tmp_popgrid_layer):
                # NOTE: geom.transform does projection in place to underlying C object
                 
                # 1. get geometry
                geom = _f.geometry()                
                # 2. change project if required
                if transform_required:
                    geom = transform.transform(geom)
                
                # 3. write to file
                gid += 1
                f.setGeometry(geom)
                f.addAttribute(0, QVariant(gid))
                f.addAttribute(1, _f.attributeMap()[pop_idx])
                writer.addFeature(f)            
            del writer, f
        except Exception as err:
            remove_shapefile(output_file)
            raise OperatorError("error creating footprint centroids: %s" % err, self.__class__)

        popgrid_layername = 'popgrid_%s' % get_unique_filename()
        popgrid_layer = load_shapefile(output_file, popgrid_layername)
        if not popgrid_layer:
            raise OperatorError('Error loading footprint centroid file' % (output_file), self.__class__)        
        
        # clean up
        del tmp_popgrid_layer
        
        # store data in output
        self.outputs[0].value = popgrid_layer
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

