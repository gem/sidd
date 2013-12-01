License & Warranty
------------------
Copyright (c) 2011-2012, ImageCat Inc.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

SIDD
==============
Last Updated: 2013-05-10

What is SIDD?
------------

SIDD is acronym of "Spatial Inventory Data Developer"  

SIDD tool serves as a conduit between base data sets derived from both 
ground observations and remotely sensed sources and a GEM compliant file. 

Data is loaded into SIDD from the remote sensing module and the field data 
collection tool and processed into a GEM suitable file. 

Data from task 1 and/or task 2 are loaded into a local data repository 
on the userís hard drive. In addition, the user has the option of loading 
land use data or delineations of ìhomogenous zonesî.  Homogenous zones are 
areas with sufficiently similar structure type distribution to be 
characterized by a mapping scheme.  

Once data is loaded into SIDD, mapping schemes are identified, created, or 
constructed (Figure 1-1, task 3b). Mapping schemes are tools for the 
statistical inference of structural parameters given data from a given area. 
The development, application, and validation of mapping scheme results are 
a primary function of the SIDD tool. Data may be based on regional defaults,
expert opinion, survey data, or a combination of these factors. 

After the mapping schemes are assembled, users apply the mapping scheme and 
data preliminary exposure database is created. For the development of 
inventories, the application of SIDD is likely to be an iterative process, 
with users checking the results carefully and adjusting both geographic and
statistical data to develop a final exposure data set that makes sense. 

DEPENDENCIES
------------

- Quantum GIS 1.8 
    - Internally, SIDD makes heavy use of Quantum GIS python library for GIS analysis

- The following should be part of the Quantum GIS 1.8 installation
    - Python 2.7.x
    - PyQT 4.8.x
    - OSGeo GDAL/OGR '1.9.x'
    
INSTALLATION
------------
Windows
- Edit enclosed setenv.bat 
- Change LIB_HOME to root directory of Quantum GIS installation
- The following are example installation directories
    - as part of OSGeo packages
    SET LIB_HOME=C:\OSGeo4W
    - as Stand-alone installation
    SET LIB_HOME=C:\Program Files\Quantum GIS\    

- running tests
- Use SIDD environment shortcut to start command window
- type the following: `python run_tests.py`

START APPLICATION
------------
Windows

- Use SIDD shortcut to start application
