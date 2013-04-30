# Copyright (c) 2011-2013, ImageCat Inc.
#
# SIDD is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
#
"""
module supporting GEM taxonomy version 1
"""
import sqlite3
import os
import re
import copy
from operator import attrgetter

from sidd.constants import logAPICall
from sidd.taxonomy import Taxonomy, TaxonomyAttribute, TaxonomyAttributeCode
from sidd.taxonomy import TaxonomyError, TaxonomyParseError
from sidd.taxonomy import TaxonomyAttributeMulticodeValue, TaxonomyAttributePairValue, TaxonomyAttributeSinglecodeValue

from utils.enum import Enum

class GemTaxonomy(Taxonomy):
    """
    main taxonomy class
    """
    
    # protected member attributes
    __GEM_TAXONOMY_FILE = 'gem_v1.0.1.db'
    __attrs = []
    __codes = {}
    __empty = []
    __defaults = []
    __initialized = False
    
    Separators = Enum("Attribute", "Level")
    
    def __init__(self):        
        db_path = os.path.dirname( __file__ ) + os.path.sep + self.__GEM_TAXONOMY_FILE
        if not os.path.exists(db_path):
            raise TaxonomyError("gem taxonomy db not found")

        # open associated sqlite DB and load attributes
        self.__initialize(db_path)

    @property
    def name(self):
        return "Gem"

    @property
    def description(self):
        return "Gem Taxonomy"
        
    @property
    def version(self):
        return "1.0"
    
    @property
    def attributes(self):
        attrs = GemTaxonomy.__attrs
        attrs.sort(key=attrgetter('order'))      
        return attrs
    
    @property
    def defaults(self):
        return self.__defaults

    @property
    def attribute_separator(self):
        return '/'
    
    @property
    def level_separator(self):
        return '+'
    
    @property
    def value_separator(self):
        return ':'
    
    @property
    def codes(self):
        return GemTaxonomy.__codes

    def get_attribute_by_name(self, name):
        for _attr in GemTaxonomy.__attrs:
            if _attr.name == name:
                return _attr
        return None 

    def get_code_by_name(self, name):
        if GemTaxonomy.__codes.has_key(name):
            return GemTaxonomy.__codes[name]
        else:
            return None

    @logAPICall
    def parse(self, taxonomy_str):
        """
        take a string and parse into a statistic case object
        this is the reverse function of case2str
        """     
        _str_attrs = taxonomy_str.split('/')
        
        if len(_str_attrs)== 0:
            raise TaxonomyParseError("Incorrect format")

        def _get_empty_attribute(attribute_name):
            for attr in self.__empty:
                if attr.attribute.name == attribute_name:
                    return copy.deepcopy(attr)                

        _attributes = []
        for _attr in _str_attrs:
            # determine type
            if re.match('\w+(\+\w+)+', _attr):
                # multiple codes, split and search each
                _levels = _attr.split('+')
                _attr_val = None
                for _i, _lvl in enumerate(_levels):
                    if not self.__codes.has_key(_lvl):
                        raise TaxonomyParseError('%s is not a valid taxonomy code' %(_lvl))
                    if _attr_val is None:
                        _attr_val = _get_empty_attribute(self.__codes[_lvl].attribute.name)
                    if isinstance(_attr_val, GemTaxonomyAttributeMulticodeValue):
                        _attr_val.add_value(_lvl)
                    else:
                        raise TaxonomyParseError('incorrect value type for %s' %(_attr))
                _attributes.append(_attr_val)
            elif re.match('\w+\:\d*', _attr):
                # code:value format
                (_type_id, _val) = _attr.split(':')
                if not self.__codes.has_key(_type_id):
                    raise TaxonomyParseError('%s is not a valid taxonomy code' %(_type_id))
                _attr_val = _get_empty_attribute(self.__codes[_type_id].attribute.name)
                if isinstance(_attr_val, GemTaxonomyAttributePairValue):
                    _attr_val.add_value(_type_id, _val)                    
                else:                    
                    raise TaxonomyParseError('additional value is not needed for code %s, found(%s)' % (_type_id, _attr))
                _attributes.append(_attr_val)
            elif re.match('\w+', _attr):
                # code only, search code table
                if not self.__codes.has_key(_attr):
                    raise TaxonomyParseError('%s is not a valid taxonomy code' %(_attr))
                _attr_val = _get_empty_attribute(self.__codes[_attr].attribute.name)
                if isinstance(_attr_val, GemTaxonomyAttributePairValue) and _attr_val.is_empty:
                    _attr_val.add_value(_attr, '')
                elif (isinstance(_attr_val, GemTaxonomyAttributeSinglecodeValue)
                        or isinstance(_attr_val, GemTaxonomyAttributeMulticodeValue)):
                    _attr_val.add_value(_attr)
                else:
                    raise TaxonomyParseError('incorrect value type for %s' %(_attr))
                _attributes.append(_attr_val)
                
        return _attributes

    def is_valid_string(self, tax_string):
        return True

    @logAPICall
    def separator(self, separator_type=Separators.Attribute):
        if separator_type==GemTaxonomy.Separators.Level:
            return self.level_separator
        else:
            return self.attribute_separator    
    
    @logAPICall
    def to_string(self, taxonomy_values):
        """ serialize a set of taxonomy values into GEM specific taxonomy string """
        outstr = ''
        for _attr_val in taxonomy_values:
            outstr = outstr + str(_attr_val) + "/"
        return outstr
    
    def __initialize(self, db_path):
        """
        prepare parser
        - load attributes and codes from underlying db
        """
        
        if GemTaxonomy.__initialized:
            return
        
        logAPICall.log('initialize taxonomy from database %s' % db_path, logAPICall.DEBUG)
        
        # load attributes / code from DB for parsing
        _conn = sqlite3.connect(db_path)
                
        sql = """
            select id, name, levels, default_value, format from gem_attribute order by id
        """
        c = _conn.cursor()
        c.execute(sql)
        GemTaxonomy.__attrs = []
        for row in c:
            _attr = GemTaxonomyAttribute(str(row[1]).strip(), int(row[0]), int(row[2]), str(row[3]).strip(), int(row[4]))
            GemTaxonomy.__attrs.append(_attr)
            attr_format = int(row[4])
            if attr_format == 1:
                self.__empty.append(GemTaxonomyAttributeMulticodeValue(_attr))
                _attr_val = GemTaxonomyAttributeMulticodeValue(_attr)
                _attr_val.add_value(_attr.default)
                self.__defaults.append(_attr_val)                
            elif attr_format == 2:
                self.__empty.append(GemTaxonomyAttributePairValue(_attr))
                _attr_val = GemTaxonomyAttributePairValue(_attr)
                _attr_val.add_value(_attr.default, "")
                self.__defaults.append(_attr_val)
            elif attr_format == 3:
                self.__empty.append(GemTaxonomyAttributeSinglecodeValue(_attr))
                _attr_val = GemTaxonomyAttributeSinglecodeValue(_attr)
                _attr_val.add_value(_attr.default)
                self.__defaults.append(_attr_val)
            else:
                raise TaxonomyParseError("attribute format not recognized for %s" % _attr)
        
        GemTaxonomy.__attr_orders = [attr.name for attr in GemTaxonomy.__attrs]
        # load codes
        sql = "select c.type_id, c.description, a.gem_attribute_id, a.level from attribute a inner join code_lookup c on a.id=c.attribute_id"
        c.execute(sql)
        for row in c:
            _code = TaxonomyAttributeCode(GemTaxonomy.__attrs[row[2]-1], int(row[3]), str(row[0]).strip(), str(row[1]).strip())
            GemTaxonomy.__codes[row[0]] = _code
            GemTaxonomy.__attrs[row[2]-1].add_valid_code(_code)
                    
        _conn.close()
        GemTaxonomy.__initialized=True


