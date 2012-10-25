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
# Version: $Id: ms.py 18 2012-10-24 20:21:41Z zh $

"""
module constains class for loading mapping scheme files
mapping scheme format defined in ms module
"""
from os.path import exists

from sidd.constants import logAPICall
from sidd.operator import *
from sidd.taxonomy import get_taxonomy
from sidd.ms.ms import MappingScheme

class MappingSchemeLoader(Operator):
    """ operator loading mapping scheme from XML """
    def __init__(self, options=None, name='Mapping Scheme Loaded'):
        """ constructor """
        Operator.__init__(self, options,  name)
        self._taxonomy = get_taxonomy(options['taxonomy'])

    # self documenting method override
    ###########################
    
    @property
    def input_types(self):
        return [OperatorDataTypes.File]
        
    @property    
    def input_names(self):
        return ["Mapping Scheme File"]
    
    input_descriptions = input_names

    @property
    def output_types(self):
        return [OperatorDataTypes.MappingScheme]
        
    @property    
    def output_names(self):
        return ["Mapping Scheme"]


    # public method override
    ###########################
    
    @logAPICall
    def do_operation(self):
        """ perform ms loading """
        
        # verify that input/output data is correctly set
        in_file = self.inputs[0].value       
        
        # load data        
        ms = MappingScheme(self._taxonomy)
        ms.read(in_file)
        
        # verify that input data is loaded correctly
        if not ms.is_valid:
            raise OperatorError('Error Loading data file' % (in_file), self.__class__)
            
        self.outputs[0].value = ms

    # protected method override
    ###########################

    def _verify_inputs(self, inputs):
        """ perform operator specific output validation """
        if not exists(inputs[0].value):
            raise OperatorDataError("input file %s does not exist" % (inputs[0].value))
    
    def _verify_outputs(self, outputs):
        """ perform operator specific output validation """
        pass
