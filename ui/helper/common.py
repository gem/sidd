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
    lines = []
    if codes.has_key(value):
        code = codes[value]
        lines.append("Code: %s" % code.code)
        lines.append("Attribute: %s" % code.attribute.name)
        #lines.append("Level: %s" % code.level)
        lines.append("Description: %s" % code.description)
    return "\n".join(lines) 

def build_multivalue_attribute_tooltip(codes, values):
    tooltips = []
    for attr in values:
        if attr.is_empty:
            continue
        if isinstance(attr, TaxonomyAttributeMulticodeValue):
            for code in attr.codes:
                tooltips.append(build_attribute_tooltip(codes, code))
        elif isinstance(attr, TaxonomyAttributeSinglecodeValue):
            tooltips.append(build_attribute_tooltip(codes, attr.code))
        elif isinstance(attr, TaxonomyAttributePairValue):
            tooltips.append(build_attribute_tooltip(codes, attr.code))
        tooltips.append("")
    return "\n".join(tooltips)
            
