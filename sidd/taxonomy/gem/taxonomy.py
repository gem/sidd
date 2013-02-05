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
# Version: $Id: taxonomy.py 18 2012-10-24 20:21:41Z zh $

"""
module supporting GEM taxonomy version 1
"""
import sqlite3
import os
import re
import copy

from sidd.constants import logAPICall
from sidd.taxonomy import Taxonomy, TaxonomyAttribute, TaxonomyAttributeCode
from sidd.taxonomy import TaxonomyError, TaxonomyParseError
from sidd.taxonomy import TaxonomyAttributeMulticodeValue, TaxonomyAttributePairValue, TaxonomyAttributeSinglecodeValue

class GemTaxonomy(Taxonomy):
    """
    main taxonomy class
    """
    
    # protected member attributes
    __GEM_TAXONOMY_FILE = 'gem_v1.0.1.db'
    __attrs = []
    __codes = {}
    __empty = []
    __initialized = False

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
        return GemTaxonomy.__attrs

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

    @logAPICall
    def parse(self, taxonomy_str):
        """
        take a string and parse into a statistic case object
        this is the reverse function of case2str
        """    
        _attributes = copy.deepcopy(self.__empty)
        _str_attrs = taxonomy_str.split('/')
        
        if len(_str_attrs)== 0:
            raise TaxonomyParseError("Incorrect format")

        for _attr in _str_attrs:
            # determine type
            if re.match('\w+(\+\w+)+', _attr):
                # multiple codes, split and search each
                _levels = _attr.split('+')
                for _i, _lvl in enumerate(_levels):
                    _attr_val = _attributes[self.__codes[_lvl].order-1]
                    if isinstance(_attr_val, GemTaxonomyAttributeMulticodeValue):
                        _attr_val.add_value(_lvl)
                    else:
                        raise TaxonomyParseError('incorrect value type for %s' %(_attr))
            elif re.match('\w+\:\d+', _attr):
                # code:value format
                (_type_id, _val) = _attr.split(':')
                _attr_val = _attributes[self.__codes[_type_id].order-1]
                if isinstance(_attr_val, GemTaxonomyAttributePairValue):
                    _attr_val.add_value(_type_id, _val)
                else:
                    raise TaxonomyParseError('additional value is not needed for code %s' % (_type_id))
                
            elif re.match('\w+', _attr):
                # code only, search code table
                _attr_val = _attributes[self.__codes[_attr].order-1]
                if isinstance(_attr_val, GemTaxonomyAttributePairValue) and _attr_val.is_empty:
                    _attr_val.add_value(_attr, '')
                elif (isinstance(_attr_val, GemTaxonomyAttributeSinglecodeValue)
                        or isinstance(_attr_val, GemTaxonomyAttributeMulticodeValue)):
                    _attr_val.add_value(_attr)
                else:
                    raise TaxonomyParseError('incorrect value type for %s' %(_attr))
                
        return _attributes
    
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
            _attr = TaxonomyAttribute(str(row[1]), int(row[0]), int(row[2]), str(row[3]))
            GemTaxonomy.__attrs.append(_attr)
            attr_format = int(row[4])
            if attr_format == 1:
                self.__empty.append(GemTaxonomyAttributeMulticodeValue(_attr))
            elif attr_format == 2:
                self.__empty.append(GemTaxonomyAttributePairValue(_attr))
            elif attr_format == 3:
                self.__empty.append(GemTaxonomyAttributeSinglecodeValue(_attr))
            else:
                raise TaxonomyParseError("attribute format not recognized for %s" % _attr)
        
        # load codes
        sql = "select c.type_id, c.description, a.gem_attribute_id, a.level from attribute a inner join code_lookup c on a.id=c.attribute_id"
        c.execute(sql)
        for row in c:
            GemTaxonomy.__codes[row[0]] = TaxonomyAttributeCode(self.__attrs[row[2]-1], int(row[3]), str(row[0]), str(row[1]))
        
        _conn.close()
        GemTaxonomy.__initialized=True

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
            return self.code + ":" + self.value # + "/"
        else:
            return ""