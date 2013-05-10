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
        
