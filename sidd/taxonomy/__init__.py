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
package provides building taxonomy support
"""
from taxonomy import (Taxonomy, TaxonomyAttributeGroup, TaxonomyAttribute, 
                      TaxonomyAttributeValue, TaxonomyAttributeCode,
                      TaxonomyAttributeMulticodeValue,
                      TaxonomyAttributeSinglecodeValue,
                      TaxonomyAttributePairValue)
from exception import TaxonomyError, TaxonomyParseError

def get_taxonomy(name):
    if name.upper() == 'GEM':
        from gem import GemTaxonomy
        return GemTaxonomy()
    return None
