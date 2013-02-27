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
from os import path
import csv

from sidd.constants import logAPICall
from sidd.operator.data import OperatorDataTypes
from sidd.operator import OperatorError

from writer import NullWriter

class MSLeavesCSVWriter(NullWriter):
    def __init__(self, options=None, name="Grid Writer"):
        """ constructor """
        super(MSLeavesCSVWriter, self).__init__(options, name)

    # self documenting method override
    ###########################
    @property
    def input_types(self):
        return [OperatorDataTypes.MappingScheme,
                OperatorDataTypes.StringAttribute,]
        
    @property    
    def input_names(self):
        return ["Mapping Scheme",
                "Output folder",]

    input_descriptions = input_names
   
    @logAPICall
    def do_operation(self):
        """ perform export operation """
        ms = self.inputs[0].value
        folder = self.inputs[1].value
        
        #test for output folder
        if not path.exists(folder):
            raise OperatorError("destination folder %s does not exist" % folder,
                                self.__class__)
                        
        for zone, stats in ms.assignments():
            # create writer 
            with open('%s/zone_%s.csv' % (folder, zone.name), 'wb') as csvfile:
                csvwriter = csv.writer(csvfile, delimiter=',',
                                      quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
                csvwriter.writerow(['Building Type', 'Building Fraction'])
                for leaf in stats.get_leaves(True, True):
                    csvwriter.writerow([str(leaf[0]), leaf[1]*100.0])                        
