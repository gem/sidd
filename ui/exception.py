# Copyright (c) 2011-2013, ImageCat Inc.
#
# SIDD is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
#
"""
Main application UI exceptions
"""

from exceptions import Exception

class SIDDUIException(Exception):
    """ SIDD application UI exceptions """
    def __init__(self, msg):
        super(SIDDUIException, self).__init__(msg)

class SIDDRangeGroupException(Exception):
    """ exception thrown during attribute value range grouping """
    def __init__(self, msg):
        super(SIDDRangeGroupException, self).__init__(msg)
