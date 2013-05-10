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
module for managing SIDD runtime configuration
"""

import types

from ConfigParser import ConfigParser

class SIDDConfig(object):
    """
    manage SIDD configurations from two sources
    - default configurations stored in app.cfg in application main directory
    - user specific configuration stored in my.cfg under user directory
    """
    # default application config file
    ###########################
    def __init__(self, config_file):
        self.config = ConfigParser()
        self.config_file = config_file
        self.read_configs()
    
    def __del__(self):        
        self.save_configs()

    # config file operations
    ###########################

    def read_configs(self):
        """
        read configuration file in following order
        1. default file
        2. user file
        """
        #self.config.read(self.DEFAULT_CONFIG_FILE)
        self.config.read(self.config_file)

    def save_configs(self):        
        with open(self.config_file, 'w') as config_file:
            self.config.write(config_file)

    # config item accesor
    ###########################

    def get(self, section, option, default, data_type=types.StringType):
        """
        get configuration value for given section/option
        set to default if missing
        type can be used to adjust the type of value read
        """
        return_val = default
        
        # retrieve configuration value as an array 
        if data_type == types.ListType:                         
            return_val = eval(self.config.get(section, option), {},{})
        else:
            # retrieve configuration as single value
            if data_type == types.FloatType:
                get_func = self.config.getfloat
            elif data_type == types.IntType:
                get_func = self.config.getint           
            elif data_type == types.BooleanType:
                get_func = self.config.getboolean
            else:            
                get_func = self.config.get
    
            # retrieve value and cast into appropriate type
            # return default, if cast fail or config not found                    
            try:
                if self.config.has_option(section, option):
                    return_val = get_func(section, option)           
            except:
                pass
        return return_val 
    
    def set(self, section, option, value):
        self.config.set(section, option, value)
