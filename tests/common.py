# Copyright (c) 2011-2013, ImageCat Inc.
#
# SIDD is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
#
import os
import shutil
import unittest

from sidd.taxonomy import get_taxonomy

class SIDDTestCase(unittest.TestCase):
    required_dirs = ['tests/tmp']
    def setUp(self):
        self.taxonomy = get_taxonomy("gem")        
        self.test_data_dir = str(os.getcwd()) +  "/tests/data/"
        self.test_tmp_dir = str(os.getcwd()) +  "/tests/tmp/"
        
    @classmethod
    def setUpClass(cls):
        for dir_path in SIDDTestCase.required_dirs:
            if not os.path.exists(dir_path):
                os.mkdir(dir_path)

    @classmethod
    def tearDownClass(cls):
        for dir_path in SIDDTestCase.required_dirs:
            try:
                shutil.rmtree(dir_path)
            except Exception as err:
                print "Error removing path %s: %s" % (dir_path, err)
        