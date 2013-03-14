# Copyright (c) 2011-2013, ImageCat Inc.
#
# SIDD is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
#
"""
package provides building taxonomy support
"""
from taxonomy import (Taxonomy, TaxonomyAttribute, TaxonomyAttributeCode,
                      TaxonomyAttributeMulticodeValue,
                      TaxonomyAttributeSinglecodeValue,
                      TaxonomyAttributePairValue)
from exception import TaxonomyError, TaxonomyParseError

def get_taxonomy(name):
    if name.upper() == 'GEM':
        from gem import GemTaxonomy
        return GemTaxonomy()
    return None
