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
