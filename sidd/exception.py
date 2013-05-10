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
SIDD application errors
"""
class SIDDException(Exception):
    """ SIDD application errors """
    def __init__(self, msg):
        super(SIDDException, self).__init__(msg)

class SIDDProjectException(Exception):
    """ project processing errors """
    def __init__(self, error, msg=''):
        self.error = error
        super(SIDDProjectException, self).__init__(msg)

class WorkflowException(Exception):
    """ Workflow related errors """    
    def __init__(self, error, msg=''):
        super(WorkflowException, self).__init__(msg)
        self.error = error