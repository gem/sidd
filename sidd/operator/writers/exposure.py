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
# Version: $Id: exposure.py 18 2012-10-24 20:21:41Z zh $

"""
module to support exposure export 
"""
from PyQt4.QtCore import *
from qgis.core import *

from utils.shapefile import *

from sidd.constants import *
from sidd.operator import *

class ExposureSHPWriter(Operator):
    def __init__(self, options=None, name="Grid Writer"):
        """ constructor """
        super(ExposureSHPWriter, self).__init__(options, name)
        self._tmp_dir = options['tmp_dir']

    # self documenting method override
    ###########################

    @property
    def input_types(self):
        return [OperatorDataTypes.Shapefile,
                OperatorDataTypes.File,]
        
    @property    
    def input_names(self):
        return ["Exposure shapefile",
                "Output path",]
    
    input_descriptions = input_names

    @property
    def output_types(self):
        return []
        
    @property    
    def output_names(self):
        return []
    
    output_descriptions = output_names
    
    @logAPICall
    def do_operation(self):
        """ perform export operation """        
        # input/output data checking already done during property set
        input_file = self.inputs[0].value
        output_file = self.inputs[1].value
        
        copy_shapefile(input_file, output_file)
        
    # protected method override
    ###########################

    def _verify_inputs(self, inputs):
        """ perform operator specific input validation """ 
        pass

    def _verify_outputs(self, outputs):
        """ perform operator specific input validation """
        pass
        
class ExposureKMLWriter(ExposureSHPWriter):    
    def __init__(self, options=None, name="Grid Writer"):
        """ constructor """
        super(ExposureKMLWriter, self).__init__(options, name)

    def do_operation(self):
        """ perform export operation """        
        # input/output data checking already done during property set
        input_file = self.inputs[0].value
        output_file = self.inputs[1].value
        
        shapefile_to_kml(input_file, output_file)

class ExposureNRMLWriter(ExposureSHPWriter):
    def __init__(self, options=None, name="Grid Writer"):
        """ constructor """
        super(ExposureKMLWriter, self).__init__(options, name)

