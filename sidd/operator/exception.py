# Copyright (c) 2011-2013, ImageCat Inc.
#
# SIDD is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
#
"""
SIDD operators errors
"""
from sidd.exception import SIDDException

class OperatorDataError(SIDDException): 
    """ SIDD operators data errors """
    def __init__(self, msg):
        Exception.__init__(self, msg)


class OperatorError(SIDDException):
    """ SIDD operators data errors """
    
    def __init__(self, msg, source):
        Exception.__init__(self, msg)
        self.error_source=source
    
    @property
    def source(self):
        return self.error_source
        