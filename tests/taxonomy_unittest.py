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
from sidd.taxonomy import get_taxonomy, TaxonomyAttributePairValue

from common import SIDDTestCase

class TaxonomyTestCase(SIDDTestCase):

    # run for every test
    ##################################
    
    def setUp(self):
        super(TaxonomyTestCase, self).setUp()
        self.taxonomy = get_taxonomy("gem")
    
    def test_Load(self):
        self.assertEquals(len(self.taxonomy.attribute_groups), 8)
        self.assertEquals(len(self.taxonomy.attributes), 22)
        
        material = self.taxonomy.get_attribute_group_by_name('Material')
        self.assertEquals(len(material.attributes), 5)
        self.assertEquals([a.name for a in material.attributes],
                          ['Material Type', 'Material Technology', 'Masonry Mortar Type', 'Masonry Reinforce Type', 'Steel Connection Type'])
        self.assertEquals([len(a.codes) for a in material.attributes],
                          [16, 36, 14, 6, 4])
        
        wood = self.taxonomy.get_code_by_name('W')        
        codes = [str(code.code) for code in self.taxonomy.get_code_by_attribute('Material Technology', wood)]
        self.assertEqual(len(codes), 7)
                
    def test_Parse(self):
        tax_string = 'MUR+CLBRS+MOL/LWAL/RWO+RWO1/FE+FM1/HEX:3/Y99/IRHO/RES+RES2C'
        attrs = self.taxonomy.parse(tax_string)
        self.assertEquals(len(attrs), 13)        
        self.assertTrue(isinstance(self._get_attribute_by_name(attrs, 'Height'), TaxonomyAttributePairValue))
                
        tax_string = 'MUR+CLBRS+MOL/RWO+RWO1/FE+FM1/HEX:3/RES+RES2C'        
        attrs = self.taxonomy.parse(tax_string)
        self.assertEquals(len(attrs), 10)
        self.assertTrue(isinstance(self._get_attribute_by_name(attrs, 'Height'), TaxonomyAttributePairValue))
        
        tax_string = 'CR+CIP/LFINF+DNO/HBET:1,3/'
        attrs = self.taxonomy.parse(tax_string)
        self.assertEquals(len(attrs), 5)
        self.assertTrue(isinstance(self._get_attribute_by_name(attrs, 'Height'), TaxonomyAttributePairValue))

    def _get_attribute_by_name(self, attrs, name):
        value = None
        for val in attrs:
            if val.attribute.name == name:
                value = val
                break
        return value