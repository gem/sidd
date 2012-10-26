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
# Version: $Id: data.py 21 2012-10-26 01:48:25Z zh $

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