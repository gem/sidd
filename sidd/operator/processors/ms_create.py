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
# Version: $Id: ms_create.py 18 2012-10-24 20:21:41Z zh $

"""
module contains class for creating mapping scheme from survey data
"""
from qgis.analysis import QgsOverlayAnalyzer

from utils.shapefile import load_shapefile, layer_features, layer_field_index, remove_shapefile, \
                            layer_fields_stats 
from utils.system import get_unique_filename

from sidd.constants import logAPICall
from sidd.ms import MappingScheme, MappingSchemeZone, Statistics

from sidd.operator import Operator, OperatorError
from sidd.operator.data import OperatorDataTypes

class EmptyMSCreator(Operator):
    def __init__(self, options=None, name='EmptyMSCreator'):
        super(EmptyMSCreator, self).__init__(options, name)
        self._tmp_dir = options['tmp_dir']
        self._taxonomy = options['taxonomy']
        self._skips = options['skips']

    # self documenting method override
    ###########################
    
    @property
    def input_types(self):
        return []
        
    @property    
    def input_names(self):
        return []
    
    input_descriptions = input_names    

    @property
    def output_types(self):
        return [OperatorDataTypes.MappingScheme]
        
    @property    
    def output_names(self):
        return ["Mapping Scheme"]

    output_descriptions = input_names

    # public method override
    ###########################
    
    @logAPICall
    def do_operation(self):
        """ perform create mapping scheme operation """
        
        # input/output verification already performed during set input/ouput
        ms = MappingScheme(self._taxonomy)
        zone = MappingSchemeZone('ALL')
        stats = Statistics(self._taxonomy)
        for _idx in self._skips:
            stats.set_attribute_skip(_idx, True)
        stats.finalize()
        stats.get_tree().value = zone.name
        ms.assign(zone, stats)
        
        self.outputs[0].value = ms
    
    # protected method override
    ###########################

    def _verify_inputs(self, inputs):
        """ perform operator specific input validation """
        pass
        
    def _verify_outputs(self, outputs):
        """ perform operator specific output validation """
        pass

class EmptyZonesMSCreator(EmptyMSCreator):
    def __init__(self, options=None, name='SurveyZonesMSCreator'):
        super(EmptyZonesMSCreator, self).__init__(options, name)    
    
    # self documenting method override
    ###########################
    
    @property
    def input_types(self):
        return [OperatorDataTypes.Zone,
                OperatorDataTypes.StringAttribute]
        
    @property    
    def input_names(self):
        return ["Zone data file", "Zone Field"]
    
    input_descriptions = input_names

    @logAPICall
    def do_operation(self):
        """ perform create mapping scheme operation """
        
        # input/output verification already performed during set input/ouput        
        zone_layer = self.inputs[0].value
        zone_field = self.inputs[1].value
        
        # load zone
        try:
            zone_classes = layer_fields_stats(zone_layer, zone_field)
        except AssertionError as err:
            raise OperatorError(str(err), self.__class__)
        
        # merge to create stats
        ms = MappingScheme(self._taxonomy)
        for _zone, _count in zone_classes.iteritems():
            stats = Statistics(self._taxonomy)
            for _idx in self._skips:
                stats.set_attribute_skip(_idx, True)
            stats.finalize()
            stats.get_tree().value = _zone                
            ms.assign(MappingSchemeZone(_zone), stats)

        self.outputs[0].value = ms
    
class SurveyZonesMSCreator(EmptyMSCreator):    
    
    def __init__(self, options=None, name='SurveyZonesMSCreator'):
        super(SurveyZonesMSCreator, self).__init__(options, name)

    # self documenting method override
    ###########################
    
    @property
    def input_types(self):
        return [OperatorDataTypes.Survey,
                OperatorDataTypes.Zone,
                OperatorDataTypes.StringAttribute]
        
    @property    
    def input_names(self):
        return ["Survey", "Zone Layer", "Zone Field"]
    
    input_descriptions = input_names

    # public method override
    ###########################
    
    @logAPICall
    def do_operation(self):
        """ perform create mapping scheme operation """
        
        # input/output verification already performed during set input/ouput        
        survey_layer = self.inputs[0].value
        zone_layer = self.inputs[1].value
        zone_field = self.inputs[2].value
        tax_field = self._tax_field
        
        logAPICall.log('survey %s, taxfield %s, zone %s, zone_field, %s' % (survey_layer.name(), tax_field, zone_layer.name(), zone_field),
                       logAPICall.DEBUG)
        tmp_join_layername = 'join_%s' % get_unique_filename()
        tmp_join_file = self._tmp_dir + tmp_join_layername + '.shp'

        # load zone classes
        try:
            zone_classes = layer_fields_stats(zone_layer, zone_field)
        except AssertionError as err:
            raise OperatorError(str(err), self.__class__)
        
        # merge to create stats
        logAPICall.log('merge survey & zone', logAPICall.DEBUG)
        analyzer = QgsOverlayAnalyzer()        
        analyzer.intersection(survey_layer, zone_layer, tmp_join_file)
        tmp_join_layer = load_shapefile(tmp_join_file, tmp_join_layername)
        
        logAPICall.log('create mapping schemes', logAPICall.DEBUG)
        ms = MappingScheme(self._taxonomy)
        for _zone, _count in zone_classes.iteritems():
            stats = Statistics(self._taxonomy)
            for _idx in self._skips:
                stats.set_attribute_skip(_idx, True)
            ms.assign(MappingSchemeZone(_zone), stats)
        
        # loop through all input features
        zone_idx = layer_field_index(tmp_join_layer, zone_field)
        tax_idx = layer_field_index(tmp_join_layer, tax_field)
        
        for _f in layer_features(tmp_join_layer):
            _zone_str = str(_f.attributeMap()[zone_idx].toString())            
            _tax_str = str(_f.attributeMap()[tax_idx].toString())
            
            logAPICall.log('zone %s => %s' % (_zone_str, _tax_str) , logAPICall.DEBUG_L2)
            ms.get_assignment_by_name(_zone_str).add_case(_tax_str)
        
        # store data in output
        for _zone, _stats in ms.assignments():
            _stats.finalize()
            _stats.get_tree().value = _zone.name

        # clean up        
        del tmp_join_layer, analyzer
        remove_shapefile(tmp_join_file)
        
        self.outputs[0].value = ms

class SurveyOnlyMSCreator(EmptyMSCreator):    
    
    def __init__(self, options=None, name='SurveyOnlyMSCreator'):
        super(SurveyOnlyMSCreator, self).__init__(options, name)

    # self documenting method override
    ###########################
    
    @property
    def input_types(self):
        return [OperatorDataTypes.Survey,]
        
    @property    
    def input_names(self):
        return ["Survey"]
    
    input_descriptions = input_names
   
    # public method override
    ###########################

    @logAPICall
    def do_operation(self):
        """ perform create mapping scheme operation """
        
        # input/output verification already performed during set input/ouput
        survey_layer = self.inputs[0].value
        tax_field = self._tax_field
        
        # merge to create stats
        ms = MappingScheme(self._taxonomy)
        stats = Statistics(self._taxonomy)
        for _idx in self._skips:
            stats.set_attribute_skip(_idx, True)
        ms.assign(MappingSchemeZone('ALL'), stats)
        
        # loop through all input features
        tax_idx = layer_field_index(survey_layer, tax_field)
        
        for _f in layer_features(survey_layer):
            _tax_str = str(_f.attributeMap()[tax_idx].toString())            
            stats.add_case(_tax_str)
        
        # store data in output
        stats.finalize()        
        
        self.outputs[0].value = ms
