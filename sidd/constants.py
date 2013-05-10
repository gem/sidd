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
SIDD constants and enumerations
"""
from utils.enum import Enum
from utils.system import get_app_dir
from sidd.logger import SIDDLogging

# decorator and loggeer for API function calls
logAPICall = SIDDLogging('core')

# constants 
###########################
SIDD_COMPANY = "GEM"
SIDD_APP_NAME = "SIDD"
SIDD_VERSION = 'Beta 1'

# maximum number of items before swithcing from in-memory algorithms
# to file-based algorithms
MAX_FEATURES_IN_MEMORY = 10000

# 30 arc second
DEFAULT_GRID_SIZE = 1 / 60. / 2.
DEFAULT_HALF_GRID_SIZE = DEFAULT_GRID_SIZE / 2.

# field names for GIS shapefiles
GID_FIELD_NAME = "GID"
LON_FIELD_NAME = "LON"
LAT_FIELD_NAME = "LAT"
AREA_FIELD_NAME = "AREA"
HT_FIELD_NAME = "HT"
ZONE_FIELD_NAME = "ZONE"
TAX_FIELD_NAME = "TAXONOMY"
CNT_FIELD_NAME = "NUM_BLDGS"
GRP_FIELD_NAME = "GROUP"

# names for template files 
###########################
FILE_PROJ_TEMPLATE = '%s/data/bsddb.template' % get_app_dir()

# enumerations
########################### input data related
FootprintTypes = Enum("None", "FootprintHt", "Footprint")
ZonesTypes = Enum("None", "Landuse", "LanduseCount")
SurveyTypes = Enum("None", "CompleteSurvey", "SampledSurvey")
OutputTypes = Enum("Zone", "Grid")
ExportTypes = Enum("Shapefile", "KML", "NRML", "CSV")
SyncModes = Enum("Read", "Write")

# project related
ProjectStatus = Enum('NotVerified', 'ReadyForExposure', 'ReadyForMS')
# processing options
ExtrapolateOptions = Enum('RandomWalk', 'Fraction', 'FractionRounded')

# exception constants
ProjectErrors = Enum("FileNotSet", "FileFormatError")
# workflow related
WorkflowErrors = Enum("NeedsCount", "NeedsZone", "NeedsHeight", "NeedsMS", "NeedSurvey", "NeedExposure", "NoActionDefined")
