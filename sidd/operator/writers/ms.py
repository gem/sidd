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
from os import path
import csv

from sidd.constants import logAPICall
from sidd.operator.data import OperatorDataTypes
from sidd.operator import OperatorError

from writer import NullWriter

class MSLeavesCSVWriter(NullWriter):
    def __init__(self, options=None, name="Mapping Scheme CSV Writer"):
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
        output_file = self.inputs[1].value

        base_name = output_file[:-3]
        for zone, stats in ms.assignments():
            # create writer 
            with open('%s_%s.csv' % (base_name, zone.name), 'wb') as csvfile:
                csvwriter = csv.writer(csvfile, delimiter=',',
                                      quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
                csvwriter.writerow(['Building Type', 'Building Fraction'])
                if len(stats.leaves) == 0:
                    stats.refresh_leaves(with_modifier=True, order_attributes=False, fill_missing=False)
                for leaf in stats.leaves:
                    csvwriter.writerow([str(leaf[0]), leaf[1]*100.0])
                                            
class MSXMLWriter(MSLeavesCSVWriter):
    def __init__(self, options=None, name="Mapping Scheme XML Writer"):
        """ constructor """
        super(MSXMLWriter, self).__init__(options, name)
        

    @logAPICall
    def do_operation(self):
        """ perform export operation """
        ms = self.inputs[0].value
        output_file = self.inputs[1].value        
        ms.save(output_file, pretty=True)
