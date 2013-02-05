# Copyright (c) 2011-2012, ImageCat Inc.
#
# SIDD is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License version 3
# only, as published by the Free Software Foundation.
#
# SIDD is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License version 3 for more details
# (a copy is included in the LICENSE file that accompanied this code).
#
# You should have received a copy of the GNU Lesser General Public License
# version 3 along with SIDD.  If not, see
# <http://www.gnu.org/licenses/lgpl-3.0.txt> for a copy of the LGPLv3 License.
#
# Version: $Id: constants.py 21 2012-10-26 01:48:25Z zh $

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
SIDD_VERSION = '0.1'


# maximum number of items before swithcing from in-memory algorithms
# to file-based algorithms
MAX_FEATURES_IN_MEMORY = 10000

# 30 arc second
DEFAULT_GRID_SIZE = 1 / 60. / 2.  

# field names for GIS shapefiles
GID_FIELD_NAME = "GID"
LON_FIELD_NAME = "LON"
LAT_FIELD_NAME = "LAT"
AREA_FIELD_NAME = "AREA"
ZONE_FIELD_NAME = "ZONE"
TAX_FIELD_NAME = "TAXONOMY"
CNT_FIELD_NAME = "NUM_BLDGS"

# names for template files 
###########################
FILE_PROJ_TEMPLATE = '%s/data/bsddb.template' % get_app_dir()

# enumerations
###########################
# input data related
FootprintTypes = Enum("None", "FootprintHt", "Footprint")
ZonesTypes = Enum("None", "Landuse", "LanduseCount")
SurveyTypes = Enum("None", "CompleteSurvey", "SampledSurvey")
OutputTypes = Enum("Zone", "Grid")
ExportTypes = Enum("Shapefile", "KML", "NRML")
SyncModes = Enum("Read", "Write")

# project related
ProjectStatus = Enum('NotVerified', 'ReadyForExposure', 'ReadyForMS')

# workflow related
WorkflowErrors = Enum("NeedsCount", "NeedsZone", "NeedsMS", "NeedSurvey", "NoActionDefined")
