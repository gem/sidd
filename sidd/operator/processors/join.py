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
module contains class for creating mapping scheme from survey data
"""
import bsddb
import os
from math import floor, ceil

from PyQt4.QtCore import QVariant, QString
from qgis.core import QGis, QgsVectorFileWriter, QgsFeature, QgsField, QgsGeometry, \
                      QgsPoint, QgsRectangle, QgsCoordinateReferenceSystem, QgsCoordinateTransform
from qgis.analysis import QgsOverlayAnalyzer

from utils.shapefile import load_shapefile, layer_features, layer_field_index, remove_shapefile, \
                            layer_multifields_stats, layer_fields_stats, load_shapefile_verify 
from utils.system import get_unique_filename
from utils.grid import latlon_to_grid, grid_to_latlon
from sidd.constants import logAPICall, GID_FIELD_NAME, AREA_FIELD_NAME, CNT_FIELD_NAME, \
                           MAX_FEATURES_IN_MEMORY, DEFAULT_GRID_SIZE
from sidd.operator import EmptyOperator, OperatorError
from sidd.operator.data import OperatorDataTypes

class ZoneGridMerger(EmptyOperator):
    """
    """
    # construction / destructor
    ###########################
    
    def __init__(self, options=None, name='Zone & Grid Merger'):
        super(ZoneGridMerger, self).__init__(options, name)        
        self._tmp_dir = options['tmp_dir']
        self._x_off = DEFAULT_GRID_SIZE
        self._y_off = DEFAULT_GRID_SIZE
        
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

        # calculate zone building count statistics
        # store into DB in feature exceed max allowed         
        use_zone_db = zone_layer.dataProvider().featureCount() > MAX_FEATURES_IN_MEMORY
        if use_zone_db:            
            tmp_zone_db_file = '%sdb_%s.db' % (self._tmp_dir, get_unique_filename())
            zone_stats = bsddb.btopen(tmp_zone_db_file, 'c')
            tmp_zone_count_db_file = '%sdb_%s.db' % (self._tmp_dir, get_unique_filename())
            zone_count_stats = bsddb.btopen(tmp_zone_count_db_file, 'c')
        else:
            zone_stats = {}
            zone_count_stats = {}
        gid_idx = layer_field_index(zone_layer, self._gid_field)         
        count_idx = layer_field_index(zone_layer, count_field)
        for _f in layer_features(zone_layer):
            gid = _f.attributeMap()[gid_idx].toString()
            zone_stats[gid] = 0
            zone_count_stats[gid] = _f.attributeMap()[count_idx].toDouble()[0]
        
        # create storage for temporary output data
        use_grid_db = grid_layer.dataProvider().featureCount() > MAX_FEATURES_IN_MEMORY
        if use_grid_db:
            tmp_grid_db_file = '%sdb_%s.db' % (self._tmp_dir, get_unique_filename())
            grid_points = bsddb.btopen(tmp_grid_db_file, 'c')
        else:
            grid_points = {}
        
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

        zone_idx = layer_field_index(tmp_join_layer, zone_field)
        count_idx = layer_field_index(tmp_join_layer, count_field)
        lon_idx = layer_field_index(tmp_join_layer, self._lon_field)
        lat_idx = layer_field_index(tmp_join_layer, self._lat_field)
        gid_idx = layer_field_index(tmp_join_layer, self._gid_field)        
        
        try:        
            for _f in layer_features(tmp_join_layer):
                lon = _f.attributeMap()[lon_idx].toDouble()[0]
                lat = _f.attributeMap()[lat_idx].toDouble()[0]
                zone_str = str(_f.attributeMap()[zone_idx].toString()).upper()
                count_val = _f.attributeMap()[count_idx].toDouble()[0]
                gid = _f.attributeMap()[gid_idx].toString()

                # update stats
                zone_stats[gid] += 1
                grid_points[self._make_key(zone_str, gid, lon, lat)] = 1 
        except Exception as err:
            raise OperatorError("error processing joined layer: " % err, self.__class__)

        # test for zones without a grid point assigned
        count_idx = layer_field_index(zone_layer, count_field)
        gid_idx = layer_field_index(zone_layer, self._gid_field)
        zone_idx = layer_field_index(zone_layer, zone_field)
        _x_off, _y_off = self._x_off / 2.0,  self._y_off / 2.0
        try:
            for _f in layer_features(zone_layer):
                centroid = _f.geometry().centroid().asPoint()
                zone_str = str(_f.attributeMap()[zone_idx].toString()).upper()
                count_val = _f.attributeMap()[count_idx].toDouble()[0]
                gid = _f.attributeMap()[gid_idx].toString()
                
                if zone_stats[gid] == 0:
                    # get lower left corner
                    lon = int(centroid.x()/DEFAULT_GRID_SIZE)*self._x_off + _x_off
                    lat = int(centroid.y()/self._y_off)*self._y_off + _y_off

                    #self._write_feature(writer, f, lon, lat, zone_str, count_val)
                    zone_stats[gid] += 1                                        
                    grid_points[self._make_key(zone_str, gid, lon, lat)] = 1                                
        except Exception as err:
            raise OperatorError("error processing missing points: " % err, self.__class__)

        # output result
        fields = {
            0 : QgsField(self._lon_field, QVariant.Double),
            1 : QgsField(self._lat_field, QVariant.Double),
            2 : QgsField(zone_field, QVariant.String),
            3 : QgsField(count_field, QVariant.Double)
        }
        grid_layername = 'grid_%s' % (get_unique_filename())
        grid_file = '%s%s.shp' % (self._tmp_dir, grid_layername)
        try:
            f = QgsFeature()
            writer = QgsVectorFileWriter(grid_file, "utf-8", fields, QGis.WKBPoint, self._crs, "ESRI Shapefile")
            for key, value in grid_points.iteritems():                
                [zone, zone_gid, lon, lat] = self._parse_key(key)                
                f.setGeometry(QgsGeometry.fromPoint(QgsPoint(lon, lat)))
                """                
                f.setGeometry(QgsGeometry.fromPoint(QgsPoint(lon, lat)))
                f.addAttribute(0, QVariant(lon))
                f.addAttribute(1, QVariant(lat))
                f.addAttribute(2, QVariant(zone_str))            
                f.addAttribute(3, QVariant(count_val / total_features))
                writer.addFeature(f)
                """
                value = float(value) / zone_stats[zone_gid] * zone_count_stats[zone_gid]
                grid_points[key] = value 
                self._write_feature(writer, f, lon, lat, zone, value)
            del writer
        except Exception as err:
            raise OperatorError("error creating joined grid file: " % err, self.__class__)
            
        # load result layer
        grid_layer = load_shapefile(grid_file, grid_layername)
        if not grid_layer:
            raise OperatorError('Error loading joined grid file' % (grid_file), self.__class__)
        
        # clean up
        del tmp_join_layer
        remove_shapefile(tmp_join_file)
        if use_zone_db:
            zone_stats.close()
            os.remove(tmp_zone_db_file)
            zone_count_stats.close()
            os.remove(tmp_zone_count_db_file)
        if use_grid_db:
            grid_points.close()
            os.remove(tmp_grid_db_file)
        
        self.outputs[0].value = grid_layer
        self.outputs[1].value = grid_file

    # protected methods
    ###########################
    def _make_key(self, zone_str, gid, lon, lat):
        return '%s,%s,%.5f,%.5f' % (zone_str, gid, lon, lat)
    
    def _parse_key(self, key):
        (zone_str, gid, lon, lat) = str(key).split(",")
        gid = QString(gid) 
        lat = float(lat)
        lon = float(lon)
        return (zone_str, gid, lon, lat)
    
    def _write_feature(self, writer, f, lon, lat, zone, zone_ratio):
        f.setGeometry(QgsGeometry.fromPoint(QgsPoint(lon, lat)))
        f.addAttribute(0, QVariant(lon))
        f.addAttribute(1, QVariant(lat))
        f.addAttribute(2, QVariant(zone))            
        f.addAttribute(3, QVariant(zone_ratio))
        writer.addFeature(f)

class ZoneFootprintMerger(EmptyOperator):
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

    # protected methods
    ###########################

class ZoneFootprintCounter(EmptyOperator):
    
    def __init__(self, options=None, name='Zone & Footprint Counter'):
        super(ZoneFootprintCounter, self).__init__(options, name)
        self._tmp_dir = options['tmp_dir']
    
    # self documenting method override
    ###########################
    
    @property
    def input_types(self):
        return [OperatorDataTypes.Zone,
                OperatorDataTypes.StringAttribute,
                OperatorDataTypes.StringAttribute,
                OperatorDataTypes.Footprint]
        
    @property    
    def input_names(self):
        return ["Homogenous Zone", "Zone Field", "Zone Count Field", "Building Footprint"]
    
    input_descriptions = input_names

    @property
    def output_types(self):
        return [OperatorDataTypes.Zone,
                OperatorDataTypes.Shapefile]
        
    @property    
    def output_names(self):
        return ["Zone with building count",
                "Zone Shapefile"]

    output_descriptions = output_names    
        

    # public method override
    ###########################
    
    @logAPICall
    def do_operation(self):
        """ perform create mapping scheme operation """
        
        # input/output verification already performed during set input/ouput
        zone_layer = self.inputs[0].value
        zone_field = self.inputs[1].value
        zone_count_field = self.inputs[2].value
        fp_layer = self.inputs[3].value

        # merge with zone 
        tmp_join = 'joined_%s' % get_unique_filename()
        tmp_join_file = '%s%s.shp' % (self._tmp_dir, tmp_join)        
        analyzer = QgsOverlayAnalyzer()
        try:
            analyzer.intersection(fp_layer, zone_layer, tmp_join_file)
            tmp_join_layer = load_shapefile(tmp_join_file, tmp_join)
        except AssertionError as err:
            raise OperatorError(str(err), self.__class__)
        except Exception as err:
            raise OperatorError(str(err), self.__class__)
        
        # count footprint in each zone
        stats = layer_fields_stats(tmp_join_layer, GID_FIELD_NAME + "_")
        
        output_layername = 'zone_%s' % get_unique_filename()
        output_file = '%s%s.shp' % (self._tmp_dir, output_layername)
        logAPICall.log('create outputfile %s ... ' % output_file, logAPICall.DEBUG)
        try:            
            fields ={
                0 : QgsField(GID_FIELD_NAME, QVariant.Int),
                1 : QgsField(zone_field, QVariant.String),
                2 : QgsField(zone_count_field, QVariant.Int),
            }
            writer = QgsVectorFileWriter(output_file, "utf-8", fields, QGis.WKBPolygon, self._crs, "ESRI Shapefile")                     
            f = QgsFeature()            
            for _f in layer_features(zone_layer):
                
                # write to file
                f.setGeometry(_f.geometry())
                f.addAttribute(0, _f.attributeMap()[0])
                f.addAttribute(1, _f.attributeMap()[1])                
                
                # retrieve count from statistic
                try:
                    gid = _f.attributeMap()[0].toString()
                    bldg_count = stats[str(gid)]
                except:
                    bldg_count = 0
                f.addAttribute(2, QVariant(bldg_count))
                writer.addFeature(f)
            
            del writer, f
        except Exception as err:            
            remove_shapefile(output_file)
            raise OperatorError("error creating zone: %s" % err, self.__class__)

        # clean up
        del tmp_join_layer
        remove_shapefile(tmp_join_file)

        # store data in output
        output_layer = load_shapefile(output_file, output_layername)
        if not output_layer:
            raise OperatorError('Error loading footprint centroid file' % (output_file), self.__class__)        
        self.outputs[0].value = output_layer
        self.outputs[1].value = output_file

class ZonePopgridCounter(EmptyOperator):
    
    
    def __init__(self, options=None, name='Zone & Footprint Counter'):
        super(ZonePopgridCounter, self).__init__(options, name)
        self._tmp_dir = options['tmp_dir']
    
    # self documenting method override
    ###########################
    
    @property
    def input_types(self):
        return [OperatorDataTypes.Zone,
                OperatorDataTypes.StringAttribute,
                OperatorDataTypes.Population,
                OperatorDataTypes.NumericAttribute]
        
    @property    
    def input_names(self):
        return ["Homogenous Zone", "Zone Field", "Population Grid", "Population to Building Ratio"]
    
    input_descriptions = input_names

    @property
    def output_types(self):
        return [OperatorDataTypes.Zone,
                OperatorDataTypes.Shapefile]
        
    @property    
    def output_names(self):
        return ["Zone with building count",
                "Zone Shapefile"]

    output_descriptions = output_names    

    # public method override
    ###########################
    
    @logAPICall
    def do_operation(self):
        """ perform create mapping scheme operation """
        
        # input/output verification already performed during set input/ouput
        zone_layer = self.inputs[0].value
        zone_field = self.inputs[1].value
        popgrid_layer = self.inputs[2].value
        pop_to_bldg = float(self.inputs[3].value)
        
        # merge with zone 
        tmp_join = 'joined_%s' % get_unique_filename()
        tmp_join_file = '%s%s.shp' % (self._tmp_dir, tmp_join)        
        analyzer = QgsOverlayAnalyzer()
        try:
            analyzer.intersection(popgrid_layer, zone_layer, tmp_join_file)
            tmp_join_layer = load_shapefile(tmp_join_file, tmp_join)
        except AssertionError as err:
            raise OperatorError(str(err), self.__class__)
        except Exception as err:
            raise OperatorError(str(err), self.__class__)
        
        # count footprint in each zone
        stats = {}
        _gid_idx = layer_field_index(tmp_join_layer, GID_FIELD_NAME + "_")        
        _cnt_idx = layer_field_index(tmp_join_layer, CNT_FIELD_NAME)
        for _f in layer_features(tmp_join_layer):
            # retrieve count from statistic
            _gid = _f.attributeMap()[_gid_idx].toString()
            _count = _f.attributeMap()[_cnt_idx].toString()
            if stats.has_key(_gid):
                stats[_gid]+=float(_count) / pop_to_bldg
            else:
                stats[_gid]=float(_count)  / pop_to_bldg          
        
        output_layername = 'zone_%s' % get_unique_filename()
        output_file = '%s%s.shp' % (self._tmp_dir, output_layername)
        logAPICall.log('create outputfile %s ... ' % output_file, logAPICall.DEBUG)
        try:            
            fields ={
                0 : QgsField(GID_FIELD_NAME, QVariant.Int),
                1 : QgsField(zone_field, QVariant.String),
                2 : QgsField(CNT_FIELD_NAME, QVariant.Int),
            }
            writer = QgsVectorFileWriter(output_file, "utf-8", fields, QGis.WKBPolygon, self._crs, "ESRI Shapefile")                     
            f = QgsFeature()            
            for _f in layer_features(zone_layer):
                
                # write to file
                f.setGeometry(_f.geometry())
                f.addAttribute(0, _f.attributeMap()[0])
                f.addAttribute(1, _f.attributeMap()[1])                
                
                # retrieve count from statistic
                try:
                    gid = _f.attributeMap()[0].toString()
                    bldg_count = stats[gid]
                except:
                    bldg_count = 0
                f.addAttribute(2, QVariant(bldg_count))
                writer.addFeature(f)
            
            del writer, f
        except Exception as err:            
            remove_shapefile(output_file)
            raise OperatorError("error creating zone: %s" % err, self.__class__)

        # clean up
        del tmp_join_layer
        remove_shapefile(tmp_join_file)

        # store data in output
        output_layer = load_shapefile(output_file, output_layername)
        if not output_layer:
            raise OperatorError('Error loading footprint centroid file' % (output_file), self.__class__)        
        self.outputs[0].value = output_layer
        self.outputs[1].value = output_file
    