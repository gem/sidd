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

# import sidd packages for testing
from common import SIDDTestCase

class UtilsTestCase(SIDDTestCase):
    
    # run for every test
    ##################################    
    def setUp(self):
        super(UtilsTestCase, self).setUp()
        
    def test_Grid(self):
        from utils.grid import latlon_to_grid, grid_to_latlon
        lats = [  33.995833,  -5.6625,    -3.1375,    6.12083]
        lons = [-112.004167, 106.104167, -12.412541, 85.22916]
        for lat, lon in map(None, lats, lons):     
            grid = latlon_to_grid(lat, lon)
            lat2, lon2 = grid_to_latlon(grid)
            self.assertAlmostEqual(lat, lat2, places=4)
            self.assertAlmostEqual(lon, lon2, places=4)
            
        
        