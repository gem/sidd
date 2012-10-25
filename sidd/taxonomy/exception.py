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
# Version: $Id: exception.py 9 2012-09-28 16:19:05Z zh $

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