# Copyright (c) 2011-2013, ImageCat Inc.
#
# SIDD is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
#
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