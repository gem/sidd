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
module contains class for applying mapping scheme
"""
from utils.shapefile import layer_features, layer_field_index

from sidd.constants import logAPICall, CNT_FIELD_NAME
from sidd.operator import Operator, OperatorError
from sidd.operator.data import OperatorDataTypes

class ExposureAnalyzer(Operator):
    def __init__(self, options=None, name='Exposure Analyzer'):
        super(ExposureAnalyzer, self).__init__(options, name)
    
    # self documenting method override
    ###########################
    
    @property
    def input_types(self):
        return [OperatorDataTypes.Exposure]
        
    @property
    def input_names(self):
        return ["Regional Exposure"]
    
    input_descriptions = input_names

    @property
    def output_types(self):
        return [OperatorDataTypes.Report]        
        
    @property    
    def output_names(self):
        return ["Exposure Analysis Report"]
    
    output_descriptions = output_names

    def _get_exposure_total(self, exposure, cnt_field):
        total_exposure=0
        try:
            cnt_idx = layer_field_index(exposure, cnt_field)
            for f in layer_features(exposure):
                total_exposure += f.attributeMap()[cnt_idx].toDouble()[0]                
        except Exception as err:
            raise OperatorError("error reading count from exposure: %s" % err, self.__class__)
        return total_exposure
        
    # protected method override
    ###########################    
    def _verify_inputs(self, inputs):
        """ perform operator specific input validation """
        pass

    def _verify_outputs(self, outputs):
        """ perform operator specific output validation """
        pass
    
class ExposureFragmentationAnalyzer(ExposureAnalyzer):
    def __init__(self, options=None, name='Exposure Count Analyzer'):
        super(ExposureFragmentationAnalyzer, self).__init__(options, name)

    # protected method override
    ###########################
    @logAPICall
    def do_operation(self):
        exposure = self.inputs[0].value
        
        frac_count, rec_count = 0, 0
        try:
            cnt_idx = layer_field_index(exposure, CNT_FIELD_NAME)
            for f in layer_features(exposure):
                rec_count += 1
                count = f.attributeMap()[cnt_idx].toDouble()[0]
                if count < 1:
                    frac_count+=1
        except Exception as err:
            raise OperatorError("error reading exposure: %s" % err, self.__class__)
        
        self.outputs[0].value = {'record_count':rec_count, 'fraction_count':frac_count}  
    
class ExposureZoneCountAnalyzer(ExposureAnalyzer):    
    def __init__(self, options=None, name='Exposure Count Analyzer'):
        super(ExposureZoneCountAnalyzer, self).__init__(options, name)

    # self documenting method override
    ###########################
        
    @property
    def input_types(self):
        return [OperatorDataTypes.Exposure,
                OperatorDataTypes.Zone,
                OperatorDataTypes.StringAttribute,]
        
    @property
    def input_names(self):
        return ["Regional Exposure",
                "Zone data Layer",
                "Building Count field"]        
    
    input_descriptions = input_names
    
    # protected method override
    ###########################
    @logAPICall
    def do_operation(self):
        exposure = self.inputs[0].value
        zone_layer = self.inputs[1].value
        cnt_field = self.inputs[2].value

        try:
            # get total building count from exposure
            total_exposure = self._get_exposure_total(exposure, CNT_FIELD_NAME)
            
            # get total building count from zone
            total_zone = 0 
            
            cnt_idx = layer_field_index(zone_layer, cnt_field)
            for f in layer_features(zone_layer):                
                total_zone += f.attributeMap()[cnt_idx].toDouble()[0]
        except Exception as err:
            raise OperatorError("error reading count from zone: %s" % err, self.__class__)        

        self.outputs[0].value = {"total_exposure":total_exposure, 
                                 "total_source":total_zone}

class ExposureFootprintCountAnalyzer(ExposureAnalyzer):    
    def __init__(self, options=None, name='Exposure Count Analyzer'):
        super(ExposureFootprintCountAnalyzer, self).__init__(options, name)

    # self documenting method override
    ###########################
        
    @property
    def input_types(self):
        return [OperatorDataTypes.Exposure,
                OperatorDataTypes.Footprint,]
        
    @property
    def input_names(self):
        return ["Regional Exposure",
                "Building Footprints"]        
    
    input_descriptions = input_names
    
    # protected method override
    ###########################
    @logAPICall
    def do_operation(self):
        exposure = self.inputs[0].value
        fp_layer = self.inputs[1].value
                
        # get total building count from exposure
        total_exposure = self._get_exposure_total(exposure, CNT_FIELD_NAME)   

        try:        
            total_fp = fp_layer.dataProvider().featureCount()
        except Exception as err:
            raise OperatorError("error reading count from zone: %s" % err, self.__class__)          

        self.outputs[0].value = {"total_exposure":total_exposure, 
                                 "total_source":total_fp}          