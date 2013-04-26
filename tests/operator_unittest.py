# Copyright (c) 2011-2013, ImageCat Inc.
#
# SIDD is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
#
import os
import logging

# import sidd packages for testing
from sidd.ms import MappingScheme
from sidd.operator import *
from utils.shapefile import remove_shapefile, layer_fields_stats, load_shapefile, layer_features, layer_field_index
from sidd.constants import AREA_FIELD_NAME, HT_FIELD_NAME, CNT_FIELD_NAME

from common import SIDDTestCase

class OperatorTestCase(SIDDTestCase):
    
    # run for every test
    ##################################
    
    def setUp(self):
        super(OperatorTestCase, self).setUp()
        
        # test data set 1        
        self.ms_file = self.test_data_dir +  "ms.xml"
        self.fp_path = self.test_data_dir +  'footprint.shp'
        self.fp_feature_count = 1475
        self.zone1_path = self.test_data_dir +  "zones1.shp"
        self.zone1_field = "ZONE"

        # test data set 2
        self.zone2_path = self.test_data_dir +  "zones2.shp"
        self.zone2_field = 'LandUse'
        self.zone2_bldg_count = 546
        self.zone2_bldgcount_field = 'NumBldg'

        # test data set 3
        self.fp3_path = self.test_data_dir +  "footprints3.shp"
        self.fp3_height_field = "HEIGHT"
        self.gemdb3_path = self.test_data_dir +  "survey3.gemdb"
        self.zone3_path = self.test_data_dir +  "zones3.shp"
        self.zone3_field = "ZONE"
        self.zone3_bldgcount_field = 'NumBldgs'
        
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
        self.assertEquals(self.fp_feature_count, layer.dataProvider().featureCount())        
        
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
        else:
            zone_path = self.zone3_path
            zone_field = self.zone3_field
        
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
        elif zone==3: 
            zone_path = self.zone3_path
            zone_field = self.zone3_field
            zone_count_field = self.zone3_bldgcount_field
        else:
            raise Exception("zone not supported")
        
        loader = ZoneCountLoader(self.operator_options)
        loader.inputs = [
            OperatorData(OperatorDataTypes.Shapefile, zone_path),
            OperatorData(OperatorDataTypes.StringAttribute, zone_field),
            OperatorData(OperatorDataTypes.StringAttribute, zone_count_field),
        ]
        loader.outputs = [
            OperatorData(OperatorDataTypes.Zone),
            OperatorData(OperatorDataTypes.Shapefile)
        ]        
        loader.do_operation()
        if skipTest:
            return loader.outputs
        
        zones = loader.outputs[0].value
        self.assertEquals(zones.featureCount(), self.zone2_bldg_count)

        classes = layer_fields_stats(zones, self.zone2_field)
        _total = 0
        for _k, _v in classes.iteritems():
            _total+=_v
        self.assertEquals(_total, self.zone2_bldg_count)
        
        # clean up
        del zones
        self._clean_layer(loader.outputs)  
    
    def test_LoadGEMDBSurvey(self, skipTest=False):   
        logging.debug('test_LoadSurvey %s' % skipTest)
        
        loader = GEMDBSurveyLoader(self.operator_options)
        loader.inputs = [
            OperatorData(OperatorDataTypes.File, self.gemdb3_path),
            OperatorData(OperatorDataTypes.StringAttribute, 'GEMDB'),            
        ]
        loader.outputs = [
            OperatorData(OperatorDataTypes.Survey),
            OperatorData(OperatorDataTypes.Shapefile),
        ]
        loader.do_operation()
        if skipTest:
            return loader.outputs
        
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
        total_cnt = 0
        for _f in layer_features(merger.outputs[0].value):
            cnt = _f.attributeMap()[cnt_idx].toDouble()[0]
            total_cnt+= cnt
        self.assertAlmostEqual(total_cnt, 292400, places=-2)
        
        # cleanup
        self._clean_layer(zone_data)
        self._clean_layer(merger.outputs)

    def test_ZoneFootprintToGridJoin(self, skipTest=False):
        logging.debug('test_ZoneFootprintJoin %s' % skipTest)
        
        # load data
        zone_data = self.test_LoadZone2(True, 3)
        fp_opdata = self.test_LoadFootprint(True, 3)
        
        # test 1
        merger = FootprintZoneToGrid(self.operator_options)
        merger.inputs = [
            fp_opdata[0],
            zone_data[0],
            OperatorData(OperatorDataTypes.StringAttribute, self.zone3_field),
            OperatorData(OperatorDataTypes.StringAttribute, self.zone3_bldgcount_field),            
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
        total_cnt = 0
        for _f in layer_features(merger.outputs[0].value):
            cnt = _f.attributeMap()[cnt_idx].toDouble()[0]
            total_cnt+= cnt
        self.assertAlmostEqual(total_cnt, 850, places=2)
        self._clean_layer(merger.outputs)

        # test 2        
        merger = FootprintZoneToGrid(self.operator_options)
        merger.inputs = [
            fp_opdata[0],
            zone_data[0],
            OperatorData(OperatorDataTypes.StringAttribute, self.zone3_field),
            OperatorData(OperatorDataTypes.StringAttribute, ''),            
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
        self.assertAlmostEqual(total_cnt, 785, places=2)
        
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
    
    
    def _clean_layer(self, output):
        del output[0].value
        remove_shapefile(output[1].value)


    