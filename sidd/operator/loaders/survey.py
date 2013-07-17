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

from sidd.taxonomy.gem import GemTaxonomyAttribute
from sidd.constants import logAPICall, \
                           GID_FIELD_NAME, LON_FIELD_NAME, LAT_FIELD_NAME, TAX_FIELD_NAME, \
                           GRP_FIELD_NAME, AREA_FIELD_NAME, HT_FIELD_NAME, COST_FIELD_NAME
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
        self.taxonomy = options['taxonomy']

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
            0 : QgsField(GID_FIELD_NAME, QVariant.String),
            1 : QgsField(LON_FIELD_NAME, QVariant.Double),
            2 : QgsField(LAT_FIELD_NAME, QVariant.Double),
            3 : QgsField(TAX_FIELD_NAME, QVariant.String, "", 255),
            4 : QgsField(GRP_FIELD_NAME, QVariant.String),
            5 : QgsField(AREA_FIELD_NAME, QVariant.String),
            6 : QgsField(HT_FIELD_NAME, QVariant.String),
            7 : QgsField(COST_FIELD_NAME, QVariant.String),
        }
    # self documenting method override
    ###########################
 
    @property
    def input_types(self):
        return [OperatorDataTypes.File, OperatorDataTypes.StringAttribute, OperatorDataTypes.StringAttribute]
        
    @property    
    def input_names(self):
        return ["Survey Input File", "Survey data type", "Project Filter"]
    
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
        project = self.inputs[2].value
        
        tmp_survey_file = '%ssurvey_%s.shp' % (self._tmp_dir, get_unique_filename())
        # load survey        
        try:
            self._loadSurvey(survey, tmp_survey_file, project)
            
        except Exception as err:
            remove_shapefile(tmp_survey_file)
            raise OperatorError("Error Loading Survey\n%s" % err,
                                self.__class__)
        try:
            # store loaded data
            tmp_survey_layername = 'survey_%s' % get_unique_filename()
            tmp_survey_layer = load_shapefile_verify(tmp_survey_file, tmp_survey_layername,
                                                     [self._lon_field, self._lat_field, self._tax_field])            
        except Exception as err:
            raise OperatorError("Error Loading Survey\n%s" % err,
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
    def _loadSurvey(self, sqlitepath, shapefilepath, proj_uid=None):
        # load data
        sql = """select OBJ_UID, X, Y, SAMPLE_GRP, PLAN_AREA, REPLC_COST,
                MAT_TYPE_L, MAT_TECH_L, MAS_REIN_L, MAS_MORT_L, STEELCON_L, 
                LLRS_L, LLRS_DCT_L,  
                ROOFSYSMAT, ROOFSYSTYP,  
                FLOOR_MAT, FLOOR_TYPE, 
                STORY_AG_Q, STORY_AG_1, STORY_AG_2,
                YR_BUILT_Q, YR_BUILT_1, YR_BUILT_2,                
                STR_IRREG, STR_HZIR_P, STR_HZIR_S, STR_VEIR_P, STR_VEIR_S, 
                OCCUPCY, OCCUPCY_DT
                from GEM_OBJECT o LEFT JOIN GED g on o.OBJ_UID=g.GEMOBJ_UID"""
        # SQL injection check not too important here given that data format is SQLite         
        if proj_uid is not None:
            sql = "%s WHERE PROJ_UID='%s'" % (sql, proj_uid)
        conn = sqlite3.connect(sqlitepath)
        c = conn.cursor()
        c.execute(sql)
        self._buildSurveyLayer(c, shapefilepath)
        c.close()
        conn.close()
        
    def _buildSurveyLayer(self, data,  shapefilepath):
        writer = QgsVectorFileWriter(shapefilepath, "utf-8", self._fields, QGis.WKBPoint, self._crs, "ESRI Shapefile")
        f = QgsFeature()
        for row in data:
            obj_uid = str(row[0])
            lon = self._tofloat(row[1])
            lat = self._tofloat(row[2])
            sample_grp = str(row[3])
            plan_area = self._tofloat(row[4])
            rep_cost = self._tofloat(row[5])
            tax_string = self._make_gem_taxstring(row[6:])
            ht = self._get_height(row[6:]) 
            
            f.setGeometry(QgsGeometry.fromPoint(QgsPoint(lon, lat)))
            f.addAttribute(0, QVariant(obj_uid))
            f.addAttribute(1, QVariant(lon))
            f.addAttribute(2, QVariant(lat))
            f.addAttribute(3, QVariant(tax_string))
            f.addAttribute(4, QVariant(sample_grp))
            f.addAttribute(5, QVariant(plan_area))
            f.addAttribute(6, QVariant(ht))
            f.addAttribute(7, QVariant(rep_cost))
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
        
        # attribute group names
        # 'Material', 'Lateral Load-Resisting System', 'Roof', 'Floor', 'Height', 'Date of Construction', 'Irregularity', 'Occupancy'

        # separator for individual attributes in group
        separator = self.taxonomy.get_separator(self.taxonomy.Separators.Attribute)
        
        # material
        mat_string = self._coalesce(mat_type_l) \
            + self._append_not_null(mat_tech_l, separator) + self._append_not_null(mas_rein_l, separator) \
            + self._append_not_null(mas_mort_l, separator)  + self._append_not_null(steel_con_l, separator) 
        
        # lateral load
        ll_string = self._coalesce(llrs_l) + self._append_not_null(llrs_duct_l,separator) 
        
        # roof 
        roof_string = self._coalesce(roofsysmat) + self._append_not_null(roofsystyp,separator) 
        
        # floor
        floor_string = self._coalesce(floor_mat) + self._append_not_null(floor_type,separator)
        
        # story
        attribute = self.taxonomy.get_attribute_by_name('Height')
        _qualifier = self._coalesce(story_ag_q)
        _story1, _story2 = self._toint(story_ag_1), self._toint(story_ag_2)
        if getattr(self, 'ht_ranges', None) is None:            
            if _qualifier == 'HBET':
                ht_string = attribute.make_string([_story2, _story1], GemTaxonomyAttribute.RANGE)                  
            elif _qualifier == 'HAPP':
                ht_string = attribute.make_string([_story2, 0], GemTaxonomyAttribute.APP) 
            else:
                ht_string = attribute.make_string([_story1, 0], GemTaxonomyAttribute.EXACT)            
        else:
            if _qualifier == "HBET":
                ht_range = self._find_range((_story1 + _story2) / 2.0,
                                             self.ht_ranges['min_values'], self.ht_ranges['max_values'])
            else: # EXACT or APPROXIMATE
                ht_range = self._find_range(_story1, 
                                            self.ht_ranges['min_values'], self.ht_ranges['max_values'])
            if _story1 is None or _story1 == 0:
                ht_range = [None, None]
            elif ht_range[0] is None and ht_range[1] is not None:
                self.ht_ranges['min_values'].insert(0, 1) 
                self.ht_ranges['max_values'].insert(0, ht_range[1])
            elif ht_range[1] is None and ht_range[0] is not None:
                self.ht_ranges['min_values'].append(ht_range[0])
                self.ht_ranges['max_values'].append(200)
            ht_string = attribute.make_string(ht_range, GemTaxonomyAttribute.RANGE)          
            
        # yr_built
        attribute = self.taxonomy.get_attribute_by_name('Date of Construction')
        _qualifier = self._coalesce(yr_built_q)
        _year1, _year2 = self._toint(yr_built_1), self._toint(yr_built_2)
        if getattr(self, 'yr_ranges', None) is None:
            if _qualifier == 'YAPP':
                yr_string = attribute.make_string([_year2, 0], GemTaxonomyAttribute.APP)
            elif _qualifier== 'YPRE':                
                yr_string = attribute.make_string([_year2, 0], GemTaxonomyAttribute.PRE)
            elif _qualifier == 'YBET':
                yr_string = attribute.make_string([_year2, _year1], GemTaxonomyAttribute.RANGE)
            else:
                yr_string = attribute.make_string([_year1, 0], GemTaxonomyAttribute.EXACT)
        else:
            if _qualifier == "YBET":
                yr_ranges = self._find_range((_year1 + _year2) / 2.0,
                                              self.yr_ranges['min_values'], self.yr_ranges['max_values'])
            else: # EXACT or APPROXIMATE
                yr_ranges = self._find_range(_year1, 
                                             self.yr_ranges['min_values'], self.yr_ranges['max_values'])
            if _year1 is None or _year1 == 0:
                yr_ranges = [None, None]
            elif yr_ranges[0] is None and yr_ranges[1] is not None:
                self.yr_ranges['min_values'].insert(0, 1) 
                self.yr_ranges['max_values'].insert(0, yr_ranges[1])
            elif yr_ranges[1] is None and yr_ranges[0] is not None:
                self.yr_ranges['min_values'].append(yr_ranges[0])
                self.yr_ranges['max_values'].append(datetime.date.today().year)
            yr_string = attribute.make_string(yr_ranges, GemTaxonomyAttribute.RANGE)
            
        # irregularity
        ir_string = self._append_no_repeat([str_irreg, str_hzir_p, str_hzir_s, str_veir_p, str_veir_s], 
                                           separator, exclude="IRN")
        # occupancy
        occ_string = self._coalesce(occupcy) + self._append_not_null(occupcy_dt,separator)
        
        # constructs output string
        separator = self.taxonomy.get_separator(self.taxonomy.Separators.AttributeGroup)
        return (mat_string + self._append_not_null(ll_string,separator)
                           + self._append_not_null(roof_string,separator)
                           + self._append_not_null(floor_string,separator)
                           + self._append_not_null(ht_string,separator)
                           + self._append_not_null(yr_string,separator)
                           + self._append_not_null(ir_string,separator)
                           + self._append_not_null(occ_string,separator))
    
    def _get_height(self, data):
        """ retrieve height as numeric value from SQLite Query Result """ 
        story_ag_q, story_ag_1, story_ag_2 = data[11:14]
        ht = 0
        if story_ag_1 is None:
            ht = 0
        elif self._coalesce(story_ag_q) == "HBET":
            ht = (self._toint(story_ag_1) + self._toint(story_ag_2)) / 2
        else:
            ht = self._toint(story_ag_1)
        return int(ht)
    
    def _coalesce(self, val):        
        """ returns val or blank string if val is null (None) """
        if (val is not None):
            return str(val).upper()
        else:
            return ""
    
    def _toint(self, val):
        """ convert val to integer, return 0 if conversion fails """
        try:
            return int(val)
        except:
            return 0
        
    def _tofloat(self, val):
        """ convert val to floating point, return 0.0 if conversion fails """
        try:
            return float(val) 
        except:
            return 0.0        
     
    def _append_not_null(self, val, separator):        
        """ append val with separator if val is not empty """
        if (val is None or val == ""):
            return ""
        else:
            return separator + str(val)

    def _append_no_repeat(self, vals, separator, exclude=''):
        """ concatenate list of values using separator if value is not empty and not excluded """
        no_repeat = {}
        for val in vals:
            if val is None or val == "" or val == exclude:
                continue
            no_repeat[val]=1
        return str(separator).join(no_repeat.keys())

    def _find_range(self, value, min_values, max_values):
        """ find min/max values surrounding given value """
        # less than minimum
        if value < min_values[0]:
            return None, min_values[0]
        # test ranges
        for min_val, max_val in map(None, min_values, max_values):
            if value >= min_val and value <= max_val:
                return min_val, max_val
        # larger than maximum
        return max_values[len(max_values)-1], None
        
    
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
        