# Copyright (c) 2011-2013, ImageCat Inc.
#
# SIDD is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
#

# import sidd packages for testing
from sidd.taxonomy import TaxonomyAttributeMulticodeValue, TaxonomyAttributePairValue

from common import SIDDTestCase

class TaxonomyTestCase(SIDDTestCase):

    # run for every test
    ##################################
    
    def setUp(self):
        super(TaxonomyTestCase, self).setUp()
    
    def test_Parse(self):
        tax_string = 'MUR+CLBRS+MOL/LWAL+ND/RWO+RWO1/FE+FM1/H:3/Y99/IRHO/RES+RES2C'
        attrs = self.taxonomy.parse(tax_string)
        self.assertEquals(len(attrs), 8)
        self.assertTrue(isinstance(attrs[0], TaxonomyAttributeMulticodeValue))
        self.assertTrue(isinstance(attrs[4], TaxonomyAttributePairValue))
        
        tax_string = 'MUR+CLBRS+MOL/RWO+RWO1/FE+FM1/H:3/RES+RES2C'        
        attrs = self.taxonomy.parse(tax_string)
        self.assertEquals(len(attrs), 5)
        self.assertTrue(isinstance(attrs[0], TaxonomyAttributeMulticodeValue))
        self.assertTrue(isinstance(attrs[3], TaxonomyAttributePairValue))
    
    