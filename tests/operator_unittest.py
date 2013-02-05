#
# SeismiCat: an on-line seismic risk assessment tool for 
# building property owners, lenders, insurers and municipal analysts. 
# 
# @copyright  (c)2012 ImageCat inc, All rights reserved
# @link       http://www.seismicat.com
# @since      SeismiCat v1.0
# @license    
# @version    $Id: operator_unittest.py 21 2012-10-26 01:48:25Z zh $
#

import os
import unittest
import logging

# import sidd packages for testing
from sidd.ms import MappingScheme
from sidd.operator import *
from utils.shapefile import remove_shapefile, layer_fields_stats, load_shapefile

class OperatorTestCase(unittest.TestCase):
    
    # run for every test
    ##################################
    
    def setUp(self):
        from sidd.taxonomy import get_taxonomy
        self.taxonomy = get_taxonomy("gem")
        self.test_data_dir = str(os.getcwd()) +  "/tests/data/"
        self.test_tmp_dir = str(os.getcwd()) +  "/tests/tmp/"
        self.ms_file = self.test_data_dir +  "ms.xml"
        self.fp_path = self.test_data_dir +  'footprint.shp'
        self.fp_feature_count = 1475
        self.survey_path = self.test_data_dir +  "survey.csv"
        self.gemdb_path = self.test_data_dir +  "survey.gemdb"
        self.zone_path = self.test_data_dir +  "zones.shp"
        self.zone_field = 'LandUse'
        self.zone_bldg_count = 546
        self.bldgcount_field = 'NumBldg'

        self.zone2_path = self.test_data_dir +  "zones2.shp"
        self.zone2_field = "ZONE"
        self.grid_path = self.test_data_dir +  "grid.shp"
        self.grid2_path = self.test_data_dir +  "grid2.shp"
        
        self.operator_options = {
            'tmp_dir': self.test_tmp_dir,
            'taxonomy':'gem',
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

    def test_LoadFootprint(self, skipTest=False):
        logging.debug('test_LoadFootprint %s' % skipTest)
        
        loader = FootprintLoader(self.operator_options)
        loader.inputs = [
            OperatorData(OperatorDataTypes.Shapefile, self.fp_path),
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
        
        if zone== 1:
            zone_path = self.zone_path
            zone_field = self.zone_field
        else:
            zone_path = self.zone2_path
            zone_field = self.zone2_field
        
        loader = ZoneLoader(self.operator_options)
        loader.inputs = [
            OperatorData(OperatorDataTypes.Shapefile, zone_path),
            OperatorData(OperatorDataTypes.StringAttribute, zone_field),
            #OperatorData(OperatorDataTypes.StringAttribute, self.bldgcount_field),
        ]
        loader.outputs = [
            OperatorData(OperatorDataTypes.Zone),
            OperatorData(OperatorDataTypes.Shapefile)
        ]        
        loader.do_operation()
        
        if skipTest:
            return loader.outputs  

        zones = loader.outputs[0].value
        self.assertEquals(zones.featureCount(), self.zone_bldg_count)        

        classes = layer_fields_stats(zones, self.zone_field)
        _total = 0
        for _k, _v in classes.iteritems():
            _total+=_v
        self.assertEquals(_total, self.zone_bldg_count)
        
        # clean up
        del zones
        self._clean_layer(loader.outputs)  

    
    def test_LoadZoneCount(self, skipTest=False):
        logging.debug('test_LoadZoneCount %s' % skipTest)
        
        loader = ZoneCountLoader(self.operator_options)
        loader.inputs = [
            OperatorData(OperatorDataTypes.Shapefile, self.zone_path),
            OperatorData(OperatorDataTypes.StringAttribute, self.zone_field),
            OperatorData(OperatorDataTypes.StringAttribute, self.bldgcount_field),
        ]
        loader.outputs = [
            OperatorData(OperatorDataTypes.Zone),
            OperatorData(OperatorDataTypes.Shapefile)
        ]        
        loader.do_operation()        
        if skipTest:
            return loader.outputs
        
        zones = loader.outputs[0].value
        self.assertEquals(zones.featureCount(), self.zone_bldg_count)

        classes = layer_fields_stats(zones, self.zone_field)
        _total = 0
        for _k, _v in classes.iteritems():
            _total+=_v
        self.assertEquals(_total, self.zone_bldg_count)
        
        # clean up
        del zones
        self._clean_layer(loader.outputs)  
    
    def test_LoadSurvey(self, skipTest=False):   
        logging.debug('test_LoadSurvey %s' % skipTest)
        
        loader = CSVSurveyLoader(self.operator_options)
        loader.inputs = [
            OperatorData(OperatorDataTypes.File, self.survey_path),
            OperatorData(OperatorDataTypes.StringAttribute, 'CSV'),            
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

    def test_LoadGEMDBSurvey(self, skipTest=False):   
        logging.debug('test_LoadSurvey %s' % skipTest)
        
        loader = GEMDBSurveyLoader(self.operator_options)
        loader.inputs = [
            OperatorData(OperatorDataTypes.File, self.gemdb_path),
            OperatorData(OperatorDataTypes.StringAttribute, 'CSV'),            
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
        
        zone_data = self.test_LoadZone(True)
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
        
        zone_data = self.test_LoadZone(True)
        
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

    # testing merging zone and grids
    ############################
    
    def test_ZoneGridJoin(self, skipTest=False):
        logging.debug('test_ZoneGridJoin %s' % skipTest)
        
        zone_data = self.test_LoadZoneCount(True)
        grid_data = self.test_MakeGridFromRegion(True)
        
        join = ZoneGridMerger(self.operator_options)
        join.inputs = [
            zone_data[0],
            OperatorData(OperatorDataTypes.StringAttribute, self.zone_field),
            OperatorData(OperatorDataTypes.StringAttribute, self.bldgcount_field),
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
        
        zone_data = self.test_LoadZone(True, 2)
        fp_opdata = self.test_LoadFootprint(True)
        
        merger = ZoneFootprintMerger(self.operator_options)
        merger.inputs = [
            zone_data[0],
            OperatorData(OperatorDataTypes.StringAttribute, self.zone2_field),
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
        
        zone_data = self.test_LoadZone(True, 2)
        fp_opdata = self.test_LoadFootprint(True)
        
        merger = ZoneFootprintCounter(self.operator_options)
        merger.inputs = [
            zone_data[0],
            OperatorData(OperatorDataTypes.StringAttribute, self.zone2_field),
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
            OperatorData(OperatorDataTypes.StringAttribute, self.zone_field),
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
        
        zone_data = self.test_LoadZone(True)
        svy_opdata = self.test_LoadSurvey(True)
        
        ms_creator = SurveyZonesMSCreator(self.operator_options)
        ms_creator.set_inputs([
            svy_opdata[0],
            zone_data[0],
            OperatorData(OperatorDataTypes.StringAttribute, self.zone_field),
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
        
        svy_opdata = self.test_LoadSurvey(True)
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
            OperatorData(OperatorDataTypes.StringAttribute, self.zone2_field),
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
        zone_data = self.test_LoadZoneCount(True)
        
        # load ms
        ms_opdata = self.test_LoadMS(True)
        
        # apply mapping scheme        
        ms_applier = ZoneMSApplier(self.operator_options)
        
        ms_applier.inputs = [
            zone_data[0],
            OperatorData(OperatorDataTypes.StringAttribute, self.zone_field),
            OperatorData(OperatorDataTypes.StringAttribute, self.bldgcount_field),
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
            OperatorData(OperatorDataTypes.StringAttribute, self.zone_field),
            OperatorData(OperatorDataTypes.StringAttribute, self.bldgcount_field),
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
        
        svy_data = self.test_LoadSurvey(True)
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

    def _clean_layer(self, output):
        del output[0].value
        remove_shapefile(output[1].value)

