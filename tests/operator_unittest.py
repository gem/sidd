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
#
import os
import logging

# import sidd packages for testing
from sidd.ms import MappingScheme
from sidd.operator import *
from utils.shapefile import remove_shapefile, layer_fields_stats, load_shapefile, layer_features, layer_field_index
from sidd.constants import AREA_FIELD_NAME, HT_FIELD_NAME, CNT_FIELD_NAME
from sidd.taxonomy import get_taxonomy

from common import SIDDTestCase

class OperatorTestCase(SIDDTestCase):
    
    # run for every test
    ##################################
    
    def setUp(self):
        super(OperatorTestCase, self).setUp()
        self.taxonomy = get_taxonomy("gem")
        
        # test data set 1        
        self.ms_file = self.test_data_dir +  "ms.xml"
        self.fp_path = self.test_data_dir +  'footprint.shp'
        self.fp_feature_count = 1475
        self.zone1_path = self.test_data_dir +  "zones1.shp"
        self.zone1_field = "ZONE"

        # test data set 2
        self.zone2_path = self.test_data_dir +  "zones2.shp"
        self.zone2_field = 'LandUse'
        self.zone2_feature_count = 546
        self.zone2_total_bldg_cnt = 292377
        self.zone2_total_bldg_area = 71582303
        self.zone2_bldgcount_field = 'NumBldg'
        self.zone2_bldgarea_field = 'SqMtBldg'

        # test data set 3
        self.fp3_path = self.test_data_dir +  "footprints3.shp"
        self.fp3_height_field = "HEIGHT"
        self.fp3_feature_count = 785
        self.fp3_total_area = 774814.441
        self.gemdb3_path = self.test_data_dir +  "survey3.db3"
        self.zone3_path = self.test_data_dir +  "zones3.shp"
        self.zone3_field = "ZONE"
        self.zone3_bldgcount_field = 'NumBldgs'
        self.zone3_bldgarea_field = 'SqMtBldg'        
        self.zone3_total_bldg_cnt = 850
        self.zone3_total_bldg_area = 500000
        
        self.popgrid_path = self.test_data_dir + 'popgrid.shp'
        self.pop_field = "Population"
        self.popgrid_feature_count = 4 
        self.popgrid_zone_path = self.test_data_dir + 'popgrid_zone.shp'
        self.popgrid_zone_field = "ZONE"
        
        self.grid_path = self.test_data_dir +  "grid.shp"
        self.grid2_path = self.test_data_dir +  "grid2.shp"
        
        self.operator_options = {
            'tmp_dir': self.test_tmp_dir,
            'taxonomy':self.taxonomy,
            'skips':[1,2,3,4,5,6],
        }

    def tearDown(self):
        pass

    # misc
    ##################################
    
    def test_OperatorByName(self):
        Operator.get_operator('sidd.operator.processors.GridWriter',
                              self.operator_options)

    # test loaders
    ##################################

    def test_LoadFootprint(self, skipTest=False, fp=1):
        logging.debug('test_LoadFootprint %s' % skipTest)
        
        if fp==1:
            fp_path = self.fp_path
        else:
            fp_path = self.fp3_path
        loader = FootprintLoader(self.operator_options)
        loader.inputs = [
            OperatorData(OperatorDataTypes.Shapefile, fp_path),
        ]
        loader.outputs = [
            OperatorData(OperatorDataTypes.Footprint),
            OperatorData(OperatorDataTypes.Shapefile),
        ]
        loader.do_operation()
        if skipTest:
            return loader.outputs
        layer = loader.outputs[0].value        
        self.assertEquals(self.fp_feature_count, layer.dataProvider().featureCount())        
        
        del layer
        self._clean_layer(loader.outputs)  

    def test_LoadFootprintHT(self, skipTest=False):
        logging.debug('test_LoadFootprint %s' % skipTest)
        
        fp_path = self.fp3_path
        loader = FootprintHtLoader(self.operator_options)
        loader.inputs = [
            OperatorData(OperatorDataTypes.Shapefile, fp_path),
            OperatorData(OperatorDataTypes.StringAttribute, self.fp3_height_field),
        ]
        loader.outputs = [
            OperatorData(OperatorDataTypes.Footprint),
            OperatorData(OperatorDataTypes.Shapefile),
        ]
        loader.do_operation()
        if skipTest:
            return loader.outputs
        layer = loader.outputs[0].value        
        self.assertEquals(self.fp3_feature_count, layer.dataProvider().featureCount())        
        
        del layer
        self._clean_layer(loader.outputs)  
    
    def test_LoadPopGrid(self, skipTest=False):
        logging.debug('test_LoadPopGrid %s' % skipTest)
        """ create operator for loading zone data and add to workflow """
        # required operator_data for additional processing
        loader = PopGridLoader(self.operator_options)
        loader.inputs = [OperatorData(OperatorDataTypes.Shapefile, self.popgrid_path),
                         OperatorData(OperatorDataTypes.StringAttribute, self.pop_field)]        
        loader.outputs = [OperatorData(OperatorDataTypes.Population),
                          OperatorData(OperatorDataTypes.Shapefile)]
        # add to workflow
        loader.do_operation()
        if skipTest:
            return loader.outputs
        layer = loader.outputs[0].value        
        self.assertEquals(self.popgrid_feature_count, layer.dataProvider().featureCount())        
        
        del layer
        self._clean_layer(loader.outputs)  
                

    def test_LoadZone(self, skipTest=False, zone=1):
        logging.debug('test_LoadZone %s' % skipTest)
        
        if zone ==1:
            zone_path = self.zone1_path
            zone_field = self.zone1_field
        elif zone ==2:
            zone_path = self.zone2_path
            zone_field = self.zone2_field
        elif zone ==3:
            zone_path = self.zone3_path
            zone_field = self.zone3_field
        elif zone==4:            
            zone_path = self.popgrid_zone_path
            zone_field = self.popgrid_zone_field
        
        loader = ZoneLoader(self.operator_options)
        loader.inputs = [
            OperatorData(OperatorDataTypes.Shapefile, zone_path),
            OperatorData(OperatorDataTypes.StringAttribute, zone_field),            
        ]
        loader.outputs = [
            OperatorData(OperatorDataTypes.Zone),
            OperatorData(OperatorDataTypes.Shapefile)
        ]        
        loader.do_operation()
        
        if skipTest:
            return loader.outputs  

        self._clean_layer(loader.outputs)  

    
    def test_LoadZone2(self, skipTest=False, zone=2):
        logging.debug('test_LoadZoneCount %s' % skipTest)
        
        if zone == 2:
            zone_path = self.zone2_path
            zone_field = self.zone2_field
            zone_count_field = self.zone2_bldgcount_field
            zone_area_field = self.zone2_bldgarea_field
        elif zone==3: 
            zone_path = self.zone3_path
            zone_field = self.zone3_field
            zone_count_field = self.zone3_bldgcount_field
            zone_area_field  = self.zone3_bldgarea_field
        else:
            raise Exception("zone not supported")
        
        loader = ZoneCountLoader(self.operator_options)
        loader.inputs = [
            OperatorData(OperatorDataTypes.Shapefile, zone_path),
            OperatorData(OperatorDataTypes.StringAttribute, zone_field),
            OperatorData(OperatorDataTypes.StringAttribute, zone_count_field),
            OperatorData(OperatorDataTypes.StringAttribute, zone_area_field),
        ]
        loader.outputs = [
            OperatorData(OperatorDataTypes.Zone),
            OperatorData(OperatorDataTypes.Shapefile)
        ]        
        loader.do_operation()
        if skipTest:
            return loader.outputs
        
        zones = loader.outputs[0].value
        self.assertEquals(zones.featureCount(), self.zone2_feature_count)
        bldg_cnt_idx = layer_field_index(zones, zone_count_field)
        bldg_area_idx = layer_field_index(zones, zone_area_field)
        total_bldg_cnt, total_bldg_area = 0, 0
        for feature in layer_features(zones):
            total_bldg_cnt += feature.attributeMap()[bldg_cnt_idx].toDouble()[0]
            total_bldg_area += feature.attributeMap()[bldg_area_idx].toDouble()[0]
        self.assertEquals(total_bldg_cnt, self.zone2_total_bldg_cnt)
        self.assertEquals(total_bldg_area, self.zone2_total_bldg_area)
        
        # clean up
        del zones
        self._clean_layer(loader.outputs)  
    
    def test_LoadGEMDBSurvey(self, skipTest=False):   
        logging.debug('test_LoadSurvey %s' % skipTest)
        
        loader = GEMDBSurveyLoader(self.operator_options)
        loader.inputs = [
            OperatorData(OperatorDataTypes.File, self.gemdb3_path),
            OperatorData(OperatorDataTypes.StringAttribute, 'GEMDB'),
            OperatorData(OperatorDataTypes.StringAttribute, None),            
        ]
        loader.outputs = [
            OperatorData(OperatorDataTypes.Survey),
            OperatorData(OperatorDataTypes.Shapefile),
        ]
        loader.do_operation()
        if skipTest:
            return loader.outputs
        
        # perform test
        survey_layer = loader.outputs[0].value
        self.assertEqual(survey_layer.dataProvider().featureCount(), 24)
        
        grp_idx = layer_field_index(survey_layer, "GROUP")
        groups = {}
        for svy in layer_features(survey_layer):
            group = str(svy.attributeMap()[grp_idx].toString())
            if not groups.has_key(group):
                groups[group]=1
            else:
                groups[group]+=1
        self.assertEqual(len(groups), 3)
        self.assertEqual(groups.values(), [8, 8, 8])
        
        # clean up
        self._clean_layer(loader.outputs)  


    def test_StratifiedSampleMS(self, skipTest=False):
        fp_data = self.test_LoadFootprintHT(skipTest=True)
        fp_area_field = OperatorData(OperatorDataTypes.StringAttribute, AREA_FIELD_NAME)
        fp_ht_field = OperatorData(OperatorDataTypes.StringAttribute, HT_FIELD_NAME)
        zone_data = self.test_LoadZone(skipTest=True, zone=3)
        zone_field = OperatorData(OperatorDataTypes.StringAttribute, self.zone3_field)
        survey_data = self.test_LoadGEMDBSurvey(skipTest=True)
        
        ms_creator = StratifiedMSCreator(self.operator_options)
        ms_creator.inputs = [fp_data[0], fp_area_field, fp_ht_field, zone_data[0], zone_field, survey_data[0]]
        ms_creator.outputs = [OperatorData(OperatorDataTypes.MappingScheme),
                              OperatorData(OperatorDataTypes.ZoneStatistic),]
        
        ms_creator.do_operation()
        ms = ms_creator.outputs[0].value
        stats = ms.get_assignment_by_name("ALL")
        stats.refresh_leaves(with_modifier=False)
        self.assertEqual(len(stats.leaves), 13) 
                        
        # clean up
        self._clean_layer(fp_data)
        self._clean_layer(survey_data)        
        self._clean_layer(zone_data)
          
    def test_LoadMS(self, skipTest=False):
        logging.debug('test_LoadMS %s' % skipTest)
                
        ms_loader = MappingSchemeLoader(self.operator_options)
        ms_loader.inputs = [
            OperatorData(OperatorDataTypes.File, self.ms_file),
        ]
        ms_loader.outputs = [
            OperatorData(OperatorDataTypes.MappingScheme),
        ]
        ms_loader.do_operation()
        
        if skipTest:
            return ms_loader.outputs
        
        # no cleanup needed, MappingSchemeLoader does not create tmp files

    # test grid writer
    ##################################
    
    def test_MakeGrid(self, skipTest=False):
        logging.debug('test_MakeGrid %s' % skipTest)
        
        zone_data = self.test_LoadZone(True, 1)
        extent = zone_data[0].value.extent()
        
        writer = GridWriter(self.operator_options)
        writer.set_inputs([
            OperatorData(OperatorDataTypes.NumericAttribute, extent.xMinimum()),
            OperatorData(OperatorDataTypes.NumericAttribute, extent.yMinimum()),
            OperatorData(OperatorDataTypes.NumericAttribute, extent.xMaximum()),
            OperatorData(OperatorDataTypes.NumericAttribute, extent.yMaximum()),
            ])
        writer.set_outputs([
            OperatorData(OperatorDataTypes.Grid),            
            OperatorData(OperatorDataTypes.Shapefile),
            ])
        writer.do_operation()
        
        # clean up intermediate data
        self._clean_layer(zone_data)  
        if skipTest:
            return writer.outputs
        
        self.assertTrue(os.path.exists(writer.outputs[1].value))
        
        # clean up
        self._clean_layer(writer.outputs)  
        
    def test_MakeGridFromRegion(self, skipTest=False):
        logging.debug('test_MakeGridFromRegion %s' % skipTest)
        
        zone_data = self.test_LoadZone(True, 2)
        
        writer = GridFromRegionWriter(self.operator_options)
        writer.set_inputs([
            zone_data[0],
            ])
        writer.set_outputs([
            OperatorData(OperatorDataTypes.Grid),            
            OperatorData(OperatorDataTypes.Shapefile),
            ])
        writer.do_operation()

        # clean up intermediate data
        self._clean_layer(zone_data)  
        if skipTest:
            return writer.outputs
        
        self.assertTrue(os.path.exists(writer.outputs[1].value))
        
        # clean up
        self._clean_layer(writer.outputs)  

    def test_MakeGridGeometry(self):        
        logging.debug('test_MakeGridGeometry %s')
        grid_data = self.test_MakeGrid(skipTest=True)
        
        writer = GridGeometryWriter(self.operator_options)
        writer.inputs = [grid_data[0]]
        writer.outputs = [
            OperatorData(OperatorDataTypes.Grid),   
            OperatorData(OperatorDataTypes.Shapefile)
        ]
        writer.do_operation()
        
        self._clean_layer(grid_data)
        self._clean_layer(writer.outputs)

    # testing merging zone and grids
    ############################
    
    def test_ZoneGridJoin(self, skipTest=False):
        logging.debug('test_ZoneGridJoin %s' % skipTest)
        
        zone_data = self.test_LoadZone2(True, 2)
        grid_data = self.test_MakeGridFromRegion(True)
        
        join = ZoneGridMerger(self.operator_options)
        join.inputs = [
            zone_data[0],
            OperatorData(OperatorDataTypes.StringAttribute, self.zone2_field),
            OperatorData(OperatorDataTypes.StringAttribute, self.zone2_bldgcount_field),
            grid_data[0],
        ]
        join.outputs = [
            OperatorData(OperatorDataTypes.Grid),   
            OperatorData(OperatorDataTypes.Shapefile),
        ]
        join.do_operation()

        # clean up intermediate data
        self._clean_layer(grid_data)
        self._clean_layer(zone_data)        
        if skipTest:
            return join.outputs
        
        self.assertTrue(os.path.exists(join.outputs[1].value))
        
        # cleanup        
        self._clean_layer(join.outputs)  
    
    def test_ZoneFootprintJoin(self, skipTest=False):
        logging.debug('test_ZoneFootprintJoin %s' % skipTest)
        
        zone_data = self.test_LoadZone(True, 1)
        fp_opdata = self.test_LoadFootprint(True)
        
        merger = ZoneFootprintMerger(self.operator_options)
        merger.inputs = [
            zone_data[0],
            OperatorData(OperatorDataTypes.StringAttribute, self.zone1_field),
            fp_opdata[0],
        ]
        merger.outputs = [
            OperatorData(OperatorDataTypes.Footprint),
            OperatorData(OperatorDataTypes.Shapefile)
        ]
        merger.do_operation()

        # clean up intermediate data
        self._clean_layer(fp_opdata)
        self._clean_layer(zone_data)

        if skipTest:
            return merger.outputs
        
        self.assertTrue(os.path.exists(merger.outputs[1].value))
        # cleanup        
        self._clean_layer(merger.outputs)  
        
    def test_ZoneFootprintCount(self, skipTest=False):
        logging.debug('test_ZoneFootprintJoin %s' % skipTest)
        
        zone_data = self.test_LoadZone(True, 1)
        fp_opdata = self.test_LoadFootprint(True)
        
        merger = ZoneFootprintCounter(self.operator_options)
        merger.inputs = [
            zone_data[0],
            OperatorData(OperatorDataTypes.StringAttribute, self.zone1_field),
            OperatorData(OperatorDataTypes.StringAttribute, 'BLDG_COUNT'),
            fp_opdata[0],
        ]
        merger.outputs = [
            OperatorData(OperatorDataTypes.Zone),
            OperatorData(OperatorDataTypes.Shapefile)
        ]
        merger.do_operation()

        # clean up intermediate data
        self._clean_layer(fp_opdata)
        self._clean_layer(zone_data)

        if skipTest:
            return merger.outputs
        
        self.assertTrue(os.path.exists(merger.outputs[1].value))
        # cleanup        
        self._clean_layer(merger.outputs)

    def test_ZoneToGridJoin(self, skipTest=False):
        logging.debug('test_ZoneFootprintJoin %s' % skipTest)
        
        # load data
        zone_data = self.test_LoadZone2(True, 2)
        
        # test 1
        merger = ZoneToGrid(self.operator_options)
        merger.inputs = [
            zone_data[0],
            OperatorData(OperatorDataTypes.StringAttribute, self.zone2_field),
            OperatorData(OperatorDataTypes.StringAttribute, self.zone2_bldgcount_field),
            OperatorData(OperatorDataTypes.StringAttribute, self.zone2_bldgarea_field),          
        ]
        merger.outputs = [
            OperatorData(OperatorDataTypes.Grid),
            OperatorData(OperatorDataTypes.Shapefile)
        ]
        merger.do_operation()

        if skipTest:
            # clean up intermediate data            
            self._clean_layer(zone_data)
            return merger.outputs
        
        self.assertTrue(os.path.exists(merger.outputs[1].value))
        cnt_idx = layer_field_index(merger.outputs[0].value, CNT_FIELD_NAME)
        area_idx = layer_field_index(merger.outputs[0].value, AREA_FIELD_NAME)
        total_cnt, total_sqmt = 0, 0
        for _f in layer_features(merger.outputs[0].value):
            cnt = _f.attributeMap()[cnt_idx].toDouble()[0]
            area = _f.attributeMap()[area_idx].toDouble()[0]
            total_cnt+= cnt
            total_sqmt+=area
        
        # sum(count)=292377  sum(sqmt)=71582303
        self.assertAlmostEqual(total_cnt, self.zone2_total_bldg_cnt, places=-2)
        self.assertAlmostEqual(total_sqmt, self.zone2_total_bldg_area, places=-2)

        # cleanup
        self._clean_layer(zone_data)
        self._clean_layer(merger.outputs)

    def test_ZoneFootprintToGridJoin(self, skipTest=False):
        logging.debug('test_ZoneFootprintJoin %s' % skipTest)
        
        # test 1
        # area from footprint
        zone_data = self.test_LoadZone2(True, 3)
        fp_opdata = self.test_LoadFootprintHT(skipTest=True)
        
        # test 1
        merger = FootprintZoneToGrid(self.operator_options)
        merger.inputs = [
            fp_opdata[0],
            zone_data[0],
            OperatorData(OperatorDataTypes.StringAttribute, self.zone3_field),
            OperatorData(OperatorDataTypes.StringAttribute, self.zone3_bldgcount_field),
            OperatorData(OperatorDataTypes.StringAttribute, self.zone3_bldgarea_field),            
        ]
        merger.outputs = [
            OperatorData(OperatorDataTypes.Grid),
            OperatorData(OperatorDataTypes.Shapefile)
        ]
        merger.do_operation()

        if skipTest:
            # clean up intermediate data
            self._clean_layer(fp_opdata)
            self._clean_layer(zone_data)
            return merger.outputs

        self.assertTrue(os.path.exists(merger.outputs[1].value))
        cnt_idx = layer_field_index(merger.outputs[0].value, CNT_FIELD_NAME)
        area_idx = layer_field_index(merger.outputs[0].value, AREA_FIELD_NAME)
        total_cnt, total_sqmt = 0, 0
        for _f in layer_features(merger.outputs[0].value):
            cnt = _f.attributeMap()[cnt_idx].toDouble()[0]
            area = _f.attributeMap()[area_idx].toDouble()[0]
            total_cnt+= cnt
            total_sqmt +=area 
        self.assertAlmostEqual(total_cnt, self.zone3_total_bldg_cnt, places=2)
        self.assertAlmostEqual(total_sqmt, self.fp3_total_area, places=-2)
        self._clean_layer(merger.outputs)
                
        # load data
        self._clean_layer(fp_opdata)
        fp_opdata = self.test_LoadFootprint(True, 3)
        
        # test 2
        # area from zone
        merger = FootprintZoneToGrid(self.operator_options)
        merger.inputs = [
            fp_opdata[0],
            zone_data[0],
            OperatorData(OperatorDataTypes.StringAttribute, self.zone3_field),
            OperatorData(OperatorDataTypes.StringAttribute, self.zone3_bldgcount_field),
            OperatorData(OperatorDataTypes.StringAttribute, self.zone3_bldgarea_field),            
        ]
        merger.outputs = [
            OperatorData(OperatorDataTypes.Grid),
            OperatorData(OperatorDataTypes.Shapefile)
        ]
        merger.do_operation()
        
        self.assertTrue(os.path.exists(merger.outputs[1].value))
        cnt_idx = layer_field_index(merger.outputs[0].value, CNT_FIELD_NAME)
        area_idx = layer_field_index(merger.outputs[0].value, AREA_FIELD_NAME)
        total_cnt, total_sqmt = 0, 0
        for _f in layer_features(merger.outputs[0].value):
            cnt = _f.attributeMap()[cnt_idx].toDouble()[0]
            area = _f.attributeMap()[area_idx].toDouble()[0]
            total_cnt+= cnt
            total_sqmt +=area 
        self.assertAlmostEqual(total_cnt, self.zone3_total_bldg_cnt, places=2)
        self.assertAlmostEqual(total_sqmt, self.zone3_total_bldg_area, places=-2)
        self._clean_layer(merger.outputs)

        # test 3
        # no area    
        merger = FootprintZoneToGrid(self.operator_options)
        merger.inputs = [
            fp_opdata[0],
            zone_data[0],
            OperatorData(OperatorDataTypes.StringAttribute, self.zone3_field),
            OperatorData(OperatorDataTypes.StringAttribute),
            OperatorData(OperatorDataTypes.StringAttribute),
        ]
        merger.outputs = [
            OperatorData(OperatorDataTypes.Grid),
            OperatorData(OperatorDataTypes.Shapefile)
        ]
        merger.do_operation()
        self.assertTrue(os.path.exists(merger.outputs[1].value))
        cnt_idx = layer_field_index(merger.outputs[0].value, CNT_FIELD_NAME)
        total_cnt = 0
        for _f in layer_features(merger.outputs[0].value):
            cnt = _f.attributeMap()[cnt_idx].toDouble()[0]
            total_cnt+= cnt
        self.assertAlmostEqual(total_cnt, self.fp3_feature_count, places=2)
        
        # cleanup
        self._clean_layer(fp_opdata)
        self._clean_layer(zone_data)
        self._clean_layer(merger.outputs)

    # test mapping scheme creator
    ##################################
    
    def test_CreateEmptyMSCreator(self, skipTest=False):
        logging.debug('test_CreateEmptyMSCreator %s' % skipTest)
        
        ms_creator = EmptyMSCreator(self.operator_options)
        ms_creator.set_inputs([])
        ms_creator.set_outputs([
            OperatorData(OperatorDataTypes.MappingScheme)
        ])
        ms_creator.do_operation()
        
        if skipTest:
            return ms_creator.outputs
        
        self.assertEquals(type(ms_creator.outputs[0].value), MappingScheme)
        
        # no cleanup needed, MappingSchemeLoader does not create tmp files

    def test_CreateEmptyZonesMSCreator(self, skipTest=False):
        logging.debug('test_CreateEmptyZonesMSCreator %s' % skipTest)
        
        zone_data = self.test_LoadZone(True)

        ms_creator = EmptyZonesMSCreator(self.operator_options)
        ms_creator.set_inputs([            
            zone_data[0],
            OperatorData(OperatorDataTypes.StringAttribute, self.zone1_field),
        ])
        ms_creator.set_outputs([
            OperatorData(OperatorDataTypes.MappingScheme)
        ])
        ms_creator.do_operation()
        
        # clean up intermediate data
        self._clean_layer(zone_data)
        
        if skipTest:
            return ms_creator.outputs        
        self.assertEquals(type(ms_creator.outputs[0].value), MappingScheme)   

        
    def test_CreateMSFromSurveyZone(self, skipTest=False):
        logging.debug('test_CreateMSFromSurveyZone %s' % skipTest)
        
        zone_data = self.test_LoadZone(True, 3)
        svy_opdata = self.test_LoadGEMDBSurvey(True)
        
        ms_creator = SurveyZonesMSCreator(self.operator_options)
        ms_creator.set_inputs([
            svy_opdata[0],
            zone_data[0],
            OperatorData(OperatorDataTypes.StringAttribute, self.zone1_field),
        ])
        ms_creator.set_outputs([
            OperatorData(OperatorDataTypes.MappingScheme)
        ])
        ms_creator.do_operation()

        # clean up intermediate data
        self._clean_layer(zone_data)
        self._clean_layer(svy_opdata)

        if skipTest:
            return ms_creator.outputs        
        self.assertEquals(type(ms_creator.outputs[0].value), MappingScheme)        

    def test_CreateMSFromSurveyOnly(self, skipTest=False):
        logging.debug('test_CreateMSFromSurveyZone %s' % skipTest)
        
        svy_opdata = self.test_LoadGEMDBSurvey(True)
        ms_creator = SurveyOnlyMSCreator(self.operator_options)
        ms_creator.set_inputs([
            svy_opdata[0],
        ])
        ms_creator.set_outputs([
            OperatorData(OperatorDataTypes.MappingScheme)
        ])
        ms_creator.do_operation()

        # clean up intermediate data
        self._clean_layer(svy_opdata)
        if skipTest:
            return ms_creator.outputs           
        self.assertEquals(type(ms_creator.outputs[0].value), MappingScheme)

    # testing footprint aggregator
    ############################        

    def test_FPAggregator(self, skipTest=False):
        logging.debug('test_FPAggregator %s' % skipTest)
        
        fp_data = self.test_ZoneFootprintJoin(True)
        
        fp_agg = FootprintAggregator(self.operator_options)
        fp_agg.inputs = [
            fp_data[0],
            OperatorData(OperatorDataTypes.StringAttribute, self.zone1_field),
        ]
        fp_agg.outputs = [
            OperatorData(OperatorDataTypes.Grid),
            OperatorData(OperatorDataTypes.Shapefile),
        ]        
        fp_agg.do_operation()
        
        # clean up intermediate data        
        self._clean_layer(fp_data)
        
        if skipTest:
            return fp_agg.outputs
        self.assertTrue(os.path.exists(fp_agg.outputs[1].value))

        # cleanup
        self._clean_layer(fp_agg.outputs)

    # testing apply MS on zone
    ############################        

    def test_ApplyMS(self):
        logging.debug('test_ApplyMS')
        
        # load zone with count
        zone_data = self.test_LoadZone2(True, 2)
        
        # load ms
        ms_opdata = self.test_LoadMS(True)
        
        # apply mapping scheme        
        ms_applier = ZoneMSApplier(self.operator_options)
        
        ms_applier.inputs = [
            zone_data[0],
            OperatorData(OperatorDataTypes.StringAttribute, self.zone2_field),
            OperatorData(OperatorDataTypes.StringAttribute, self.zone2_bldgcount_field),
            ms_opdata[0],
        ]
        ms_applier.outputs = [
            OperatorData(OperatorDataTypes.Exposure),
            OperatorData(OperatorDataTypes.Shapefile),
        ]
        ms_applier.do_operation()
        self.assertTrue(os.path.exists(ms_applier.outputs[1].value))
        
        # cleanup
        self._clean_layer(zone_data)
        self._clean_layer(ms_applier.outputs)        
        del ms_applier
        
        # testing apply MS on grid
        ############################
        
        ms_applier = GridMSApplier(self.operator_options)
        ms_applier.inputs = [
            OperatorData(OperatorDataTypes.Grid, load_shapefile(self.grid2_path, 'test_input_grid')),            
            OperatorData(OperatorDataTypes.StringAttribute, self.zone2_field),
            OperatorData(OperatorDataTypes.StringAttribute, self.zone2_bldgcount_field),
            ms_opdata[0],
        ]
        ms_applier.outputs = [
            OperatorData(OperatorDataTypes.Exposure),
            OperatorData(OperatorDataTypes.Shapefile),
        ]
        ms_applier.do_operation()
        self.assertTrue(os.path.exists(ms_applier.outputs[1].value))
        
        # cleanup
        self._clean_layer(ms_applier.outputs)
        del ms_applier
        

    def test_SurveyAggregate(self):
        logging.debug('test_SurveyAggregate')
        
        svy_data = self.test_LoadGEMDBSurvey(True)
        svy_agg = SurveyAggregator(self.operator_options)
        svy_agg.inputs = [
            svy_data[0]
        ]
        svy_agg.outputs = [
            OperatorData(OperatorDataTypes.Exposure),
            OperatorData(OperatorDataTypes.Shapefile),
        ]
        svy_agg.do_operation()
        self.assertTrue(os.path.exists(svy_agg.outputs[1].value))        
        # cleanup
        self._clean_layer(svy_data)
        self._clean_layer(svy_agg.outputs)

    def test_VerifyExposure(self):
        logging.debug('test_VerifyExposure')

        exposure_path = self.test_data_dir + 'exposure3.shp'
        exposure = load_shapefile(exposure_path, 'exposure3')
        exposure_opdata = OperatorData(OperatorDataTypes.Exposure, exposure)

        fp_path = self.test_data_dir +  'footprints3.shp'
        fp = load_shapefile(fp_path, 'fp3')
        fp_opdata = OperatorData(OperatorDataTypes.Footprint, fp)

        # check fragmentation
        report = OperatorData(OperatorDataTypes.Report)
        
        frag_analyzer = ExposureFragmentationAnalyzer(self.operator_options)
        frag_analyzer.inputs = [exposure_opdata]
        frag_analyzer.outputs = [report]
        frag_analyzer.do_operation()
        #print report.value
        self.assertEquals(report.value['fraction_count'], 0)
        
        fp_cnt_analyzer = ExposureFootprintCountAnalyzer(self.operator_options)
        fp_cnt_analyzer.inputs = [exposure_opdata, fp_opdata]
        fp_cnt_analyzer.outputs = [report]
        fp_cnt_analyzer.do_operation()
        #print report.value
        self.assertEquals(report.value['total_source'], report.value['total_exposure'])
        
        exposure_path = self.test_data_dir + 'exposure2.shp'
        exposure = load_shapefile(exposure_path, 'exposure2')
        exposure_opdata = OperatorData(OperatorDataTypes.Exposure, exposure)
                
        zone_path = self.test_data_dir +  'zones2.shp'
        zone = load_shapefile(zone_path, 'zones2')
        zone_opdata = OperatorData(OperatorDataTypes.Zone, zone)
        
        zone_cnt_analyzer = ExposureZoneCountAnalyzer(self.operator_options)
        zone_cnt_analyzer.inputs = [exposure_opdata,
                                    zone_opdata,
                                    OperatorData(OperatorDataTypes.StringAttribute, self.zone2_bldgcount_field)]
        zone_cnt_analyzer.outputs = [report]
        zone_cnt_analyzer.do_operation()
        #print report.value
        self.assertEquals(report.value['total_source'], report.value['total_exposure'])
    
    def test_ZonePopGridJoin(self):
        # 1 attach population counts to zones (convert to building count in process)
        ###################################        
        
        pop_grid = self.test_LoadPopGrid(skipTest=True)
        zone = self.test_LoadZone(skipTest=True, zone=4)

        grid_writer = ZonePopgridCounter(self.operator_options)
        grid_writer.inputs = [zone[0],
                              OperatorData(OperatorDataTypes.StringAttribute, self.popgrid_zone_field),                              
                              pop_grid[0],
                              OperatorData(OperatorDataTypes.NumericAttribute, 10)]                         
                    
        grid_writer.outputs = [OperatorData(OperatorDataTypes.Zone),
                               OperatorData(OperatorDataTypes.Shapefile),]        
        grid_writer.do_operation()
                
        grid_writer = PopgridZoneToGrid(self.operator_options)
        grid_writer.inputs = [pop_grid[0],
                              zone[0],
                              OperatorData(OperatorDataTypes.StringAttribute, self.popgrid_zone_field),                              
                              OperatorData(OperatorDataTypes.NumericAttribute, 10)]                         
                    
        grid_writer.outputs = [OperatorData(OperatorDataTypes.Grid),
                               OperatorData(OperatorDataTypes.Shapefile),]        
        grid_writer.do_operation()

            
    def _clean_layer(self, output):
        del output[0].value
        remove_shapefile(output[1].value)


    