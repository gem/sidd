# Copyright (c) 2011-2013, ImageCat Inc.
#
# SIDD is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
#
"""
SIDD operators data types
"""
from utils.enum import Enum
from sidd.constants import logAPICall

OperatorDataTypes = Enum(
    # input for loader
    "File",
    "StringAttribute",
    "NumericAttribute",
    
    # internal data types
    "Population",
    "Footprint",
    "FootprintHt",
    "Survey",
    "Zone",
    "ZoneBldgCount",
    "ZoneStatistic",
    "MappingScheme",
    "Grid",
    "Layer",
    "Exposure",
    "Report",
    
    # formula
    "PopulationToBuilding",
    
    # data format
    "Shapefile",
    "XMLFile",
    )

class OperatorData(object):
    """ operator data container """
    def __init__(self, data_type, value=None):
        """ constructor """
        self.type = data_type
        self.value = value
    
    def __eq__(self, other):
        """ compare two operator data object """
        logAPICall.log('comparing self.type(%s) and other.type(%s)' % (self.type, other.type),
                       logAPICall.DEBUG_L2)
        return self.type == other.type
    
    @logAPICall
    def __str__(self):
        """ return string representation of an operator data object"""
        return "OperatorData (%s)" % (self.type)