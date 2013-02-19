# Copyright (c) 2011-2012, ImageCat Inc.
#
# SIDD is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License version 3
# only, as published by the Free Software Foundation.
#
# SIDD is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License version 3 for more details
# (a copy is included in the LICENSE file that accompanied this code).
#
# You should have received a copy of the GNU Lesser General Public License
# version 3 along with SIDD.  If not, see
# <http://www.gnu.org/licenses/lgpl-3.0.txt> for a copy of the LGPLv3 License.
#
# Version: $Id: shapefile.py 21 2012-10-26 01:48:25Z zh $

"""
GEM implementation specific
"""

def latlon_to_grid(lat, lon):
    """
    algorithm by Paul Henshaw 
    create a unique ID based on given lat/lon that conforms to the GED 30 arc-second grid
    
    A fixed size, evenly spaced 30-arc-second grid covering the world has 
        (360 * 60 * 2) x (180 * 6 * 20) = 43200 x 21600 
    cells. Since both 43200 and 21600 are less than 2^16, it is possible to use a 32bit 
    integer id (as with the current scheme) for all possible cells.

      id = (x << 16) | y
    Where:
        x = lon - half_cell * 60 * 2; 
        y = lat - half_cell * 60 * 2; 
        half_cell = half the size of a cell in degrees = 1/240 =~ 0.00416666666666667 
        i << j means a bitwise left shift i by the j bits 
        | means bitwise or (equivalent to +) 
    The "- half_cell operation" is intended to place the lat lon of a cell in the center 
    of the cell (as opposed to the corner)
    
    original PostgreSQL function

    CREATE OR REPLACE FUNCTION
      paul.to_grid_id(lat double precision, lon double precision)
      RETURNS integer AS $$
    BEGIN
      RETURN
        ( ( round( (lon - 0.00416666666666667) * 120 )::integer) << 16 ) |
        ( ( round( (lat - 0.00416666666666667) * 120 )::integer & 65535 ) );
    END
    $$ LANGUAGE plpgsql;
    """
    HALF_CELL=0.00416666666666667 # 1/240.0
    return int(round( (lon-HALF_CELL)*120, 0)) << 16 | int(round( (lat-HALF_CELL)*120, 0)) & 65535