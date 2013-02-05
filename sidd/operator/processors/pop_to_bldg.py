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
# Version: $Id: pop_to_bldg.py 18 2012-10-24 20:21:41Z zh $

"""
module constains class for converting population count to building count
"""
from sidd.operator import Operator

class PopulationToBuildingMapper(Operator):    
    
    def __init__(self, options=None, name="Population To Building Mapper"):
        Operator.__init__(self, options, name)

    # self documenting method override
    ###########################

    # public method override
    ###########################

    def do_operation(self):
        # verify that input/output data is correctly set
        pass 
        
        # store data in output

    # protected method override
    ###########################
    def _verify_inputs(self, inputs):
        """ perform operator specific input validation """
        pass

    def _verify_outputs(self, outputs):
        """ perform operator specific output validation """
        pass
