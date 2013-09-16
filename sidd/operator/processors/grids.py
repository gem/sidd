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
                      QgsRectangle, QgsCoordinateReferenceSystem, QgsCoordinateTransform
from qgis.analysis import QgsOverlayAnalyzer

from utils.shapefile import load_shapefile, layer_features, layer_field_index, remove_shapefile                             
from utils.system import get_unique_filename
from utils.grid import latlon_to_grid, grid_to_latlon
from sidd.constants import logAPICall, GID_FIELD_NAME, AREA_FIELD_NAME, CNT_FIELD_NAME, HT_FIELD_NAME, \
                           MAX_FEATURES_IN_MEMORY, DEFAULT_GRID_SIZE, DEFAULT_HALF_GRID_SIZE
from sidd.operator import Operator, OperatorError
from sidd.operator.data import OperatorDataTypes

class ToGrid(Operator):
    [STAT_AREA_IDX, STAT_COUNT_IDX]= range(2)
    
    def __init__(self, options=None, name='Base Abstract Grid Operator'):
        super(ToGrid, self).__init__(options, name)
        self._tmp_dir = options['tmp_dir']
        
        self.mercator_crs = QgsCoordinateReferenceSystem()        
        self.mercator_crs.createFromEpsg(3395)        

        
    @property
    def output_types(self):
        return [OperatorDataTypes.Grid,
                OperatorDataTypes.Shapefile]
        
    @property    
    def output_names(self):
        return ["Grid with Zone and Count Attributes",
                "Grid Shapefile"]

    output_descriptions = output_names

    # protected methods override
    ###########################
    def _verify_inputs(self, inputs):
        pass

    def _verify_outputs(self, outputs):
        pass

    # protected methods
    ###########################
    def _outputGeometryType(self):
        return QGis.WKBPolygon
    
    def _outputGeometryFromLatLon(self, lat, lon):
        # conversion lat/lon to grid_id is required  
        # it acts as rounding function to lat/lon
        return self._outputGeometryFromGridId(latlon_to_grid(lat, lon)) 

    def _outputGeometryFromGridId(self, grid_id):
        [lat, lon] = grid_to_latlon(int(grid_id))    
        return QgsGeometry.fromRect(QgsRectangle(lon-DEFAULT_HALF_GRID_SIZE, lat-DEFAULT_HALF_GRID_SIZE,
                                                 lon+DEFAULT_HALF_GRID_SIZE, lat+DEFAULT_HALF_GRID_SIZE))

    def _create_grid(self, grid_name, grid_file, x_min, y_min, x_max, y_max, x_off, y_off):
        x_off2, y_off2 = x_off / 2.0, y_off / 2.0
        x_min = floor(x_min / x_off) * x_off
        x_max = ceil(x_max / x_off) * x_off
        y_min = floor(y_min / y_off) * y_off
        y_max = ceil(y_max / y_off) * y_off
        
        xtotal = int((x_max - x_min) / x_off)+1
        ytotal = int((y_max - y_min) / y_off)+1

        logAPICall.log('x_min %f x_max %f y_min %f y_max %f x_off %f y_off %f xtotal %d, ytotal %d'
                       % (x_min, x_max, y_min, y_max, x_off, y_off, xtotal, ytotal),
                       logAPICall.DEBUG_L2)
        fields = {
            0 : QgsField('GRID_GID', QVariant.String),            
        }
        writer = QgsVectorFileWriter(grid_file, "utf-8", fields, QGis.WKBPolygon, self._crs, "ESRI Shapefile")
        f = QgsFeature()
        for x in range(xtotal):
            for y in range(ytotal):
                lon = x_min + (x * x_off) + (x_off2)
                lat = y_min + (y * y_off) + (y_off2)                
                #out_geom = QgsGeometry.fromRect(QgsRectangle(lon-x_off2, lat-y_off2,
                #                                             lon+x_off2, lat+y_off2))                                
                f.setGeometry(self._outputGeometryFromLatLon(lat, lon))                
                f.addAttribute(0, QVariant(latlon_to_grid(lat, lon)))                
                writer.addFeature(f)
        del writer 
        return load_shapefile(grid_file, grid_name)        

    def _create_zone_statistics(self, zone_layer, zone_field, count_field, zone_stat, zone_names):
        # project geometry into mercator and get area in m2
        mercator_transform = QgsCoordinateTransform(zone_layer.crs(),
                                                    self.mercator_crs)    
        zone_gid_idx = layer_field_index(zone_layer, GID_FIELD_NAME)
        zone_field_idx = layer_field_index(zone_layer, zone_field)
        count_field_idx = layer_field_index(zone_layer, count_field)
        for _f in layer_features(zone_layer):            
            # project into mercator and get area in m2
            geom = _f.geometry()
            geom.transform(mercator_transform)
            area = geom.area()
                
            gid = _f.attributeMap()[zone_gid_idx].toString()            
            # if count field is not defined, then set count to 0
            if count_field_idx >= 0:
                count = _f.attributeMap()[count_field_idx].toDouble()[0]
            else:
                count = 0            
            
            self._update_stat(zone_stat, gid, count, area)
            zone_names[gid] = _f.attributeMap()[zone_field_idx]

    def _update_stat(self, stats, key, count, area):
        if not stats.has_key(key):
            stats[key] = [0,0]
        stat = stats[key]
        stat[ToGrid.STAT_COUNT_IDX] +=count
        stat[ToGrid.STAT_AREA_IDX] +=area
            
    def _load_output(self, output_file, output_layername):
        output_layer = load_shapefile(output_file, output_layername)
        if not output_layer:
            raise OperatorError('Error loading grid file' % (output_file), self.__class__)        
        self.outputs[0].value = output_layer
        self.outputs[1].value = output_file

