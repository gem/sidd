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
# Version: $Id: logger.py 18 2012-10-24 20:21:41Z zh $

"""
configurable logging system for SIDD application
"""

import logging
import functools
import types

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
            return f(*args, **kw)
        return wrapper

    def setLevel(self, level):
        self.level = level
        #self.logger.setLevel(level)

    def log(self, msg, level=INFO):
        """ write log message according to internal configuration """        
        if level < self.level:
            return
        if level == self.ERROR:
            import traceback
            traceback.print_exc()
        self.functions[level](msg)
