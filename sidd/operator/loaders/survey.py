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
# Version: $Id: survey.py 18 2012-10-24 20:21:41Z zh $

"""
module constains class for loading survey data in SQLite format 
"""
import csv
import sqlite3
import datetime

from os.path import exists

from PyQt4.QtCore import QVariant
from qgis.core import QGis, QgsVectorFileWriter, QgsFeature, QgsField, QgsGeometry, QgsPoint

from utils.shapefile import load_shapefile_verify, remove_shapefile
from utils.system import get_unique_filename

from sidd.constants import logAPICall, \
                           GID_FIELD_NAME, LON_FIELD_NAME, LAT_FIELD_NAME, TAX_FIELD_NAME, GRP_FIELD_NAME, AREA_FIELD_NAME
from sidd.operator import Operator,OperatorError, OperatorDataError
from sidd.operator.data import OperatorDataTypes

class GEMDBSurveyLoader(Operator):
    """ loading field survey data in CSV format"""
    HT_ATTRIBUTE_NAME='Height'
    YR_ATTRIBUTE_NAME='Date of Construction'
    
    def __init__(self, options=None, name="Survey Loader"):
        """ constructor """
        Operator.__init__(self, options, name)
        self._tmp_dir = options['tmp_dir']
        if options.has_key('year_translator'):
            self._make_year_string = (options['year_translator']).translate
        if options.has_key('ht_translator'):   
            self._make_year_string = (options['ht_translator']).translate 

        # check if height/year range is requested
        # range is stored as dictionary {'min_values':min_values, 'max_values':max_values}
        # where min_value and max_value are arrays of values
        if options.has_key(self.HT_ATTRIBUTE_NAME):
            ht_ranges = options[self.HT_ATTRIBUTE_NAME]
            min_values_count = len(ht_ranges['min_values'])            
            max_values_count = len(ht_ranges['max_values'])            
            # use range only if it is correctly set              
            if min_values_count>0 and max_values_count>0 and min_values_count==max_values_count:
                self.ht_ranges = options[self.HT_ATTRIBUTE_NAME]            
        if options.has_key(self.YR_ATTRIBUTE_NAME):
            ht_ranges = options[self.YR_ATTRIBUTE_NAME]
            min_values_count = len(ht_ranges['min_values'])            
            max_values_count = len(ht_ranges['max_values'])            
            # use range only if it is correctly set              
            if min_values_count>0 and max_values_count>0 and min_values_count==max_values_count:
                self.yr_ranges = options[self.YR_ATTRIBUTE_NAME]
            
        self._fields = {
            0 : QgsField(GID_FIELD_NAME, QVariant.Int),
            1 : QgsField(LON_FIELD_NAME, QVariant.Double),
            2 : QgsField(LAT_FIELD_NAME, QVariant.Double),
            3 : QgsField(TAX_FIELD_NAME, QVariant.String),
            4 : QgsField(GRP_FIELD_NAME, QVariant.String),
            5 : QgsField(AREA_FIELD_NAME, QVariant.String),
        }
    # self documenting method override
    ###########################
 
    @property
    def input_types(self):
        return [OperatorDataTypes.File, OperatorDataTypes.StringAttribute]
        
    @property    
    def input_names(self):
        return ["Survey Input File", "Survey data type"]
    
    input_descriptions = input_names

    @property
    def output_types(self):
        return [OperatorDataTypes.Survey, OperatorDataTypes.Shapefile]
        
    @property    
    def output_names(self):
        return ["Survey", "Survey Shapefile"]
    output_descriptions = output_names
    
    # public method override
    ###########################

    @logAPICall
    def do_operation(self):
        """ perform survey data loading """        
        # input/output data checking already done during property set
        survey = self.inputs[0].value
        
        tmp_survey_file = '%ssurvey_%s.shp' % (self._tmp_dir, get_unique_filename())
        # load survey        
        try:
            self._loadSurvey(survey, tmp_survey_file)
            
        except Exception as err:
            remove_shapefile(tmp_survey_file)
            raise OperatorError("Error Loading Survey: %s" % err,
                                self.__class__)
        try:
            # store loaded data
            tmp_survey_layername = 'survey_%s' % get_unique_filename()
            tmp_survey_layer = load_shapefile_verify(tmp_survey_file, tmp_survey_layername,
                                                     [self._lon_field, self._lat_field, self._tax_field])            
        except Exception as err:
            raise OperatorError("Error Loading Survey: %s" % err,
                                self.__class__)
        
        self.outputs[0].value = tmp_survey_layer
        self.outputs[1].value = tmp_survey_file

    # protected method override
    ####################################
    
    def _verify_inputs(self, inputs):
        """ perform operator specific input validation """
        if not exists(inputs[0].value):
            raise OperatorDataError("input file %s does not exist" % (inputs[0].value))

    def _verify_outputs(self, outputs):
        """ perform operator specific input validation """
        pass

    # internal helper methods
    ####################################
    def _loadSurvey(self, sqlitepath, shapefilepath):
        # load data
        sql = """select X, Y, SAMPLE_GRP, PLAN_AREA,
                MAT_TYPE_L, MAT_TECH_L, MAS_REIN_L, MAS_MORT_L, STEEL_CON_L, 
                LLRS_L, LLRS_DUCT_L,  
                ROOFSYSMAT, ROOFSYSTYP,  
                FLOOR_MAT, FLOOR_TYPE, 
                STORY_AG_Q, STORY_AG_1, STORY_AG_2,
                YR_BUILT_Q, YR_BUILT_1, YR_BUILT_2,                
                STR_IRREG, STR_HZIR_P, STR_HZIR_S, STR_VEIR_P, STR_VEIR_S, 
                OCCUPCY, OCCUPCY_DT
                from GEM_OBJECT o LEFT JOIN GED g on o.OBJ_UID=g.GEMOBJ_UID"""
        conn = sqlite3.connect(sqlitepath)
        c = conn.cursor()
        c.execute(sql)        
        self._buildSurveyLayer(c, shapefilepath)
        c.close()
        conn.close()
        
    def _buildSurveyLayer(self, data,  shapefilepath):
        writer = QgsVectorFileWriter(shapefilepath, "utf-8", self._fields, QGis.WKBPoint, self._crs, "ESRI Shapefile")
        f = QgsFeature()
        gid = 0
        for row in data:
            lon = self._tofloat(row[0])
            lat = self._tofloat(row[1])
            sample_grp = str(row[2])
            plan_area = self._tofloat(row[3])
            tax_string = self._make_gem_taxstring(row[4:])
            
            f.setGeometry(QgsGeometry.fromPoint(QgsPoint(lon, lat)))
            gid+=1
            f.addAttribute(0, QVariant(gid))
            f.addAttribute(1, QVariant(lon))
            f.addAttribute(2, QVariant(lat))
            f.addAttribute(3, QVariant(tax_string))
            f.addAttribute(4, QVariant(sample_grp))
            f.addAttribute(5, QVariant(plan_area))
            writer.addFeature(f)
        del writer, f
        
    def _make_gem_taxstring(self, data):
        (mat_type_l, mat_tech_l, mas_rein_l, mas_mort_l, steel_con_l, 
         llrs_l, llrs_duct_l, 
         roofsysmat, roofsystyp,  
         floor_mat, floor_type, 
         story_ag_q, story_ag_1, story_ag_2,
         yr_built_q, yr_built_1, yr_built_2,
         str_irreg, str_hzir_p, str_hzir_s, str_veir_p, str_veir_s, 
         occupcy, occupcy_dt) = [(x) for x in data]
        
        separator = "+"
        
        # material
        mat_string = self._coalesce(mat_type_l) \
            + self._append_not_null(mat_tech_l, separator) + self._append_not_null(mas_rein_l, separator) \
            + self._append_not_null(mas_mort_l, separator)  + self._append_not_null(steel_con_l, separator) 
        
        # lateral load
        ll_string = llrs_l + self._append_not_null(llrs_duct_l,separator) 
        
        # roof 
        roof_string = self._coalesce(roofsysmat) + self._append_not_null(roofsystyp,separator) 
        
        # floor
        floor_string = self._coalesce(floor_mat) + self._append_not_null(floor_type,separator)
        
        # story
        if getattr(self, 'ht_ranges', None) is None:
            ht_string = self._make_height_string(self._coalesce(story_ag_q), 
                                                 self._toint(story_ag_1), self._toint(story_ag_2))
        else:
            ht_string = self._make_range_height_string(self._coalesce(story_ag_q), 
                                                       self._toint(story_ag_1), self._toint(story_ag_2))
        # yr_built
        if getattr(self, 'yr_ranges', None) is None:
            yr_string = self._make_year_string(self._coalesce(yr_built_q), 
                                               self._toint(yr_built_1), self._toint(yr_built_2))
        else:
            yr_string = self._make_range_year_string(self._coalesce(yr_built_q), 
                                                     self._toint(yr_built_1), self._toint(yr_built_2))

        # irregularity
        ir_string = self._coalesce(str_irreg) \
            + self._append_not_null(str_hzir_p,separator) + self._append_not_null(str_hzir_s,separator) \
            + self._append_not_null(str_veir_p,separator) + self._append_not_null(str_veir_s,separator) 
        
        # occupancy
        occ_string = self._coalesce(occupcy) + self._append_not_null(occupcy_dt,separator)
        
        separator = "/"
        return (mat_string + self._append_not_null(ll_string,separator)
                           + self._append_not_null(roof_string,separator)
                           + self._append_not_null(floor_string,separator)
                           + self._append_not_null(ht_string,separator)
                           + self._append_not_null(yr_string,separator)
                           + self._append_not_null(ir_string,separator)
                           + self._append_not_null(occ_string,separator))
    
    def _coalesce(self, val):
        return str(val) if (val is not None) else ""
    
    def _toint(self, val):
        try:
            return int(val) 
        except:
            return 0
    def _tofloat(self, val):
        try:
            return float(val) 
        except:
            return 0.0        
     
    def _append_not_null(self, val, separator):        
        if (val is None or val == ""):
            return ""
        else:
            return separator + str(val)

    def _make_height_string(self, story_ag_q, story_ag_1, story_ag_2):
        # create story string from given qualifier and parameters
        ht_string = "H99"
        if story_ag_1 is None:
            ht_string = "H99"
        elif story_ag_q.upper() == "CIRCA":
            ht_string = "H:" + self._coalesce(story_ag_1)
        elif story_ag_q.upper() == "BETWEEN":
            ht_string = "H" + story_ag_1 + "," + story_ag_2
        else:
            ht_string = "H:" + self._coalesce(story_ag_1)
        return ht_string
    
    def _make_year_string(self, yr_built_q, yr_built_1, yr_built_2):
        yr_string = "Y99"
        if yr_built_1 is None:
            yr_string = "Y99"
        elif yr_built_q.upper() == "CIRCA":
            yr_string = "YA:" + self._coalesce(yr_built_1)
        elif yr_built_q.upper() == "BETWEEN":
            yr_string = "YA" + int((yr_built_1 + yr_built_2)/2)
        else:
            yr_string = "YN:" + self._coalesce(yr_built_1)
        return yr_string

    def _make_range_height_string(self, story_ag_q, story_ag_1, story_ag_2):
        ht_string = "H99"
        if story_ag_1 is None:
            ht_string = "H99"
        elif story_ag_q.upper() == "CIRCA":
            ht_range = self._find_range(story_ag_1, 
                                        self.ht_ranges['min_values'], self.ht_ranges['max_values'])
        elif story_ag_q.upper() == "BETWEEN":
            ht_range = self._find_range((story_ag_1 + story_ag_2) / 2.0, 
                                        self.ht_ranges['min_values'], self.ht_ranges['max_values'])
        else:
            ht_range = self._find_range(story_ag_1, 
                                        self.ht_ranges['min_values'], self.ht_ranges['max_values'])
        if ht_range[0] is None:     # less than minimum
            ht_string = "H:1,%s"%(ht_range[1])
        elif ht_range[1] is None:   # larger than maximum
            ht_string = "H:%s,"%(ht_range[0])
        else:                       # in range
            ht_string = "H:%s,%s"%(ht_range)
        return ht_string

    def _make_range_year_string(self, yr_built_q, yr_built_1, yr_built_2):
        yr_string = "Y99"
        if yr_built_1 is None:
            yr_string = "Y99"
        elif yr_built_q.upper() == "CIRCA":            
            yr_range = self._find_range(yr_built_1, 
                                        self.yr_ranges['min_values'], self.yr_ranges['max_values'])            
        elif yr_built_q.upper() == "BETWEEN":
            yr_range = self._find_range((yr_built_1 + yr_built_2)/2, 
                                        self.yr_ranges['min_values'], self.yr_ranges['max_values'])            
        else:
            yr_range = self._find_range(yr_built_1, 
                                        self.yr_ranges['min_values'], self.yr_ranges['max_values'])
        if yr_range[0] is None:     # less than minimum
            yr_string = "YP:%s"%(yr_range[1])
        elif yr_range[1] is None:   # larger than maximum
            yr_string = "YN:%s,%s"%(yr_range[1],datetime.date.today().year)
        else:                       # in range
            yr_string = "YN:%s,%s"%(yr_range)
        return yr_string

    
    def _find_range(self, value, min_values, max_values):
        # less than minimum
        if value < min_values[0]:
            return None, min_values[0]
        # test ranges
        for min_val, max_val in map(None, min_values, max_values):
            if value >= min_val and value <= max_val:
                return min_val, max_val
        # larger than maximum
        return max_values[len(max_values)-1], None
        
    def _range_year_string(self, yr_built_q, yr_built_1, yr_built_2):
        input_val = '_get_val'
        for min_val, max_val in map(None, self.yr_ranges['min_values'], self.yr_ranges['max_values']):
            if input_val >= min_val and input_val <= max_val:
                return 'label'
        return None
       
    
class CSVSurveyLoader(GEMDBSurveyLoader):
    """ loading field survey data in CSV format"""
    
    def __init__(self, options=None, name="Survey Loader"):
        """ constructor """
        super(CSVSurveyLoader, self).__init__(options, name)
    
    def _loadSurvey(self, csvpath, shapefilepath):
        # load data
        data = csv.reader(open(csvpath, 'r'), delimiter=',', quotechar='"')
        # skip header, there is probably a better way to accomplish this
        data.next()
        writer = QgsVectorFileWriter(shapefilepath, "utf-8", self._fields, QGis.WKBPoint, self._crs, "ESRI Shapefile")
        f = QgsFeature()
        gid = 0
        for row in data:
            lon = float(row[0])
            lat = float(row[1])
            f.setGeometry(QgsGeometry.fromPoint(QgsPoint(lon, lat)))
            gid+=1
            f.addAttribute(0, QVariant(gid))
            f.addAttribute(1, QVariant(lon))
            f.addAttribute(2, QVariant(lat))
            f.addAttribute(3, QVariant(row[2]))
            writer.addFeature(f)
        del writer, f        
        