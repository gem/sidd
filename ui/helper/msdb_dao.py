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
"""
module supports reading mapping scheme library SQLite database
"""
import sqlite3

from ui.constants import logUICall

class MSDatabaseDAO:
    """
    supports reading mapping scheme library SQLite database
    """

    # SQL used to query db
    sql = {        
        'GET_REGIONS':"""select distinct region from mapping_scheme order by region """,
        'GET_TYPES':"""select distinct source from mapping_scheme where region=? order by source""",
        'GET_MSNAME':"""select ms_name from mapping_scheme where region=? and source=? order by ms_name""",
        'GET_MS':"""select date_created, data_source, quality, use_notes, ms_xml from mapping_scheme where region=? and source=? and ms_name=?""",
        'GET_MAX_MS_ID':"""select max(id) from mapping_scheme""",
        'INSERT_MS':"""
        insert into mapping_scheme (id, region, ms_name, source, date_created, data_source, quality, use_notes, ms_xml, taxonomy)
        values (?, ?, ?, ?, ?, ?, ?, ?, ?, 'GEM')
        """,
        'DELETE_MS':"""delete from mapping_scheme where region=? and source=? and ms_name=?""",
    }
    
    def __init__(self, dbpath):
        """ initialize """
        try:
            logUICall.log('opening ms db file %s ' % (dbpath), logUICall.INFO)
            self.conn = sqlite3.connect(dbpath)
            self.initialized = True
        except:
            self.initialized = False
    
    def close(self):
        if self.initialized:
            self.conn.close()
    
    def get_regions(self):
        logUICall.log('get_regions', logUICall.DEBUG_L2)
        undefined_region = 'Undefined-Region'
        if not self.initialized:
            return []
        else:
            regions = self._get_list( self.sql['GET_REGIONS'] )
            # add undefined region to allow user to store 
            # mapping schemes not associated with any region
            try:
                regions.remove(undefined_region)                
            except:
                pass
            regions.insert(0, undefined_region)
            return regions
        
    def get_types_in_region(self, region):
        logUICall.log('get_types_in_region %s' % region, logUICall.DEBUG_L2)
        if not self.initialized:
            return []
        else:
            return self._get_list( self.sql['GET_TYPES'], [region] )
    
    def get_ms_in_region_type(self, region, ms_type):
        logUICall.log('get_ms_in_region_type %s %s' % (region, ms_type), logUICall.DEBUG_L2)
        if not self.initialized:
            return []
        else:
            return self._get_list( self.sql['GET_MSNAME'], [region, ms_type])
    
    def get_ms(self, region, ms_type, ms_name):
        logUICall.log('get_ms %s %s %s' % (region, ms_type, ms_name), logUICall.DEBUG_L2)        
        if not self.initialized:
            return []
        else:
            return self._get_list( self.sql['GET_MS'], [region, ms_type, ms_name], first_column=False)[0]
    
    def save_ms(self, region, ms_name, source, date, datasource, quality, notes, ms_xml):
        logUICall.log('get_ms %s %s %s %s %s %s %s %s' % (region, ms_name, source,
                                                          date, datasource, quality,
                                                          notes, ms_xml[0:20]), 
                      logUICall.DEBUG_L2)
        _id = int(self._get_list(self.sql['GET_MAX_MS_ID'])[0]) + 1
        return self._exec(self.sql['INSERT_MS'], [_id, region, ms_name,
                                                   source, date, datasource,
                                                   quality, notes, ms_xml], True)
     
    
    def delete_ms(self, region, ms_type, ms_name):
        return self._exec(self.sql['DELETE_MS'], [region, ms_type, ms_name], True)
    
    def _get_list(self, sql, param=[], first_column=True):
        results = []
        try:
            c = self.conn.cursor()                        
            c.execute(sql, param)            
            for row in c:     
                if first_column:
                    results.append(row[0])
                else:
                    results.append(row)
            c.close()
        except Exception as e:
            logUICall.log(e, logUICall.ERROR)
        return results   
    
    def _exec(self, sql, param, require_commit=False):
        try:
            c = self.conn.cursor()                        
            c.execute(sql, param)            
            if require_commit:
                self.conn.commit()
            c.close()
        except Exception as e:
            logUICall.log(e, logUICall.ERROR)
            return False
        return True           
    