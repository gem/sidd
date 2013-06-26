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
base class for SIDD operators 
"""
from qgis.core import QgsCoordinateReferenceSystem

from sidd.constants import logAPICall, LON_FIELD_NAME, LAT_FIELD_NAME, TAX_FIELD_NAME, GID_FIELD_NAME
from data import OperatorData
from exception import OperatorError, OperatorDataError
from utils.shapefile import layer_field_index

class Operator(object):
    """
    base abstract class for SIDD operators 
    """
    # operator name
    _name = ""
    # list of inputs, inputs will be validated before operation 
    _inputs = []
    # list of outputs, outputs will be validated before operation
    _outputs = []

    # static factory method 
    ###########################

    @staticmethod
    @logAPICall
    def get_operator(op_name, options=[]):
        """ factory method to create a new operator """        
        tokens = op_name.split('.')
        if len(tokens) < 1:
            raise OperatorError('Cannot initantiace operator %s' % op_name)
        try:
            module = __import__('.'.join(tokens[0:-1]))
            class_ = getattr(module, tokens[-1])
            return class_(options)
        except ImportError:
            raise OperatorError('Cannot initantiace operator %s' % op_name)
        except Exception:
            raise OperatorError('Cannot initantiace operator %s' % op_name)

    def __init__(self, options=None, name=__name__):
        """ constructor """
        self._options = options
        self._name = name
        
        # common parameters to be used operators when creating temp GIS files
        self._crs = QgsCoordinateReferenceSystem(4326, QgsCoordinateReferenceSystem.PostgisCrsId)
        self._lon_field = LON_FIELD_NAME 
        self._lat_field = LAT_FIELD_NAME 
        self._tax_field = TAX_FIELD_NAME
        self._gid_field = GID_FIELD_NAME 

    # self documenting method signatures
    ###########################
    
    @property 
    def name(self):
        return self._name

    @property
    def input_types(self):
        raise NotImplementedError("abstract method not implemented")
        
    @property    
    def input_names(self):
        raise NotImplementedError("abstract method not implemented")      

    @property
    def input_descriptions(self):
        raise NotImplementedError("abstract method not implemented")      

    @property
    def output_types(self):
        raise NotImplementedError("abstract method not implemented")      
        
    @property    
    def output_names(self):
        raise NotImplementedError("abstract method not implemented")      
    
    @property
    def output_descriptions(self):
        raise NotImplementedError("abstract method not implemented")      

    def set_inputs(self, inputs):
        """ set and validate operator inputs """
        
        # make sure each input is of type Operator Data
        for _in in inputs:
            if not isinstance(_in, OperatorData):
                raise OperatorDataError(
                    "Operator %s only accept input type OperatorData, found %s "
                    % (self.name, type(_in)))

        # check input size
        if (len(inputs) != len(self.input_types)):
            raise OperatorDataError("incorrect number of inputs")
        
        # verify input types
        _i = 1
        for _input, _expected in map(None, inputs, self.input_types):
            if _input.type != _expected:                
                raise OperatorDataError("Operator %s: incorrect type for input %d. expected %s, found %s."
                                        %(self.name, _i, _expected, _input.type))
            _i += 1

        # additional verification specific to operator
        self._verify_inputs(inputs)
        
        # at this step, input is validated
        self._inputs = inputs
    
    def get_inputs(self):
        """ return operator inputs """
        return self._inputs
    
    # property access to operator input
    inputs = property(get_inputs, set_inputs)
    
    def get_outputs(self):
        """ return operator outpus """
        return self._outputs
    
    def set_outputs(self, outputs):
        """ set and validate operator outputs """

        # make sure each output is of type Operator Data
        for _out in outputs:
            if not isinstance(_out, OperatorData):
                raise OperatorDataError(
                    "Operator %s only accept output type OperatorData, found %s "
                    % (self.name, type(_out)))

        # check out size
        if (len(outputs) != len(self.output_types)):
            raise OperatorDataError("incorrect number of output")
        
        # verify output types
        _i = 1
        for _output, _expected in map(None, outputs, self.output_types):
            if _output.type != _expected:
                raise OperatorDataError(
                    "Operator %s: incorrect type for output %d. expected %s, found %s."
                    %(self.name, _i, _expected, _output.type))
            _i += 1

        # additional verification specific to operator
        self._verify_outputs(outputs)

        # at this step, output is validated
        self._outputs = outputs
    
    # property access to operator output  
    outputs = property(get_outputs, set_outputs)
    
    # public methods signature
    ###########################
    
    def do_operation(self):
        """ perform operator action. must be implemented in subclass """
        raise NotImplementedError("abstract method not implemented")      

    # protected methods signature
    ###########################

    def _verify_inputs(self, inputs):
        """
        perform operator specific input validation.
        must be implemented in subclass
        """
        raise NotImplementedError("abstract method not implemented")      

    def _verify_outputs(self, outputs):
        """
        perform operator specific output validation.
        must be implemented in subclass
        """
        raise NotImplementedError("abstract method not implemented")     
    
    # common input test methods
    ###########################
    
    def _test_layer_loaded(self, layer):        
        if layer.dataProvider() is None:
            raise OperatorDataError("layer %s not correctly loaded" % layer.name())
    
    def _test_layer_field_exists(self, layer, field):
        idx = layer_field_index(layer, field) 
        if idx == -1:
            raise OperatorDataError("field %s not found in input layer" % field)
        return idx

class EmptyOperator(Operator):
    '''
    Empty Operator implements all the abstract methods from Operator      
    '''
    def __init__(self, options=None, name="Empty Operator"):
        super(EmptyOperator, self).__init__(options, name)

    # self documenting methods
    ###########################    
    @property
    def input_types(self):
        return []
        
    @property    
    def input_names(self):
        return []      

    @property
    def input_descriptions(self):
        return []      

    @property
    def output_types(self):
        return []      
        
    @property    
    def output_names(self):
        return []      
    
    @property
    def output_descriptions(self):
        return []

    # public methods signature
    ###########################
    
    def do_operation(self):        
        pass      

    # protected methods signature
    ###########################

    def _verify_inputs(self, inputs):
        pass

    def _verify_outputs(self, outputs):
        pass