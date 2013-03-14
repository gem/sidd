# Copyright (c) 2011-2013, ImageCat Inc.
#
# SIDD is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
#
"""
module to support exposure export 
"""
from sidd.operator import Operator

class NullWriter(Operator):
    def __init__(self, options=None, name="Grid Writer"):
        """ constructor """
        super(NullWriter, self).__init__(options, name)
        self._tmp_dir = options['tmp_dir']

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
        return []
        
    @property    
    def output_names(self):
        return []
    
    output_descriptions = output_names
    
    def do_operation(self):
        """ perform export operation """ 
        pass
        
    # protected method override
    ###########################

    def _verify_inputs(self, inputs):
        """ perform operator specific input validation """ 
        pass

    def _verify_outputs(self, outputs):
        """ perform operator specific input validation """
        pass
        
