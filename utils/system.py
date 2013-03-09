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
# Version: $Id: system.py 18 2012-10-24 20:21:41Z zh $

"""
system helper functions
"""

import os
import random
import datetime

from PyQt4.QtCore import QDir

def get_random_name(length=0):
    """ return random file name """
    if length==0:
        length = random.randint(6,10)
    _name = ''

    # acceptable characters for random directory name
    acceptable = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789';
    for i in range(length):
        _name += acceptable[random.randint(0, len(acceptable)-1)]
    return _name

def get_unique_filename():    
    return get_random_name(3) + datetime.datetime.now().strftime('%y%m%d%H%M%S')

def get_temp_dir(dirname=''):
    """ get path to temporary directory """
    temp = str(QDir.tempPath()+'/sidd/')
    if not os.path.exists(temp):
        os.mkdir(temp)    
    if dirname != '':
        temp = temp + dirname + '/'
        if not os.path.exists(temp):
            os.mkdir(temp)
    return temp
    
def get_user_dir():
    """ get path to user directory """    
    home = str(QDir.homePath()+'/.sidd/')
    if not os.path.exists(home):
        os.mkdir(home)
    return home

def get_app_dir():
    """ get the path to the application's root directory."""    
    return str(QDir.currentPath())

def get_dictionary_value(dictionary, key, default):
    """ return value in dictionary for given key if key exists, or default if not """
    if dictionary.has_key(key):
        return dictionary[key]
    else:
        return default