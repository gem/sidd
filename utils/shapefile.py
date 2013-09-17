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
shapefile helper functions
"""
import os
import shutil 
import osgeo.ogr as ogr

from qgis.core import QgsVectorLayer, QgsFeature
from utils.system import get_random_name

# internal helper methods
###########################

def _str_icmp(left, right):
    """ compare two strings """
    return str(left).upper() == str(right).upper()

# method on shapefile
###########################
def load_shapefile(input_file, layer_name):    
    """ create a vector layer from given shapefile file """
    _layer = False
    if os.path.exists(input_file):
        _layer = QgsVectorLayer(input_file, layer_name, 'ogr')
        # create spatial index if missing
        # QGIS spatial index file has ,qix extension  
        if _layer.dataProvider() is None:
            raise Exception('Error Loading Shapefile %s\n'%input_file)
        if not os.path.exists('%s.qix'%input_file[:-4]):
            _layer.dataProvider().createSpatialIndex()       
    return _layer

def shapefile_fields(input_file):
    """ return list of field names from given shapefile """
    layer = load_shapefile(input_file, get_random_name())
    names = []
    if layer:
        for idx in layer.dataProvider().fields():
            names.append(layer.dataProvider().fields()[idx].name())
    del layer
    return names

def shapefile_projection(input_file):
    layer = load_shapefile(input_file, get_random_name())
    crs_string = ''
    if layer:
        crs_string = layer.crs().description()
        del layer
    return crs_string

def remove_shapefile(input_file):    
    base = input_file[0:input_file.rfind('.')]
    for _ext in ['.shp', '.shx', '.dbf', '.prj', '.xml', '.qpj']:
        if (os.path.exists(base + _ext)):
            try:
                os.remove(base + _ext)
            except:
                pass

def copy_shapefile(input_file, output_file, extensions=['.shp', '.shx', '.dbf', '.prj', '.xml']):
    input_base = input_file[0:input_file.rfind('.')]
    output_base = output_file[0:output_file.rfind('.')]
    for _ext in extensions:
        if (os.path.exists(input_base + _ext)):
            try:
                shutil.copyfile(input_base+_ext, output_base+_ext)    
            except:
                pass

def shapefile_to_kml(input_file, output_file):
    try:
        input_ds = ogr.Open(input_file)
        kml_driver = ogr.GetDriverByName('KML')
        kml_driver.CopyDataSource(input_ds, output_file)
    except Exception:
        return False
    return True

# method on layers (loaded shapefile)
###########################
def layer_field_exists(layer, field):
    """ determine if given vector layer constains field """
    provider = layer.dataProvider()
    if provider is None:
        return False
    for _idx, _field in provider.fields().iteritems():
        if _str_icmp(field, _field.name()):
            return True
    return False

def layer_field_index(layer, field):
    """
    return index of field in vector layer, -1 if field is not in layer
    """
    provider = layer.dataProvider()
    if provider is None:
        return -1
    for _idx, _field in provider.fields().iteritems():
        if _str_icmp(field, _field.name()):
            return _idx
    return -1

def layer_multifields_stats(layer, fields):
    """ return value distribution for field in given vector layer """
    provider = layer.dataProvider()
    if provider is None:
        return False
    # retrieve index for all fields
    f_indices = []
    for field in fields:
        idx = layer_field_index(layer, field)
        if idx == -1:
            return False
        f_indices.append(idx)
        
    f = QgsFeature()
    stats = {}
    provider.select(f_indices, provider.extent())
    provider.rewind()
    for _idx in range(provider.featureCount()):
        provider.nextFeature(f)
        # create compound key
        _key = ''
        for idx in f_indices:
            if _key != '':
                _key = _key + '_'
            _key += str(f.attributeMap()[idx].toString()).upper()
        # update stats based on compound key
        if stats.has_key(_key):
            stats[_key]+=1
        else:
            stats[_key]=1
    return stats

def layer_field_stats(layer, field):
    """ aggregate stats for field in layer """
    return layer_multifields_stats(layer, [field])

def layer_features(layer):
    """ generator for traversing all features within given vector layer """
    provider = layer.dataProvider()
    if provider is None:
        raise Exception('Error accessing layer features in %s\n' % layer.name())
    provider.select(provider.attributeIndexes())
    f = QgsFeature()
    provider.rewind()
    for _idx in range(provider.featureCount()):
        provider.nextFeature(f)
        yield f

# complex methods 
###########################
def load_shapefile_verify(input_file, layer_name, fields):
    """ create a vector layer from given shapefile file """
    layer = load_shapefile(input_file, layer_name)
    if not layer:
        raise AssertionError('failed to load %s' % (input_file))
    for field in fields:
        if not layer_field_exists(layer, field):
            raise AssertionError('%s field does not exist in %s' % (fields, input_file))
    return layer