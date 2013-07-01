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
module supporting GEM taxonomy version 1
"""
import sqlite3
import os
import re
import copy
from operator import attrgetter

from sidd.constants import logAPICall
from sidd.taxonomy import Taxonomy, TaxonomyAttributeGroup, TaxonomyAttribute, TaxonomyAttributeCode
from sidd.taxonomy import TaxonomyError, TaxonomyParseError
from sidd.taxonomy import TaxonomyAttributeMulticodeValue, TaxonomyAttributePairValue, TaxonomyAttributeSinglecodeValue

class GemTaxonomy(Taxonomy):
    """
    main taxonomy class
    """
    # protected member attributes
    __GEM_TAXONOMY_FILE = 'gemdb.db'
    def __init__(self):        
        db_path = os.path.dirname( __file__ ) + os.path.sep + self.__GEM_TAXONOMY_FILE
        if not os.path.exists(db_path):
            raise TaxonomyError("gem taxonomy db not found")

        # open associated sqlite DB and load attributes
        self.__initialized = False
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
    def attributeGroups(self):
        return self.__attrGroups
    
    @property
    def attributes(self):
        return self.__attrs
    
    @property
    def codes(self):
        return self.__codes

    def get_attribute_group_by_name(self, name):
        for _grp in self.__attrGroups:
            if _grp.name == name:
                return _grp
        return None

    def get_attribute_by_name(self, name):
        for _attr in self.__attrs:
            if _attr.name == name:
                return _attr
        return None
    
    def get_code_by_name(self, name):        
        if self.__codes.has_key(name):
            return self.__codes[name]
        return None

    def get_code_by_attribute(self, attribute_name):        
        for code in self.__codes.values():                
            if code.attribute.name == attribute_name:
                yield code        

    @logAPICall
    def parse(self, taxonomy_str):
        _str_attrs = str(taxonomy_str).split('/')
        if len(_str_attrs)== 0:
            raise TaxonomyParseError("Incorrect format")

        _attributes = {}
        for _attr in _str_attrs:
            # determine type
            if re.match('\w+(\+\w+)+', _attr):
                # multiple codes, split and search each
                _levels = _attr.split('+')
                _attr_val = None
                for _i, _lvl in enumerate(_levels):
                    if not self.__codes.has_key(_lvl):
                        raise TaxonomyParseError('%s is not a valid taxonomy code' %(_lvl))
                    _code = self.__codes[_lvl]
                    _codeValue = GemTaxonomyAttributeSinglecodeValue(_code.attribute)
                    _codeValue.add_value(_code)
                    _attributes[_code.attribute.name]=_codeValue
            elif re.match('\w+\:\d*', _attr):
                # code:value format
                (_type_id, _val) = _attr.split(':')
                if not self.__codes.has_key(_type_id):
                    raise TaxonomyParseError('%s is not a valid taxonomy code' %(_type_id))
                _code = self.__codes[_type_id]
                _codeValue = GemTaxonomyAttributePairValue(_code.attribute)
                _codeValue.add_value(_code, _val)
                _attributes[_code.attribute.name]=_codeValue
            elif re.match('\w+', _attr):
                # code only, search code table
                if not self.__codes.has_key(_attr):
                    raise TaxonomyParseError('%s is not a valid taxonomy code' %(_attr))
                _code = self.__codes[_attr]
                _codeValue = GemTaxonomyAttributeSinglecodeValue(_code.attribute)
                _codeValue.add_value(_code)
                _attributes[_code.attribute.name]=_codeValue                
        return _attributes

    def is_valid_string(self, tax_string):
        return True

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
        if self.__initialized:
            return
        
        logAPICall.log('initialize taxonomy from database %s' % db_path, logAPICall.DEBUG)
        
        # load attributes / code from DB for parsing
        _conn = sqlite3.connect(db_path)

        c = _conn.cursor()
        
        # load attribute groups
        # attribute group default value for fill-in to missing groups                 
        sql = """
            select a.attribute, a.default_value from gem_attributes g inner join attributes a on g.attribute=a.attribute  where level=1 and order_in_basic <> ''
        """     
        c.execute(sql)
        _default_values = {}
        for row in c:
            _default_values[str(row[0])]=str(row[1])
        
        sql = """
            select g.order_in_basic as id, g.attribute, max(a.level) levels, g.format
            from gem_attributes g
            inner join attributes a on g.attribute=a.attribute 
            where order_in_basic <> '' 
            group by g.order_in_basic, g.attribute, g.format
            order by order_in_basic
        """
        c.execute(sql)
        self.__attrGroups = []
        for row in c:            
            _grp = GemTaxonomyAttributeGroup(str(row[1]).strip(), int(row[0]), int(row[2]), 
                                             _default_values[str(row[1])], int(row[3]))
            self.__attrGroups.append(_grp)
            
        # load attributes
        sql = """
            select a.name, a.level, g.attribute, a.format
            from gem_attributes g
            inner join attributes a on g.attribute=a.attribute 
            where order_in_basic <> '' 
            group by a.name, a.level, g.attribute, a.format
            order by g.order_in_basic, a.level
        """
        c.execute(sql)
        self.__attrs = []
        for row in c:
            _grp = self.get_attribute_group_by_name(str(row[2]).strip())
            _attr = GemTaxonomyAttribute(str(row[0]).strip(), _grp, 
                                         int(row[1]), None, int(row[3]))
            _grp.add_attribute(_attr)
            self.__attrs.append(_attr)

        # load codes
        sql = """
            select c.attribute, code, description, scope, is_default
            from code_lookup c
            inner join gem_attributes g on c.gem_attribute=g.attribute 
            where g.order_in_basic <> ''
        """
        c.execute(sql)
        self.__codes = {}
        for row in c: 
            _attr = self.get_attribute_by_name(str(row[0]).strip())
            _code_value = str(row[1]).strip()
            _code = TaxonomyAttributeCode(_attr, 
                                          _code_value, str(row[2]).strip(), str(row[3]).strip())
            self.__codes[_code_value] = _code
            _attr.add_code(_code)
                    
        _conn.close()
        self.__initialized=True

class GemTaxonomyAttribute(TaxonomyAttribute):
    """
    Gem taxonomy attribute. used to create range strings and validate strings
    """
    (EXACT, RANGE, APP, PRE) = range(4) 
    
    def __init__(self, name="", attribute_group=None, order=1, default="", attribute_type=1, codes=None):    
        super(GemTaxonomyAttribute, self).__init__(name, attribute_group, order, default, attribute_type, codes)

    def make_string(self, values, qualifier=None):
        if self.type == 1:
            return '+'.join([str(v) for v in values])
        else:
            if qualifier is None:
                if (values[0] is not None and values[1] is not None):
                    qualifier=GemTaxonomyAttribute.RANGE
                else:
                    qualifier=GemTaxonomyAttribute.EXACT                    
            if self.name == "Height":                
                # construct valid height string from given values
                if (values[0] is None or values[1] is None) or (values[0] == 0 and values[1] == 0):
                    return "H99"
                elif qualifier==GemTaxonomyAttribute.EXACT:                        
                    return "HEX:%s" % ( values[0] )
                elif qualifier==GemTaxonomyAttribute.RANGE:
                    return "HBET:%s,%s" % (values[0], values[1])
                else:
                    return "H99"
                                                        
            elif self.name == "Date of Construction":
                # construct valid date of construction string from given values                
                if (values[0] is None or values[1] is None) or (values[0] == 0 and values[1] == 0):
                    return "Y99"
                elif qualifier==GemTaxonomyAttribute.PRE:
                    return "YPRE:%s" % ( values[0] )
                elif qualifier==GemTaxonomyAttribute.APP:
                    return "YAPP:%s" % ( values[0] )
                elif qualifier==GemTaxonomyAttribute.RANGE:
                    return "YBET:%s,%s" % (values[0], values[1])
                else:
                    return "Y99"


class GemTaxonomyAttributeGroup(TaxonomyAttributeGroup):
    """
    Gem taxonomy multicode value used for
    - height
    - yearbuilt
    """
    def __init__(self, name="", order=1, levels=1, default="", attribute_type=1, attributes=None):
        super(GemTaxonomyAttributeGroup, self).__init__(name, order, levels, default, attribute_type, attributes)
    
    def make_string(self, values, qualifier=None):
        raise NotImplementedError("abstract method not implemented")
    
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
            outstr += '+%s' % (self.codes[_i].code)
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
        if self.code is not None:
            return self.code.code  
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
                return self.code.code + ":" + self.value
            else:
                return self.code.code 
        else:
            return ""