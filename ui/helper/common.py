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
common functions for ui helper classes
"""
from sidd.taxonomy import TaxonomyAttributeSinglecodeValue, TaxonomyAttributeMulticodeValue, TaxonomyAttributePairValue

def _build_tooltip(code):
    lines = []
    if code is not None:        
        lines.append("Code: %s" % code.code)
        lines.append("Attribute: %s" % code.attribute.name)
        #lines.append("Level: %s" % code.level)
        lines.append("Description: %s" % code.description)
    return "\n".join(lines) 

def build_attribute_tooltip(valid_codes, attributes):
    tooltips = []
    for attr in attributes.values():
        if attr.is_empty:
            continue
        if isinstance(attr, TaxonomyAttributeMulticodeValue):
            for code in attr.codes:
                tooltips.append(_build_tooltip(code))
        elif isinstance(attr, TaxonomyAttributeSinglecodeValue):
            tooltips.append(_build_tooltip(attr.code))
        elif isinstance(attr, TaxonomyAttributePairValue):
            tooltips.append(_build_tooltip(attr.code))
        tooltips.append("")
    return "\n".join(tooltips)
            