class ZoneToGrid(ToGrid):
    def __init__(self, options=None, name='Grid Zone Merger'):
        super(ZoneToGrid, self).__init__(options, name)

    @property
    def input_types(self):
        return [OperatorDataTypes.Zone,
                OperatorDataTypes.StringAttribute,
                OperatorDataTypes.StringAttribute,
                OperatorDataTypes.StringAttribute]
        
    @property    
    def input_names(self):
        return ["Zone Layer",
                "Zone Field",
                "Building Count Field",
                "Building Area Field"]

    input_descriptions = input_names
    
    @logAPICall
    def do_operation(self):
        # validate inputs        
        zone_layer = self.inputs[0].value
        zone_field = self.inputs[1].value
        count_field = self.inputs[2].value
        area_field = self.inputs[3].value
        
        # make sure input is correct
        # NOTE: these checks cannot be performed at set input time
        #       because the data layer maybe is not loaded yet
        self._test_layer_loaded(zone_layer)
        self._test_layer_field_exists(zone_layer, GID_FIELD_NAME)
        self._test_layer_field_exists(zone_layer, zone_field)        
        self._test_layer_field_exists(zone_layer, count_field)
        
        # local variables 
        analyzer = QgsOverlayAnalyzer()
        area_idx = ToGrid.STAT_AREA_IDX
        #cnt_idx = ToGrid.STAT_COUNT_IDX
        
        # 1. find building count and total area for each zone
        zone_names, zone_stat= {}, {}
        try:
            self._create_zone_statistics(zone_layer, zone_field, count_field, 
                                         zone_stat, zone_names)
        except Exception as err:
            raise OperatorError(str(err), self.__class__)    
    
        # 2. create grids around extent of zone 
        tmp_grid1 = 'grid_' + get_unique_filename()
        tmp_grid1_file = self._tmp_dir + tmp_grid1 + '.shp'
        try:
            extent = zone_layer.extent()
            [x_min, y_min, x_max, y_max] = [extent.xMinimum(), extent.yMinimum(), extent.xMaximum(), extent.yMaximum()]
            tmp_grid_lyr1 = self._create_grid(tmp_grid1, tmp_grid1_file, \
                                              x_min, y_min, x_max, y_max, \
                                              DEFAULT_GRID_SIZE, DEFAULT_GRID_SIZE)            
        except Exception as err:
            raise OperatorError(str(err), self.__class__)    
        
        # 3. intersect grids and zones to obtain polygons with 
        # - grid_id and zone_id
        # - ratio of grid covered by zone (polygon area / zone area) 
        # apply ratio to zone building count to obtain count assigned to polygon                  
        tmp_join = 'joined_%s' % get_unique_filename()
        tmp_join_file = '%s%s.shp' % (self._tmp_dir, tmp_join)
        try:
            # do intersection
            analyzer.intersection(tmp_grid_lyr1, zone_layer, tmp_join_file)
            tmp_join_layer = load_shapefile(tmp_join_file, tmp_join)
        except AssertionError as err:
            raise OperatorError(str(err), self.__class__)
        except Exception as err:
            raise OperatorError(str(err), self.__class__)
        
        # do tally        
        zone_gid_idx = layer_field_index(tmp_join_layer, GID_FIELD_NAME)
        grid_gid_idx = layer_field_index(tmp_join_layer, "GRID_GID")
        bldg_cnt_idx = layer_field_index(tmp_join_layer, count_field)
        bldg_area_idx = layer_field_index(tmp_join_layer, area_field)
        mercator_transform = QgsCoordinateTransform(tmp_join_layer.crs(),
                                                    self.mercator_crs)          

        fields = {
            0 : QgsField(GID_FIELD_NAME, QVariant.String),            
            1 : QgsField(zone_field, QVariant.String),
            2 : QgsField(CNT_FIELD_NAME, QVariant.Double),
            3 : QgsField(AREA_FIELD_NAME, QVariant.Double),
        }    
        output_layername = 'grid_%s' % get_unique_filename()
        output_file = '%s%s.shp' % (self._tmp_dir, output_layername)                
        writer = QgsVectorFileWriter(output_file, "utf-8", fields, QGis.WKBPolygon, self._crs, "ESRI Shapefile")
        f = QgsFeature() 
        for _f in layer_features(tmp_join_layer):
            # get area of polygon            
            geom = _f.geometry()
            geom.transform(mercator_transform)
            area = geom.area()

            # generate all stats of interest
            zone_gid = _f.attributeMap()[zone_gid_idx].toString()
            grid_gid = _f.attributeMap()[grid_gid_idx].toString()
            stat = zone_stat[zone_gid]
            
            # calculate count/area as proportion of total zone area
            bldg_cnt = _f.attributeMap()[bldg_cnt_idx].toDouble()[0] * (area/stat[area_idx])
            if bldg_area_idx> 0:
                bldg_area = _f.attributeMap()[bldg_area_idx].toDouble()[0] * (area/stat[area_idx])                
            else:
                bldg_area = 0 

            # create output record
            f.setGeometry(self._outputGeometryFromGridId(grid_gid))
            f.addAttribute(0, grid_gid)
            f.addAttribute(1, zone_names[QString(zone_gid)])
            f.addAttribute(2, bldg_cnt)
            f.addAttribute(3, bldg_area)
            writer.addFeature(f)        
        del writer    

        # clean up
        del tmp_grid_lyr1
        del tmp_join_layer
        remove_shapefile(tmp_grid1_file)
        remove_shapefile(tmp_join_file)
                
        # store data in output
        self._load_output(output_file, output_layername)

