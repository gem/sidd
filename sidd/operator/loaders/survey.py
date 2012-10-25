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

from os.path import exists

from PyQt4.QtCore import *
from qgis.core import *

from utils.shapefile import *
from utils.system import get_unique_filename

from sidd.constants import logAPICall
from sidd.operator import *


class SurveyLoader(Operator):
    """ loading field survey data in CSV format"""
    
    def __init__(self, options=None, name="Survey Loader"):
        """ constructor """
        Operator.__init__(self, options, name)
        self._tmp_dir = options['tmp_dir']

        self._fields = {
            0 : QgsField(self._lon_field, QVariant.Double),
            1 : QgsField(self._lat_field, QVariant.Double),
            2 : QgsField(self._tax_field, QVariant.String),
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
        survey_type = self.inputs[1].value
        taxfield = 'taxonomy'
        
        tmp_survey_file = '%ssurvey_%s.shp' % (self._tmp_dir, get_unique_filename())
        # load survey        
        try:
            if (survey_type == 'CSV'):
                self._loadCSVSurvey(survey, tmp_survey_file)
            else:
                self._loadSQLiteSurvey(survey, tmp_survey_file)
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

    def _loadCSVSurvey(self, csvpath, shapefilepath):
        # load data
        survey = csv.reader(open(csvpath, 'r'), delimiter=',', quotechar='"')
        header = survey.next()
        self._buildSurveyLayer(survey, shapefilepath)

    def _loadSQLiteSurvey(self, sqlitepath, shapefilepath):
        # load data
        sql = ""
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
            lon = float(row[0])
            lat = float(row[1])
            f.setGeometry(QgsGeometry.fromPoint(QgsPoint(lon, lat)))
            f.addAttribute(0, QVariant(lon))
            f.addAttribute(1, QVariant(lat))
            f.addAttribute(2, QVariant(row[2]))
            writer.addFeature(f)
        del writer, f
        