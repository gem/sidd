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
#

# import sidd packages for testing
from sidd.taxonomy import get_taxonomy, \
                          TaxonomyAttributeMulticodeValue, TaxonomyAttributePairValue

from common import SIDDTestCase

class TaxonomyTestCase(SIDDTestCase):

    # run for every test
    ##################################
    
    def setUp(self):
        super(TaxonomyTestCase, self).setUp()
        self.taxonomy = get_taxonomy("gem")
    
    def test_Load(self):
        self.assertEquals(len(self.taxonomy.attributes), 8)
        
        material = self.taxonomy.get_attribute_by_name('Material')                
        codes = [c for c in material.get_valid_codes()]
        self.assertEqual(len(codes), 76)
        codes1 = [c for c in material.get_valid_codes(level=1)]
        self.assertEqual(len(codes1), 16)        
        codes2 = [c for c in material.get_valid_codes(level=2)]
        self.assertEqual(len(codes2), 36)        
        codes3 = [c for c in material.get_valid_codes(level=3)]
        self.assertEqual(len(codes3), 24)
    
        cr = self.taxonomy.get_code_by_name('CR')
        cr_codes = [c for c in material.get_valid_codes(parent=cr, level=2)]
        self.assertEquals(len(cr_codes), 5)
                
    def test_Parse(self):
        tax_string = 'MUR+CLBRS+MOL/LWAL/RWO+RWO1/FE+FM1/HEX:3/Y99/IRHO/RES+RES2C'
        attrs = self.taxonomy.parse(tax_string)
        self.assertEquals(len(attrs), 8)
        self.assertTrue(isinstance(attrs[0], TaxonomyAttributeMulticodeValue))
        self.assertTrue(isinstance(attrs[4], TaxonomyAttributePairValue))
        
        tax_string = 'MUR+CLBRS+MOL/RWO+RWO1/FE+FM1/HEX:3/RES+RES2C'        
        attrs = self.taxonomy.parse(tax_string)
        self.assertEquals(len(attrs), 5)
        self.assertTrue(isinstance(attrs[0], TaxonomyAttributeMulticodeValue))
        self.assertTrue(isinstance(attrs[3], TaxonomyAttributePairValue))
    
        tax_string = 'CR+CIP/LFINF+DNO/HBET:1,3/'
        attrs = self.taxonomy.parse(tax_string)
