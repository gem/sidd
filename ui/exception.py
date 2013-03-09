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
# Version: $Id: exception.py 14 2012-10-16 22:25:11Z zh $

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
