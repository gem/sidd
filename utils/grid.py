# Copyright (c) 2011-2013, ImageCat Inc.
#
# SIDD is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
#
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