class GemTaxonomyAttribute(TaxonomyAttribute):
    """
    Gem taxonomy attribute. used to create range strings and validate strings
    """
    (EXACT, RANGE, AVERAGE) = range(3) 
    
    def __init__(self, name="", order=1, levels=1, default="", attribute_type=1):
        super(GemTaxonomyAttribute, self).__init__(name, order, levels, default, attribute_type)
        self._valid_codes = []    
    
    def add_valid_code(self, code):
        self._valid_codes.append(code)
        
    @logAPICall
    def get_valid_codes(self, parent=None, levels=None):
        for code in self._valid_codes:            
            if levels is None or code.level == levels:
                yield code

    def make_string(self, values, qualifier=None):
        if self.type == 1:
            return '+'.join([str(v) for v in values])
        else:
            if self.name == "Height":                
                # construct valid height string from given values
                if len(values) == 1:
                    if values[0] is None:
                        return "H99"
                    else:
                        return "H:%s" % (values[0])
                elif len(values) == 2:
                    if values[0] is None or values[1] is None :
                        return "H99"
                    if values[0] == 0 and values[1] == 0:
                        return "H99"
                    elif qualifier==GemTaxonomyAttribute.AVERAGE:                        
                        return "H:%s" % ( int((values[0]+values[1])/2) )
                    else:
                        return "H:%s,%s" % (values[0], values[1])
                else:
                    return "H99"
                                                        
            elif self.name == "Date of Construction":
                # construct valid date of construction string from given values                
                if len(values) == 1:
                    if values[0] is None:
                        return "Y99"
                    else:
                        return "YN:%s" % (values[0])
                elif len(values) == 2:
                    if values[0] is None or values[1] is None :
                        return "Y99"
                    if values[0] == 0 and values[1] == 0:
                        return "Y99"
                    elif qualifier==GemTaxonomyAttribute.AVERAGE:
                        return "YN:%s" % ( int((values[0]+values[1])/2) )
                    else:
                        return "YN:%s,%s" % (values[0], values[1])
                else:
                    return "Y99"

class GemTaxonomyAttributeMulticodeValue(TaxonomyAttributeMulticodeValue):
    """
    Gem taxonomy multicode value used for
    - height
    - yearbuilt
    """
    def __init__(self, attribute):
        TaxonomyAttributeMulticodeValue.__init__(self, attribute)
    
    def __str__(self):
        """ string representation """
        outstr=""
        __total = len(self.codes)
        if __total == 0:
            return outstr        
        # first code is primary
        outstr = self.codes[0]
        for _i in range(1, __total):
            outstr += '+%s' % (self.codes[_i])
        #outstr += "/"
        return outstr
        
class GemTaxonomyAttributeSinglecodeValue(TaxonomyAttributeSinglecodeValue):
    """
    Gem taxonomy single code value used for
    - 
    """
    def __init__(self, attribute):
        """ constructor """
        TaxonomyAttributeSinglecodeValue.__init__(self, attribute)
    
    def __str__(self):
        """ string representation """
        if self.__code is not None:
            return self.code  
        else:
            return ""
        
class GemTaxonomyAttributePairValue(TaxonomyAttributePairValue):
    """
    Gem taxonomy single code value used for
    - 
    """
    def __init__(self, attribute):
        """ constructor """
        TaxonomyAttributePairValue.__init__(self, attribute)

    def __str__(self):
        """ string representation """        
        if self.code is not None:
            if self.value is not None and self.value != "":
                return self.code + ":" + self.value
            else:
                return self.code 
        else:
            return ""