class FootprintZoneToGrid(ZoneToGrid):
    def __init__(self, options=None, name='Grid Zone Merger'):
        super(FootprintZoneToGrid, self).__init__(options, name)
    
    @property
    def input_types(self):
        return [OperatorDataTypes.Footprint,                
                OperatorDataTypes.Zone,
                OperatorDataTypes.StringAttribute,
                OperatorDataTypes.StringAttribute,
                OperatorDataTypes.StringAttribute]

    @property    
    def input_names(self):
        return ["Footprint",                
                "Zone Layer",
                "Zone Field",
                "Building Count Field"
                "Building Area Field"]
    
    input_descriptions = input_names

    # public method override
    ###########################
    
    @logAPICall
    def do_operation(self):
        """ perform create mapping scheme operation """    
        
        # validate inputs 
        fp_layer = self.inputs[0].value
        zone_layer = self.inputs[1].value
        zone_field = self.inputs[2].value
        count_field = self.inputs[3].value
        area_field = self.inputs[4].value 

        # make sure input is correct
        # NOTE: these checks cannot be performed at set input time
        #       because the data layer maybe is not loaded yet
        self._test_layer_loaded(fp_layer)
        self._test_layer_loaded(zone_layer)
        self._test_layer_field_exists(zone_layer, GID_FIELD_NAME)
        self._test_layer_field_exists(zone_layer, zone_field)
        # count_field is not required        
        # if count field is not defined, then generate building count from footprints        
        # area_field is not required
        
        # local variables 
        analyzer = QgsOverlayAnalyzer()
        area_idx = ToGrid.STAT_AREA_IDX
        cnt_idx = ToGrid.STAT_COUNT_IDX
        
        zone_names, zone_stat, zone_stat2, zone_totals = {}, {}, {}, {}
        
        # 1. find building count and total area for each zone
        # project geometry into mercator and get area in m2
        mercator_crs = QgsCoordinateReferenceSystem()        
        mercator_crs.createFromEpsg(3395)        
        mercator_transform = QgsCoordinateTransform(zone_layer.crs(), mercator_crs)
        
        try:
            # use zone geometry area 
            self._create_zone_statistics(zone_layer, zone_field, count_field, 
                     zone_stat, zone_names)
        except Exception as err:
            raise OperatorError(str(err), self.__class__)

        # 2. create grids around extent of zone 
        tmp_grid1 = 'grid_' + get_unique_filename()
        tmp_grid1_file = self._tmp_dir + tmp_grid1 + '.shp'
        extent = zone_layer.extent()
        [x_min, y_min, x_max, y_max] = [extent.xMinimum(), extent.yMinimum(), extent.xMaximum(), extent.yMaximum()]
        tmp_grid_lyr1 = self._create_grid(tmp_grid1, tmp_grid1_file, \
                                          x_min, y_min, x_max, y_max, \
                                          DEFAULT_GRID_SIZE, DEFAULT_GRID_SIZE)            

        # tally total building area if there is defined
        bldg_area_idx = layer_field_index(zone_layer, area_field)
        zone_area = {}
        zone_has_area = False        
        if bldg_area_idx > 0:
            zone_has_area = True
            zone_gid_idx = layer_field_index(zone_layer, GID_FIELD_NAME)
            for _f in layer_features(zone_layer):            
                gid = _f.attributeMap()[zone_gid_idx].toString()            
                area = _f.attributeMap()[bldg_area_idx].toDouble()[0]            
                if zone_area.has_key(gid):
                    zone_area[gid] = str(float(zone_area[gid]))+area
                else: 
                    zone_area[gid] = area
        
        # 3. intersect grids and zones to obtain polygons with 
        # - grid_id and zone_id
        # - ratio of grid covered by zone (polygon area / zone area) 
        # apply ratio to zone building count to obtain count assigned to polygon                  
        tmp_join = 'joined_%s' % get_unique_filename()
        tmp_join_file = '%s%s.shp' % (self._tmp_dir, tmp_join)
        try:
            # do intersection
            analyzer.intersection(tmp_grid_lyr1, zone_layer, tmp_join_file)
            tmp_join_layer = load_shapefile(tmp_join_file, tmp_join)
        except AssertionError as err:
            raise OperatorError(str(err), self.__class__)
        except Exception as err:
            raise OperatorError(str(err), self.__class__)
        
        # do tally
        zone_gid_idx = layer_field_index(tmp_join_layer, GID_FIELD_NAME)
        grid_gid_idx = layer_field_index(tmp_join_layer, "GRID_GID")
        bldg_cnt_idx = layer_field_index(tmp_join_layer, count_field)
        for _f in layer_features(tmp_join_layer):
            geom = _f.geometry()
            geom.transform(mercator_transform)
            area = geom.area()
            
            # generate all stats of interest
            zone_gid = _f.attributeMap()[zone_gid_idx].toString()
            grid_gid = _f.attributeMap()[grid_gid_idx].toString()
            stat = zone_stat[zone_gid]            
            # calculate count/area as proportion of total zone area
            area_ratio = (area/stat[area_idx])
            if bldg_cnt_idx > 0:
                bldg_cnt = _f.attributeMap()[bldg_cnt_idx].toDouble()[0] * area_ratio
            else:
                bldg_cnt = 0
            if zone_has_area: 
                area = zone_area[zone_gid] * area_ratio
            else:
                area = stat[area_idx] * area_ratio                 
            self._update_stat(zone_stat2, '%s|%s'%(grid_gid, zone_gid), bldg_cnt, area)
        
        # 4. find total buildings in each zone based on footprint
        # - simply join the files and tally count and total area 
        tmp_join1 = 'joined_%s' % get_unique_filename()
        tmp_join1_file = '%s%s.shp' % (self._tmp_dir, tmp_join1)        
        try:
            # do intersection
            analyzer.intersection(fp_layer, tmp_join_layer, tmp_join1_file)
            tmp_join1_layer = load_shapefile(tmp_join1_file, tmp_join1)
        except AssertionError as err:
            raise OperatorError(str(err), self.__class__)
        except Exception as err:
            raise OperatorError(str(err), self.__class__)
        
        # do tally
        zone_fp_stat = {}
        zone_gid_idx = layer_field_index(tmp_join1_layer, '%s_'% GID_FIELD_NAME)
        grid_gid_idx = layer_field_index(tmp_join1_layer, "GRID_GID")        
        fp_area_idx = layer_field_index(tmp_join1_layer, AREA_FIELD_NAME)
        fp_ht_idx = layer_field_index(tmp_join1_layer, HT_FIELD_NAME)
        fp_has_height = False
        for _f in layer_features(tmp_join1_layer):
            zone_gid = _f.attributeMap()[zone_gid_idx].toString()
            grid_gid = _f.attributeMap()[grid_gid_idx].toString()
            area = _f.attributeMap()[fp_area_idx].toDouble()[0] # area comes from geometry, always exists
            ht = _f.attributeMap()[fp_ht_idx].toDouble()[0]
            if ht > 0:
                fp_has_height = True
                area *= ht      # this is actual area to be aggregated at the end
            self._update_stat(zone_fp_stat, '%s|%s'%(grid_gid, zone_gid), 1, area)
            self._update_stat(zone_totals, zone_gid, 1, area)
        
        # 5. generate grid with adjusted building counts
        fields = {
            0 : QgsField(GID_FIELD_NAME, QVariant.String),            
            1 : QgsField(zone_field, QVariant.String),
            2 : QgsField(CNT_FIELD_NAME, QVariant.Double),
            3 : QgsField(AREA_FIELD_NAME, QVariant.Double),
        }
        output_layername = 'grid_%s' % get_unique_filename()
        output_file = '%s%s.shp' % (self._tmp_dir, output_layername)                
        writer = QgsVectorFileWriter(output_file, "utf-8", fields, QGis.WKBPolygon, self._crs, "ESRI Shapefile")
        f = QgsFeature()
        for key in zone_stat2.keys():
            (grid_gid, zone_gid) = str(key).split("|")
            s_zone = zone_stat[QString(zone_gid)]           # overall statistics for the zone from zone file (always exists)
            s_zone_grid = zone_stat2[key]                   # grid specific statistic from from zone file    (always exists)            
            if zone_totals.has_key(QString(zone_gid)):      # overall statistics for the zone from footprints
                s_total = zone_totals[QString(zone_gid)]       
            else:
                s_total = [0,0] # set to zero if missing
            if zone_fp_stat.has_key(key):                   # grid specific statistic from from footprint
                s_fp = zone_fp_stat[key]                        
            else:
                s_fp = [0, 0]   # set to zero if missing

            zone_leftover_count = s_zone[cnt_idx] - s_total[cnt_idx]   
            if zone_has_area:
                zone_leftover_area = zone_area[QString(zone_gid)] - s_total[area_idx]
            else:
                zone_leftover_area = s_zone[area_idx] - s_total[area_idx]
            if zone_leftover_count > 0:
                # there are still building not accounted for
                # distribute to grid based on ratio of grid leftover area over zone leftover area
                # (leftover area is area of zone after subtracting footprint areas                
                grid_leftover_count = zone_leftover_count * ((s_zone_grid[area_idx]-s_fp[area_idx])/zone_leftover_area)
                grid_count = s_fp[cnt_idx] + grid_leftover_count
            else:
                grid_count = s_fp[cnt_idx]
            
            if fp_has_height:
                # area can be actual area based on footprint area * height
                area = s_fp[area_idx]
            elif zone_has_area:
                area = s_zone_grid[area_idx]
            else:
                # no area defined
                area = 0 # max(s_zone_grid[area_idx], s_fp[area_idx])
                
            f.setGeometry(self._outputGeometryFromGridId(grid_gid))
            f.addAttribute(0, grid_gid)
            f.addAttribute(1, zone_names[QString(zone_gid)])
            f.addAttribute(2, grid_count)
            f.addAttribute(3, area)
            writer.addFeature(f)
        del writer
        
        # clean up
        del tmp_grid_lyr1
        del tmp_join_layer
        del tmp_join1_layer
        remove_shapefile(tmp_grid1_file)
        remove_shapefile(tmp_join_file)
        remove_shapefile(tmp_join1_file)
                
        # store data in output
        self._load_output(output_file, output_layername)


