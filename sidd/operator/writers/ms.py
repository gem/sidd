# Copyright (c) 2011-2013, ImageCat Inc.
#
# SIDD is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
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
