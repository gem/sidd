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