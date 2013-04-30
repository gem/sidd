# Copyright (c) 2011-2013, ImageCat Inc.
#
# SIDD is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. 
#
"""
SIDD operators
"""

from data import OperatorData, OperatorDataTypes
from operator import Operator, EmptyOperator
from exception import OperatorError, OperatorDataError

from loaders import *
from processors import *
from writers import *
from verify import *