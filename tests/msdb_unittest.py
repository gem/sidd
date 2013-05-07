# Copyright (c) 2011-2013, ImageCat Inc.
#
# SIDD is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
#
import os
import shutil

# import sidd packages for testing
from ui.helper.msdb_dao import MSDatabaseDAO
from common import SIDDTestCase

class MSDBTestCase(SIDDTestCase):

    # run for every test
    ##################################    
    def setUp(self):
        super(MSDBTestCase, self).setUp()
        self.lib_ms_file = self.test_data_dir + '/mslib.db'
        self.lib_ms_file2 = self.test_tmp_dir + '/mslib2.db'
    
    def test_Read(self):
        ms_db_reader = MSDatabaseDAO(self.lib_ms_file)
        regions = ms_db_reader.get_regions()
        self.assertEquals(len(regions), 2)
        
        types = ms_db_reader.get_types_in_region(regions[1])
        self.assertEquals(len(types), 1)
        ms_names = ms_db_reader.get_ms_in_region_type(regions[1], types[0])
        self.assertEquals(len(ms_names), 8)
        
    def test_SaveDelete(self):
        if os.path.exists(self.lib_ms_file2):
            os.remove(self.lib_ms_file2)
        shutil.copyfile(self.lib_ms_file, self.lib_ms_file2)
        ms_db_reader = MSDatabaseDAO(self.lib_ms_file2)
        
        region = 'REGION'
        ms_name = 'NAME'
        source = 'SOURCE'
        date_created = 'DATE CREATED'
        datasource = 'DATASOURCE'
        quality = 'QUALITY'
        notes = 'NOTES'
        ms_xml = 'MS_XML'
        ms_db_reader.save_ms(region, ms_name, source, date_created, datasource, quality, notes, ms_xml)
        
        regions = ms_db_reader.get_regions()
        self.assertEquals(len(regions), 3)        
        types = ms_db_reader.get_types_in_region(region)
        self.assertEquals(len(types), 1)
        ms_names = ms_db_reader.get_ms_in_region_type(region, source)
        self.assertEquals(len(ms_names), 1)
        [_date_created, _data_source, _quality, _use_notes, _ms_xml] = ms_db_reader.get_ms(region, source, ms_name)
        self.assertEqual(date_created, _date_created)
        self.assertEqual(datasource, _data_source)
        self.assertEqual(quality, _quality)
        self.assertEqual(notes, _use_notes)
        self.assertEqual(ms_xml, _ms_xml)
    
        ms_db_reader.delete_ms(region, source, ms_name)

        regions = ms_db_reader.get_regions()
        self.assertEquals(len(regions), 2)        
        types = ms_db_reader.get_types_in_region(region)
        self.assertEquals(len(types), 0)
        
        del ms_db_reader
        os.remove(self.lib_ms_file2)
                
        
        
