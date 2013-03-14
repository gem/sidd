# Copyright (c) 2011-2013, ImageCat Inc.
#
# SIDD is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
#
"""
common functions for ui helper classes
"""
from sidd.taxonomy import TaxonomyAttributeSinglecodeValue, TaxonomyAttributeMulticodeValue, TaxonomyAttributePairValue

def _build_tooltip(codes, value):
    lines = []
    if codes.has_key(value):
        code = codes[value]
        lines.append("Code: %s" % code.code)
        lines.append("Attribute: %s" % code.attribute.name)
        #lines.append("Level: %s" % code.level)
        lines.append("Description: %s" % code.description)
    return "\n".join(lines) 

def build_attribute_tooltip(codes, values):
    tooltips = []
    for attr in values:
        if attr.is_empty:
            continue
        if isinstance(attr, TaxonomyAttributeMulticodeValue):
            for code in attr.codes:
                tooltips.append(_build_tooltip(codes, code))
        elif isinstance(attr, TaxonomyAttributeSinglecodeValue):
            tooltips.append(_build_tooltip(codes, attr.code))
        elif isinstance(attr, TaxonomyAttributePairValue):
            tooltips.append(_build_tooltip(codes, attr.code))
        tooltips.append("")
    return "\n".join(tooltips)
            
