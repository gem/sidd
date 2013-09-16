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
from sidd.taxonomy import Taxonomy, TaxonomyAttributeGroup, TaxonomyAttribute, TaxonomyAttributeValue, TaxonomyAttributeCode
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
    def attribute_groups(self):
        return self.__attrGroups
    
    @property
    def attributes(self):
        return self.__attrs
    
    @property
    def codes(self):
        return self.__codes

    def get_separator(self, separator_type):
        if separator_type == GemTaxonomy.Separators.AttributeGroup:
            return GemTaxonomyAttributeGroup.Separator
        elif separator_type == GemTaxonomy.Separators.Attribute:
            return GemTaxonomyAttribute.Separator
        elif separator_type == GemTaxonomy.Separators.AttributeValue:
            return GemTaxonomyAttributeValue.Separator
        else:
            raise TaxonomyError("Separator Type (%s) not supported" % separator_type)

    def get_attribute_group_by_name(self, name):
        for grp in self.__attrGroups:
            if grp.name == name:
                return grp
        return None

    def get_attribute_by_name(self, name):
        for attr in self.__attrs:
            if attr.name == name:
                return attr
        return None
    
    def get_code_by_name(self, name):        
        if self.__codes.has_key(name):
            return self.__codes[name]
        return None

    def get_code_by_attribute(self, attribute_name, parent_code=None):
        has_rule = False
        if isinstance(parent_code, TaxonomyAttributeCode):    
            parent_lookup = parent_code.attribute.lookup_table
            child_lookup = self.get_attribute_by_name(attribute_name).lookup_table                
            rule_key = '%s|%s' % (parent_lookup, child_lookup)
            has_rule = self.rules.has_key(rule_key)
        
        if has_rule:
            rule = self.rules[rule_key]
            if not rule.has_key(parent_code):
                return
            for code in rule[parent_code]:
                yield code
        else:
            for code in self.__codes.values():                
                if code.attribute.name == attribute_name:
                    yield code
            
    def has_rule(self, attribute):
        if type(attribute) == str: 
            attribute = self.get_attribute_by_name(attribute)
        for keys in self.rules.keys():
            if keys.find(attribute.lookup_table) >= 0:
                return True
        return False        

    @logAPICall
    def parse(self, taxonomy_str):
        str_attrs = str(taxonomy_str).split('/')
        if len(str_attrs)== 0:
            raise TaxonomyParseError("Incorrect format")

        attributes = []
        for attr in str_attrs:
            # determine type
            if re.match('\w+(\+\w+)+', attr):
                # multiple codes, split and search each
                levels = attr.split('+')
                for lvl in levels:
                    if not self.__codes.has_key(lvl):
                        raise TaxonomyParseError('%s is not a valid taxonomy code' %(lvl))
                    code = self.__codes[lvl]
                    codeValue = GemTaxonomyAttributeSinglecodeValue(code.attribute)
                    codeValue.add_value(code)
                    attributes.append(codeValue)
            elif re.match('\w+\:\d*', attr):
                # code:value format
                (type_id, val) = attr.split(':')
                if not self.__codes.has_key(type_id):
                    raise TaxonomyParseError('%s is not a valid taxonomy code' %(type_id))
                code = self.__codes[type_id]
                codeValue = GemTaxonomyAttributePairValue(code.attribute)
                codeValue.add_value(code, val)
                attributes.append(codeValue)
            elif re.match('\w+', attr):
                # code only, search code table
                if not self.__codes.has_key(attr):
                    raise TaxonomyParseError('%s is not a valid taxonomy code' %(attr))
                code = self.__codes[attr]
                codeValue = GemTaxonomyAttributeSinglecodeValue(code.attribute)
                codeValue.add_value(code)
                attributes.append(codeValue)                
        return attributes

    def is_valid_string(self, tax_string):
        return True

    @logAPICall
    def to_string2(self, taxonomy_values, order_attributes=False, fill_missing=False):
        """ serialize a set of taxonomy values into GEM specific taxonomy string """
        vals = self.parse("/".join([str(n) for n in taxonomy_values]))        
        if (fill_missing):
            to_add = [g.name for g in self.attribute_groups]
            for v in vals:
                try:
                    to_add.remove(v.code.attribute.group.name)
                except:
                    pass
            str_add = []
            for name in to_add:
                str_add.append(self.get_attribute_group_by_name(name).default)
            vals = vals + self.parse("/".join(str_add))
            order_attributes=True

        if (order_attributes):
            vals.sort(key=attrgetter('code.attribute.group.order'))
        
        out_str = []
        for idx, v in enumerate(vals):
            if idx > 0:
                if v.code.attribute.group.order == vals[idx-1].code.attribute.group.order:
                    out_str.append(GemTaxonomyAttribute.Separator)
                else:
                    out_str.append(GemTaxonomyAttributeGroup.Separator)
            out_str.append(str(v))
        return "".join(out_str)
 
    @logAPICall
    def to_string(self, taxonomy_values, order_attributes=False, fill_missing=False):
        """ serialize a set of taxonomy values into GEM specific taxonomy string """
        vals = self.parse("/".join([str(n) for n in taxonomy_values]))
        if not order_attributes:
            out_str = []
            for idx, v in enumerate(vals):
                if idx > 0:
                    if v.code.attribute.group.order == vals[idx-1].code.attribute.group.order:
                        out_str.append(GemTaxonomyAttribute.Separator)
                    else:
                        out_str.append(GemTaxonomyAttributeGroup.Separator)
                out_str.append(str(v))
            return "".join(out_str)             
        else:
            out_str = ['']*len(self._output_str)
            # set directions
            out_str[0], out_str[3] = 'DX','DY'
            vals.sort(key=lambda val:val.code.attribute.group.order*100+val.code.attribute.order)
            for v in vals:
                g_name = v.attribute.group.name
                idxlist = [i for i,val in enumerate(self._output_str) if val==g_name]
                for idx in idxlist:
                    if out_str[idx] == '':
                        out_str[idx] = str(v)
                    else:
                        out_str[idx] = "%s+%s" % (out_str[idx], str(v))
            return "/".join(out_str)
    
    def __initialize(self, db_path):
        """
        prepare parser
        - load attributes and codes from underlying db
        """        
        if self.__initialized:
            return
        
        logAPICall.log('initialize taxonomy from database %s' % db_path, logAPICall.DEBUG)
        
        # load attributes / code from DB for parsing
        conn = sqlite3.connect(db_path)

        c = conn.cursor()
        
        # load attribute groups
        # attribute group default value for fill-in to missing groups                 
        sql = """
            select a.attribute, a.default_value from dic_gem_attributes g inner join dic_gem_attribute_levels a on g.attribute=a.attribute where level=1 and order_in_basic <> ''
        """     
        c.execute(sql)
        default_values = {}
        for row in c:
            default_values[str(row[0])]=str(row[1])

        sql = """
            select order_in_extended, attribute from dic_gem_attributes g order by order_in_extended asc
        """     
        c.execute(sql)
        output_str = []
        for row in c:
            output_str.append(str(row[1]))                  
        self._output_str = output_str[:3]+output_str
        sql = """
            select g.order_in_basic,  g.attribute, max(a.level) levels, g.format
            from dic_gem_attributes g
            inner join dic_gem_attribute_levels a on g.attribute=a.attribute 
            where order_in_basic <> ''
            group by g.order_in_basic, g.attribute, g.format
            order by order_in_basic
        """
        c.execute(sql)
        self.__attrGroups = []
        for row in c:            
            grp = GemTaxonomyAttributeGroup(str(row[1]).strip(), int(row[0]), int(row[2]), 
                                            default_values[str(row[1])], int(row[3]))
            self.__attrGroups.append(grp)
            
        # load attributes
        sql = """
            select a.name, a.level, g.attribute, a.format, a.lookup_table
            from dic_gem_attributes g
            inner join dic_gem_attribute_levels a on g.attribute=a.attribute 
            where order_in_basic <> '' 
            group by a.name, a.level, g.attribute, a.lookup_table, a.format
            order by g.order_in_basic, a.level
        """
        c.execute(sql)
        self.__attrs = []
        for row in c:
            grp = self.get_attribute_group_by_name(str(row[2]).strip())
            attr = GemTaxonomyAttribute(str(row[0]).strip(), grp, 
                                        int(row[1]), None, int(row[3]))
            attr.lookup_table = str(row[4])
            grp.add_attribute(attr)
            self.__attrs.append(attr)

        # load codes
        sql = """select code, description, scope from %s"""
        self.__codes = {}
        for attr in self.__attrs:
            if attr.lookup_table == "":
                continue
            c.execute(sql % attr.lookup_table)
            for row in c: 
                code_value = str(row[0]).strip()
                code = TaxonomyAttributeCode(attr, 
                                             code_value, str(row[1]).strip(), str(row[2]).strip())
                self.__codes[code_value] = code
                attr.add_code(code)
        
        # load rules
        sql = """ select parent_table, child_table, parent_code, child_code from GEM_RULES """
        c.execute(sql)
        self.rules = {}
        for row in c:
            rule_key = '%s|%s' % (str(row[0]).strip(), str(row[1]).strip())
            parent_code = self.__codes[str(row[2]).strip()]            
            child_code = self.__codes[str(row[3]).strip()]
            if not self.rules.has_key(rule_key):
                self.rules[rule_key] = {}
            rule = self.rules[rule_key]
            if not rule.has_key(parent_code):
                rule[parent_code] = []
            rule[parent_code].append(child_code)
                        
        conn.close()
        self.__initialized=True

class GemTaxonomyAttribute(TaxonomyAttribute):
    """
    Gem taxonomy attribute. used to create range strings and validate strings
    """
    (EXACT, RANGE, APP, PRE) = range(4) 

    Separator = "+"
    
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
    Separator = "/"
    
    def __init__(self, name="", order=1, levels=1, default="", attribute_type=1, attributes=None):
        super(GemTaxonomyAttributeGroup, self).__init__(name, order, levels, default, attribute_type, attributes)

    def make_string(self, values, qualifier=None):
        raise NotImplementedError("abstract method not implemented")

class GemTaxonomyAttributeValue(TaxonomyAttributeValue):
    """
    This is an abstract class that can be derived to stores valid value
    for a taxonomy attribute 
    """
    Separator = ":"
    
    def __init__(self, attribute):
        """ constructor """
        super(GemTaxonomyAttributeValue, self).__init__(attribute)
    
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
        total = len(self.codes)
        if total == 0:
            return outstr        
        # first code is primary
        outstr = self.codes[0]
        for i in range(1, total):
            outstr += '+%s' % (self.codes[i].code)
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