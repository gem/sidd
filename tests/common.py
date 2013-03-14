# SeismiCat: an on-line seismic risk assessment tool for 
# building property owners, lenders, insurers and municipal analysts. 
# @copyright  (c)2012 ImageCat inc, All rights reserved
# @link       http://www.seismicat.com
# @since      SeismiCat v1.0
# @license    
# @version    $Id: run_tests.py 18 2012-10-24 20:21:41Z zh $
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
        