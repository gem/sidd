# Copyright (c) 2011-2013, ImageCat Inc.
#
# SIDD is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
#
"""
GEM implementation specific
"""
HALF_CELL=0.00416666666666667 # 1/240.0
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
    return int(round( (lon-HALF_CELL)*120, 0)) << 16 | int(round( (lat-HALF_CELL)*120, 0)) & 65535

def grid_to_latlon(grid_id):
    """
    algorithm by Paul Henshaw 
    reverse of latlon_to_grid function
    
    CREATE OR REPLACE FUNCTION paul.to_lat_lon(grid_id integer)
      RETURNS record AS
    $BODY$
    DECLARE
            rec RECORD;
    BEGIN
            SELECT INTO rec (( grid_id & 65535) + 0.5 )/ 120.0 AS lat, (( (grid_id >>16) ) + 0.5 ) / 120.0 AS lon;
            RETURN rec;
    END
    $BODY$
    """
    lon_id = grid_id >>16
    lat_id = grid_id & 65535

    if lat_id < 65535/2:
        lat = (lat_id + 0.5)/ 120.0
    else:
        lat = -((65535 - lat_id + 0.5) / 120.0) 
    
    if lon_id < 65535/2:
        lon = (lon_id + 0.5) / 120.0
    else:
        lon = -((65535 - lon_id + 0.5) / 120.0)
    return lat, lon
