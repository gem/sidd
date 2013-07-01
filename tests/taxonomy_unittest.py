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
        self.assertEquals(len(self.taxonomy.attributeGroups), 8)
        self.assertEquals(len(self.taxonomy.attributes), 22)
        
        material = self.taxonomy.get_attribute_group_by_name('Material')
        self.assertEquals(len(material.attributes), 5)
        self.assertEquals([a.name for a in material.attributes],
                          ['Masonry Mortar Type', 'Masonry Reinforce Type', 'Material Technology', 'Material Type', 'Steel Connection Type'])
        self.assertEquals([len(a.codes) for a in material.attributes],
                          [14, 6, 36, 16, 4])
                
    def test_Parse(self):
        tax_string = 'MUR+CLBRS+MOL/LWAL/RWO+RWO1/FE+FM1/HEX:3/Y99/IRHO/RES+RES2C'
        attrs = self.taxonomy.parse(tax_string)
        self.assertEquals(len(attrs), 13)
        self.assertTrue(isinstance(attrs['Height'], TaxonomyAttributePairValue))
                
        tax_string = 'MUR+CLBRS+MOL/RWO+RWO1/FE+FM1/HEX:3/RES+RES2C'        
        attrs = self.taxonomy.parse(tax_string)
        self.assertEquals(len(attrs), 10)
        self.assertTrue(isinstance(attrs['Height'], TaxonomyAttributePairValue))
        
        tax_string = 'CR+CIP/LFINF+DNO/HBET:1,3/'
        attrs = self.taxonomy.parse(tax_string)
        self.assertEquals(len(attrs), 5)
        self.assertTrue(isinstance(attrs['Height'], TaxonomyAttributePairValue))
