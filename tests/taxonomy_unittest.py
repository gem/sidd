# SeismiCat: an on-line seismic risk assessment tool for 
# building property owners, lenders, insurers and municipal analysts. 
# @copyright  (c)2012 ImageCat inc, All rights reserved
# @link       http://www.seismicat.com
# @since      SeismiCat v1.0
# @license    
# @version    $Id: ms_unittest.py 19 2012-10-25 01:06:59Z zh $
# import sidd packages for testing
from sidd.taxonomy import get_taxonomy, TaxonomyAttributeMulticodeValue, TaxonomyAttributePairValue

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
    
    