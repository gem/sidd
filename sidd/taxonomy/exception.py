# Copyright (c) 2011-2013, ImageCat Inc.
#
# SIDD is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
#
"""
module contains taxonomy exceptions
"""

from sidd.exception import SIDDException
class TaxonomyError(SIDDException):
    def __init__(self, msg):
        Exception.__init__(self, msg)

class TaxonomyParseError(SIDDException):
    def __init__(self, msg):
        Exception.__init__(self, msg)