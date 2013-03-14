# Copyright (c) 2011-2013, ImageCat Inc.
#
# SIDD is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
#
"""
Mapping scheme is a statiscal translation useful for assigning structural
attributes for a building stock
"""

from statistic import Statistics
from node import StatisticNode, StatisticModifier
from exceptions import StatisticError, StatisticNodeError
from ms import MappingScheme, MappingSchemeZone