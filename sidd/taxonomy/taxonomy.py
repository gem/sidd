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
module contains abstract taxonomy interface to be extended
"""
class Taxonomy(object):
    """
    main Taxonomy class
    with serializing and deserializing functinos
    """
    
    def __init__(self):
        """ constructor """
        raise NotImplementedError("abstract method not implemented")
    
    @property
    def name(self):
        raise NotImplementedError("abstract method not implemented")

    @property
    def description(self):
        raise NotImplementedError("abstract method not implemented")
      
    @property
    def version(self):
        raise NotImplementedError("abstract method not implemented")
    
    @property
    def attributes(self):
        raise NotImplementedError("abstract method not implemented")
    
    @property
    def defaults(self):
        raise NotImplementedError("abstract method not implemented")
    
    @property
    def codes(self):
        raise NotImplementedError("abstract method not implemented")

    def get_attribute_by_name(self, name):
        raise NotImplementedError("abstract method not implemented")

    def get_code_by_name(self, name):
        raise NotImplementedError("abstract method not implemented")
    
    def parse(self, string):
        raise NotImplementedError("abstract method not implemented")
    
    def separator(self, separator_type=None):
        raise NotImplementedError("abstract method not implemented")
    
    def to_string(self, attributes):
        raise NotImplementedError("abstract method not implemented")
    
    def is_valid_string(self, tax_string):
        raise NotImplementedError("abstract method not implemented")
    
class TaxonomyAttribute(object):
    """
    TaxonomyAttribute is a building characteristic that can be
    represented by the taxonomy
    """
    
    def __init__(self, name="", order=1, levels=1, default="", attribute_type=1):
        """ constructor """
        self.__name = name
        self.__order = order
        self.__levels = levels
        self.__default = default
        self.__type = attribute_type

    def __str__(self):
        """ string representation """
        return "name:%s\ttype:%s\torder:%s\t\tdefault=%s" % (
            self.__name, self.__type, self.__order, self.__default)

    @property
    def name(self):
        return self.__name

    @property
    def order(self):
        return self.__order

    @order.setter
    def order(self, order):
        self.__order = order
    
    @property
    def levels(self):
        return self.__levels

    @property
    def default(self):
        return self.__default

    @property
    def type(self):
        return self.__type

    def get_valid_codes(self, parent=None, levels=None):
        raise NotImplementedError("abstract method not implemented")
    
    def make_string(self, values, qualifier=None):
        raise NotImplementedError("abstract method not implemented")
    
class TaxonomyAttributeValue(object):
    """
    This is an abstract class that can be derived to stores valid value
    for a taxonomy attribute 
    """

    def __init__(self, attribute):
        """ constructor """
        self.__attribute = attribute
        self.__is_empty = True
    
    @property
    def attribute(self):
        return self.__attribute
    
    @property
    def is_empty(self):        
        return self.__is_empty

class TaxonomyAttributeMulticodeValue(TaxonomyAttributeValue):
    """
    This class represent a valid taxonomy value that is composed
    of a set of valid codes
    """
    
    def __init__(self, attribute):
        """ constructor """
        TaxonomyAttributeValue.__init__(self, attribute)
        self.__codes = []

    def __str__(self):
        """ string representation """
        raise NotImplementedError("taxonomy specific implementation is required")
    
    @property
    def is_empty(self):
        return len(self.__codes)==0
    
    @property
    def codes(self):
        return self.__codes

    def add_value(self, code):
        """ add another code to set """
        self.__codes.append(code)
        self.__is_empty = False
        
class TaxonomyAttributeSinglecodeValue(TaxonomyAttributeValue):
    """
    This class represent a valid taxonomy value that is composed
    of a valid code    
    """
    
    def __init__(self, attribute):
        """ constructor """
        TaxonomyAttributeValue.__init__(self, attribute)
        self.__code = None

    def __str__(self):
        """ constructor """
        raise NotImplementedError("taxonomy specific implementation is required")

    @property
    def is_empty(self):
        return self.__code == None
    
    @property
    def code(self):
        return self.__code
    
    def add_value(self, code):
        """ set code """
        self.__code = code
        self.__is_empty = False
        
class TaxonomyAttributePairValue(TaxonomyAttributeValue):
    """
    This class represent a valid taxonomy value that is composed
    of a valid code and associated value pair
    """
    
    def __init__(self, attribute):
        """ constructor """
        TaxonomyAttributeValue.__init__(self, attribute)
        self.__code = None
        self.__value = None

    def __str__(self):
        """ string representation """
        raise NotImplementedError("taxonomy specific implementation is required")

    @property
    def is_empty(self):
        return self.__code == None    
    
    @property
    def code(self):
        return self.__code
    
    @property
    def value(self):
        return self.__value

    def add_value(self, code, value):
        """ set code / value pair """
        self.__code = code
        self.__value = value
        self.__is_empty = False

class TaxonomyAttributeCode(object):
    """
    TaxonomyAttributeCode stores an acceptable code for the Taxonomy    
    """
    
    def __init__(self, attribute, level, code, description, scope=''):
        """ constructor """
        self.__attribute = attribute
        self.__level = level
        self.__code = code
        self.__desc = description
        self.__scope = scope

    def __str__(self):
        """ string representation """
        return "%s[%d]: %s (%s)" % (self.__attribute.name, self.__level, self.__code, self.__desc)
        
    @property
    def attribute(self):
        return self.__attribute
    
    @property
    def level(self):
        return self.__level
    
    @property
    def format(self):
        return self.__attribute.format

    @property
    def order(self):
        return self.__attribute.order
    
    @property
    def code(self):
        return self.__code
    
    @property
    def description(self):
        return self.__desc
    
    @property
    def scope(self):
        return self.__scope