class PopgridZoneToGrid(ToGrid):
    def __init__(self, options=None, name='Population to Building Count Grid'):
        super(PopgridZoneToGrid, self).__init__(options, name)
    
    @property
    def input_types(self):
        return [OperatorDataTypes.Population,
                OperatorDataTypes.Zone,
                OperatorDataTypes.StringAttribute,
                OperatorDataTypes.NumericAttribute]

    @property    
    def input_names(self):
        return ["Population Grid",
                "Zone Layer",
                "Zone Field",
                "Population to Building Convertion"]
    
    input_descriptions = input_names

    # public method override
    ###########################
    
    @logAPICall
    def do_operation(self):
        """ perform create mappin """
        # validate inputs 
        popgrid_layer = self.inputs[0].value        
        zone_layer = self.inputs[1].value
        zone_field = self.inputs[2].value
        pop_to_bldg = float(self.inputs[3].value)

        # make sure input is correct
        # NOTE: these checks cannot be performed at set input time
        #       because the data layer maybe is not loaded yet
        self._test_layer_loaded(popgrid_layer)
        self._test_layer_field_exists(popgrid_layer, CNT_FIELD_NAME)
        self._test_layer_loaded(zone_layer)
        self._test_layer_field_exists(zone_layer, zone_field)        
        # count_field is not required        
        # if count field is not defined, then generate building count from footprints
        
        # local variables 
        analyzer = QgsOverlayAnalyzer()

        # intersect grids and zones to obtain polygons with 
        # - population and zone_id
        # - apply ratio to population to obtain building count                  
        tmp_join = 'joined_%s' % get_unique_filename()
        tmp_join_file = '%s%s.shp' % (self._tmp_dir, tmp_join)
        try:
            # do intersection
            analyzer.intersection(popgrid_layer, zone_layer, tmp_join_file)
            tmp_join_layer = load_shapefile(tmp_join_file, tmp_join)
        except AssertionError as err:
            raise OperatorError(str(err), self.__class__)
        except Exception as err:
            raise OperatorError(str(err), self.__class__)

        # generate grid with  building counts
        fields = {
            0 : QgsField(GID_FIELD_NAME, QVariant.String),            
            1 : QgsField(zone_field, QVariant.String),
            2 : QgsField(CNT_FIELD_NAME, QVariant.Double),
        }
        output_layername = 'grid_%s' % get_unique_filename()
        output_file = '%s%s.shp' % (self._tmp_dir, output_layername)                
        writer = QgsVectorFileWriter(output_file, "utf-8", fields, QGis.WKBPolygon, self._crs, "ESRI Shapefile")
        f = QgsFeature()
        pop_idx = layer_field_index(tmp_join_layer, CNT_FIELD_NAME)
        zone_idx = layer_field_index(tmp_join_layer, zone_field) 
        for _f in layer_features(tmp_join_layer):
            pop_count = _f.attributeMap()[pop_idx].toDouble()[0]
            zone = _f.attributeMap()[zone_idx].toString()
            
            # 1. get geometry
            geom = _f.geometry()
            # 2. get original centroid point and project is required
            centroid  = geom.centroid().asPoint()
            grid_gid = latlon_to_grid(centroid.y(), centroid.x())
            f.setGeometry(self._outputGeometryFromGridId(grid_gid))
            f.addAttribute(0, grid_gid)
            f.addAttribute(1, zone)
            f.addAttribute(2, pop_count / pop_to_bldg)
            writer.addFeature(f)
        del writer
        
        # clean up
        del tmp_join_layer
        remove_shapefile(tmp_join_file)
                
        # store data in output
        self._load_output(output_file, output_layername)
