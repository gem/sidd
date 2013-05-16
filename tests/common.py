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
import os
import shutil
import unittest

class SIDDTestCase(unittest.TestCase):
    required_dirs = ['tests/tmp']
    def setUp(self):
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
        