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
# Version: $Id: __init__.py 5 2012-08-28 23:14:35Z zh $

"""
common functions for ui helper classes
"""
from sidd.taxonomy import TaxonomyAttributeSinglecodeValue, TaxonomyAttributeMulticodeValue, TaxonomyAttributePairValue

def build_attribute_tooltip(codes, value):
    if codes.has_key(value):
        code = codes[value]
        return "Code: %s\nAttribute: %s\nLevel: %s\nDescription: %s\n" % (code.code, code.attribute.name, code.level, code.description)
    else:
        return ""

def build_multivalue_attribute_tooltip(codes, values):
    tooltip = []
    for attr in values:
        if attr.is_empty:
            continue
        if isinstance(attr, TaxonomyAttributeMulticodeValue):
            for code in attr.codes:
                tooltip.append(build_attribute_tooltip(codes, code))
                tooltip.append("\n")
        elif isinstance(attr, TaxonomyAttributeSinglecodeValue):
            tooltip.append(build_attribute_tooltip(codes, attr.code))
        elif isinstance(attr, TaxonomyAttributePairValue):
            tooltip.append(build_attribute_tooltip(codes, attr.code))
    return "".join(tooltip)            
            
