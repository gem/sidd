# Copyright (c) 2011-2013, ImageCat Inc.
#
# SIDD is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
#
"""
Mapping scheme related exception and errors
"""

from sidd.exception import SIDDException

class StatisticError(SIDDException):
    """ errors caused by Statistic handling """
    def __init__(self, msg):
        Exception.__init__(self, msg)

class StatisticNodeError(SIDDException):
    """ errors caused by Statistic nodes handling """
    pass
