# Copyright (c) 2011-2013, ImageCat Inc.
#
# SIDD is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
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
            
        
        