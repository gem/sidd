# Copyright (c) 2011-2013, ImageCat Inc.
#
# SIDD is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
#
"""
system helper functions
"""

import os
import fnmatch
import shutil
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
    
def delete_folders_in_dir(dirname='.', pattern='*.*'):    
    for folder in os.listdir(dirname):
        fullpath_folder = os.path.join(dirname, folder)
        if os.path.isdir(fullpath_folder) and fnmatch.fnmatch(folder, pattern):
            shutil.rmtree(fullpath_folder)
    
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