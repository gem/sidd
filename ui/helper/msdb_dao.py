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
# Version: $Id: msdb_dao.py 19 2012-10-25 01:06:59Z zh $

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
        'GET_ALL_REGIONS':"""select name from regions order by name""",
        'GET_MS_REGIONS':"""select distinct region from mapping_scheme order by region """,
        'GET_TYPES':"""select distinct source from mapping_scheme where region='%s' order by source""",
        'GET_MSNAME':"""select ms_name from mapping_scheme where region='%s' and source='%s' order by ms_name""",
        'GET_MS':"""select date_created, data_source, quality, use_notes, ms_xml from mapping_scheme where region='%s' and source='%s' and ms_name='%s'""",
        'GET_MAX_MS_ID':"""select max(id) from mapping_scheme""",
        'INSERT_MS':"""
        insert into mapping_scheme (id, region, ms_name, source, date_created, data_source, quality, use_notes, ms_xml, taxonomy)
        values (?, ?, ?, ?, ?, ?, ?, ?, ?, 'GEM')
        """,
        'DELETE_MS':"""delete from mapping_scheme where region='%s' and source='%s' and ms_name='%s'""",
    }
    
    def __init__(self, dbpath):
        """ initialize """
        try:
            logUICall.log('opening ms db file %s ' % (dbpath), logUICall.INFO)
            self.conn = sqlite3.connect(dbpath)
            self.initialized = True
        except:
            self.initialized = False
    
    def __del__(self):
        if self.initialized:
            self.conn.close()
    
    def get_regions(self, with_ms=False):        
        logUICall.log('get_regions', logUICall.DEBUG_L2)
        if not self.initialized:
            return []
        else:
            if with_ms:
                return self.__get_list( self.sql['GET_MS_REGIONS'] )
            else:
                return self.__get_list( self.sql['GET_ALL_REGIONS'] )
        
    def get_types_in_region(self, region):
        logUICall.log('get_types_in_region %s' % region, logUICall.DEBUG_L2)
        if not self.initialized:
            return []
        else:
            return self.__get_list( self.sql['GET_TYPES'] % (region) )
    
    def get_ms_in_region_type(self, region, ms_type):
        logUICall.log('get_ms_in_region_type %s %s' % (region, ms_type), logUICall.DEBUG_L2)
        if not self.initialized:
            return []
        else:
            return self.__get_list( self.sql['GET_MSNAME'] % (region, ms_type))
    
    def get_ms(self, region, ms_type, ms_name):
        logUICall.log('get_ms %s %s %s' % (region, ms_type, ms_name), logUICall.DEBUG_L2)        
        if not self.initialized:
            return []
        else:
            return self.__get_list( self.sql['GET_MS'] % (region, ms_type, ms_name), first_column=False)[0]
    
    def save_ms(self, region, ms_name, source, date, datasource, quality, notes, ms_xml):
        logUICall.log('get_ms %s %s %s %s %s %s %s %s' % (region, ms_name, source,
                                                          date, datasource, quality,
                                                          notes, ms_xml[0:20]), 
                      logUICall.DEBUG_L2)
        id = int(self.__get_list(self.sql['GET_MAX_MS_ID'])[0]) + 1
        return self.__exec(self.sql['INSERT_MS'], [id, region, ms_name,
                                                   source, date, datasource,
                                                   quality, notes, ms_xml])
     
    
    def delete_ms(self, region, ms_type, ms_name):
        return self.__exec(self.sql['DELETE_MS'] % (region, ms_type, ms_name), [])
    
    def __get_list(self, sql, first_column=True):
        results = []
        try:
            c = self.conn.cursor()                        
            c.execute(sql)            
            for row in c:     
                if first_column:
                    results.append(row[0])
                else:
                    results.append(row)
            c.close()
        except Exception as e:
            logUICall.log(e, logUICall.ERROR)
        return results   
    
    def __exec(self, sql, param):
        try:
            c = self.conn.cursor()                        
            c.execute(sql, param)            
            c.close()
        except Exception as e:
            logUICall.log(e, logUICall.ERROR)
            return False
        return True           
    