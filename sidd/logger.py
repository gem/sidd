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
configurable logging system for SIDD application
"""

import logging
import functools
import types
import traceback

class SIDDLogging(object):
    """ logging decorator class """
    ERROR = 50
    WARNING = 40
    INFO = 30
    DEBUG = 20
    DEBUG_L2 = 10
    
    def __init__(self, name, level=0):
        self.logger = logging.getLogger(name)        
        self.level = level
        self.functions = {
            self.ERROR:self.logger.error,
            self.WARNING:self.logger.warning,
            self.INFO:self.logger.info,
            self.DEBUG:self.logger.debug,
            self.DEBUG_L2:self.logger.debug,
        }

    def __call__(self, f):
        """ create wrapper for function calls """
        @functools.wraps(f)
        def wrapper(*args, **kw):
            if isinstance(f, types.MethodType):
                self.func_name = f.im_class + '.' + f.__name__
            else:
                self.func_name = f.__name__
            self.mod_name = f.__module__
            self.log('function call %s from module %s' % (self.func_name,
                                                          self.mod_name),
                     logging.DEBUG)            
            try:
                return f(*args, **kw)
            except Exception, err:
                raise err
        return wrapper

    def setLevel(self, level):
        self.level = level
        #self.logger.setLevel(level)

    def log(self, msg, level=INFO):
        """ write log message according to internal configuration """        
        if level < self.level:
            return
        if level == self.ERROR:            
            traceback.print_exc()
        else:
            self.functions[level](msg)
