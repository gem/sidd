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
module contains class for creating mapping scheme from survey data
"""
from qgis.analysis import QgsOverlayAnalyzer

from utils.shapefile import load_shapefile, layer_features, layer_field_index, remove_shapefile, \
                            layer_fields_stats
from utils.system import get_unique_filename, get_temp_dir, get_dictionary_value

from sidd.constants import logAPICall, AREA_FIELD_NAME, GRP_FIELD_NAME, TAX_FIELD_NAME, HT_FIELD_NAME
from sidd.ms import MappingScheme, MappingSchemeZone, Statistics
from sidd.taxonomy import get_taxonomy
from sidd.operator import Operator, OperatorError
from sidd.operator.data import OperatorDataTypes

class EmptyMSCreator(Operator):
    def __init__(self, options=None, name='Empty MS Creator'):
        super(EmptyMSCreator, self).__init__(options, name)
        self._tmp_dir = get_dictionary_value(options, 'tmp_dir', get_temp_dir())
        self._taxonomy = get_dictionary_value(options, 'taxonomy', get_taxonomy('GEM'))  
        self._skips = get_dictionary_value(options, 'skips', [])
        self._parse_modifiers = get_dictionary_value(options, 'parse_modifiers', True)
        self._parse_order = get_dictionary_value(options, 'attribute.order', None)

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
    def __init__(self, options=None, name='Empty Zones MSCreator'):
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
            ms.get_assignment_by_name(_zone_str).add_case(_tax_str, self._parse_order, self._parse_modifiers)
            
        
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
            stats.add_case(_tax_str, self._parse_order, self._parse_modifiers)
        
        # store data in output
        stats.finalize()        
        
        self.outputs[0].value = ms

class StratifiedMSCreator(EmptyMSCreator):    
    
    def __init__(self, options=None, name='Stratified Sampling Mapping Scheme'):
        super(StratifiedMSCreator, self).__init__(options, name)
        self.weights=[0.3, 0.4, 0.3]
        #self._parse_modifiers = False
    
    @property
    def input_types(self):
        return [OperatorDataTypes.Footprint, 
                OperatorDataTypes.StringAttribute, OperatorDataTypes.StringAttribute,
                OperatorDataTypes.Zone, OperatorDataTypes.StringAttribute,
                OperatorDataTypes.Survey,]
        
    @property    
    def input_names(self):
        return ["Footprint", 
                "Footprint Area Field", "Footprint Height Field",
                "Zone", "Zone Identifier Field",
                "Survey"]

    input_descriptions = input_names

    @property
    def output_types(self):
        return [OperatorDataTypes.MappingScheme, 
                OperatorDataTypes.ZoneStatistic]
        
    @property    
    def output_names(self):
        return ["Mapping Scheme", "Zone Statistics"]

    output_descriptions = input_names
            
    # public method override
    ###########################
    @logAPICall
    def do_operation(self):
        # input/output verification not performed yet
        fp_layer = self.inputs[0].value
        area_field = self.inputs[1].value
        ht_field = self.inputs[2].value
        zone_layer = self.inputs[3].value
        zone_field = self.inputs[4].value
        svy_layer = self.inputs[5].value
        
        # make sure required data fields are populated
        area_idx = layer_field_index(fp_layer, area_field)
        if area_idx == -1:        
            raise OperatorError("Field %s does not exist in %s" %(area_field, fp_layer.name()), self.__class__)        
        ht_idx = layer_field_index(fp_layer, ht_field)
        if ht_idx == -1:        
            raise OperatorError("Field %s does not exist in %s" %(ht_field, fp_layer.name()), self.__class__)        
        zone_idx = layer_field_index(zone_layer, zone_field)
        if zone_idx == -1:        
            raise OperatorError("Field %s does not exist in %s" %(zone_field, zone_layer.name()), self.__class__)
        svy_samp_idx = layer_field_index(svy_layer, GRP_FIELD_NAME)
        if svy_samp_idx == -1:
            raise OperatorError("Field %s does not exist in %s" %(GRP_FIELD_NAME, svy_layer.name()), self.__class__)
        svy_ht_idx = layer_field_index(svy_layer, HT_FIELD_NAME)
        if svy_ht_idx == -1:
            raise OperatorError("Field %s does not exist in %s" %(HT_FIELD_NAME, svy_layer.name()), self.__class__)        
        svy_size_idx = layer_field_index(svy_layer, AREA_FIELD_NAME)
        if svy_size_idx == -1:
            raise OperatorError("Field %s does not exist in %s" %(AREA_FIELD_NAME, svy_layer.name()))
        tax_idx = layer_field_index(svy_layer, TAX_FIELD_NAME)
        if tax_idx == -1:
            raise OperatorError("Field %s does not exist in %s" %(TAX_FIELD_NAME, svy_layer.name()))
        
        # load zone classes
        # the operations below must be performed for each zone 
        try:
            zone_classes = layer_fields_stats(zone_layer, zone_field)
        except AssertionError as err:
            raise OperatorError(str(err), self.__class__)

        # join survey with zones        
        logAPICall.log('merge survey & zone', logAPICall.DEBUG)
        tmp_join_layername = 'join_%s' % get_unique_filename()
        tmp_join_file = self._tmp_dir + tmp_join_layername + '.shp'        
        analyzer = QgsOverlayAnalyzer()        
        analyzer.intersection(svy_layer, zone_layer, tmp_join_file)        
        tmp_join_layer = load_shapefile(tmp_join_file, tmp_join_layername)
        
        logAPICall.log('compile zone statistics', logAPICall.DEBUG)
        zone_idx = layer_field_index(tmp_join_layer, zone_field)
        svy_samp_idx = layer_field_index(tmp_join_layer, GRP_FIELD_NAME)
        svy_ht_idx = layer_field_index(tmp_join_layer, HT_FIELD_NAME)
        
        svy_size_idx = layer_field_index(tmp_join_layer, AREA_FIELD_NAME)
        if svy_size_idx == -1:
            raise OperatorError("Field %s does not exist in %s" %(AREA_FIELD_NAME, svy_layer.name()))
        tax_idx = layer_field_index(tmp_join_layer, TAX_FIELD_NAME)
        if tax_idx == -1:
            raise OperatorError("Field %s does not exist in %s" %(TAX_FIELD_NAME, svy_layer.name()))
        
        # empty fields for holding the stats
        _zone_n_exp, _zone_p_exp, _zone_a_exp, _zone_e_exp = {}, {}, {}, {}
        _zone_group_counts, _zone_group_stories, _zone_group_weight = {}, {}, {}
        _zone_total_area, _zone_total_count, _zone_total_ht = {}, {}, {} 
        for _zone in zone_classes.iterkeys():
            _zone_n_exp[_zone] = {}
            _zone_p_exp[_zone] = {}
            _zone_a_exp[_zone] = {}
            _zone_e_exp[_zone] = {}
            _zone_group_counts[_zone] = {} 
            _zone_group_stories[_zone] = {}
            _zone_group_weight[_zone] = {}
            _zone_total_area[_zone] = 0
            _zone_total_count[_zone] = 0
            _zone_total_ht[_zone] = 0

        # associate group to ratio value
        for _rec in layer_features(tmp_join_layer):
            _ht = _rec.attributeMap()[svy_ht_idx].toInt()[0]
            _samp_grp = str(_rec.attributeMap()[svy_samp_idx].toString())            
            _tax_str = str(_rec.attributeMap()[tax_idx].toString())
            try:
                self._taxonomy.parse(_tax_str)            
                self.increment_dict(_zone_group_counts[_zone], _samp_grp, 1)
                self.increment_dict(_zone_group_stories[_zone], _samp_grp, _ht)
            except Exception as err:
                logAPICall.log("Error processing record %s" % err, logAPICall.WARNING)
            
        for _zone in zone_classes.iterkeys():
            if len(_zone_group_counts[_zone]) != 3:
                raise OperatorError("Survey must have 3 sampling groups", self.__class__)
            cmp_value = -1
            for _grp, _count in _zone_group_counts[_zone].iteritems():
                if cmp_value==-1:
                    cmp_value = _count
                if cmp_value != _count:
                    raise OperatorError("Survey groups must have same number of samples", self.__class__)
            # sort by stories        
            group_stories_for_sort = {}
            for _grp, _ht in _zone_group_stories[_zone].iteritems():
                group_stories_for_sort[_ht] = _grp
            sorted_keys = group_stories_for_sort.keys()
            sorted_keys.sort()
            # assign group to weight 
            for idx, key in enumerate(sorted_keys):
                _zone_group_weight[_zone][group_stories_for_sort[key]] = self.weights[idx]
                
        # aggregate values from survey for each building type
        # - count (n)
        # - floor area (p)
        # - total area (a)
        for _f in layer_features(tmp_join_layer):
            _zone_str = str(_f.attributeMap()[zone_idx].toString())
            _tax_str = str(_f.attributeMap()[tax_idx].toString())            
            _sample_grp = str(_f.attributeMap()[svy_samp_idx].toString())
            _sample_size = _f.attributeMap()[svy_size_idx].toDouble()[0]
            _sample_ht = _f.attributeMap()[svy_size_idx].toDouble()[0]            
            group_weight = _zone_group_weight[_zone]
            try:
                self._taxonomy.parse(_tax_str)            
                self.increment_dict(_zone_n_exp[_zone_str], _tax_str, group_weight[_sample_grp])
                self.increment_dict(_zone_p_exp[_zone_str], _tax_str, _sample_size*group_weight[_sample_grp])
                self.increment_dict(_zone_a_exp[_zone_str], _tax_str, _sample_size*_ht*group_weight[_sample_grp])
                self.increment_dict(_zone_e_exp[_zone_str], _tax_str, 0)
            except Exception as err:
                logAPICall.log("error processing sample with building type: %s" % _tax_str, logAPICall.WARNING)
                pass              

        # adjust ratio using footprint ht/area
        tmp_join_layername2 = 'join_%s' % get_unique_filename()
        tmp_join_file2 = self._tmp_dir + tmp_join_layername2 + '.shp'        
        analyzer = QgsOverlayAnalyzer()        
        analyzer.intersection(fp_layer, zone_layer, tmp_join_file2)        
        tmp_join_layer2 = load_shapefile(tmp_join_file2, tmp_join_layername)
        
        zone_idx = layer_field_index(tmp_join_layer2, zone_field)        
        area_idx = layer_field_index(tmp_join_layer2, area_field)
        ht_idx = layer_field_index(tmp_join_layer2, ht_field)        
        for _f in layer_features(tmp_join_layer2):
            _zone_str = str(_f.attributeMap()[zone_idx].toString())
            _area = _f.attributeMap()[area_idx].toDouble()[0]
            _ht = _f.attributeMap()[ht_idx].toDouble()[0]

            _zone_total_area[_zone_str] += _area
            _zone_total_count[_zone_str] += 1
            _zone_total_ht[_zone_str] += _ht
        
        # calculate building ratios for each zone        
        for _zone in zone_classes.iterkeys():
            # for total count (n) and area (a) 
            e_nt_cluster_total = sum(_zone_n_exp[_zone].itervalues())
            e_at_cluster_total = sum(_zone_a_exp[_zone].itervalues())            
            # E[A] estimated total building area for zone
            e_at_total = _zone_total_area[_zone] * _zone_total_ht[_zone]/_zone_total_count[_zone]
            
            # calculate expected values  
            for t, e_at_cluster in _zone_a_exp[_zone].iteritems():
                e_nt_cluster = _zone_n_exp[_zone][t]         
                if e_at_cluster == 0 or e_at_total == 0: 
                    # area is missing, use count instead
                    _zone_e_exp[_zone][t] = e_nt_cluster / e_nt_cluster_total
                    _zone_a_exp[_zone][t] = 0
                else:
                    # use ratio of area over total area
                    # E[f(t)] building fraction based on sampled area 
                    e_ft_cluster = e_at_cluster / e_at_cluster_total
                    # E[G(t)] average area per building 
                    e_gt_cluster = e_at_cluster / e_nt_cluster

                    # E[A(t)] estimated total building area for zone for building type
                    e_at = e_at_total * e_ft_cluster
                    # E[N(t)] estimated total number of buildings zone-wide by type
                    e_nt = e_at / e_gt_cluster
                                        
                    _zone_e_exp[_zone][t] = e_nt
                    _zone_a_exp[_zone][t] = e_ft_cluster
        
        # convert the building ratios
        logAPICall.log('create mapping scheme for zones', logAPICall.DEBUG)
        ms = MappingScheme(self._taxonomy)
        for _zone in zone_classes.iterkeys():
            # create mapping scheme for zone
            stats = Statistics(self._taxonomy)

            # use building ratio to create statistic
            for _tax_str, _e_exp in _zone_e_exp[_zone].iteritems():
                for i in range(int(_e_exp*1000)):
                    stats.add_case(_tax_str, self._parse_order, self._parse_modifiers)
            # finalize call is required 
            stats.finalize()
            ms.assign(MappingSchemeZone(_zone), stats)            
        
        # clean up
        del tmp_join_layer, analyzer
        remove_shapefile(tmp_join_file)
        
        # assign output        
        self.outputs[0].value = ms
        self.outputs[1].value = _zone_a_exp    
    
    def increment_dict(self, dict_stat, key, value):
        if dict_stat.has_key(key):
            dict_stat[key] += value
        else:
            dict_stat[key] = value