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
# Version: $Id: exception.py 18 2012-10-24 20:21:41Z zh $

"""
SIDD application errors
"""
class SIDDException(Exception):
    """ SIDD application errors """
    def __init__(self, msg):
        super(SIDDException, self).__init__(msg)

class WorkflowException(Exception):
    """ Workflow related errors """    
    
    def __init__(self, error):
        super(WorkflowException, self).__init__(
            'Exception occured while building workflow')
        self.error = error